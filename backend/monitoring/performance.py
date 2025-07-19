import time
import logging
import psutil
import threading
from django.core.cache import cache
from django.conf import settings
from django.db import connection
from collections import defaultdict, deque
import json

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Moniteur de performance en temps réel"""
    
    def __init__(self):
        self.metrics = {
            'request_times': deque(maxlen=1000),
            'db_queries': deque(maxlen=1000),
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': deque(maxlen=100),
            'memory_usage': deque(maxlen=100),
            'cpu_usage': deque(maxlen=100)
        }
        self.lock = threading.Lock()
        self.start_monitoring()
    
    def record_request(self, path, method, duration, status_code):
        """Enregistre une requête"""
        with self.lock:
            self.metrics['request_times'].append({
                'path': path,
                'method': method,
                'duration': duration,
                'status_code': status_code,
                'timestamp': time.time()
            })
    
    def record_db_query(self, query, duration):
        """Enregistre une requête de base de données"""
        with self.lock:
            self.metrics['db_queries'].append({
                'query': query[:100],  # Limiter la taille
                'duration': duration,
                'timestamp': time.time()
            })
    
    def record_cache_hit(self):
        """Enregistre un cache hit"""
        with self.lock:
            self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Enregistre un cache miss"""
        with self.lock:
            self.metrics['cache_misses'] += 1
    
    def record_error(self, error_type, error_message, path):
        """Enregistre une erreur"""
        with self.lock:
            self.metrics['errors'].append({
                'type': error_type,
                'message': error_message,
                'path': path,
                'timestamp': time.time()
            })
    
    def get_performance_stats(self):
        """Récupère les statistiques de performance"""
        with self.lock:
            # Statistiques des requêtes
            request_times = list(self.metrics['request_times'])
            if request_times:
                durations = [r['duration'] for r in request_times]
                avg_response_time = sum(durations) / len(durations)
                max_response_time = max(durations)
                min_response_time = min(durations)
            else:
                avg_response_time = max_response_time = min_response_time = 0
            
            # Statistiques de cache
            total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
            cache_hit_rate = (self.metrics['cache_hits'] / total_cache_requests * 100) if total_cache_requests > 0 else 0
            
            # Statistiques de base de données
            db_queries = list(self.metrics['db_queries'])
            if db_queries:
                db_durations = [q['duration'] for q in db_queries]
                avg_db_time = sum(db_durations) / len(db_durations)
                total_db_queries = len(db_queries)
            else:
                avg_db_time = total_db_queries = 0
            
            # Utilisation système
            memory_usage = psutil.virtual_memory().percent
            cpu_usage = psutil.cpu_percent()
            
            return {
                'response_times': {
                    'average': round(avg_response_time, 3),
                    'maximum': round(max_response_time, 3),
                    'minimum': round(min_response_time, 3),
                    'total_requests': len(request_times)
                },
                'cache': {
                    'hits': self.metrics['cache_hits'],
                    'misses': self.metrics['cache_misses'],
                    'hit_rate': round(cache_hit_rate, 2)
                },
                'database': {
                    'total_queries': total_db_queries,
                    'average_query_time': round(avg_db_time, 3)
                },
                'system': {
                    'memory_usage': memory_usage,
                    'cpu_usage': cpu_usage
                },
                'errors': {
                    'total': len(self.metrics['errors']),
                    'recent': list(self.metrics['errors'])[-10:]  # 10 dernières erreurs
                }
            }
    
    def start_monitoring(self):
        """Démarre le monitoring en arrière-plan"""
        def monitor_system():
            while True:
                try:
                    # Enregistrer l'utilisation système
                    memory = psutil.virtual_memory().percent
                    cpu = psutil.cpu_percent()
                    
                    with self.lock:
                        self.metrics['memory_usage'].append(memory)
                        self.metrics['cpu_usage'].append(cpu)
                    
                    time.sleep(60)  # Mise à jour toutes les minutes
                    
                except Exception as e:
                    logger.error(f"Erreur dans le monitoring système: {str(e)}")
                    time.sleep(60)
        
        # Démarrer le thread de monitoring
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()


class DatabaseMonitor:
    """Moniteur spécifique pour la base de données"""
    
    @staticmethod
    def get_db_stats():
        """Récupère les statistiques de base de données"""
        try:
            with connection.cursor() as cursor:
                # Nombre de connexions actives
                cursor.execute("SELECT COUNT(*) FROM pg_stat_activity")
                active_connections = cursor.fetchone()[0]
                
                # Taille de la base de données
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """)
                db_size = cursor.fetchone()[0]
                
                # Statistiques des tables
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        n_tup_ins as inserts,
                        n_tup_upd as updates,
                        n_tup_del as deletes
                    FROM pg_stat_user_tables
                    ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC
                    LIMIT 10
                """)
                table_stats = cursor.fetchall()
                
                return {
                    'active_connections': active_connections,
                    'database_size': db_size,
                    'table_statistics': table_stats
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats DB: {str(e)}")
            return {
                'active_connections': 0,
                'database_size': 'Unknown',
                'table_statistics': []
            }


class CacheMonitor:
    """Moniteur spécifique pour le cache"""
    
    @staticmethod
    def get_cache_stats():
        """Récupère les statistiques du cache"""
        try:
            # Test de performance du cache
            start_time = time.time()
            cache.set('monitoring_test', 'test_value', 10)
            write_time = time.time() - start_time
            
            start_time = time.time()
            test_value = cache.get('monitoring_test')
            read_time = time.time() - start_time
            
            cache.delete('monitoring_test')
            
            return {
                'write_time': round(write_time * 1000, 2),  # ms
                'read_time': round(read_time * 1000, 2),    # ms
                'cache_backend': settings.CACHES['default']['BACKEND'],
                'cache_enabled': True
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats cache: {str(e)}")
            return {
                'write_time': 0,
                'read_time': 0,
                'cache_backend': 'Unknown',
                'cache_enabled': False
            }


class AlertManager:
    """Gestionnaire d'alertes de performance"""
    
    def __init__(self):
        self.alerts = deque(maxlen=100)
        self.thresholds = {
            'response_time': 2.0,      # 2 secondes
            'memory_usage': 80,        # 80%
            'cpu_usage': 80,           # 80%
            'error_rate': 5,           # 5%
            'cache_hit_rate': 50       # 50%
        }
    
    def check_alerts(self, stats):
        """Vérifie les alertes basées sur les statistiques"""
        alerts = []
        
        # Alerte temps de réponse
        if stats['response_times']['average'] > self.thresholds['response_time']:
            alerts.append({
                'type': 'HIGH_RESPONSE_TIME',
                'message': f"Temps de réponse élevé: {stats['response_times']['average']}s",
                'severity': 'warning'
            })
        
        # Alerte utilisation mémoire
        if stats['system']['memory_usage'] > self.thresholds['memory_usage']:
            alerts.append({
                'type': 'HIGH_MEMORY_USAGE',
                'message': f"Utilisation mémoire élevée: {stats['system']['memory_usage']}%",
                'severity': 'critical'
            })
        
        # Alerte utilisation CPU
        if stats['system']['cpu_usage'] > self.thresholds['cpu_usage']:
            alerts.append({
                'type': 'HIGH_CPU_USAGE',
                'message': f"Utilisation CPU élevée: {stats['system']['cpu_usage']}%",
                'severity': 'warning'
            })
        
        # Alerte taux de cache
        if stats['cache']['hit_rate'] < self.thresholds['cache_hit_rate']:
            alerts.append({
                'type': 'LOW_CACHE_HIT_RATE',
                'message': f"Taux de cache faible: {stats['cache']['hit_rate']}%",
                'severity': 'info'
            })
        
        # Enregistrer les alertes
        for alert in alerts:
            self.alerts.append({
                **alert,
                'timestamp': time.time()
            })
            logger.warning(f"Alerte performance: {alert['message']}")
        
        return alerts
    
    def get_recent_alerts(self, limit=10):
        """Récupère les alertes récentes"""
        return list(self.alerts)[-limit:]


# Instance globale du moniteur
performance_monitor = PerformanceMonitor()
alert_manager = AlertManager() 
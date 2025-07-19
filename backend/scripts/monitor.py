#!/usr/bin/env python3
"""
Script de monitoring pour CommuniConnect en production
Surveille l'état de l'application, Redis, PostgreSQL et les performances
"""

import os
import sys
import time
import json
import logging
import requests
import psutil
import redis
import psycopg2
from datetime import datetime, timedelta
from decouple import config
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings_production')
django.setup()

from django.core.cache import cache
from django.db import connection
from posts.models import Post
from users.models import User

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/communiconnect/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CommuniConnectMonitor:
    def __init__(self):
        self.redis_client = None
        self.db_connection = None
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': {},
            'database': {},
            'redis': {},
            'application': {},
            'performance': {}
        }
    
    def check_system_resources(self):
        """Vérifier les ressources système"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.metrics['system'] = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'memory_total': memory.total,
                'disk_percent': disk.percent,
                'disk_free': disk.free,
                'disk_total': disk.total,
                'load_average': psutil.getloadavg()
            }
            
            logger.info(f"Système: CPU {cpu_percent}%, RAM {memory.percent}%, Disque {disk.percent}%")
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification système: {e}")
    
    def check_redis(self):
        """Vérifier l'état de Redis"""
        try:
            if not self.redis_client:
                self.redis_client = redis.Redis(
                    host=config('REDIS_HOST', default='localhost'),
                    port=config('REDIS_PORT', default=6379, cast=int),
                    password=config('REDIS_PASSWORD', default=''),
                    db=0,
                    socket_timeout=5
                )
            
            # Test de connexion
            self.redis_client.ping()
            
            # Informations Redis
            info = self.redis_client.info()
            
            self.metrics['redis'] = {
                'connected': True,
                'used_memory': info.get('used_memory', 0),
                'used_memory_human': info.get('used_memory_human', '0B'),
                'connected_clients': info.get('connected_clients', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'uptime_in_seconds': info.get('uptime_in_seconds', 0)
            }
            
            # Calculer le hit ratio
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            hit_ratio = (hits / total * 100) if total > 0 else 0
            
            self.metrics['redis']['hit_ratio'] = hit_ratio
            
            logger.info(f"Redis: Connecté, {info.get('connected_clients', 0)} clients, Hit ratio: {hit_ratio:.2f}%")
            
        except Exception as e:
            logger.error(f"Erreur Redis: {e}")
            self.metrics['redis'] = {'connected': False, 'error': str(e)}
    
    def check_database(self):
        """Vérifier l'état de la base de données"""
        try:
            with connection.cursor() as cursor:
                # Test de connexion
                cursor.execute("SELECT 1")
                cursor.fetchone()
                
                # Statistiques de la base de données
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE schemaname = 'public'
                    LIMIT 10
                """)
                
                # Compter les enregistrements
                cursor.execute("SELECT COUNT(*) FROM posts_post")
                posts_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM users_user")
                users_count = cursor.fetchone()[0]
                
                # Taille de la base de données
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """)
                db_size = cursor.fetchone()[0]
                
                self.metrics['database'] = {
                    'connected': True,
                    'posts_count': posts_count,
                    'users_count': users_count,
                    'database_size': db_size,
                    'active_connections': len(connection.queries) if hasattr(connection, 'queries') else 0
                }
                
                logger.info(f"Base de données: Connectée, {posts_count} posts, {users_count} utilisateurs")
                
        except Exception as e:
            logger.error(f"Erreur base de données: {e}")
            self.metrics['database'] = {'connected': False, 'error': str(e)}
    
    def check_application(self):
        """Vérifier l'état de l'application Django"""
        try:
            # Test du cache Django
            cache_key = 'monitor_test'
            cache.set(cache_key, 'test_value', 60)
            cache_value = cache.get(cache_key)
            
            # Statistiques de l'application
            recent_posts = Post.objects.filter(
                created_at__gte=datetime.now() - timedelta(hours=1)
            ).count()
            
            recent_users = User.objects.filter(
                date_joined__gte=datetime.now() - timedelta(hours=1)
            ).count()
            
            self.metrics['application'] = {
                'cache_working': cache_value == 'test_value',
                'recent_posts': recent_posts,
                'recent_users': recent_users,
                'total_posts': Post.objects.count(),
                'total_users': User.objects.count(),
                'django_version': django.get_version()
            }
            
            logger.info(f"Application: Cache OK, {recent_posts} posts récents, {recent_users} nouveaux utilisateurs")
            
        except Exception as e:
            logger.error(f"Erreur application: {e}")
            self.metrics['application'] = {'error': str(e)}
    
    def check_performance(self):
        """Vérifier les performances"""
        try:
            # Test de performance des requêtes
            start_time = time.time()
            
            # Test de requête simple
            posts = Post.objects.all()[:10]
            list(posts)  # Forcer l'exécution
            
            query_time = time.time() - start_time
            
            # Test de cache
            start_time = time.time()
            cache.get('performance_test')
            cache_time = time.time() - start_time
            
            self.metrics['performance'] = {
                'query_response_time': query_time,
                'cache_response_time': cache_time,
                'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
                'open_files': len(psutil.Process().open_files()),
                'threads': psutil.Process().num_threads()
            }
            
            logger.info(f"Performance: Requête {query_time:.3f}s, Cache {cache_time:.3f}s")
            
        except Exception as e:
            logger.error(f"Erreur performance: {e}")
            self.metrics['performance'] = {'error': str(e)}
    
    def check_external_services(self):
        """Vérifier les services externes"""
        try:
            # Test Cloudinary (si configuré)
            cloudinary_cloud_name = config('CLOUDINARY_CLOUD_NAME', default='')
            if cloudinary_cloud_name:
                response = requests.get(
                    f'https://res.cloudinary.com/{cloudinary_cloud_name}/image/upload/v1/test',
                    timeout=5
                )
                cloudinary_status = response.status_code == 200
            else:
                cloudinary_status = 'not_configured'
            
            self.metrics['external_services'] = {
                'cloudinary': cloudinary_status
            }
            
            if cloudinary_status == True:
                logger.info("Services externes: Cloudinary OK")
            elif cloudinary_status == 'not_configured':
                logger.info("Services externes: Cloudinary non configuré")
            else:
                logger.warning("Services externes: Cloudinary erreur")
                
        except Exception as e:
            logger.error(f"Erreur services externes: {e}")
            self.metrics['external_services'] = {'error': str(e)}
    
    def generate_alert(self):
        """Générer des alertes basées sur les métriques"""
        alerts = []
        
        # Alertes système
        if self.metrics['system'].get('cpu_percent', 0) > 80:
            alerts.append("CPU usage élevé (>80%)")
        
        if self.metrics['system'].get('memory_percent', 0) > 85:
            alerts.append("Mémoire usage élevé (>85%)")
        
        if self.metrics['system'].get('disk_percent', 0) > 90:
            alerts.append("Espace disque faible (>90%)")
        
        # Alertes Redis
        if not self.metrics['redis'].get('connected', False):
            alerts.append("Redis non connecté")
        
        # Alertes base de données
        if not self.metrics['database'].get('connected', False):
            alerts.append("Base de données non connectée")
        
        # Alertes application
        if not self.metrics['application'].get('cache_working', False):
            alerts.append("Cache Django défaillant")
        
        # Alertes performance
        if self.metrics['performance'].get('query_response_time', 0) > 1.0:
            alerts.append("Requêtes lentes (>1s)")
        
        if alerts:
            logger.warning(f"Alertes détectées: {', '.join(alerts)}")
            # Ici vous pourriez envoyer des notifications (email, Slack, etc.)
        
        return alerts
    
    def save_metrics(self):
        """Sauvegarder les métriques"""
        try:
            # Sauvegarder dans Redis pour l'historique
            if self.redis_client and self.redis_client.ping():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.redis_client.setex(
                    f'metrics:{timestamp}',
                    86400,  # 24 heures
                    json.dumps(self.metrics)
                )
                
                # Garder seulement les 100 dernières métriques
                keys = self.redis_client.keys('metrics:*')
                if len(keys) > 100:
                    keys.sort()
                    for key in keys[:-100]:
                        self.redis_client.delete(key)
            
            # Sauvegarder dans un fichier JSON
            metrics_file = '/var/log/communiconnect/metrics.json'
            with open(metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
                
        except Exception as e:
            logger.error(f"Erreur sauvegarde métriques: {e}")
    
    def run_monitoring_cycle(self):
        """Exécuter un cycle complet de monitoring"""
        logger.info("Début du cycle de monitoring...")
        
        self.metrics['timestamp'] = datetime.now().isoformat()
        
        self.check_system_resources()
        self.check_redis()
        self.check_database()
        self.check_application()
        self.check_performance()
        self.check_external_services()
        
        alerts = self.generate_alert()
        self.save_metrics()
        
        logger.info("Cycle de monitoring terminé")
        return alerts

def main():
    """Fonction principale"""
    monitor = CommuniConnectMonitor()
    
    logger.info("Démarrage du monitoring CommuniConnect...")
    
    while True:
        try:
            alerts = monitor.run_monitoring_cycle()
            
            # Attendre 5 minutes avant le prochain cycle
            time.sleep(300)
            
        except KeyboardInterrupt:
            logger.info("Arrêt du monitoring...")
            break
        except Exception as e:
            logger.error(f"Erreur critique dans le monitoring: {e}")
            time.sleep(60)  # Attendre 1 minute avant de réessayer

if __name__ == '__main__':
    main() 
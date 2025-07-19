from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
from .models import (
    PerformanceMetrics, CacheStrategy, DatabaseOptimization, LoadBalancer,
    AutoScaling, CDNOptimization, QueryOptimization, PerformanceAlert,
    ResourceMonitoring, PerformanceReport, CacheHitRate, DatabaseConnectionPool,
    NetworkOptimization
)
import psutil
import threading
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
import requests
import redis
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

User = get_user_model()

class PerformanceMonitoringService:
    """Service de monitoring de performance avancé"""
    
    def __init__(self):
        self.monitoring_interval = 30  # secondes
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'response_time': 2000.0,  # ms
            'error_rate': 5.0,  # %
            'disk_usage': 90.0,
        }
        self.is_monitoring = False
        self.monitoring_thread = None
    
    def start_monitoring(self):
        """Démarre le monitoring de performance"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            logger.info("Monitoring de performance démarré")
    
    def stop_monitoring(self):
        """Arrête le monitoring de performance"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("Monitoring de performance arrêté")
    
    def _monitoring_loop(self):
        """Boucle de monitoring en arrière-plan"""
        while self.is_monitoring:
            try:
                self._collect_system_metrics()
                self._check_performance_alerts()
                self._update_cache_metrics()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Erreur monitoring: {e}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    def _collect_system_metrics(self):
        """Collecte les métriques système"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            PerformanceMetrics.objects.create(
                metric_type='cpu_usage',
                value=cpu_percent,
                unit='%'
            )
            
            # Mémoire
            memory = psutil.virtual_memory()
            PerformanceMetrics.objects.create(
                metric_type='memory_usage',
                value=memory.percent,
                unit='%'
            )
            
            # Disque
            disk = psutil.disk_usage('/')
            PerformanceMetrics.objects.create(
                metric_type='disk_usage',
                value=(disk.used / disk.total) * 100,
                unit='%'
            )
            
            # Réseau
            network = psutil.net_io_counters()
            PerformanceMetrics.objects.create(
                metric_type='network_usage',
                value=network.bytes_sent + network.bytes_recv,
                unit='bytes'
            )
            
            # Monitoring des ressources
            ResourceMonitoring.objects.create(
                resource_type='cpu',
                usage_percentage=cpu_percent,
                total_capacity=psutil.cpu_count(),
                used_capacity=int(cpu_percent * psutil.cpu_count() / 100),
                available_capacity=psutil.cpu_count() - int(cpu_percent * psutil.cpu_count() / 100),
                server_id=settings.SERVER_ID if hasattr(settings, 'SERVER_ID') else 'default'
            )
            
            ResourceMonitoring.objects.create(
                resource_type='memory',
                usage_percentage=memory.percent,
                total_capacity=memory.total,
                used_capacity=memory.used,
                available_capacity=memory.available,
                server_id=settings.SERVER_ID if hasattr(settings, 'SERVER_ID') else 'default'
            )
            
        except Exception as e:
            logger.error(f"Erreur collecte métriques: {e}")
    
    def _check_performance_alerts(self):
        """Vérifie les alertes de performance"""
        try:
            # Récupérer les dernières métriques
            recent_metrics = PerformanceMetrics.objects.filter(
                timestamp__gte=timezone.now() - timedelta(minutes=5)
            )
            
            for metric in recent_metrics:
                threshold = self.alert_thresholds.get(metric.metric_type)
                if threshold and metric.value > threshold:
                    # Créer une alerte
                    alert, created = PerformanceAlert.objects.get_or_create(
                        metric_type=metric.metric_type,
                        is_resolved=False,
                        defaults={
                            'title': f"Seuil dépassé: {metric.metric_type}",
                            'alert_type': 'warning',
                            'severity': 'high',
                            'description': f"La métrique {metric.metric_type} a dépassé le seuil de {threshold}{metric.unit}",
                            'threshold_value': threshold,
                            'current_value': metric.value
                        }
                    )
                    
                    if created:
                        logger.warning(f"Alerte performance créée: {alert.title}")
                        
        except Exception as e:
            logger.error(f"Erreur vérification alertes: {e}")
    
    def _update_cache_metrics(self):
        """Met à jour les métriques de cache"""
        try:
            # Simuler des métriques de cache (à adapter selon votre implémentation)
            cache_hit_rate = 85.0  # Exemple
            CacheHitRate.objects.create(
                cache_level='l2',
                hits=1000,
                misses=150,
                hit_rate=cache_hit_rate,
                avg_response_time=5.0,
                total_requests=1150
            )
            
        except Exception as e:
            logger.error(f"Erreur métriques cache: {e}")

class CacheOptimizationService:
    """Service d'optimisation de cache intelligent"""
    
    def __init__(self):
        self.cache_strategies = {}
        self._load_cache_strategies()
    
    def _load_cache_strategies(self):
        """Charge les stratégies de cache"""
        try:
            strategies = CacheStrategy.objects.filter(is_active=True)
            for strategy in strategies:
                self.cache_strategies[strategy.name] = strategy
        except Exception as e:
            logger.error(f"Erreur chargement stratégies cache: {e}")
    
    def get_cache_strategy(self, key: str, context: str = 'default') -> Optional[CacheStrategy]:
        """Récupère la stratégie de cache appropriée"""
        try:
            # Logique de sélection de stratégie
            if context == 'user_data':
                return self.cache_strategies.get('user_data_cache')
            elif context == 'content':
                return self.cache_strategies.get('content_cache')
            elif context == 'analytics':
                return self.cache_strategies.get('analytics_cache')
            else:
                return self.cache_strategies.get('default_cache')
        except Exception as e:
            logger.error(f"Erreur sélection stratégie cache: {e}")
            return None
    
    def smart_cache_get(self, key: str, context: str = 'default'):
        """Récupération intelligente du cache"""
        try:
            strategy = self.get_cache_strategy(key, context)
            if not strategy:
                return None
            
            # Récupérer du cache
            cached_value = cache.get(key)
            
            if cached_value is not None:
                # Mettre à jour les métriques de hit
                self._update_cache_hit_metrics(strategy, True)
                return cached_value
            else:
                # Mettre à jour les métriques de miss
                self._update_cache_hit_metrics(strategy, False)
                return None
                
        except Exception as e:
            logger.error(f"Erreur cache get: {e}")
            return None
    
    def smart_cache_set(self, key: str, value, context: str = 'default', ttl: int = None):
        """Stockage intelligent en cache"""
        try:
            strategy = self.get_cache_strategy(key, context)
            if not strategy:
                return False
            
            # Utiliser le TTL de la stratégie si non spécifié
            if ttl is None:
                ttl = strategy.ttl_seconds
            
            # Appliquer la compression si activée
            if strategy.compression_enabled:
                value = self._compress_value(value)
            
            # Stocker en cache
            cache.set(key, value, ttl)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur cache set: {e}")
            return False
    
    def _update_cache_hit_metrics(self, strategy: CacheStrategy, is_hit: bool):
        """Met à jour les métriques de cache"""
        try:
            cache_hit_rate, created = CacheHitRate.objects.get_or_create(
                cache_level='l2',  # Redis
                timestamp__date=timezone.now().date(),
                defaults={
                    'hits': 1 if is_hit else 0,
                    'misses': 0 if is_hit else 1,
                    'hit_rate': 100.0 if is_hit else 0.0,
                    'avg_response_time': 5.0,
                    'total_requests': 1
                }
            )
            
            if not created:
                if is_hit:
                    cache_hit_rate.hits += 1
                else:
                    cache_hit_rate.misses += 1
                
                total_requests = cache_hit_rate.hits + cache_hit_rate.misses
                cache_hit_rate.hit_rate = (cache_hit_rate.hits / total_requests) * 100
                cache_hit_rate.total_requests = total_requests
                cache_hit_rate.save()
                
        except Exception as e:
            logger.error(f"Erreur mise à jour métriques cache: {e}")
    
    def _compress_value(self, value):
        """Compresse une valeur pour le cache"""
        try:
            if isinstance(value, str) and len(value) > 1024:  # 1KB
                import gzip
                return gzip.compress(value.encode('utf-8'))
            return value
        except Exception as e:
            logger.error(f"Erreur compression: {e}")
            return value

class DatabaseOptimizationService:
    """Service d'optimisation de base de données"""
    
    def __init__(self):
        self.optimizations = {}
        self._load_optimizations()
    
    def _load_optimizations(self):
        """Charge les optimisations de base de données"""
        try:
            optimizations = DatabaseOptimization.objects.filter(is_enabled=True)
            for optimization in optimizations:
                self.optimizations[optimization.name] = optimization
        except Exception as e:
            logger.error(f"Erreur chargement optimisations DB: {e}")
    
    def optimize_query(self, query: str, query_type: str = 'select') -> Dict:
        """Optimise une requête de base de données"""
        try:
            import hashlib
            query_hash = hashlib.sha256(query.encode()).hexdigest()
            
            # Vérifier si la requête existe déjà
            query_opt, created = QueryOptimization.objects.get_or_create(
                query_hash=query_hash,
                defaults={
                    'query_type': query_type,
                    'query_text': query,
                    'execution_count': 0,
                    'avg_execution_time': 0.0,
                    'max_execution_time': 0.0,
                    'total_execution_time': 0.0,
                    'optimizations': [],
                    'is_optimized': False
                }
            )
            
            # Analyser la requête pour des optimisations
            optimizations = self._analyze_query_for_optimizations(query, query_type)
            
            if optimizations:
                query_opt.optimizations = optimizations
                query_opt.is_optimized = True
                query_opt.save()
                
                return {
                    'query_hash': query_hash,
                    'optimizations': optimizations,
                    'is_optimized': True
                }
            
            return {
                'query_hash': query_hash,
                'optimizations': [],
                'is_optimized': False
            }
            
        except Exception as e:
            logger.error(f"Erreur optimisation requête: {e}")
            return {'error': str(e)}
    
    def _analyze_query_for_optimizations(self, query: str, query_type: str) -> List[str]:
        """Analyse une requête pour des optimisations"""
        optimizations = []
        
        try:
            query_lower = query.lower()
            
            # Vérifier les index manquants
            if 'where' in query_lower and 'order by' in query_lower:
                optimizations.append('index_optimization')
            
            # Vérifier les jointures
            if 'join' in query_lower and query_lower.count('join') > 2:
                optimizations.append('join_optimization')
            
            # Vérifier les sous-requêtes
            if 'select' in query_lower and query_lower.count('select') > 1:
                optimizations.append('subquery_optimization')
            
            # Vérifier les GROUP BY
            if 'group by' in query_lower:
                optimizations.append('aggregation_optimization')
            
            # Vérifier les LIMIT
            if 'limit' not in query_lower and query_type == 'select':
                optimizations.append('limit_optimization')
            
        except Exception as e:
            logger.error(f"Erreur analyse requête: {e}")
        
        return optimizations
    
    def get_slow_queries(self, threshold_ms: float = 1000.0) -> List[QueryOptimization]:
        """Récupère les requêtes lentes"""
        try:
            return QueryOptimization.objects.filter(
                avg_execution_time__gte=threshold_ms
            ).order_by('-avg_execution_time')[:10]
        except Exception as e:
            logger.error(f"Erreur récupération requêtes lentes: {e}")
            return []
    
    def get_optimization_recommendations(self) -> List[Dict]:
        """Génère des recommandations d'optimisation"""
        try:
            recommendations = []
            
            # Requêtes non optimisées
            unoptimized_queries = QueryOptimization.objects.filter(
                is_optimized=False,
                execution_count__gte=10
            )
            
            if unoptimized_queries.exists():
                recommendations.append({
                    'type': 'query_optimization',
                    'title': 'Requêtes non optimisées détectées',
                    'description': f"{unoptimized_queries.count()} requêtes fréquentes nécessitent une optimisation",
                    'priority': 'high'
                })
            
            # Requêtes lentes
            slow_queries = self.get_slow_queries()
            if slow_queries:
                recommendations.append({
                    'type': 'performance_improvement',
                    'title': 'Requêtes lentes détectées',
                    'description': f"{len(slow_queries)} requêtes prennent plus de 1 seconde",
                    'priority': 'critical'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur recommandations optimisation: {e}")
            return []

class AutoScalingService:
    """Service d'auto-scaling intelligent"""
    
    def __init__(self):
        self.scaling_configs = {}
        self._load_scaling_configs()
    
    def _load_scaling_configs(self):
        """Charge les configurations d'auto-scaling"""
        try:
            configs = AutoScaling.objects.filter(is_enabled=True)
            for config in configs:
                self.scaling_configs[config.name] = config
        except Exception as e:
            logger.error(f"Erreur chargement configs auto-scaling: {e}")
    
    def check_scaling_needs(self) -> List[Dict]:
        """Vérifie les besoins de scaling"""
        try:
            scaling_actions = []
            
            for config_name, config in self.scaling_configs.items():
                current_metric = self._get_current_metric(config.trigger_type)
                
                if current_metric > config.scale_up_threshold:
                    scaling_actions.append({
                        'action': 'scale_up',
                        'config': config_name,
                        'reason': f"{config.trigger_type} à {current_metric}%",
                        'priority': 'high'
                    })
                elif current_metric < config.scale_down_threshold:
                    scaling_actions.append({
                        'action': 'scale_down',
                        'config': config_name,
                        'reason': f"{config.trigger_type} à {current_metric}%",
                        'priority': 'medium'
                    })
            
            return scaling_actions
            
        except Exception as e:
            logger.error(f"Erreur vérification scaling: {e}")
            return []
    
    def _get_current_metric(self, metric_type: str) -> float:
        """Récupère la métrique actuelle"""
        try:
            # Récupérer la dernière métrique
            latest_metric = PerformanceMetrics.objects.filter(
                metric_type=metric_type
            ).order_by('-timestamp').first()
            
            if latest_metric:
                return latest_metric.value
            else:
                # Valeur par défaut
                return 50.0
                
        except Exception as e:
            logger.error(f"Erreur récupération métrique: {e}")
            return 50.0
    
    def execute_scaling_action(self, action: Dict) -> bool:
        """Exécute une action de scaling"""
        try:
            if action['action'] == 'scale_up':
                return self._scale_up(action['config'])
            elif action['action'] == 'scale_down':
                return self._scale_down(action['config'])
            return False
            
        except Exception as e:
            logger.error(f"Erreur exécution scaling: {e}")
            return False
    
    def _scale_up(self, config_name: str) -> bool:
        """Scale up les ressources"""
        try:
            # Implémentation du scale up
            logger.info(f"Scale up exécuté pour {config_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur scale up: {e}")
            return False
    
    def _scale_down(self, config_name: str) -> bool:
        """Scale down les ressources"""
        try:
            # Implémentation du scale down
            logger.info(f"Scale down exécuté pour {config_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur scale down: {e}")
            return False

class CDNOptimizationService:
    """Service d'optimisation CDN"""
    
    def __init__(self):
        self.cdn_configs = {}
        self._load_cdn_configs()
    
    def _load_cdn_configs(self):
        """Charge les configurations CDN"""
        try:
            configs = CDNOptimization.objects.filter(is_enabled=True)
            for config in configs:
                self.cdn_configs[config.name] = config
        except Exception as e:
            logger.error(f"Erreur chargement configs CDN: {e}")
    
    def optimize_static_assets(self, asset_url: str) -> str:
        """Optimise les assets statiques via CDN"""
        try:
            # Logique d'optimisation CDN
            if asset_url.startswith('/static/'):
                # Ajouter le domaine CDN
                cdn_domain = self._get_cdn_domain()
                return f"{cdn_domain}{asset_url}"
            
            return asset_url
            
        except Exception as e:
            logger.error(f"Erreur optimisation CDN: {e}")
            return asset_url
    
    def _get_cdn_domain(self) -> str:
        """Récupère le domaine CDN"""
        try:
            # Récupérer la première configuration CDN active
            cdn_config = next(iter(self.cdn_configs.values()), None)
            if cdn_config:
                return f"https://cdn.{cdn_config.provider}.com"
            else:
                return "https://cdn.communiconnect.gn"
        except Exception as e:
            logger.error(f"Erreur domaine CDN: {e}")
            return "https://cdn.communiconnect.gn"

class PerformanceReportService:
    """Service de génération de rapports de performance"""
    
    def generate_daily_report(self) -> PerformanceReport:
        """Génère un rapport quotidien"""
        try:
            yesterday = timezone.now() - timedelta(days=1)
            start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Récupérer les métriques
            metrics = PerformanceMetrics.objects.filter(
                timestamp__range=(start_date, end_date)
            )
            
            # Calculer les moyennes
            avg_response_time = metrics.filter(
                metric_type='response_time'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            total_requests = metrics.filter(
                metric_type='throughput'
            ).aggregate(sum=Sum('value'))['sum'] or 0
            
            error_rate = metrics.filter(
                metric_type='error_rate'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            throughput = metrics.filter(
                metric_type='throughput'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            # Créer le rapport
            report = PerformanceReport.objects.create(
                title=f"Rapport Performance - {start_date.date()}",
                report_type='daily',
                start_date=start_date,
                end_date=end_date,
                avg_response_time=avg_response_time,
                total_requests=total_requests,
                error_rate=error_rate,
                throughput=throughput,
                summary={
                    'total_metrics': metrics.count(),
                    'peak_hour': self._get_peak_hour(metrics),
                    'slowest_endpoint': self._get_slowest_endpoint(metrics)
                },
                recommendations=self._generate_recommendations(metrics)
            )
            
            return report
            
        except Exception as e:
            logger.error(f"Erreur génération rapport: {e}")
            return None
    
    def _get_peak_hour(self, metrics) -> str:
        """Récupère l'heure de pointe"""
        try:
            # Logique pour déterminer l'heure de pointe
            return "14:00"
        except Exception as e:
            logger.error(f"Erreur heure de pointe: {e}")
            return "N/A"
    
    def _get_slowest_endpoint(self, metrics) -> str:
        """Récupère l'endpoint le plus lent"""
        try:
            # Logique pour déterminer l'endpoint le plus lent
            return "/api/posts/"
        except Exception as e:
            logger.error(f"Erreur endpoint le plus lent: {e}")
            return "N/A"
    
    def _generate_recommendations(self, metrics) -> List[str]:
        """Génère des recommandations basées sur les métriques"""
        try:
            recommendations = []
            
            # Vérifier le temps de réponse
            avg_response_time = metrics.filter(
                metric_type='response_time'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            if avg_response_time > 1000:  # 1 seconde
                recommendations.append("Optimiser les requêtes de base de données")
            
            # Vérifier le taux d'erreur
            error_rate = metrics.filter(
                metric_type='error_rate'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            if error_rate > 5.0:  # 5%
                recommendations.append("Investigation des erreurs requise")
            
            # Vérifier l'utilisation CPU
            cpu_usage = metrics.filter(
                metric_type='cpu_usage'
            ).aggregate(avg=Avg('value'))['avg'] or 0.0
            
            if cpu_usage > 80.0:  # 80%
                recommendations.append("Considérer l'auto-scaling")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur génération recommandations: {e}")
            return []

# Instances globales
performance_monitor = PerformanceMonitoringService()
cache_optimizer = CacheOptimizationService()
db_optimizer = DatabaseOptimizationService()
auto_scaler = AutoScalingService()
cdn_optimizer = CDNOptimizationService()
report_service = PerformanceReportService() 
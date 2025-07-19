from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Avg, Max, Min, Count, Sum, Q
from .models import (
    PerformanceMetrics, CacheStrategy, DatabaseOptimization, LoadBalancer,
    AutoScaling, CDNOptimization, QueryOptimization, PerformanceAlert,
    ResourceMonitoring, PerformanceReport, CacheHitRate, DatabaseConnectionPool,
    NetworkOptimization
)
from .services import (
    performance_monitor, cache_optimizer, db_optimizer, 
    auto_scaler, cdn_optimizer, report_service
)
import logging
from datetime import datetime, timedelta
import psutil

logger = logging.getLogger(__name__)

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_performance_metrics(request):
    """
    Endpoint pour récupérer les métriques de performance
    """
    try:
        # Paramètres de filtrage
        metric_type = request.GET.get('type')
        hours = int(request.GET.get('hours', 24))
        limit = int(request.GET.get('limit', 100))
        
        # Construire la requête
        query = PerformanceMetrics.objects.all()
        
        if metric_type:
            query = query.filter(metric_type=metric_type)
        
        # Filtrer par période
        start_time = timezone.now() - timedelta(hours=hours)
        query = query.filter(timestamp__gte=start_time)
        
        # Limiter les résultats
        metrics = query.order_by('-timestamp')[:limit]
        
        # Formater les données
        metrics_data = []
        for metric in metrics:
            metrics_data.append({
                'id': metric.id,
                'metric_type': metric.metric_type,
                'value': metric.value,
                'unit': metric.unit,
                'timestamp': metric.timestamp.isoformat(),
                'endpoint': metric.endpoint,
                'user_id': metric.user_id.id if metric.user_id else None,
                'region': metric.region,
                'server_id': metric.server_id,
                'environment': metric.environment
            })
        
        # Calculer les statistiques
        stats = query.aggregate(
            avg_value=Avg('value'),
            max_value=Max('value'),
            min_value=Min('value'),
            count=Count('id')
        )
        
        response_data = {
            'metrics': metrics_data,
            'statistics': {
                'average': stats['avg_value'] or 0.0,
                'maximum': stats['max_value'] or 0.0,
                'minimum': stats['min_value'] or 0.0,
                'count': stats['count'] or 0
            },
            'filters': {
                'metric_type': metric_type,
                'hours': hours,
                'limit': limit
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération métriques performance: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des métriques'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_system_resources(request):
    """
    Endpoint pour récupérer les ressources système
    """
    try:
        # Récupérer les dernières métriques de ressources
        recent_resources = ResourceMonitoring.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).order_by('-timestamp')
        
        resources_data = {}
        for resource in recent_resources:
            if resource.resource_type not in resources_data:
                resources_data[resource.resource_type] = []
            
            resources_data[resource.resource_type].append({
                'timestamp': resource.timestamp.isoformat(),
                'usage_percentage': resource.usage_percentage,
                'total_capacity': resource.total_capacity,
                'used_capacity': resource.used_capacity,
                'available_capacity': resource.available_capacity,
                'details': resource.details
            })
        
        # Métriques système en temps réel
        real_time_metrics = {
            'cpu': {
                'usage_percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'used': psutil.virtual_memory().used,
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
            },
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv,
                'packets_sent': psutil.net_io_counters().packets_sent,
                'packets_recv': psutil.net_io_counters().packets_recv
            }
        }
        
        response_data = {
            'historical_data': resources_data,
            'real_time_metrics': real_time_metrics
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération ressources système: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des ressources système'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_cache_performance(request):
    """
    Endpoint pour récupérer les performances du cache
    """
    try:
        # Récupérer les métriques de cache récentes
        cache_metrics = CacheHitRate.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-timestamp')
        
        cache_data = {}
        for metric in cache_metrics:
            if metric.cache_level not in cache_data:
                cache_data[metric.cache_level] = []
            
            cache_data[metric.cache_level].append({
                'timestamp': metric.timestamp.isoformat(),
                'hits': metric.hits,
                'misses': metric.misses,
                'hit_rate': metric.hit_rate,
                'avg_response_time': metric.avg_response_time,
                'total_requests': metric.total_requests
            })
        
        # Statistiques globales du cache
        global_stats = cache_metrics.aggregate(
            avg_hit_rate=Avg('hit_rate'),
            total_hits=Sum('hits'),
            total_misses=Sum('misses'),
            avg_response_time=Avg('avg_response_time')
        )
        
        # Stratégies de cache actives
        active_strategies = CacheStrategy.objects.filter(is_active=True)
        strategies_data = []
        for strategy in active_strategies:
            strategies_data.append({
                'name': strategy.name,
                'cache_type': strategy.cache_type,
                'strategy_type': strategy.strategy_type,
                'ttl_seconds': strategy.ttl_seconds,
                'max_size_mb': strategy.max_size_mb,
                'compression_enabled': strategy.compression_enabled,
                'encryption_enabled': strategy.encryption_enabled
            })
        
        response_data = {
            'cache_metrics': cache_data,
            'global_statistics': {
                'average_hit_rate': global_stats['avg_hit_rate'] or 0.0,
                'total_hits': global_stats['total_hits'] or 0,
                'total_misses': global_stats['total_misses'] or 0,
                'average_response_time': global_stats['avg_response_time'] or 0.0
            },
            'active_strategies': strategies_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération performance cache: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des performances du cache'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_slow_queries(request):
    """
    Endpoint pour récupérer les requêtes lentes
    """
    try:
        threshold_ms = float(request.GET.get('threshold', 1000.0))
        limit = int(request.GET.get('limit', 20))
        
        # Récupérer les requêtes lentes
        slow_queries = QueryOptimization.objects.filter(
            avg_execution_time__gte=threshold_ms
        ).order_by('-avg_execution_time')[:limit]
        
        queries_data = []
        for query in slow_queries:
            queries_data.append({
                'query_hash': query.query_hash,
                'query_type': query.query_type,
                'query_text': query.query_text[:200] + '...' if len(query.query_text) > 200 else query.query_text,
                'execution_count': query.execution_count,
                'avg_execution_time': query.avg_execution_time,
                'max_execution_time': query.max_execution_time,
                'total_execution_time': query.total_execution_time,
                'optimizations': query.optimizations,
                'is_optimized': query.is_optimized,
                'first_seen': query.first_seen.isoformat(),
                'last_seen': query.last_seen.isoformat()
            })
        
        # Statistiques des requêtes
        query_stats = QueryOptimization.objects.aggregate(
            total_queries=Count('id'),
            optimized_queries=Count('id', filter=Q(is_optimized=True)),
            avg_execution_time=Avg('avg_execution_time'),
            max_execution_time=Max('max_execution_time')
        )
        
        response_data = {
            'slow_queries': queries_data,
            'statistics': {
                'total_queries': query_stats['total_queries'] or 0,
                'optimized_queries': query_stats['optimized_queries'] or 0,
                'average_execution_time': query_stats['avg_execution_time'] or 0.0,
                'max_execution_time': query_stats['max_execution_time'] or 0.0
            },
            'filters': {
                'threshold_ms': threshold_ms,
                'limit': limit
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération requêtes lentes: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des requêtes lentes'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_performance_alerts(request):
    """
    Endpoint pour récupérer les alertes de performance
    """
    try:
        # Paramètres de filtrage
        severity = request.GET.get('severity')
        is_resolved = request.GET.get('resolved')
        hours = int(request.GET.get('hours', 24))
        
        # Construire la requête
        query = PerformanceAlert.objects.all()
        
        if severity:
            query = query.filter(severity=severity)
        
        if is_resolved is not None:
            query = query.filter(is_resolved=is_resolved.lower() == 'true')
        
        # Filtrer par période
        start_time = timezone.now() - timedelta(hours=hours)
        query = query.filter(created_at__gte=start_time)
        
        alerts = query.order_by('-created_at')
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': alert.id,
                'title': alert.title,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'description': alert.description,
                'metric_type': alert.metric_type,
                'threshold_value': alert.threshold_value,
                'current_value': alert.current_value,
                'is_resolved': alert.is_resolved,
                'resolved_at': alert.resolved_at.isoformat() if alert.resolved_at else None,
                'resolved_by': alert.resolved_by.username if alert.resolved_by else None,
                'created_at': alert.created_at.isoformat(),
                'updated_at': alert.updated_at.isoformat()
            })
        
        # Statistiques des alertes
        alert_stats = query.aggregate(
            total_alerts=Count('id'),
            critical_alerts=Count('id', filter=Q(severity='critical')),
            high_alerts=Count('id', filter=Q(severity='high')),
            resolved_alerts=Count('id', filter=Q(is_resolved=True))
        )
        
        response_data = {
            'alerts': alerts_data,
            'statistics': {
                'total_alerts': alert_stats['total_alerts'] or 0,
                'critical_alerts': alert_stats['critical_alerts'] or 0,
                'high_alerts': alert_stats['high_alerts'] or 0,
                'resolved_alerts': alert_stats['resolved_alerts'] or 0
            },
            'filters': {
                'severity': severity,
                'resolved': is_resolved,
                'hours': hours
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération alertes performance: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des alertes'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def resolve_alert(request):
    """
    Endpoint pour résoudre une alerte
    """
    try:
        alert_id = request.data.get('alert_id')
        user = request.user
        
        if not alert_id:
            return Response(
                {'error': 'ID d\'alerte requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            alert = PerformanceAlert.objects.get(id=alert_id)
        except PerformanceAlert.DoesNotExist:
            return Response(
                {'error': 'Alerte non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Marquer l'alerte comme résolue
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = user
        alert.save()
        
        response_data = {
            'alert_id': alert_id,
            'resolved': True,
            'resolved_at': alert.resolved_at.isoformat(),
            'resolved_by': user.username,
            'message': 'Alerte résolue avec succès'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur résolution alerte: {e}")
        return Response(
            {'error': 'Erreur lors de la résolution de l\'alerte'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_auto_scaling_status(request):
    """
    Endpoint pour récupérer le statut de l'auto-scaling
    """
    try:
        # Récupérer les configurations d'auto-scaling
        scaling_configs = AutoScaling.objects.filter(is_enabled=True)
        
        configs_data = []
        for config in scaling_configs:
            # Vérifier les besoins de scaling
            scaling_needs = auto_scaler.check_scaling_needs()
            current_needs = [need for need in scaling_needs if need['config'] == config.name]
            
            configs_data.append({
                'name': config.name,
                'scaling_type': config.scaling_type,
                'trigger_type': config.trigger_type,
                'min_instances': config.min_instances,
                'max_instances': config.max_instances,
                'scale_up_threshold': config.scale_up_threshold,
                'scale_down_threshold': config.scale_down_threshold,
                'cooldown_period': config.cooldown_period,
                'is_enabled': config.is_enabled,
                'scaling_needs': current_needs
            })
        
        # Statut global de l'auto-scaling
        global_scaling_needs = auto_scaler.check_scaling_needs()
        
        response_data = {
            'configurations': configs_data,
            'global_status': {
                'total_configs': len(configs_data),
                'active_configs': len([c for c in configs_data if c['is_enabled']]),
                'scaling_actions_needed': len(global_scaling_needs),
                'scaling_needs': global_scaling_needs
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération statut auto-scaling: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération du statut auto-scaling'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def execute_scaling_action(request):
    """
    Endpoint pour exécuter une action de scaling
    """
    try:
        action = request.data.get('action')
        config_name = request.data.get('config_name')
        
        if not action or not config_name:
            return Response(
                {'error': 'Action et nom de configuration requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Exécuter l'action de scaling
        success = auto_scaler.execute_scaling_action({
            'action': action,
            'config': config_name
        })
        
        response_data = {
            'action': action,
            'config_name': config_name,
            'success': success,
            'message': f"Action de scaling {action} exécutée" if success else f"Échec de l'action {action}"
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur exécution action scaling: {e}")
        return Response(
            {'error': 'Erreur lors de l\'exécution de l\'action de scaling'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_performance_reports(request):
    """
    Endpoint pour récupérer les rapports de performance
    """
    try:
        report_type = request.GET.get('type')
        limit = int(request.GET.get('limit', 10))
        
        # Construire la requête
        query = PerformanceReport.objects.all()
        
        if report_type:
            query = query.filter(report_type=report_type)
        
        reports = query.order_by('-generated_at')[:limit]
        
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'title': report.title,
                'report_type': report.report_type,
                'start_date': report.start_date.isoformat(),
                'end_date': report.end_date.isoformat(),
                'avg_response_time': report.avg_response_time,
                'total_requests': report.total_requests,
                'error_rate': report.error_rate,
                'throughput': report.throughput,
                'summary': report.summary,
                'recommendations': report.recommendations,
                'generated_at': report.generated_at.isoformat(),
                'generated_by': report.generated_by.username if report.generated_by else None
            })
        
        response_data = {
            'reports': reports_data,
            'filters': {
                'report_type': report_type,
                'limit': limit
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération rapports performance: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des rapports'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_performance_report(request):
    """
    Endpoint pour générer un rapport de performance
    """
    try:
        report_type = request.data.get('report_type', 'daily')
        user = request.user
        
        # Générer le rapport
        if report_type == 'daily':
            report = report_service.generate_daily_report()
        else:
            return Response(
                {'error': 'Type de rapport non supporté'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if report:
            response_data = {
                'report_id': report.id,
                'title': report.title,
                'report_type': report.report_type,
                'start_date': report.start_date.isoformat(),
                'end_date': report.end_date.isoformat(),
                'avg_response_time': report.avg_response_time,
                'total_requests': report.total_requests,
                'error_rate': report.error_rate,
                'throughput': report.throughput,
                'summary': report.summary,
                'recommendations': report.recommendations,
                'generated_at': report.generated_at.isoformat(),
                'generated_by': user.username,
                'message': 'Rapport généré avec succès'
            }
        else:
            response_data = {
                'error': 'Erreur lors de la génération du rapport'
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur génération rapport performance: {e}")
        return Response(
            {'error': 'Erreur lors de la génération du rapport'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_optimization_recommendations(request):
    """
    Endpoint pour récupérer les recommandations d'optimisation
    """
    try:
        # Récupérer les recommandations de la base de données
        db_recommendations = db_optimizer.get_optimization_recommendations()
        
        # Recommandations système
        system_recommendations = []
        
        # Vérifier l'utilisation CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 80:
            system_recommendations.append({
                'type': 'system_optimization',
                'title': 'Utilisation CPU élevée',
                'description': f"L'utilisation CPU est à {cpu_usage}%. Considérer l'auto-scaling.",
                'priority': 'high'
            })
        
        # Vérifier l'utilisation mémoire
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 85:
            system_recommendations.append({
                'type': 'system_optimization',
                'title': 'Utilisation mémoire élevée',
                'description': f"L'utilisation mémoire est à {memory_usage}%. Optimiser le cache.",
                'priority': 'high'
            })
        
        # Vérifier l'utilisation disque
        disk_usage = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
        if disk_usage > 90:
            system_recommendations.append({
                'type': 'system_optimization',
                'title': 'Espace disque faible',
                'description': f"L'utilisation disque est à {disk_usage:.1f}%. Nettoyer les logs.",
                'priority': 'critical'
            })
        
        response_data = {
            'database_recommendations': db_recommendations,
            'system_recommendations': system_recommendations,
            'total_recommendations': len(db_recommendations) + len(system_recommendations)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération recommandations: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des recommandations'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def start_performance_monitoring(request):
    """
    Endpoint pour démarrer le monitoring de performance
    """
    try:
        performance_monitor.start_monitoring()
        
        response_data = {
            'status': 'started',
            'message': 'Monitoring de performance démarré',
            'interval_seconds': performance_monitor.monitoring_interval
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur démarrage monitoring: {e}")
        return Response(
            {'error': 'Erreur lors du démarrage du monitoring'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def stop_performance_monitoring(request):
    """
    Endpoint pour arrêter le monitoring de performance
    """
    try:
        performance_monitor.stop_monitoring()
        
        response_data = {
            'status': 'stopped',
            'message': 'Monitoring de performance arrêté'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur arrêt monitoring: {e}")
        return Response(
            {'error': 'Erreur lors de l\'arrêt du monitoring'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
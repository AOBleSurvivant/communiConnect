from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .performance import (
    performance_monitor, 
    alert_manager, 
    DatabaseMonitor, 
    CacheMonitor
)
import json

@api_view(['GET'])
@permission_classes([IsAdminUser])
def performance_dashboard(request):
    """Dashboard de performance pour les administrateurs"""
    
    # Récupérer les statistiques de performance
    performance_stats = performance_monitor.get_performance_stats()
    
    # Récupérer les statistiques de base de données
    db_stats = DatabaseMonitor.get_db_stats()
    
    # Récupérer les statistiques de cache
    cache_stats = CacheMonitor.get_cache_stats()
    
    # Vérifier les alertes
    alerts = alert_manager.check_alerts(performance_stats)
    
    # Compiler le dashboard
    dashboard_data = {
        'performance': performance_stats,
        'database': db_stats,
        'cache': cache_stats,
        'alerts': alerts,
        'recent_alerts': alert_manager.get_recent_alerts(5)
    }
    
    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def performance_metrics(request):
    """Métriques détaillées de performance"""
    
    # Récupérer les métriques selon les paramètres
    metric_type = request.GET.get('type', 'all')
    
    if metric_type == 'response_times':
        stats = performance_monitor.get_performance_stats()
        return Response({
            'response_times': stats['response_times'],
            'system': stats['system']
        })
    
    elif metric_type == 'cache':
        cache_stats = CacheMonitor.get_cache_stats()
        perf_stats = performance_monitor.get_performance_stats()
        return Response({
            'cache': cache_stats,
            'cache_performance': perf_stats['cache']
        })
    
    elif metric_type == 'database':
        db_stats = DatabaseMonitor.get_db_stats()
        perf_stats = performance_monitor.get_performance_stats()
        return Response({
            'database': db_stats,
            'db_performance': perf_stats['database']
        })
    
    else:
        # Toutes les métriques
        performance_stats = performance_monitor.get_performance_stats()
        db_stats = DatabaseMonitor.get_db_stats()
        cache_stats = CacheMonitor.get_cache_stats()
        
        return Response({
            'performance': performance_stats,
            'database': db_stats,
            'cache': cache_stats
        })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def performance_alerts(request):
    """Gestion des alertes de performance"""
    
    # Récupérer les alertes récentes
    recent_alerts = alert_manager.get_recent_alerts(
        limit=int(request.GET.get('limit', 10))
    )
    
    # Vérifier les nouvelles alertes
    current_stats = performance_monitor.get_performance_stats()
    new_alerts = alert_manager.check_alerts(current_stats)
    
    return Response({
        'recent_alerts': recent_alerts,
        'new_alerts': new_alerts,
        'alert_thresholds': alert_manager.thresholds
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_alert_thresholds(request):
    """Met à jour les seuils d'alerte"""
    
    try:
        new_thresholds = request.data.get('thresholds', {})
        
        # Mettre à jour les seuils
        for key, value in new_thresholds.items():
            if key in alert_manager.thresholds:
                alert_manager.thresholds[key] = float(value)
        
        return Response({
            'message': 'Seuils mis à jour avec succès',
            'thresholds': alert_manager.thresholds
        })
        
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la mise à jour: {str(e)}'
        }, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def system_health(request):
    """État de santé du système"""
    
    import psutil
    
    # Informations système
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Informations réseau
    network = psutil.net_io_counters()
    
    # État de santé global
    health_status = 'healthy'
    issues = []
    
    if cpu_percent > 80:
        health_status = 'warning'
        issues.append(f'CPU élevé: {cpu_percent}%')
    
    if memory.percent > 80:
        health_status = 'warning'
        issues.append(f'Mémoire élevée: {memory.percent}%')
    
    if disk.percent > 90:
        health_status = 'critical'
        issues.append(f'Espace disque critique: {disk.percent}%')
    
    return Response({
        'status': health_status,
        'issues': issues,
        'system': {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available': memory.available,
            'disk_percent': disk.percent,
            'disk_free': disk.free,
            'network_bytes_sent': network.bytes_sent,
            'network_bytes_recv': network.bytes_recv
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def performance_history(request):
    """Historique des performances"""
    
    # Récupérer l'historique selon les paramètres
    hours = int(request.GET.get('hours', 24))
    
    # Pour l'instant, on retourne les données récentes
    # En production, on utiliserait une base de données pour l'historique
    performance_stats = performance_monitor.get_performance_stats()
    
    return Response({
        'period': f'{hours}h',
        'current_stats': performance_stats,
        'note': 'L\'historique complet nécessite une base de données de métriques'
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_cache(request):
    """Vide le cache"""
    
    from django.core.cache import cache
    
    try:
        # Vider tout le cache
        cache.clear()
        
        return Response({
            'message': 'Cache vidé avec succès',
            'timestamp': time.time()
        })
        
    except Exception as e:
        return Response({
            'error': f'Erreur lors du vidage du cache: {str(e)}'
        }, status=500)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def cache_info(request):
    """Informations détaillées sur le cache"""
    
    from django.core.cache import cache
    from django.conf import settings
    
    try:
        # Test de performance du cache
        import time
        start_time = time.time()
        
        # Test d'écriture
        cache.set('test_key', 'test_value', 60)
        write_time = time.time() - start_time
        
        # Test de lecture
        start_time = time.time()
        test_value = cache.get('test_key')
        read_time = time.time() - start_time
        
        # Nettoyer
        cache.delete('test_key')
        
        return Response({
            'backend': settings.CACHES['default']['BACKEND'],
            'location': settings.CACHES['default'].get('LOCATION', 'N/A'),
            'timeout': settings.CACHES['default'].get('TIMEOUT', 'N/A'),
            'performance': {
                'write_time_ms': round(write_time * 1000, 2),
                'read_time_ms': round(read_time * 1000, 2)
            },
            'status': 'operational'
        })
        
    except Exception as e:
        return Response({
            'backend': 'Unknown',
            'error': str(e),
            'status': 'error'
        }) 
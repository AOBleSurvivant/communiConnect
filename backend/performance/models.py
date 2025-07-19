from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
import uuid
import json
import psutil
import threading
import time
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class PerformanceMetrics(models.Model):
    """Métriques de performance en temps réel"""
    METRIC_TYPES = [
        ('response_time', 'Temps de Réponse'),
        ('throughput', 'Débit'),
        ('error_rate', 'Taux d\'Erreur'),
        ('cpu_usage', 'Utilisation CPU'),
        ('memory_usage', 'Utilisation Mémoire'),
        ('disk_usage', 'Utilisation Disque'),
        ('network_usage', 'Utilisation Réseau'),
        ('database_queries', 'Requêtes Base de Données'),
        ('cache_hit_rate', 'Taux de Cache'),
        ('user_sessions', 'Sessions Utilisateurs'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20)  # ms, req/s, %, MB, etc.
    
    # Contexte
    endpoint = models.CharField(max_length=200, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.CharField(max_length=50, blank=True)
    
    # Métadonnées
    server_id = models.CharField(max_length=100, blank=True)
    environment = models.CharField(max_length=20, default='production')
    
    class Meta:
        verbose_name = "Métrique de Performance"
        verbose_name_plural = "Métriques de Performance"
        indexes = [
            models.Index(fields=['timestamp', 'metric_type']),
            models.Index(fields=['metric_type', 'value']),
        ]
    
    def __str__(self):
        return f"{self.metric_type} - {self.value}{self.unit} - {self.timestamp}"

class CacheStrategy(models.Model):
    """Stratégies de cache intelligentes"""
    CACHE_TYPES = [
        ('redis', 'Redis'),
        ('memcached', 'Memcached'),
        ('database', 'Base de Données'),
        ('cdn', 'CDN'),
        ('browser', 'Navigateur'),
    ]
    
    STRATEGY_TYPES = [
        ('lru', 'LRU (Least Recently Used)'),
        ('lfu', 'LFU (Least Frequently Used)'),
        ('ttl', 'TTL (Time To Live)'),
        ('adaptive', 'Adaptatif'),
        ('predictive', 'Prédictif'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    cache_type = models.CharField(max_length=20, choices=CACHE_TYPES)
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_TYPES)
    
    # Configuration
    ttl_seconds = models.IntegerField(default=3600)  # 1 heure par défaut
    max_size_mb = models.IntegerField(default=100)  # 100 MB par défaut
    compression_enabled = models.BooleanField(default=True)
    encryption_enabled = models.BooleanField(default=False)
    
    # Règles intelligentes
    rules = models.JSONField(default=dict)
    conditions = models.JSONField(default=dict)
    
    # Métadonnées
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stratégie de Cache"
        verbose_name_plural = "Stratégies de Cache"
    
    def __str__(self):
        return f"{self.name} ({self.get_cache_type_display()})"

class DatabaseOptimization(models.Model):
    """Optimisations de base de données"""
    OPTIMIZATION_TYPES = [
        ('indexing', 'Indexation'),
        ('query_optimization', 'Optimisation de Requêtes'),
        ('connection_pooling', 'Pool de Connexions'),
        ('partitioning', 'Partitionnement'),
        ('sharding', 'Sharding'),
        ('replication', 'Réplication'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    optimization_type = models.CharField(max_length=30, choices=OPTIMIZATION_TYPES)
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)
    
    # Performance
    improvement_percentage = models.FloatField(default=0.0)
    execution_time_ms = models.FloatField(default=0.0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    applied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Optimisation Base de Données"
        verbose_name_plural = "Optimisations Base de Données"
    
    def __str__(self):
        return f"{self.name} ({self.get_optimization_type_display()})"

class LoadBalancer(models.Model):
    """Configuration de load balancer"""
    LB_TYPES = [
        ('round_robin', 'Round Robin'),
        ('least_connections', 'Moins de Connexions'),
        ('ip_hash', 'Hash IP'),
        ('weighted', 'Pondéré'),
        ('adaptive', 'Adaptatif'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    lb_type = models.CharField(max_length=30, choices=LB_TYPES)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    health_check_enabled = models.BooleanField(default=True)
    health_check_interval = models.IntegerField(default=30)  # secondes
    
    # Serveurs
    servers = models.JSONField(default=list)
    weights = models.JSONField(default=dict)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Load Balancer"
        verbose_name_plural = "Load Balancers"
    
    def __str__(self):
        return f"{self.name} ({self.get_lb_type_display()})"

class AutoScaling(models.Model):
    """Configuration d'auto-scaling"""
    SCALING_TYPES = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('hybrid', 'Hybride'),
    ]
    
    TRIGGER_TYPES = [
        ('cpu_usage', 'Utilisation CPU'),
        ('memory_usage', 'Utilisation Mémoire'),
        ('response_time', 'Temps de Réponse'),
        ('request_count', 'Nombre de Requêtes'),
        ('error_rate', 'Taux d\'Erreur'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    scaling_type = models.CharField(max_length=20, choices=SCALING_TYPES)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    
    # Seuils
    min_instances = models.IntegerField(default=1)
    max_instances = models.IntegerField(default=10)
    scale_up_threshold = models.FloatField(default=80.0)  # %
    scale_down_threshold = models.FloatField(default=20.0)  # %
    
    # Configuration
    cooldown_period = models.IntegerField(default=300)  # 5 minutes
    is_enabled = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Auto Scaling"
        verbose_name_plural = "Auto Scaling"
    
    def __str__(self):
        return f"{self.name} ({self.get_scaling_type_display()})"

class CDNOptimization(models.Model):
    """Optimisations CDN"""
    CDN_PROVIDERS = [
        ('cloudflare', 'Cloudflare'),
        ('aws_cloudfront', 'AWS CloudFront'),
        ('google_cdn', 'Google CDN'),
        ('azure_cdn', 'Azure CDN'),
        ('custom', 'Personnalisé'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=30, choices=CDN_PROVIDERS)
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    cache_ttl = models.IntegerField(default=3600)  # 1 heure
    compression_enabled = models.BooleanField(default=True)
    ssl_enabled = models.BooleanField(default=True)
    
    # Règles
    rules = models.JSONField(default=dict)
    edge_locations = models.JSONField(default=list)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Optimisation CDN"
        verbose_name_plural = "Optimisations CDN"
    
    def __str__(self):
        return f"{self.name} ({self.get_provider_display()})"

class QueryOptimization(models.Model):
    """Optimisations de requêtes"""
    QUERY_TYPES = [
        ('select', 'SELECT'),
        ('insert', 'INSERT'),
        ('update', 'UPDATE'),
        ('delete', 'DELETE'),
        ('complex', 'Complexe'),
    ]
    
    query_hash = models.CharField(max_length=64, unique=True)
    query_type = models.CharField(max_length=20, choices=QUERY_TYPES)
    query_text = models.TextField()
    
    # Performance
    execution_count = models.IntegerField(default=0)
    avg_execution_time = models.FloatField(default=0.0)
    max_execution_time = models.FloatField(default=0.0)
    total_execution_time = models.FloatField(default=0.0)
    
    # Optimisations appliquées
    optimizations = models.JSONField(default=list)
    is_optimized = models.BooleanField(default=False)
    
    # Métadonnées
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Optimisation de Requête"
        verbose_name_plural = "Optimisations de Requêtes"
        indexes = [
            models.Index(fields=['avg_execution_time', 'execution_count']),
            models.Index(fields=['is_optimized', 'query_type']),
        ]
    
    def __str__(self):
        return f"{self.query_hash[:16]}... ({self.query_type})"

class PerformanceAlert(models.Model):
    """Alertes de performance"""
    ALERT_TYPES = [
        ('critical', 'Critique'),
        ('warning', 'Avertissement'),
        ('info', 'Information'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    ]
    
    title = models.CharField(max_length=200)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    
    # Détails
    description = models.TextField()
    metric_type = models.CharField(max_length=30)
    threshold_value = models.FloatField()
    current_value = models.FloatField()
    
    # Statut
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Alerte de Performance"
        verbose_name_plural = "Alertes de Performance"
        indexes = [
            models.Index(fields=['is_resolved', 'severity']),
            models.Index(fields=['created_at', 'alert_type']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"

class ResourceMonitoring(models.Model):
    """Monitoring des ressources système"""
    RESOURCE_TYPES = [
        ('cpu', 'CPU'),
        ('memory', 'Mémoire'),
        ('disk', 'Disque'),
        ('network', 'Réseau'),
        ('database', 'Base de Données'),
        ('cache', 'Cache'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    # Métriques
    usage_percentage = models.FloatField()
    total_capacity = models.BigIntegerField()  # bytes, cores, etc.
    used_capacity = models.BigIntegerField()
    available_capacity = models.BigIntegerField()
    
    # Détails spécifiques
    details = models.JSONField(default=dict)
    
    # Serveur
    server_id = models.CharField(max_length=100)
    environment = models.CharField(max_length=20, default='production')
    
    class Meta:
        verbose_name = "Monitoring des Ressources"
        verbose_name_plural = "Monitoring des Ressources"
        indexes = [
            models.Index(fields=['timestamp', 'resource_type']),
            models.Index(fields=['resource_type', 'usage_percentage']),
        ]
    
    def __str__(self):
        return f"{self.resource_type} - {self.usage_percentage}% - {self.timestamp}"

class PerformanceReport(models.Model):
    """Rapports de performance"""
    REPORT_TYPES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('custom', 'Personnalisé'),
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    
    # Période
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Métriques
    avg_response_time = models.FloatField()
    total_requests = models.BigIntegerField()
    error_rate = models.FloatField()
    throughput = models.FloatField()
    
    # Résumé
    summary = models.JSONField(default=dict)
    recommendations = models.JSONField(default=list)
    
    # Métadonnées
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Rapport de Performance"
        verbose_name_plural = "Rapports de Performance"
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['report_type', 'generated_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.start_date.date()} - {self.end_date.date()})"

class CacheHitRate(models.Model):
    """Taux de réussite du cache"""
    CACHE_LEVELS = [
        ('l1', 'L1 (CPU)'),
        ('l2', 'L2 (RAM)'),
        ('l3', 'L3 (Redis)'),
        ('l4', 'L4 (CDN)'),
        ('l5', 'L5 (Browser)'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    cache_level = models.CharField(max_length=10, choices=CACHE_LEVELS)
    
    # Métriques
    hits = models.BigIntegerField(default=0)
    misses = models.BigIntegerField(default=0)
    hit_rate = models.FloatField()  # Calculé: hits / (hits + misses)
    
    # Performance
    avg_response_time = models.FloatField()  # ms
    total_requests = models.BigIntegerField()
    
    # Métadonnées
    cache_strategy = models.ForeignKey(CacheStrategy, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = "Taux de Réussite Cache"
        verbose_name_plural = "Taux de Réussite Cache"
        indexes = [
            models.Index(fields=['timestamp', 'cache_level']),
            models.Index(fields=['cache_level', 'hit_rate']),
        ]
    
    def __str__(self):
        return f"{self.cache_level} - {self.hit_rate:.2f}% - {self.timestamp}"

class DatabaseConnectionPool(models.Model):
    """Pool de connexions base de données"""
    POOL_TYPES = [
        ('read', 'Lecture'),
        ('write', 'Écriture'),
        ('mixed', 'Mixte'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    pool_type = models.CharField(max_length=20, choices=POOL_TYPES)
    
    # Configuration
    max_connections = models.IntegerField(default=20)
    min_connections = models.IntegerField(default=5)
    current_connections = models.IntegerField(default=0)
    available_connections = models.IntegerField(default=0)
    
    # Performance
    avg_connection_time = models.FloatField(default=0.0)  # ms
    max_connection_time = models.FloatField(default=0.0)  # ms
    connection_errors = models.IntegerField(default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pool de Connexions Base de Données"
        verbose_name_plural = "Pools de Connexions Base de Données"
    
    def __str__(self):
        return f"{self.name} ({self.get_pool_type_display()}) - {self.current_connections}/{self.max_connections}"

class NetworkOptimization(models.Model):
    """Optimisations réseau"""
    OPTIMIZATION_TYPES = [
        ('compression', 'Compression'),
        ('minification', 'Minification'),
        ('bundling', 'Bundling'),
        ('lazy_loading', 'Chargement Lazy'),
        ('prefetching', 'Préchargement'),
        ('cdn_routing', 'Routage CDN'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    optimization_type = models.CharField(max_length=30, choices=OPTIMIZATION_TYPES)
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)
    
    # Performance
    bandwidth_saved = models.BigIntegerField(default=0)  # bytes
    load_time_improvement = models.FloatField(default=0.0)  # %
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Optimisation Réseau"
        verbose_name_plural = "Optimisations Réseau"
    
    def __str__(self):
        return f"{self.name} ({self.get_optimization_type_display()})" 
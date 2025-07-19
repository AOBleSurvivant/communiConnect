from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from geography.models import Quartier, Commune
from posts.models import Post
import json
from datetime import datetime, timedelta

User = get_user_model()

class UserAnalytics(models.Model):
    """Métriques détaillées par utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    
    # Métriques d'engagement
    total_posts = models.IntegerField(default=0)
    total_likes_given = models.IntegerField(default=0)
    total_likes_received = models.IntegerField(default=0)
    total_comments_given = models.IntegerField(default=0)
    total_comments_received = models.IntegerField(default=0)
    total_shares = models.IntegerField(default=0)
    
    # Métriques de connexions
    total_friends = models.IntegerField(default=0)
    total_followers = models.IntegerField(default=0)
    total_following = models.IntegerField(default=0)
    
    # Métriques temporelles
    first_activity = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    total_session_time = models.DurationField(default=timedelta(0))
    avg_session_duration = models.DurationField(default=timedelta(0))
    
    # Métriques géographiques
    local_engagement_rate = models.FloatField(default=0.0)
    global_engagement_rate = models.FloatField(default=0.0)
    geographic_reach = models.IntegerField(default=0)
    
    # Métriques de rétention
    days_active = models.IntegerField(default=0)
    retention_score = models.FloatField(default=0.0)
    churn_risk = models.FloatField(default=0.0)
    
    # Métriques de croissance
    growth_rate = models.FloatField(default=0.0)
    viral_coefficient = models.FloatField(default=0.0)
    influence_score = models.FloatField(default=0.0)
    
    # Métriques de contenu
    content_quality_score = models.FloatField(default=0.0)
    content_variety_score = models.FloatField(default=0.0)
    content_engagement_rate = models.FloatField(default=0.0)
    
    # Métriques de satisfaction
    satisfaction_score = models.FloatField(default=0.0)
    nps_score = models.IntegerField(default=0)
    feedback_positive_ratio = models.FloatField(default=0.0)
    
    # Métriques de performance
    response_time_avg = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    performance_score = models.FloatField(default=0.0)
    
    # Métriques business
    monetization_potential = models.FloatField(default=0.0)
    lifetime_value = models.FloatField(default=0.0)
    conversion_rate = models.FloatField(default=0.0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_calculated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Analytics Utilisateur"
        verbose_name_plural = "Analytics Utilisateurs"
    
    def __str__(self):
        return f"Analytics de {self.user.username}"
    
    def calculate_engagement_rate(self):
        """Calcule le taux d'engagement global"""
        if self.total_posts > 0:
            total_engagement = self.total_likes_received + self.total_comments_received + self.total_shares
            self.global_engagement_rate = total_engagement / self.total_posts
        return self.global_engagement_rate
    
    def calculate_retention_score(self):
        """Calcule le score de rétention"""
        if self.days_active > 0:
            # Score basé sur l'activité récente vs historique
            recent_activity = self.get_recent_activity_days()
            self.retention_score = min(1.0, recent_activity / self.days_active)
        return self.retention_score
    
    def get_recent_activity_days(self):
        """Calcule les jours d'activité récente (7 derniers jours)"""
        from django.utils import timezone
        week_ago = timezone.now() - timedelta(days=7)
        recent_posts = Post.objects.filter(
            author=self.user,
            created_at__gte=week_ago
        ).count()
        return min(7, recent_posts)

class EventTracking(models.Model):
    """Suivi des événements utilisateur"""
    EVENT_TYPES = [
        ('post_created', 'Post Créé'),
        ('post_liked', 'Post Liké'),
        ('post_commented', 'Post Commenté'),
        ('post_shared', 'Post Partagé'),
        ('user_followed', 'Utilisateur Suivi'),
        ('user_unfollowed', 'Utilisateur Désuivi'),
        ('profile_viewed', 'Profil Consulté'),
        ('search_performed', 'Recherche Effectuée'),
        ('notification_received', 'Notification Reçue'),
        ('notification_clicked', 'Notification Cliquée'),
        ('feature_used', 'Fonctionnalité Utilisée'),
        ('error_occurred', 'Erreur Survenue'),
        ('session_started', 'Session Démarrée'),
        ('session_ended', 'Session Terminée'),
        ('payment_made', 'Paiement Effectué'),
        ('ad_clicked', 'Publicité Cliquée'),
        ('content_viewed', 'Contenu Consulté'),
        ('location_changed', 'Localisation Changée'),
        ('settings_updated', 'Paramètres Mis à Jour'),
        ('feedback_given', 'Feedback Donné'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    location = models.ForeignKey(Quartier, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Métriques de performance
    response_time = models.FloatField(null=True, blank=True)
    error_code = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = "Événement Utilisateur"
        verbose_name_plural = "Événements Utilisateurs"
        indexes = [
            models.Index(fields=['user', 'event_type', 'timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['location', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"

class GeographicAnalytics(models.Model):
    """Analytics par zone géographique"""
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='analytics')
    
    # Métriques d'utilisateurs
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    new_users_today = models.IntegerField(default=0)
    new_users_week = models.IntegerField(default=0)
    new_users_month = models.IntegerField(default=0)
    
    # Métriques d'engagement
    total_posts = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_shares = models.IntegerField(default=0)
    avg_engagement_rate = models.FloatField(default=0.0)
    
    # Métriques de croissance
    growth_rate = models.FloatField(default=0.0)
    retention_rate = models.FloatField(default=0.0)
    churn_rate = models.FloatField(default=0.0)
    
    # Métriques de contenu
    content_diversity_score = models.FloatField(default=0.0)
    trending_topics = models.JSONField(default=list, blank=True)
    popular_content_types = models.JSONField(default=dict, blank=True)
    
    # Métriques de communauté
    community_health_score = models.FloatField(default=0.0)
    interaction_density = models.FloatField(default=0.0)
    social_cohesion = models.FloatField(default=0.0)
    
    # Métriques business
    monetization_potential = models.FloatField(default=0.0)
    ad_revenue_potential = models.FloatField(default=0.0)
    partnership_opportunities = models.IntegerField(default=0)
    
    # Métadonnées
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytics Géographique"
        verbose_name_plural = "Analytics Géographiques"
    
    def __str__(self):
        return f"Analytics {self.quartier.nom}"

class PredictiveAnalytics(models.Model):
    """Prédictions et insights avancés"""
    PREDICTION_TYPES = [
        ('user_churn', 'Risque de Churn'),
        ('content_viral', 'Contenu Viral'),
        ('user_growth', 'Croissance Utilisateurs'),
        ('engagement_trend', 'Tendance Engagement'),
        ('revenue_forecast', 'Prévision Revenus'),
        ('feature_adoption', 'Adoption Fonctionnalité'),
        ('geographic_expansion', 'Expansion Géographique'),
        ('content_performance', 'Performance Contenu'),
        ('user_behavior', 'Comportement Utilisateur'),
        ('market_trend', 'Tendance Marché'),
    ]
    
    prediction_type = models.CharField(max_length=50, choices=PREDICTION_TYPES)
    target_date = models.DateField()
    confidence_score = models.FloatField(default=0.0)
    prediction_data = models.JSONField(default=dict)
    
    # Métriques de précision
    accuracy_score = models.FloatField(default=0.0)
    precision_score = models.FloatField(default=0.0)
    recall_score = models.FloatField(default=0.0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Prédiction Analytics"
        verbose_name_plural = "Prédictions Analytics"
        indexes = [
            models.Index(fields=['prediction_type', 'target_date']),
            models.Index(fields=['confidence_score', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.prediction_type} - {self.target_date}"

class PerformanceMetrics(models.Model):
    """Métriques de performance système"""
    METRIC_TYPES = [
        ('response_time', 'Temps de Réponse'),
        ('throughput', 'Débit'),
        ('error_rate', 'Taux d\'Erreur'),
        ('availability', 'Disponibilité'),
        ('cpu_usage', 'Utilisation CPU'),
        ('memory_usage', 'Utilisation Mémoire'),
        ('disk_usage', 'Utilisation Disque'),
        ('network_latency', 'Latence Réseau'),
        ('database_performance', 'Performance Base de Données'),
        ('cache_hit_rate', 'Taux de Cache'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    metric_value = models.FloatField()
    metric_unit = models.CharField(max_length=20, default='ms')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Contexte
    endpoint = models.CharField(max_length=200, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Métadonnées
    environment = models.CharField(max_length=20, default='production')
    version = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Métrique Performance"
        verbose_name_plural = "Métriques Performance"
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.metric_value}{self.metric_unit}"

class BusinessMetrics(models.Model):
    """Métriques business et monétisation"""
    METRIC_TYPES = [
        ('revenue', 'Revenus'),
        ('arpu', 'ARPU'),
        ('ltv', 'Lifetime Value'),
        ('cac', 'Customer Acquisition Cost'),
        ('conversion_rate', 'Taux de Conversion'),
        ('retention_rate', 'Taux de Rétention'),
        ('churn_rate', 'Taux de Churn'),
        ('engagement_rate', 'Taux d\'Engagement'),
        ('ad_revenue', 'Revenus Publicitaires'),
        ('subscription_revenue', 'Revenus Abonnements'),
        ('partnership_revenue', 'Revenus Partenariats'),
        ('user_growth', 'Croissance Utilisateurs'),
        ('content_engagement', 'Engagement Contenu'),
        ('geographic_expansion', 'Expansion Géographique'),
        ('feature_adoption', 'Adoption Fonctionnalités'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    metric_value = models.FloatField()
    metric_date = models.DateField()
    period = models.CharField(max_length=20, default='daily')  # daily, weekly, monthly
    
    # Contexte géographique
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True)
    
    # Métadonnées
    calculated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=50, default='system')
    
    class Meta:
        verbose_name = "Métrique Business"
        verbose_name_plural = "Métriques Business"
        indexes = [
            models.Index(fields=['metric_type', 'metric_date']),
            models.Index(fields=['quartier', 'metric_date']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.metric_value} ({self.metric_date})"

class UserJourney(models.Model):
    """Suivi du parcours utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    session_id = models.CharField(max_length=100)
    
    # Étapes du parcours
    entry_point = models.CharField(max_length=100, blank=True)
    exit_point = models.CharField(max_length=100, blank=True)
    total_steps = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    
    # Métriques de parcours
    duration = models.DurationField(default=timedelta(0))
    bounce_rate = models.FloatField(default=0.0)
    conversion_achieved = models.BooleanField(default=False)
    
    # Données de parcours
    journey_data = models.JSONField(default=dict)
    touchpoints = models.JSONField(default=list)
    
    # Métadonnées
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Parcours Utilisateur"
        verbose_name_plural = "Parcours Utilisateurs"
        indexes = [
            models.Index(fields=['user', 'started_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"Parcours {self.user.username} - {self.session_id}"

class AITrainingData(models.Model):
    """Données d'entraînement pour l'IA"""
    DATA_TYPES = [
        ('user_behavior', 'Comportement Utilisateur'),
        ('content_performance', 'Performance Contenu'),
        ('engagement_patterns', 'Patterns d\'Engagement'),
        ('geographic_activity', 'Activité Géographique'),
        ('temporal_patterns', 'Patterns Temporels'),
        ('social_interactions', 'Interactions Sociales'),
        ('feature_usage', 'Utilisation Fonctionnalités'),
        ('conversion_events', 'Événements Conversion'),
        ('retention_factors', 'Facteurs Rétention'),
        ('churn_indicators', 'Indicateurs Churn'),
    ]
    
    data_type = models.CharField(max_length=50, choices=DATA_TYPES)
    data_content = models.JSONField()
    data_quality_score = models.FloatField(default=0.0)
    
    # Métadonnées
    collected_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    is_training_ready = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Données Entraînement IA"
        verbose_name_plural = "Données Entraînement IA"
        indexes = [
            models.Index(fields=['data_type', 'collected_at']),
            models.Index(fields=['is_training_ready']),
        ]
    
    def __str__(self):
        return f"{self.data_type} - {self.collected_at}" 
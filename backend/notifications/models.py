from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
import uuid

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Commentaire'),
        ('follow', 'Suivi'),
        ('live_started', 'Live démarré'),
        ('live_ended', 'Live terminé'),
        ('mention', 'Mention'),
        ('post_shared', 'Post partagé'),
        ('system', 'Système'),
        ('community_alert', 'Alerte Communautaire'),  # Ajout du nouveau type
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Pour référencer le contenu lié (post, commentaire, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Données supplémentaires (JSON)
    extra_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username} - {self.created_at}"
    
    @property
    def time_ago(self):
        """Retourne le temps écoulé depuis la création"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "à l'instant"


class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Préférences par type de notification
    likes_notifications = models.BooleanField(default=True)
    comments_notifications = models.BooleanField(default=True)
    follows_notifications = models.BooleanField(default=True)
    live_notifications = models.BooleanField(default=True)
    mention_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    community_alert_notifications = models.BooleanField(default=True)  # Ajout pour les alertes
    
    # Méthodes de notification
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Fréquence
    notification_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immédiat'),
            ('hourly', 'Toutes les heures'),
            ('daily', 'Quotidien'),
        ],
        default='immediate'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Préférences de {self.user.username}"


class CommunityAlert(models.Model):
    """Modèle pour les alertes communautaires avec toutes les améliorations demandées"""
    
    # 1. ✅ Catégoriser les types d'alerte
    ALERT_CATEGORIES = [
        ('fire', 'Incendie 🔥'),
        ('power_outage', 'Coupure d\'électricité ⚡'),
        ('road_blocked', 'Route bloquée 🚧'),
        ('security', 'Agression ou sécurité 🚨'),
        ('medical', 'Urgence médicale 🏥'),
        ('flood', 'Inondation 🌊'),
        ('gas_leak', 'Fuite de gaz ⛽'),
        ('noise', 'Bruit excessif 🔊'),
        ('vandalism', 'Vandalisme 🎨'),
        ('other', 'Autre 📋'),
    ]
    
    # 5. ✅ Statut de l'alerte
    ALERT_STATUS = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours de traitement'),
        ('resolved', 'Résolue'),
        ('false_alarm', 'Fausse alerte'),
    ]
    
    # Identifiant unique
    alert_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Informations de base
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ALERT_CATEGORIES)
    status = models.CharField(max_length=20, choices=ALERT_STATUS, default='pending')
    
    # 2. 📍 Localisation automatique ou manuelle
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    
    # Auteur de l'alerte
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_alerts')
    
    # 4. 🧩 Système de fiabilité / signalement
    reliability_score = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    false_alarm_count = models.IntegerField(default=0)
    verified_by_count = models.IntegerField(default=0)
    reported_by_users = models.ManyToManyField(
        User, 
        through='AlertReport',
        related_name='reported_alerts'
    )
    
    # 6. 🤝 Entraide instantanée
    help_offers = models.ManyToManyField(
        User,
        through='HelpOffer',
        related_name='offered_help_alerts'
    )
    help_offers_count = models.IntegerField(default=0)
    
    # Médias
    images = models.JSONField(default=list, blank=True)  # URLs des images
    videos = models.JSONField(default=list, blank=True)  # URLs des vidéos
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resolved_alerts'
    )
    
    # Données supplémentaires
    extra_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['neighborhood', 'city']),
            models.Index(fields=['reliability_score']),
        ]
        verbose_name = "Alerte Communautaire"
        verbose_name_plural = "Alertes Communautaires"
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.title} ({self.get_status_display()})"
    
    @property
    def time_ago(self):
        """Retourne le temps écoulé depuis la création"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "à l'instant"
    
    @property
    def is_urgent(self):
        """Détermine si l'alerte est urgente basée sur la catégorie"""
        urgent_categories = ['fire', 'medical', 'gas_leak', 'security']
        return self.category in urgent_categories
    
    @property
    def is_reliable(self):
        """Détermine si l'alerte est fiable"""
        return self.reliability_score >= 70.0
    
    def update_reliability_score(self):
        """Met à jour le score de fiabilité basé sur les rapports"""
        total_reports = self.alertreports.count()
        false_reports = self.alertreports.filter(report_type='false_alarm').count()
        
        if total_reports > 0:
            false_percentage = (false_reports / total_reports) * 100
            self.reliability_score = max(0.0, 100.0 - false_percentage)
        else:
            self.reliability_score = 100.0
        
        self.save()
    
    def mark_as_resolved(self, resolved_by_user=None):
        """Marque l'alerte comme résolue"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        if resolved_by_user:
            self.resolved_by = resolved_by_user
        self.save()


class AlertReport(models.Model):
    """Rapports sur les alertes (fausses alertes, confirmations, etc.)"""
    REPORT_TYPES = [
        ('false_alarm', 'Fausse alerte'),
        ('confirmed', 'Confirmée'),
        ('inappropriate', 'Inappropriée'),
        ('duplicate', 'Doublon'),
        ('resolved', 'Résolue'),
    ]
    
    alert = models.ForeignKey(CommunityAlert, on_delete=models.CASCADE, related_name='alertreports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['alert', 'reporter']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reporter.username} - {self.get_report_type_display()} - {self.alert.title}"


class HelpOffer(models.Model):
    """Offres d'aide pour les alertes"""
    OFFER_TYPES = [
        ('physical_help', 'Aide physique'),
        ('information', 'Information'),
        ('transport', 'Transport'),
        ('medical', 'Aide médicale'),
        ('technical', 'Aide technique'),
        ('other', 'Autre'),
    ]
    
    alert = models.ForeignKey(CommunityAlert, on_delete=models.CASCADE, related_name='help_offers_rel')
    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_offers')
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    description = models.TextField()
    contact_info = models.JSONField(default=dict, blank=True)  # {phone: "", email: ""}
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['alert', 'helper']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.helper.username} - {self.get_offer_type_display()} - {self.alert.title}"


class AlertNotification(models.Model):
    """Notifications spécifiques aux alertes communautaires"""
    NOTIFICATION_TYPES = [
        ('new_alert', 'Nouvelle alerte'),
        ('status_update', 'Mise à jour statut'),
        ('help_needed', 'Aide demandée'),
        ('alert_resolved', 'Alerte résolue'),
        ('nearby_alert', 'Alerte à proximité'),
    ]
    
    alert = models.ForeignKey(CommunityAlert, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Données supplémentaires
    extra_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['alert', 'notification_type']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username} - {self.alert.title}"


class AlertStatistics(models.Model):
    """Statistiques des alertes pour les rapports"""
    STATISTIC_TYPES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    
    statistic_type = models.CharField(max_length=20, choices=STATISTIC_TYPES)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Compteurs par catégorie
    fire_count = models.IntegerField(default=0)
    power_outage_count = models.IntegerField(default=0)
    road_blocked_count = models.IntegerField(default=0)
    security_count = models.IntegerField(default=0)
    medical_count = models.IntegerField(default=0)
    flood_count = models.IntegerField(default=0)
    gas_leak_count = models.IntegerField(default=0)
    noise_count = models.IntegerField(default=0)
    vandalism_count = models.IntegerField(default=0)
    other_count = models.IntegerField(default=0)
    
    # Statistiques générales
    total_alerts = models.IntegerField(default=0)
    resolved_alerts = models.IntegerField(default=0)
    false_alarms = models.IntegerField(default=0)
    avg_resolution_time_hours = models.FloatField(default=0.0)
    
    # Géographie
    neighborhoods_data = models.JSONField(default=dict, blank=True)
    cities_data = models.JSONField(default=dict, blank=True)
    
    # Fiabilité
    avg_reliability_score = models.FloatField(default=0.0)
    reliable_alerts_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['statistic_type', 'period_start', 'period_end']
        ordering = ['-period_start']
    
    def __str__(self):
        return f"{self.get_statistic_type_display()} - {self.period_start.date()} - {self.total_alerts} alertes" 
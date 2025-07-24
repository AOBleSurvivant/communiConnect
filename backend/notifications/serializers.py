from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import (
    Notification, 
    NotificationPreference, 
    CommunityAlert, 
    AlertReport, 
    HelpOffer, 
    AlertNotification,
    AlertStatistics
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les informations utilisateur de base"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class NotificationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les notifications"""
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    time_ago = serializers.ReadOnlyField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'recipient', 'notification_type', 'title', 
            'message', 'is_read', 'created_at', 'time_ago', 'extra_data'
        ]
        read_only_fields = ['created_at', 'time_ago']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les préférences de notification"""
    class Meta:
        model = NotificationPreference
        fields = [
            'likes_notifications', 'comments_notifications', 'follows_notifications',
            'live_notifications', 'mention_notifications', 'system_notifications',
            'community_alert_notifications', 'email_notifications', 'push_notifications',
            'in_app_notifications', 'notification_frequency'
        ]


class CommunityAlertSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les alertes communautaires"""
    author = UserSerializer(read_only=True)
    resolved_by = UserSerializer(read_only=True)
    time_ago = serializers.ReadOnlyField()
    is_urgent = serializers.ReadOnlyField()
    is_reliable = serializers.ReadOnlyField()
    help_offers_count = serializers.ReadOnlyField()
    verified_by_count = serializers.ReadOnlyField()
    false_alarm_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CommunityAlert
        fields = [
            'alert_id', 'title', 'description', 'category', 'status',
            'latitude', 'longitude', 'address', 'neighborhood', 'city', 'postal_code',
            'author', 'reliability_score', 'help_offers_count', 'verified_by_count',
            'false_alarm_count', 'images', 'videos', 'created_at', 'updated_at',
            'resolved_at', 'resolved_by', 'time_ago', 'is_urgent', 'is_reliable',
            'extra_data'
        ]
        read_only_fields = [
            'alert_id', 'author', 'reliability_score', 'help_offers_count',
            'verified_by_count', 'false_alarm_count', 'created_at', 'updated_at',
            'resolved_at', 'resolved_by', 'time_ago', 'is_urgent', 'is_reliable'
        ]


class CommunityAlertCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer une nouvelle alerte"""
    class Meta:
        model = CommunityAlert
        fields = [
            'title', 'description', 'category', 'latitude', 'longitude',
            'address', 'neighborhood', 'city', 'postal_code', 'images', 'videos'
        ]
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommunityAlertUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour mettre à jour une alerte"""
    class Meta:
        model = CommunityAlert
        fields = [
            'title', 'description', 'category', 'status', 'latitude', 'longitude',
            'address', 'neighborhood', 'city', 'postal_code', 'images', 'videos'
        ]
        read_only_fields = ['author']


class AlertReportSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les rapports d'alertes"""
    reporter = UserSerializer(read_only=True)
    alert = CommunityAlertSerializer(read_only=True)
    
    class Meta:
        model = AlertReport
        fields = ['id', 'alert', 'reporter', 'report_type', 'reason', 'created_at']
        read_only_fields = ['reporter', 'created_at']
    
    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        report = super().create(validated_data)
        
        # Mettre à jour le score de fiabilité de l'alerte
        alert = report.alert
        alert.update_reliability_score()
        
        return report


class HelpOfferSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les offres d'aide"""
    helper = UserSerializer(read_only=True)
    alert = CommunityAlertSerializer(read_only=True)
    
    class Meta:
        model = HelpOffer
        fields = [
            'id', 'alert', 'helper', 'offer_type', 'description', 'contact_info',
            'is_active', 'created_at', 'accepted_at'
        ]
        read_only_fields = ['helper', 'created_at', 'accepted_at']
    
    def create(self, validated_data):
        validated_data['helper'] = self.context['request'].user
        
        # Mettre à jour le compteur d'offres d'aide
        help_offer = super().create(validated_data)
        alert = help_offer.alert
        alert.help_offers_count = alert.help_offers_rel.count()
        alert.save()
        
        return help_offer


class AlertNotificationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les notifications d'alertes"""
    recipient = UserSerializer(read_only=True)
    alert = CommunityAlertSerializer(read_only=True)
    
    class Meta:
        model = AlertNotification
        fields = [
            'id', 'alert', 'recipient', 'notification_type', 'title', 'message',
            'is_read', 'is_sent', 'sent_at', 'created_at', 'extra_data'
        ]
        read_only_fields = ['recipient', 'created_at']


class AlertStatisticsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les statistiques d'alertes"""
    class Meta:
        model = AlertStatistics
        fields = [
            'id', 'statistic_type', 'period_start', 'period_end',
            'fire_count', 'power_outage_count', 'road_blocked_count', 'security_count',
            'medical_count', 'flood_count', 'gas_leak_count', 'noise_count',
            'vandalism_count', 'other_count', 'total_alerts', 'resolved_alerts',
            'false_alarms', 'avg_resolution_time_hours', 'neighborhoods_data',
            'cities_data', 'avg_reliability_score', 'reliable_alerts_count',
            'created_at'
        ]
        read_only_fields = ['created_at']


class CommunityAlertListSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour la liste des alertes"""
    author = UserSerializer(read_only=True)
    time_ago = serializers.ReadOnlyField()
    is_urgent = serializers.ReadOnlyField()
    is_reliable = serializers.ReadOnlyField()
    
    class Meta:
        model = CommunityAlert
        fields = [
            'alert_id', 'title', 'description', 'category', 'status', 'neighborhood', 'city',
            'author', 'reliability_score', 'help_offers_count', 'verified_by_count',
            'created_at', 'time_ago', 'is_urgent', 'is_reliable'
        ]


class CommunityAlertDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur détaillé pour une alerte spécifique"""
    author = UserSerializer(read_only=True)
    resolved_by = UserSerializer(read_only=True)
    time_ago = serializers.ReadOnlyField()
    is_urgent = serializers.ReadOnlyField()
    is_reliable = serializers.ReadOnlyField()
    help_offers = HelpOfferSerializer(many=True, read_only=True)
    alertreports = AlertReportSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommunityAlert
        fields = [
            'alert_id', 'title', 'description', 'category', 'status',
            'latitude', 'longitude', 'address', 'neighborhood', 'city', 'postal_code',
            'author', 'reliability_score', 'help_offers_count', 'verified_by_count',
            'false_alarm_count', 'images', 'videos', 'created_at', 'updated_at',
            'resolved_at', 'resolved_by', 'time_ago', 'is_urgent', 'is_reliable',
            'help_offers', 'alertreports', 'extra_data'
        ]


class NearbyAlertsSerializer(serializers.Serializer):
    """Sérialiseur pour les alertes à proximité"""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    radius_km = serializers.FloatField(default=5.0, min_value=0.1, max_value=50.0)
    category_filter = serializers.CharField(required=False, allow_blank=True)
    urgent_only = serializers.BooleanField(default=False)
    
    def validate(self, data):
        """Validation personnalisée"""
        if data.get('radius_km', 5.0) > 50.0:
            raise serializers.ValidationError("Le rayon ne peut pas dépasser 50 km")
        return data


class AlertSearchSerializer(serializers.Serializer):
    """Sérialiseur pour la recherche d'alertes"""
    query = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    neighborhood = serializers.CharField(required=False, allow_blank=True)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    urgent_only = serializers.BooleanField(default=False)
    reliable_only = serializers.BooleanField(default=False)
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100) 
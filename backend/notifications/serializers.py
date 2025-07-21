from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Notification, NotificationPreference
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'notification_type', 'title', 
            'message', 'is_read', 'created_at', 'time_ago', 'extra_data'
        ]
        read_only_fields = ['created_at', 'time_ago']
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_time_ago(self, obj):
        """Retourne le temps écoulé depuis la notification"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"Il y a {diff.days}j"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"Il y a {hours}h"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"Il y a {minutes}min"
        else:
            return "À l'instant"


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'likes_notifications', 'comments_notifications', 'follows_notifications',
            'live_notifications', 'mention_notifications', 'system_notifications',
            'email_notifications', 'push_notifications', 'in_app_notifications',
            'notification_frequency'
        ]


class NotificationCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField()
    total_count = serializers.IntegerField()


class MarkAsReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    mark_all = serializers.BooleanField(default=False) 
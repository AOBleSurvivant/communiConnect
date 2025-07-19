from rest_framework import serializers
from .models import Notification, NotificationPreference
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    time_ago = serializers.ReadOnlyField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'notification_type', 'title', 
            'message', 'is_read', 'created_at', 'time_ago', 'extra_data'
        ]
        read_only_fields = ['created_at', 'time_ago']


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
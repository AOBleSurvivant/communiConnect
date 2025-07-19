from django.contrib import admin
from .models import Notification, NotificationPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'recipient', 'sender', 'notification_type', 
        'title', 'is_read', 'created_at'
    ]
    list_filter = [
        'notification_type', 'is_read', 'created_at'
    ]
    search_fields = [
        'recipient__username', 'recipient__first_name', 'recipient__last_name',
        'sender__username', 'sender__first_name', 'sender__last_name',
        'title', 'message'
    ]
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('recipient', 'sender', 'notification_type', 'title', 'message')
        }),
        ('État', {
            'fields': ('is_read', 'created_at')
        }),
        ('Contenu lié', {
            'fields': ('content_type', 'object_id', 'extra_data'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'likes_notifications', 'comments_notifications', 
        'follows_notifications', 'live_notifications', 'notification_frequency'
    ]
    list_filter = [
        'likes_notifications', 'comments_notifications', 'follows_notifications',
        'live_notifications', 'mention_notifications', 'system_notifications',
        'email_notifications', 'push_notifications', 'in_app_notifications',
        'notification_frequency'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Types de notifications', {
            'fields': (
                'likes_notifications', 'comments_notifications', 'follows_notifications',
                'live_notifications', 'mention_notifications', 'system_notifications'
            )
        }),
        ('Méthodes de notification', {
            'fields': ('email_notifications', 'push_notifications', 'in_app_notifications')
        }),
        ('Fréquence', {
            'fields': ('notification_frequency',)
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 
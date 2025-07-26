from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import HelpRequest, HelpResponse, HelpRequestCategory


@admin.register(HelpRequestCategory)
class HelpRequestCategoryAdmin(admin.ModelAdmin):
    """Admin pour les catégories de demandes d'aide"""
    
    list_display = ['name', 'icon', 'color', 'is_active', 'order']
    list_filter = ['is_active', 'color']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'icon', 'description')
        }),
        ('Apparence', {
            'fields': ('color', 'order')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    """Admin pour les demandes d'aide"""
    
    list_display = [
        'title', 'author_link', 'request_type', 'need_type', 'status', 
        'is_urgent', 'city', 'created_at', 'responses_count', 'views_count'
    ]
    list_filter = [
        'request_type', 'need_type', 'status', 'is_urgent', 'duration_type',
        'proximity_zone', 'created_at', 'city'
    ]
    search_fields = [
        'title', 'description', 'author__username', 'author__first_name', 
        'author__last_name', 'address', 'neighborhood', 'city'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'time_ago', 'location_display', 
        'is_expired', 'responses_count', 'views_count', 'duration_display'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('id', 'author', 'title', 'description')
        }),
        ('Type et statut', {
            'fields': ('request_type', 'need_type', 'custom_need_type', 'status', 'is_urgent')
        }),
        ('Pour qui et durée', {
            'fields': ('for_who', 'custom_for_who', 'duration_type', 'specific_date', 'estimated_hours')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude', 'address', 'neighborhood', 'city', 'postal_code', 'proximity_zone')
        }),
        ('Contact', {
            'fields': ('contact_preference', 'phone', 'email')
        }),
        ('Médias', {
            'fields': ('photo',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'expires_at', 'responses_count', 'views_count')
        }),
        ('Lien avec alerte', {
            'fields': ('related_alert',),
            'classes': ('collapse',)
        }),
    )
    
    def author_link(self, obj):
        """Lien vers l'auteur"""
        if obj.author:
            url = reverse('admin:users_user_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.username)
        return '-'
    author_link.short_description = 'Auteur'
    
    def time_ago(self, obj):
        """Temps écoulé depuis la création"""
        return obj.time_ago
    time_ago.short_description = 'Il y a'
    
    def location_display(self, obj):
        """Affichage de la localisation"""
        return obj.location_display
    location_display.short_description = 'Localisation'
    
    def duration_display(self, obj):
        """Affichage de la durée"""
        return obj.duration_display
    duration_display.short_description = 'Durée'
    
    def is_expired(self, obj):
        """Vérifier si la demande a expiré"""
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expirée'
    
    actions = ['mark_as_completed', 'mark_as_cancelled', 'mark_as_urgent', 'mark_as_not_urgent']
    
    def mark_as_completed(self, request, queryset):
        """Marquer les demandes comme terminées"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} demande(s) marquée(s) comme terminée(s).')
    mark_as_completed.short_description = "Marquer comme terminées"
    
    def mark_as_cancelled(self, request, queryset):
        """Marquer les demandes comme annulées"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} demande(s) marquée(s) comme annulée(s).')
    mark_as_cancelled.short_description = "Marquer comme annulées"
    
    def mark_as_urgent(self, request, queryset):
        """Marquer les demandes comme urgentes"""
        updated = queryset.update(is_urgent=True)
        self.message_user(request, f'{updated} demande(s) marquée(s) comme urgente(s).')
    mark_as_urgent.short_description = "Marquer comme urgentes"
    
    def mark_as_not_urgent(self, request, queryset):
        """Marquer les demandes comme non urgentes"""
        updated = queryset.update(is_urgent=False)
        self.message_user(request, f'{updated} demande(s) marquée(s) comme non urgente(s).')
    mark_as_not_urgent.short_description = "Marquer comme non urgentes"


@admin.register(HelpResponse)
class HelpResponseAdmin(admin.ModelAdmin):
    """Admin pour les réponses aux demandes d'aide"""
    
    list_display = [
        'help_request_link', 'author_link', 'response_type', 'is_accepted', 
        'is_rejected', 'created_at'
    ]
    list_filter = [
        'response_type', 'is_accepted', 'is_rejected', 'created_at'
    ]
    search_fields = [
        'message', 'help_request__title', 'author__username', 
        'author__first_name', 'author__last_name'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('id', 'help_request', 'author', 'response_type', 'message')
        }),
        ('Contact', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Statut', {
            'fields': ('is_accepted', 'is_rejected')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def help_request_link(self, obj):
        """Lien vers la demande d'aide"""
        if obj.help_request:
            url = reverse('admin:help_requests_helprequest_change', args=[obj.help_request.id])
            return format_html('<a href="{}">{}</a>', url, obj.help_request.title)
        return '-'
    help_request_link.short_description = 'Demande d\'aide'
    
    def author_link(self, obj):
        """Lien vers l'auteur"""
        if obj.author:
            url = reverse('admin:users_user_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.username)
        return '-'
    author_link.short_description = 'Auteur'
    
    actions = ['accept_responses', 'reject_responses']
    
    def accept_responses(self, request, queryset):
        """Accepter les réponses sélectionnées"""
        updated = 0
        for response in queryset:
            response.accept()
            updated += 1
        self.message_user(request, f'{updated} réponse(s) acceptée(s).')
    accept_responses.short_description = "Accepter les réponses"
    
    def reject_responses(self, request, queryset):
        """Rejeter les réponses sélectionnées"""
        updated = 0
        for response in queryset:
            response.reject()
            updated += 1
        self.message_user(request, f'{updated} réponse(s) rejetée(s).')
    reject_responses.short_description = "Rejeter les réponses" 
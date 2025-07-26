from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from users.serializers import UserSerializer
from .models import HelpRequest, HelpResponse, HelpRequestCategory


class HelpRequestCategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories de demandes d'aide"""
    
    class Meta:
        model = HelpRequestCategory
        fields = ['id', 'name', 'icon', 'color', 'description', 'is_active', 'order']


class HelpRequestSerializer(serializers.ModelSerializer):
    """Sérialiseur principal pour les demandes d'aide"""
    
    author = UserSerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    time_ago = serializers.ReadOnlyField()
    location_display = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    responses_count = serializers.ReadOnlyField()
    views_count = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField()
    need_type_display = serializers.SerializerMethodField()
    request_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = HelpRequest
        fields = [
            'id', 'author', 'author_name', 'request_type', 'request_type_display', 'need_type', 'need_type_display',
            'for_who', 'title', 'description', 'latitude', 'longitude', 'address',
            'neighborhood', 'city', 'postal_code', 'status', 'status_display', 'is_urgent',
            'expires_at', 'created_at', 'updated_at', 'time_ago', 'location_display', 
            'is_expired', 'responses_count', 'views_count', 'custom_need_type', 
            'custom_for_who', 'photo', 'contact_preference', 'phone', 'email',
            'duration_type', 'duration_display', 'specific_date', 'estimated_hours',
            'proximity_zone', 'related_alert'
        ]
        read_only_fields = ['id', 'author', 'author_name', 'created_at', 'updated_at', 'time_ago', 
                           'location_display', 'is_expired', 'responses_count', 'views_count',
                           'duration_display', 'need_type_display', 'request_type_display', 'status_display']
    
    def get_author_name(self, obj):
        """Retourne le nom affiché de l'auteur"""
        if obj.author:
            if obj.author.first_name and obj.author.last_name:
                return f"{obj.author.first_name} {obj.author.last_name}"
            return obj.author.username
        return "Utilisateur"
    
    def get_need_type_display(self, obj):
        """Retourne le nom affiché du type de besoin"""
        return obj.get_need_type_display()
    
    def get_request_type_display(self, obj):
        """Retourne le nom affiché du type de demande"""
        return obj.get_request_type_display()
    
    def get_status_display(self, obj):
        """Retourne le nom affiché du statut"""
        return obj.get_status_display()
    
    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que custom_need_type est fourni si need_type est 'other'
        if data.get('need_type') == 'other' and not data.get('custom_need_type'):
            raise serializers.ValidationError({
                'custom_need_type': 'Veuillez spécifier le type de besoin personnalisé.'
            })
        
        # Vérifier que custom_for_who est fourni si for_who est 'other'
        if data.get('for_who') == 'other' and not data.get('custom_for_who'):
            raise serializers.ValidationError({
                'custom_for_who': 'Veuillez spécifier pour qui cette aide est destinée.'
            })
        
        # Vérifier que specific_date est fourni si duration_type est 'specific_date'
        if data.get('duration_type') == 'specific_date' and not data.get('specific_date'):
            raise serializers.ValidationError({
                'specific_date': 'Veuillez spécifier une date pour ce type de durée.'
            })
        
        # Vérifier que les coordonnées géographiques sont cohérentes
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is not None and longitude is not None:
            if not (-90 <= latitude <= 90):
                raise serializers.ValidationError({
                    'latitude': 'La latitude doit être comprise entre -90 et 90.'
                })
            if not (-180 <= longitude <= 180):
                raise serializers.ValidationError({
                    'longitude': 'La longitude doit être comprise entre -180 et 180.'
                })
        
        # Définir une date d'expiration par défaut (7 jours) si non spécifiée
        if not data.get('expires_at'):
            data['expires_at'] = timezone.now() + timedelta(days=7)
        
        return data
    
    def create(self, validated_data):
        """Créer une nouvelle demande d'aide"""
        # L'auteur est automatiquement défini comme l'utilisateur connecté
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class HelpRequestListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la liste des demandes d'aide (version allégée)"""
    
    author_name = serializers.SerializerMethodField()
    time_ago = serializers.ReadOnlyField()
    location_display = serializers.ReadOnlyField()
    need_type_display = serializers.SerializerMethodField()
    request_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    duration_display = serializers.ReadOnlyField()
    
    class Meta:
        model = HelpRequest
        fields = [
            'id', 'author_name', 'request_type', 'request_type_display', 'need_type', 'need_type_display',
            'title', 'description', 'latitude', 'longitude', 'location_display', 'status', 'status_display',
            'is_urgent', 'created_at', 'time_ago', 'responses_count', 'views_count', 'photo',
            'duration_type', 'duration_display', 'proximity_zone', 'for_who'
        ]
    
    def get_author_name(self, obj):
        """Retourne le nom affiché de l'auteur"""
        if obj.author:
            if obj.author.first_name and obj.author.last_name:
                return f"{obj.author.first_name} {obj.author.last_name}"
            return obj.author.username
        return "Utilisateur"
    
    def get_need_type_display(self, obj):
        """Retourne le nom affiché du type de besoin"""
        return obj.get_need_type_display()
    
    def get_request_type_display(self, obj):
        """Retourne le nom affiché du type de demande"""
        return obj.get_request_type_display()
    
    def get_status_display(self, obj):
        """Retourne le nom affiché du statut"""
        return obj.get_status_display()


class HelpRequestMapSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les données de carte (version minimale)"""
    
    author_name = serializers.SerializerMethodField()
    need_type_display = serializers.SerializerMethodField()
    request_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = HelpRequest
        fields = [
            'id', 'title', 'author_name', 'request_type', 'request_type_display', 'need_type', 'need_type_display',
            'latitude', 'longitude', 'is_urgent', 'status', 'responses_count', 'created_at'
        ]
    
    def get_author_name(self, obj):
        """Retourne le nom affiché de l'auteur"""
        if obj.author:
            if obj.author.first_name and obj.author.last_name:
                return f"{obj.author.first_name} {obj.author.last_name}"
            return obj.author.username
        return "Utilisateur"
    
    def get_need_type_display(self, obj):
        """Retourne le nom affiché du type de besoin"""
        return obj.get_need_type_display()
    
    def get_request_type_display(self, obj):
        """Retourne le nom affiché du type de demande"""
        return obj.get_request_type_display()


class HelpRequestStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les statistiques des demandes d'aide"""
    
    class Meta:
        model = HelpRequest
        fields = ['id', 'title', 'status', 'created_at', 'responses_count', 'views_count']


class HelpRequestFilterSerializer(serializers.Serializer):
    """Sérialiseur pour les filtres de recherche"""
    
    request_type = serializers.ChoiceField(choices=HelpRequest.REQUEST_TYPES, required=False)
    need_type = serializers.ChoiceField(choices=HelpRequest.NEED_TYPES, required=False)
    status = serializers.ChoiceField(choices=HelpRequest.STATUS_CHOICES, required=False)
    duration_type = serializers.ChoiceField(choices=HelpRequest.DURATION_CHOICES, required=False)
    proximity_zone = serializers.ChoiceField(choices=[
        ('local', 'Quartier'),
        ('city', 'Ville'),
        ('region', 'Région'),
    ], required=False)
    is_urgent = serializers.BooleanField(required=False)
    search = serializers.CharField(max_length=200, required=False)
    radius = serializers.IntegerField(min_value=1, max_value=100, required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)


class HelpResponseSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les réponses aux demandes d'aide"""
    
    author = UserSerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    help_request_title = serializers.CharField(source='help_request.title', read_only=True)
    response_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = HelpResponse
        fields = [
            'id', 'help_request', 'help_request_title', 'author', 'author_name', 'response_type', 
            'response_type_display', 'message', 'contact_phone', 'contact_email', 'is_accepted', 
            'is_rejected', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'author_name', 'help_request_title', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        """Retourne le nom affiché de l'auteur"""
        if obj.author:
            if obj.author.first_name and obj.author.last_name:
                return f"{obj.author.first_name} {obj.author.last_name}"
            return obj.author.username
        return "Utilisateur"
    
    def get_response_type_display(self, obj):
        """Retourne le nom affiché du type de réponse"""
        return obj.get_response_type_display()
    
    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que le message n'est pas vide
        if not data.get('message', '').strip():
            raise serializers.ValidationError({
                'message': 'Le message ne peut pas être vide.'
            })
        
        return data
    
    def create(self, validated_data):
        """Créer une nouvelle réponse"""
        # L'auteur est automatiquement défini comme l'utilisateur connecté
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data) 
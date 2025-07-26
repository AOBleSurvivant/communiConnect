from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
import uuid

class HelpRequest(models.Model):
    """
    Modèle pour les demandes d'aide communautaire (solidarité locale)
    Inspiré de Nextdoor - Différent des alertes d'urgence
    """
    
    # Types de besoins (solidarité, non-urgent)
    NEED_TYPES = [
        ('material', 'Matériel'),
        ('presence', 'Présence/Accompagnement'),
        ('service', 'Service'),
        ('transport', 'Transport'),
        ('shopping', 'Courses'),
        ('technical', 'Aide technique'),
        ('education', 'Aide éducative'),
        ('other', 'Autre'),
    ]
    
    # Types de demande
    REQUEST_TYPES = [
        ('request', 'Demande d\'aide'),
        ('offer', 'Offre d\'aide'),
    ]
    
    # Statuts de suivi
    STATUS_CHOICES = [
        ('open', 'Ouverte'),
        ('in_progress', 'En cours'),
        ('completed', 'Clôturée'),
        ('cancelled', 'Annulée'),
    ]
    
    # Durée estimée
    DURATION_CHOICES = [
        ('immediate', 'Immédiat'),
        ('this_week', 'Cette semaine'),
        ('this_month', 'Ce mois'),
        ('specific_date', 'Avant une date spécifique'),
        ('ongoing', 'En continu'),
    ]
    
    # Pour qui
    FOR_WHO_CHOICES = [
        ('myself', 'Moi-même'),
        ('family', 'Ma famille'),
        ('neighbor', 'Mon voisin'),
        ('community', 'La communauté'),
        ('other', 'Autre'),
    ]
    
    # Champs principaux
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='help_requests')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES, default='request')
    need_type = models.CharField(max_length=20, choices=NEED_TYPES)
    for_who = models.CharField(max_length=20, choices=FOR_WHO_CHOICES, default='myself')
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5), MaxLengthValidator(200)])
    description = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(2000)])
    
    # Durée et planning
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, default='this_week')
    specific_date = models.DateField(null=True, blank=True)
    estimated_hours = models.PositiveIntegerField(null=True, blank=True, help_text="Durée estimée en heures")
    
    # Géolocalisation et zone
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    proximity_zone = models.CharField(max_length=50, default='local', choices=[
        ('local', 'Quartier'),
        ('city', 'Ville'),
        ('region', 'Région'),
    ])
    
    # Statut et gestion
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_urgent = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Lien avec une alerte (optionnel)
    related_alert = models.ForeignKey(
        'notifications.CommunityAlert', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='related_help_requests'
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    responses_count = models.PositiveIntegerField(default=0)
    
    # Champs optionnels
    custom_need_type = models.CharField(max_length=100, blank=True)  # Si "other" est sélectionné
    custom_for_who = models.CharField(max_length=100, blank=True)    # Si "other" est sélectionné
    photo = models.ImageField(upload_to='help_requests/', null=True, blank=True)
    contact_preference = models.CharField(max_length=20, choices=[
        ('message', 'Message privé'),
        ('phone', 'Téléphone'),
        ('email', 'Email'),
        ('any', 'N\'importe lequel'),
    ], default='message')
    
    # Champs de contact (optionnels)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    class Meta:
        db_table = 'help_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['request_type', 'need_type']),
            models.Index(fields=['status', 'is_urgent']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['city', 'neighborhood']),
            models.Index(fields=['created_at']),
            models.Index(fields=['duration_type']),
            models.Index(fields=['proximity_zone']),
        ]
    
    def __str__(self):
        return f"{self.get_request_type_display()} - {self.title} ({self.author.username})"
    
    @property
    def is_expired(self):
        """Vérifie si la demande a expiré"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def location_display(self):
        """Affiche la localisation de manière lisible"""
        if self.address:
            return self.address
        elif self.neighborhood and self.city:
            return f"{self.neighborhood}, {self.city}"
        elif self.city:
            return self.city
        return "Localisation non spécifiée"
    
    @property
    def time_ago(self):
        """Retourne le temps écoulé depuis la création"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "à l'instant"
    
    @property
    def duration_display(self):
        """Affiche la durée de manière lisible"""
        if self.duration_type == 'immediate':
            return "Immédiat"
        elif self.duration_type == 'this_week':
            return "Cette semaine"
        elif self.duration_type == 'this_month':
            return "Ce mois"
        elif self.duration_type == 'specific_date' and self.specific_date:
            return f"Avant le {self.specific_date.strftime('%d/%m/%Y')}"
        elif self.duration_type == 'ongoing':
            return "En continu"
        return "Non spécifié"
    
    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_responses(self):
        """Incrémente le compteur de réponses"""
        self.responses_count += 1
        self.save(update_fields=['responses_count'])


class HelpResponse(models.Model):
    """
    Modèle pour les réponses aux demandes d'aide
    """
    
    RESPONSE_TYPES = [
        ('offer_help', 'Je peux aider'),
        ('need_help', 'J\'ai besoin d\'aide'),
        ('contact', 'Contacter'),
        ('question', 'Question'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='help_responses')
    response_type = models.CharField(max_length=20, choices=RESPONSE_TYPES)
    message = models.TextField(validators=[MinLengthValidator(5), MaxLengthValidator(1000)])
    
    # Contact info (optionnel)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    
    # Statut
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'help_responses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Réponse de {self.author.username} à {self.help_request.title}"
    
    def accept(self):
        """Accepte la réponse"""
        self.is_accepted = True
        self.is_rejected = False
        self.save()
        self.help_request.increment_responses()
    
    def reject(self):
        """Rejette la réponse"""
        self.is_rejected = True
        self.is_accepted = False
        self.save()


class HelpRequestCategory(models.Model):
    """
    Catégories pour organiser les types de besoins
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)  # Emoji
    color = models.CharField(max_length=20, default='blue')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'help_request_categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name 
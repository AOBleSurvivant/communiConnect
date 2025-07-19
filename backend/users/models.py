from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from geography.models import Quartier


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec restrictions géographiques"""
    
    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('ambassador', 'Ambassadeur'),
        ('admin', 'Administrateur'),
    ]
    
    # Informations de base
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Informations géographiques
    quartier = models.ForeignKey(
        Quartier, 
        on_delete=models.PROTECT, 
        related_name='residents',
        verbose_name="Quartier de résidence",
        null=True,
        blank=True
    )
    
    # Rôle et statut
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_verified = models.BooleanField(default=False)
    is_geographically_verified = models.BooleanField(default=False)
    
    # Informations supplémentaires
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Champs requis pour l'inscription
    REQUIRED_FIELDS = ['email', 'quartier']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.quartier.nom})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def location_info(self):
        """Retourne les informations de localisation complètes"""
        return {
            'quartier': self.quartier.nom,
            'commune': self.quartier.commune.nom,
            'prefecture': self.quartier.prefecture.nom,
            'region': self.quartier.region.nom,
            'full_address': self.quartier.full_address
        }
    
    @property
    def is_ambassador(self):
        return self.role in ['ambassador', 'admin']
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def can_access_guinea_only(self):
        """Vérifie si l'utilisateur peut accéder au contenu réservé à la Guinée"""
        return self.is_geographically_verified and self.quartier is not None
    
    def get_neighbors(self):
        """Retourne les utilisateurs du même quartier"""
        return User.objects.filter(
            quartier=self.quartier,
            is_active=True
        ).exclude(id=self.id)
    
    def get_commune_users(self):
        """Retourne les utilisateurs de la même commune"""
        return User.objects.filter(
            quartier__commune=self.quartier.commune,
            is_active=True
        ).exclude(id=self.id)
    
    def get_prefecture_users(self):
        """Retourne les utilisateurs de la même préfecture"""
        return User.objects.filter(
            quartier__prefecture=self.quartier.prefecture,
            is_active=True
        ).exclude(id=self.id)
    
    def get_followers_count(self):
        """Retourne le nombre de followers"""
        return self.followers.count()
    
    def get_following_count(self):
        """Retourne le nombre d'utilisateurs suivis"""
        return self.following.count()
    
    def is_following(self, user):
        """Vérifie si l'utilisateur suit un autre utilisateur"""
        return self.following.filter(followed=user).exists()
    
    def get_suggested_friends(self, limit=10):
        """Retourne des suggestions d'amis basées sur le quartier"""
        if not self.quartier:
            return User.objects.none()
        
        # Utilisateurs du même quartier qui ne sont pas déjà suivis
        followed_ids = self.following.values_list('followed_id', flat=True)
        return User.objects.filter(
            quartier=self.quartier,
            is_active=True
        ).exclude(
            id__in=followed_ids
        ).exclude(
            id=self.id
        )[:limit]


class UserRelationship(models.Model):
    """Modèle pour gérer les relations d'amitié entre utilisateurs"""
    
    RELATIONSHIP_STATUS = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
        ('blocked', 'Bloqué'),
    ]
    
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following',
        verbose_name="Utilisateur qui suit"
    )
    followed = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers',
        verbose_name="Utilisateur suivi"
    )
    status = models.CharField(
        max_length=20, 
        choices=RELATIONSHIP_STATUS, 
        default='accepted',
        verbose_name="Statut de la relation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Relation Utilisateur"
        verbose_name_plural = "Relations Utilisateurs"
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} suit {self.followed.username}"
    
    @property
    def is_active(self):
        """Vérifie si la relation est active"""
        return self.status == 'accepted'
    
    def accept(self):
        """Accepte la demande d'amitié"""
        self.status = 'accepted'
        self.save(update_fields=['status', 'updated_at'])
    
    def reject(self):
        """Refuse la demande d'amitié"""
        self.status = 'rejected'
        self.save(update_fields=['status', 'updated_at'])
    
    def block(self):
        """Bloque l'utilisateur"""
        self.status = 'blocked'
        self.save(update_fields=['status', 'updated_at'])


class UserProfile(models.Model):
    """Profil étendu pour les informations supplémentaires"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Informations professionnelles
    profession = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    # Informations sociales
    interests = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    
    # Paramètres de confidentialité
    show_phone = models.BooleanField(default=False)
    show_email = models.BooleanField(default=False)
    show_location = models.BooleanField(default=True)
    
    # Statistiques
    posts_count = models.PositiveIntegerField(default=0)
    connections_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def increment_posts_count(self):
        self.posts_count += 1
        self.save(update_fields=['posts_count'])
    
    def decrement_posts_count(self):
        if self.posts_count > 0:
            self.posts_count -= 1
            self.save(update_fields=['posts_count'])
    
    def update_connections_count(self):
        """Met à jour le nombre de connexions"""
        followers_count = self.user.get_followers_count()
        following_count = self.user.get_following_count()
        self.connections_count = followers_count + following_count
        self.save(update_fields=['connections_count'])


class GeographicVerification(models.Model):
    """Historique des vérifications géographiques"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='geo_verifications')
    ip_address = models.GenericIPAddressField()
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_guinea = models.BooleanField()
    verification_method = models.CharField(max_length=20, choices=[
        ('ip', 'Géolocalisation IP'),
        ('manual', 'Sélection manuelle'),
        ('admin', 'Administrateur'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vérification Géographique"
        verbose_name_plural = "Vérifications Géographiques"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Vérification {self.user.username} - {self.created_at}" 
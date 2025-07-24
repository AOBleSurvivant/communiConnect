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


class CommunityGroup(models.Model):
    """Modèle pour les groupes communautaires"""
    
    GROUP_TYPES = [
        ('neighborhood', 'Quartier'),
        ('community', 'Communauté'),
        ('sports', 'Sport'),
        ('education', 'Éducation'),
        ('business', 'Commerce'),
        ('culture', 'Culture'),
        ('health', 'Santé'),
        ('environment', 'Environnement'),
        ('youth', 'Jeunesse'),
        ('women', 'Femmes'),
        ('other', 'Autre'),
    ]
    
    PRIVACY_LEVELS = [
        ('public', 'Public'),
        ('private', 'Privé'),
        ('secret', 'Secret'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom du groupe")
    description = models.TextField(blank=True, verbose_name="Description")
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES, default='community')
    privacy_level = models.CharField(max_length=10, choices=PRIVACY_LEVELS, default='public')
    
    # Géolocalisation
    quartier = models.ForeignKey('geography.Quartier', on_delete=models.CASCADE, verbose_name="Quartier")
    
    # Créateur et administrateurs
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups', verbose_name="Créateur")
    admins = models.ManyToManyField(User, related_name='administered_groups', blank=True, verbose_name="Administrateurs")
    
    # Médias
    cover_image = models.ImageField(upload_to='groups/covers/', blank=True, null=True, verbose_name="Image de couverture")
    profile_image = models.ImageField(upload_to='groups/profiles/', blank=True, null=True, verbose_name="Image de profil")
    
    # Statistiques
    member_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de membres")
    post_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de posts")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Groupe Communautaire"
        verbose_name_plural = "Groupes Communautaires"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.quartier.nom})"
    
    def get_members(self):
        """Retourne tous les membres du groupe"""
        return self.members.all()
    
    def get_admins(self):
        """Retourne tous les administrateurs du groupe"""
        return self.admins.all()
    
    def is_member(self, user):
        """Vérifie si un utilisateur est membre du groupe"""
        return self.members.filter(id=user.id).exists()
    
    def is_admin(self, user):
        """Vérifie si un utilisateur est administrateur du groupe"""
        return self.admins.filter(id=user.id).exists() or self.creator == user


class GroupMembership(models.Model):
    """Modèle pour les adhésions aux groupes"""
    
    MEMBERSHIP_STATUS = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Refusé'),
        ('banned', 'Banni'),
    ]
    
    ROLE_TYPES = [
        ('member', 'Membre'),
        ('moderator', 'Modérateur'),
        ('admin', 'Administrateur'),
    ]
    
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='memberships', verbose_name="Groupe")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships', verbose_name="Utilisateur")
    status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='pending', verbose_name="Statut")
    role = models.CharField(max_length=20, choices=ROLE_TYPES, default='member', verbose_name="Rôle")
    
    # Métadonnées
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'adhésion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Adhésion au Groupe"
        verbose_name_plural = "Adhésions aux Groupes"
        unique_together = ('group', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
    
    def approve(self):
        """Approuve l'adhésion"""
        self.status = 'approved'
        self.save(update_fields=['status', 'updated_at'])
        self.group.member_count = self.group.members.count()
        self.group.save(update_fields=['member_count'])
    
    def reject(self):
        """Refuse l'adhésion"""
        self.status = 'rejected'
        self.save(update_fields=['status', 'updated_at'])
    
    def ban(self):
        """Bannit le membre"""
        self.status = 'banned'
        self.save(update_fields=['status', 'updated_at'])
        self.group.member_count = self.group.members.count()
        self.group.save(update_fields=['member_count'])


class CommunityEvent(models.Model):
    """Modèle pour les événements communautaires"""
    
    EVENT_TYPES = [
        ('meeting', 'Réunion'),
        ('celebration', 'Célébration'),
        ('sports', 'Sport'),
        ('education', 'Éducation'),
        ('business', 'Commerce'),
        ('culture', 'Culture'),
        ('health', 'Santé'),
        ('environment', 'Environnement'),
        ('youth', 'Jeunesse'),
        ('other', 'Autre'),
    ]
    
    EVENT_STATUS = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meeting')
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='draft')
    
    # Dates et heures
    start_date = models.DateTimeField(verbose_name="Date et heure de début")
    end_date = models.DateTimeField(verbose_name="Date et heure de fin")
    
    # Localisation
    quartier = models.ForeignKey('geography.Quartier', on_delete=models.CASCADE, verbose_name="Quartier")
    location_details = models.CharField(max_length=500, blank=True, verbose_name="Détails du lieu")
    
    # Organisateur et groupe associé
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', verbose_name="Organisateur")
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='events', blank=True, null=True, verbose_name="Groupe associé")
    
    # Médias
    cover_image = models.ImageField(upload_to='events/covers/', blank=True, null=True, verbose_name="Image de couverture")
    
    # Statistiques
    attendee_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de participants")
    max_attendees = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nombre maximum de participants")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_public = models.BooleanField(default=True, verbose_name="Public")
    
    class Meta:
        verbose_name = "Événement Communautaire"
        verbose_name_plural = "Événements Communautaires"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%d/%m/%Y')}"
    
    def get_attendees(self):
        """Retourne tous les participants"""
        return self.attendees.all()
    
    def is_attendee(self, user):
        """Vérifie si un utilisateur participe à l'événement"""
        return self.attendees.filter(id=user.id).exists()
    
    def can_join(self, user):
        """Vérifie si un utilisateur peut rejoindre l'événement"""
        if not self.is_public:
            return False
        if self.max_attendees and self.attendee_count >= self.max_attendees:
            return False
        return not self.is_attendee(user)


class EventAttendance(models.Model):
    """Modèle pour les participations aux événements"""
    
    ATTENDANCE_STATUS = [
        ('going', 'Participe'),
        ('maybe', 'Peut-être'),
        ('not_going', 'Ne participe pas'),
    ]
    
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE, related_name='attendances', verbose_name="Événement")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances', verbose_name="Utilisateur")
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default='going', verbose_name="Statut")
    
    # Métadonnées
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Participation à l'Événement"
        verbose_name_plural = "Participations aux Événements"
        unique_together = ('event', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec mise à jour du compteur"""
        super().save(*args, **kwargs)
        self.event.attendee_count = self.event.attendances.filter(status='going').count()
        self.event.save(update_fields=['attendee_count'])


class UserAchievement(models.Model):
    """Modèle pour les réalisations utilisateur (gamification)"""
    
    ACHIEVEMENT_TYPES = [
        ('first_post', 'Premier Post'),
        ('first_friend', 'Premier Ami'),
        ('first_group', 'Premier Groupe'),
        ('first_event', 'Premier Événement'),
        ('post_milestone', 'Palier de Posts'),
        ('friend_milestone', 'Palier d\'Amis'),
        ('group_milestone', 'Palier de Groupes'),
        ('event_milestone', 'Palier d\'Événements'),
        ('engagement_milestone', 'Palier d\'Engagement'),
        ('community_leader', 'Leader Communautaire'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements', verbose_name="Utilisateur")
    achievement_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPES, verbose_name="Type de réalisation")
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    icon = models.CharField(max_length=10, verbose_name="Icône")
    points = models.PositiveIntegerField(default=0, verbose_name="Points")
    
    # Métadonnées
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de déblocage")
    
    class Meta:
        verbose_name = "Réalisation Utilisateur"
        verbose_name_plural = "Réalisations Utilisateur"
        unique_together = ('user', 'achievement_type')
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserSocialScore(models.Model):
    """Modèle pour le score social utilisateur"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_score', verbose_name="Utilisateur")
    total_points = models.PositiveIntegerField(default=0, verbose_name="Points totaux")
    level = models.PositiveIntegerField(default=1, verbose_name="Niveau")
    achievements_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de réalisations")
    
    # Statistiques détaillées
    posts_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de posts")
    friends_count = models.PositiveIntegerField(default=0, verbose_name="Nombre d'amis")
    groups_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de groupes")
    events_count = models.PositiveIntegerField(default=0, verbose_name="Nombre d'événements")
    likes_received = models.PositiveIntegerField(default=0, verbose_name="Likes reçus")
    comments_received = models.PositiveIntegerField(default=0, verbose_name="Commentaires reçus")
    
    # Métadonnées
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Score Social Utilisateur"
        verbose_name_plural = "Scores Sociaux Utilisateur"
    
    def __str__(self):
        return f"{self.user.username} - Niveau {self.level} ({self.total_points} points)"
    
    def calculate_level(self):
        """Calcule le niveau basé sur les points"""
        # Formule : niveau = 1 + (points // 100)
        self.level = 1 + (self.total_points // 100)
        return self.level
    
    def add_points(self, points):
        """Ajoute des points et recalcule le niveau"""
        self.total_points += points
        self.calculate_level()
        self.save(update_fields=['total_points', 'level', 'last_updated'])
    
    def update_stats(self):
        """Met à jour toutes les statistiques"""
        self.posts_count = self.user.posts.count()
        self.friends_count = self.user.followers.filter(userrelationship__status='accepted').count()
        self.groups_count = self.user.group_memberships.filter(status='approved').count()
        self.events_count = self.user.event_attendances.filter(status='going').count()
        self.achievements_count = self.user.achievements.count()
        
        # Calculer les likes et commentaires reçus
        total_likes = sum(post.likes.count() for post in self.user.posts.all())
        total_comments = sum(post.comments.count() for post in self.user.posts.all())
        
        self.likes_received = total_likes
        self.comments_received = total_comments
        
        self.save() 
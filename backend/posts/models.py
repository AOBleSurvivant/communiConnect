from django.db import models
from django.contrib.auth import get_user_model
from geography.models import Quartier
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_video_duration(value):
    """Valide que la vidéo ne dépasse pas 60 secondes"""
    # Cette validation sera complétée côté serveur avec FFmpeg
    pass

def validate_file_size(value):
    """Valide la taille du fichier (max 50MB pour vidéos, 10MB pour images)"""
    filesize = value.size
    
    if hasattr(value, 'content_type'):
        if 'video' in value.content_type:
            if filesize > 50 * 1024 * 1024:  # 50MB
                raise ValidationError("La vidéo ne peut pas dépasser 50MB")
        elif 'image' in value.content_type:
            if filesize > 10 * 1024 * 1024:  # 10MB
                raise ValidationError("L'image ne peut pas dépasser 10MB")

class Media(models.Model):
    """Modèle pour les fichiers médias (images et vidéos)"""
    
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
        ('live', 'Live'),
    ]
    
    APPROVAL_STATUS = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('inappropriate', 'Inapproprié'),
    ]
    
    # Informations de base
    file = models.FileField(
        upload_to='media/%Y/%m/%d/',
        validators=[validate_file_size],
        verbose_name="Fichier"
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    
    # Métadonnées
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    duration = models.DurationField(null=True, blank=True, verbose_name="Durée (vidéo)")
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name="Taille du fichier")
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name="Largeur")
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name="Hauteur")
    
    # CDN Cloudinary
    cdn_url = models.URLField(blank=True, null=True, verbose_name="URL CDN")
    cdn_public_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID public CDN")
    
    # Modération et conformité
    is_appropriate = models.BooleanField(default=True, verbose_name="Contenu approprié")
    approval_status = models.CharField(
        max_length=20, 
        choices=APPROVAL_STATUS, 
        default='pending',
        verbose_name="Statut d'approbation"
    )
    moderation_score = models.FloatField(null=True, blank=True, verbose_name="Score de modération")
    moderation_details = models.JSONField(default=dict, blank=True, verbose_name="Détails de modération")
    
    # Live streaming
    is_live = models.BooleanField(default=False, verbose_name="En direct")
    live_stream_key = models.CharField(max_length=100, blank=True, verbose_name="Clé de stream")
    live_viewers_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de spectateurs")
    live_started_at = models.DateTimeField(null=True, blank=True, verbose_name="Début du live")
    live_ended_at = models.DateTimeField(null=True, blank=True, verbose_name="Fin du live")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_media_type_display()} - {self.title or self.file.name}"
    
    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    @property
    def file_url(self):
        """Retourne l'URL du fichier (CDN en priorité)"""
        if self.cdn_url:
            return self.cdn_url
        elif self.file:
            return self.file.url
        return None
    
    @property
    def thumbnail_url(self):
        """Retourne l'URL de la miniature (pour vidéos)"""
        if self.media_type == 'video' and self.file:
            # Logique pour générer/retourner la miniature
            return self.file.url.replace('.mp4', '_thumb.jpg')
        return self.file_url
    
    def is_approved_for_publication(self):
        """Vérifie si le média peut être publié"""
        return (
            self.approval_status == 'approved' and 
            self.is_appropriate and 
            not self.is_live
        )

class Post(models.Model):
    """Modèle pour les posts/messages de la communauté"""
    
    POST_TYPES = [
        ('info', 'Information'),
        ('event', 'Événement'),
        ('help', 'Demande d\'aide'),
        ('announcement', 'Annonce'),
        ('discussion', 'Discussion'),
        ('live', 'Live'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='posts')
    
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='info')
    
    # Médias du post
    media_files = models.ManyToManyField(Media, blank=True, related_name='posts', verbose_name="Fichiers médias")
    
    # Live streaming
    is_live_post = models.BooleanField(default=False, verbose_name="Publication live")
    live_stream = models.OneToOneField(
        Media, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='live_post',
        verbose_name="Stream live"
    )
    
    # Métadonnées
    is_pinned = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    
    # Statistiques
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return f"Post de {self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_likes(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def decrement_likes(self):
        if self.likes_count > 0:
            self.likes_count -= 1
            self.save(update_fields=['likes_count'])
    
    @property
    def has_media(self):
        """Vérifie si le post contient des médias"""
        return self.media_files.exists() or self.live_stream is not None
    
    @property
    def media_count(self):
        """Retourne le nombre de médias"""
        count = self.media_files.count()
        if self.live_stream:
            count += 1
        return count

class PostLike(models.Model):
    """Modèle pour les likes sur les posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
        verbose_name = "Like"
        verbose_name_plural = "Likes"
    
    def __str__(self):
        return f"Like de {self.user.username} sur {self.post}"

class PostComment(models.Model):
    """Modèle pour les commentaires sur les posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    
    # Support des réponses aux commentaires
    parent_comment = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        verbose_name="Commentaire parent"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.post}"
    
    @property
    def is_reply(self):
        """Vérifie si c'est une réponse à un commentaire"""
        return self.parent_comment is not None
    
    @property
    def replies_count(self):
        """Retourne le nombre de réponses"""
        return self.replies.count()
    
    @property
    def level(self):
        """Retourne le niveau de profondeur du commentaire"""
        if self.parent_comment is None:
            return 0
        return self.parent_comment.level + 1
    
    def get_replies(self):
        """Retourne les réponses directes à ce commentaire"""
        return self.replies.all()
    
    def get_all_replies(self):
        """Retourne toutes les réponses (récursif)"""
        all_replies = []
        for reply in self.replies.all():
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())
        return all_replies 

class PostShare(models.Model):
    """Modèle pour les partages de posts"""
    SHARE_TYPES = [
        ('share', 'Partage'),
        ('repost', 'Repost'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    share_type = models.CharField(max_length=10, choices=SHARE_TYPES, default='share')
    comment = models.TextField(blank=True, verbose_name="Commentaire du partage")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post', 'share_type']
        verbose_name = "Partage de post"
        verbose_name_plural = "Partages de posts"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Partage de {self.user.username} sur {self.post}"
    
    def save(self, *args, **kwargs):
        # Incrémenter le compteur de partages du post
        if not self.pk:  # Nouveau partage
            self.post.shares_count = getattr(self.post, 'shares_count', 0) + 1
            self.post.save(update_fields=['shares_count'])
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Décrémenter le compteur de partages du post
        self.post.shares_count = max(0, getattr(self.post, 'shares_count', 0) - 1)
        self.post.save(update_fields=['shares_count'])
        super().delete(*args, **kwargs) 

class ExternalShare(models.Model):
    """Modèle pour les partages externes (réseaux sociaux)"""
    EXTERNAL_PLATFORMS = [
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('telegram', 'Telegram'),
        ('email', 'Email'),
        ('copy_link', 'Copier le lien'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='external_shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='external_shares')
    platform = models.CharField(max_length=20, choices=EXTERNAL_PLATFORMS)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post', 'platform']
        verbose_name = "Partage externe"
        verbose_name_plural = "Partages externes"
        ordering = ['-shared_at']
    
    def __str__(self):
        return f"{self.user.username} a partagé sur {self.get_platform_display()}" 

class PostAnalytics(models.Model):
    """Modèle pour les statistiques avancées des posts"""
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='analytics')
    
    # Métriques de base
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    total_external_shares = models.PositiveIntegerField(default=0)
    
    # Métriques de viralité
    viral_score = models.FloatField(default=0.0)  # Score de viralité (0-100)
    engagement_rate = models.FloatField(default=0.0)  # Taux d'engagement
    reach_multiplier = models.FloatField(default=1.0)  # Multiplicateur de portée
    
    # Détails des partages externes
    whatsapp_shares = models.PositiveIntegerField(default=0)
    facebook_shares = models.PositiveIntegerField(default=0)
    twitter_shares = models.PositiveIntegerField(default=0)
    telegram_shares = models.PositiveIntegerField(default=0)
    email_shares = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytics de post"
        verbose_name_plural = "Analytics de posts"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Analytics pour post {self.post.id}"
    
    def calculate_viral_score(self):
        """Calcule le score de viralité basé sur les métriques"""
        # Formule : (likes + comments + shares) / views * 100
        if self.total_views > 0:
            engagement = (self.total_likes + self.total_comments + self.total_shares) / self.total_views
            self.viral_score = min(engagement * 100, 100.0)
        else:
            self.viral_score = 0.0
        return self.viral_score
    
    def calculate_engagement_rate(self):
        """Calcule le taux d'engagement"""
        if self.total_views > 0:
            self.engagement_rate = ((self.total_likes + self.total_comments + self.total_shares) / self.total_views) * 100
        else:
            self.engagement_rate = 0.0
        return self.engagement_rate
    
    def update_analytics(self):
        """Met à jour toutes les métriques"""
        # Récupérer les données du post
        self.total_likes = self.post.likes_count
        self.total_comments = self.post.comments_count
        self.total_views = self.post.views_count
        self.total_shares = self.post.shares_count
        
        # Compter les partages externes
        external_shares = self.post.external_shares.all()
        self.total_external_shares = external_shares.count()
        
        # Compter par plateforme
        self.whatsapp_shares = external_shares.filter(platform='whatsapp').count()
        self.facebook_shares = external_shares.filter(platform='facebook').count()
        self.twitter_shares = external_shares.filter(platform='twitter').count()
        self.telegram_shares = external_shares.filter(platform='telegram').count()
        self.email_shares = external_shares.filter(platform='email').count()
        
        # Calculer les scores
        self.calculate_viral_score()
        self.calculate_engagement_rate()
        
        self.save() 
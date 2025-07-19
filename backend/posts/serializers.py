from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Post, PostLike, PostComment, Media, PostShare, ExternalShare, PostAnalytics
from users.serializers import UserSerializer
from geography.serializers import QuartierSerializer
import logging

logger = logging.getLogger(__name__)


class MediaSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les médias
    
    Inclut les URLs CDN et les métadonnées optimisées
    """
    file_url = serializers.ReadOnlyField(help_text="URL du fichier (CDN en priorité)")
    thumbnail_url = serializers.ReadOnlyField(help_text="URL de la miniature (pour vidéos)")
    is_approved_for_publication = serializers.ReadOnlyField(help_text="Indique si le média peut être publié")
    cdn_url = serializers.ReadOnlyField(help_text="URL CDN Cloudinary si configuré")
    cdn_public_id = serializers.ReadOnlyField(help_text="ID public du CDN")
    width = serializers.ReadOnlyField(help_text="Largeur de l'image/vidéo")
    height = serializers.ReadOnlyField(help_text="Hauteur de l'image/vidéo")
    
    class Meta:
        model = Media
        fields = [
            'id', 'file', 'media_type', 'title', 'description', 'duration',
            'file_size', 'width', 'height', 'is_appropriate', 'approval_status', 
            'moderation_score', 'is_live', 'live_viewers_count', 'file_url', 
            'thumbnail_url', 'is_approved_for_publication', 'cdn_url', 
            'cdn_public_id', 'created_at'
        ]
        read_only_fields = [
            'file_size', 'width', 'height', 'is_appropriate', 'approval_status', 
            'moderation_score', 'is_live', 'live_viewers_count', 'file_url', 
            'thumbnail_url', 'is_approved_for_publication', 'cdn_url', 
            'cdn_public_id', 'created_at'
        ]


class MediaCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer des médias"""
    
    class Meta:
        model = Media
        fields = ['id', 'file', 'title', 'description']
        read_only_fields = ['id']
    
    def validate_file(self, value):
        """Validation personnalisée du fichier"""
        # Vérifier le type de fichier
        content_type = value.content_type
        if 'image' not in content_type and 'video' not in content_type:
            raise serializers.ValidationError("Seuls les fichiers image et vidéo sont autorisés")
        
        # Vérifier la taille
        if value.size > 50 * 1024 * 1024:  # 50MB max
            raise serializers.ValidationError("Le fichier ne peut pas dépasser 50MB")
        
        return value
    
    def create(self, validated_data):
        # Déterminer le type de média
        file = validated_data['file']
        if 'image' in file.content_type:
            validated_data['media_type'] = 'image'
        elif 'video' in file.content_type:
            validated_data['media_type'] = 'video'
        
        return super().create(validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    is_reply = serializers.ReadOnlyField()
    level = serializers.ReadOnlyField()
    
    class Meta:
        model = PostComment
        fields = [
            'id', 'author', 'content', 'is_anonymous', 'parent_comment', 
            'replies', 'replies_count', 'is_reply', 'level',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'author', 'replies', 'replies_count', 'is_reply', 'level',
            'created_at', 'updated_at'
        ]
    
    def get_replies(self, obj):
        """Retourne les réponses directes (pas récursif pour éviter les boucles infinies)"""
        replies = obj.replies.all()
        return PostCommentSerializer(replies, many=True, context=self.context).data


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    quartier = QuartierSerializer(read_only=True)
    media_files = MediaSerializer(many=True, read_only=True)
    live_stream = MediaSerializer(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    likes = PostLikeSerializer(many=True, read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()
    has_media = serializers.ReadOnlyField()
    media_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'quartier', 'title', 'content', 'post_type',
            'media_files', 'live_stream', 'is_live_post', 'is_pinned', 'is_anonymous', 
            'likes_count', 'comments_count', 'views_count', 'created_at', 'updated_at', 
            'comments', 'likes', 'is_liked_by_user', 'has_media', 'media_count'
        ]
        read_only_fields = [
            'author', 'quartier', 'media_files', 'live_stream', 'likes_count', 
            'comments_count', 'views_count', 'created_at', 'updated_at', 
            'comments', 'likes', 'is_liked_by_user', 'has_media', 'media_count'
        ]
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    media_files = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'is_anonymous', 'media_files']
        extra_kwargs = {
            'title': {'required': False, 'allow_blank': True},
            'content': {'required': True},
            'post_type': {'required': False, 'default': 'info'},
            'is_anonymous': {'required': False, 'default': False},
        }
    
    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié")
        
        if not request.user.quartier:
            raise serializers.ValidationError("Vous devez avoir un quartier assigné pour publier")
        
        # Vérifier qu'il y a au moins du contenu ou des médias
        content = data.get('content', '').strip()
        media_files = data.get('media_files', [])
        
        logger.info(f"Validation PostCreateSerializer - Contenu: '{content}', Médias: {media_files}")
        
        if not content and not media_files:
            raise serializers.ValidationError("Vous devez ajouter du contenu ou des médias")
        
        # Vérifier la limite du nombre de fichiers (5 maximum)
        if len(media_files) > 5:
            raise serializers.ValidationError("Vous ne pouvez pas ajouter plus de 5 fichiers à une publication")
        
        return data
    
    def create(self, validated_data):
        media_files_ids = validated_data.pop('media_files', [])
        request = self.context.get('request')
        
        logger.info(f"Création post - Médias IDs: {media_files_ids}")
        
        # Créer le post
        validated_data['author'] = request.user
        validated_data['quartier'] = request.user.quartier
        
        # S'assurer que les champs optionnels ont des valeurs par défaut
        if 'title' not in validated_data:
            validated_data['title'] = ''
        if 'post_type' not in validated_data:
            validated_data['post_type'] = 'info'
        if 'is_anonymous' not in validated_data:
            validated_data['is_anonymous'] = False
            
        post = super().create(validated_data)
        
        # Associer les médias
        if media_files_ids:
            media_files = Media.objects.filter(
                id__in=media_files_ids,
                approval_status='approved',
                is_appropriate=True
            )
            logger.info(f"Médias trouvés: {media_files.count()}")
            logger.info(f"Médias IDs recherchés: {media_files_ids}")
            logger.info(f"Médias trouvés: {[m.id for m in media_files]}")
            
            post.media_files.set(media_files)
            logger.info(f"Médias associés au post {post.id}: {post.media_files.count()}")
        else:
            logger.info("Aucun média à associer")
        
        return post


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['content', 'is_anonymous', 'parent_comment']
        extra_kwargs = {
            'parent_comment': {'required': False, 'allow_null': True}
        }
    
    def validate(self, data):
        request = self.context.get('request')
        post = self.context.get('post')
        
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié")
        
        if not post:
            raise serializers.ValidationError("Post non trouvé")
        
        # Vérifier que le commentaire parent appartient bien au même post
        parent_comment = data.get('parent_comment')
        if parent_comment and parent_comment.post != post:
            raise serializers.ValidationError("Le commentaire parent doit appartenir au même post")
        
        # Vérifier que le niveau de profondeur ne dépasse pas 3
        if parent_comment:
            level = parent_comment.level + 1
            if level > 3:
                raise serializers.ValidationError("La profondeur maximale des réponses est de 3 niveaux")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        post = self.context.get('post')
        
        validated_data['author'] = request.user
        validated_data['post'] = post
        return super().create(validated_data) 


class PostShareSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les partages de posts"""
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = PostShare
        fields = ['id', 'user', 'post', 'share_type', 'comment', 'created_at', 'time_ago']
        read_only_fields = ['user', 'created_at']
    
    def get_time_ago(self, obj):
        """Retourne le temps écoulé depuis le partage"""
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


class PostShareCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer un partage"""
    
    class Meta:
        model = PostShare
        fields = ['share_type', 'comment']
    
    def validate(self, data):
        """Validation du partage"""
        user = self.context['request'].user
        post = self.context['post']
        
        # Vérifier si l'utilisateur a déjà partagé ce post
        if PostShare.objects.filter(user=user, post=post, share_type=data.get('share_type', 'share')).exists():
            raise serializers.ValidationError("Vous avez déjà partagé ce post")
        
        return data
    
    def create(self, validated_data):
        """Créer le partage"""
        user = self.context['request'].user
        post = self.context['post']
        
        return PostShare.objects.create(
            user=user,
            post=post,
            **validated_data
        ) 


class ExternalShareSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les partages externes"""
    user = UserSerializer(read_only=True)
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = ExternalShare
        fields = ['id', 'user', 'platform', 'platform_display', 'shared_at', 'time_ago']
        read_only_fields = ['user', 'shared_at']
    
    def get_time_ago(self, obj):
        """Retourne le temps écoulé depuis le partage"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.shared_at
        
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

class ExternalShareCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer un partage externe"""
    
    class Meta:
        model = ExternalShare
        fields = ['platform']
    
    def create(self, validated_data):
        user = self.context['request'].user
        post = self.context['post']
        
        # Créer le partage externe
        external_share = ExternalShare.objects.create(
            user=user,
            post=post,
            platform=validated_data['platform']
        )
        
        return external_share 


class PostAnalyticsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les analytics des posts"""
    post = PostSerializer(read_only=True)
    viral_score_formatted = serializers.SerializerMethodField()
    engagement_rate_formatted = serializers.SerializerMethodField()
    external_shares_breakdown = serializers.SerializerMethodField()
    
    class Meta:
        model = PostAnalytics
        fields = [
            'id', 'post', 'total_views', 'unique_views', 'total_likes', 
            'total_comments', 'total_shares', 'total_external_shares',
            'viral_score', 'viral_score_formatted', 'engagement_rate', 
            'engagement_rate_formatted', 'reach_multiplier',
            'whatsapp_shares', 'facebook_shares', 'twitter_shares', 
            'telegram_shares', 'email_shares', 'external_shares_breakdown',
            'created_at', 'updated_at'
        ]
    
    def get_viral_score_formatted(self, obj):
        """Retourne le score viral formaté"""
        if obj.viral_score >= 80:
            return f"{obj.viral_score:.1f}% 🔥 VIRAL"
        elif obj.viral_score >= 50:
            return f"{obj.viral_score:.1f}% ⚡ POPULAIRE"
        elif obj.viral_score >= 20:
            return f"{obj.viral_score:.1f}% 📈 ENGAGÉ"
        else:
            return f"{obj.viral_score:.1f}% 📊 NORMAL"
    
    def get_engagement_rate_formatted(self, obj):
        """Retourne le taux d'engagement formaté"""
        return f"{obj.engagement_rate:.1f}%"
    
    def get_external_shares_breakdown(self, obj):
        """Retourne la répartition des partages externes"""
        return {
            'whatsapp': obj.whatsapp_shares,
            'facebook': obj.facebook_shares,
            'twitter': obj.twitter_shares,
            'telegram': obj.telegram_shares,
            'email': obj.email_shares,
            'total': obj.total_external_shares
        }

class PostAnalyticsSummarySerializer(serializers.Serializer):
    """Sérialiseur pour le résumé des analytics"""
    total_posts = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    total_external_shares = serializers.IntegerField()
    average_viral_score = serializers.FloatField()
    average_engagement_rate = serializers.FloatField()
    top_performing_posts = PostAnalyticsSerializer(many=True)
    platform_breakdown = serializers.DictField()
    viral_posts_count = serializers.IntegerField()
    popular_posts_count = serializers.IntegerField() 
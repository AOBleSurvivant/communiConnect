import logging
import os
import requests
import io
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess
from datetime import timedelta
from PIL import Image, ImageOps
from django.core.cache import cache
from django.db.models import Q, Count
from .models import Post, PostLike, PostComment, Media

# Import conditionnel de Cloudinary
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

logger = logging.getLogger(__name__)

class ModerationService:
    """Service pour la modération automatique des médias"""
    
    @staticmethod
    def analyze_image_with_vision_api(image_file):
        """
        Analyse une image avec Google Cloud Vision API
        Retourne un score de modération et des détails
        """
        try:
            # Si pas de clé API, simulation
            if not settings.GOOGLE_CLOUD_VISION_API_KEY:
                return ModerationService._simulate_vision_analysis()
            
            # Préparer l'image pour l'API
            image_content = image_file.read()
            image_file.seek(0)  # Reset file pointer
            
            # Appel à l'API Google Cloud Vision
            url = f"https://vision.googleapis.com/v1/images:annotate?key={settings.GOOGLE_CLOUD_VISION_API_KEY}"
            
            request_data = {
                "requests": [
                    {
                        "image": {
                            "content": image_content.decode('latin-1')
                        },
                        "features": [
                            {
                                "type": "SAFE_SEARCH_DETECTION"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, json=request_data)
            
            if response.status_code == 200:
                result = response.json()
                return ModerationService._parse_vision_response(result)
            else:
                logger.error(f"Erreur API Vision: {response.status_code}")
                return ModerationService._simulate_vision_analysis()
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse Vision: {str(e)}")
            return ModerationService._simulate_vision_analysis()
    
    @staticmethod
    def _parse_vision_response(response):
        """Parse la réponse de l'API Vision"""
        try:
            safe_search = response['responses'][0]['safeSearchAnnotation']
            
            # Calculer un score global de modération
            scores = {
                'adult': safe_search.get('adult', 'UNKNOWN'),
                'violence': safe_search.get('violence', 'UNKNOWN'),
                'racy': safe_search.get('racy', 'UNKNOWN'),
                'medical': safe_search.get('medical', 'UNKNOWN'),
                'spoof': safe_search.get('spoof', 'UNKNOWN')
            }
            
            # Convertir en score numérique
            score_mapping = {
                'VERY_LIKELY': 0.9,
                'LIKELY': 0.7,
                'POSSIBLE': 0.5,
                'UNLIKELY': 0.3,
                'VERY_UNLIKELY': 0.1,
                'UNKNOWN': 0.5
            }
            
            moderation_score = sum(score_mapping.get(score, 0.5) for score in scores.values()) / len(scores)
            
            return {
                'moderation_score': moderation_score,
                'is_appropriate': moderation_score < 0.7,
                'moderation_details': scores
            }
            
        except Exception as e:
            logger.error(f"Erreur parsing réponse Vision: {str(e)}")
            return ModerationService._simulate_vision_analysis()
    
    @staticmethod
    def _simulate_vision_analysis():
        """Simulation d'analyse pour les tests"""
        return {
            'moderation_score': 0.2,  # Score bas = contenu approprié
            'is_appropriate': True,
            'moderation_details': {
                'adult': 'VERY_UNLIKELY',
                'violence': 'VERY_UNLIKELY',
                'racy': 'VERY_UNLIKELY',
                'medical': 'VERY_UNLIKELY',
                'spoof': 'VERY_UNLIKELY'
            }
        }

class VideoProcessingService:
    """Service pour le traitement des vidéos"""
    
    @staticmethod
    def get_video_duration(video_path):
        """Récupère la durée d'une vidéo avec FFmpeg"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 
                'format=duration', '-of', 'csv=p=0', video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                duration_seconds = float(result.stdout.strip())
                return timedelta(seconds=duration_seconds)
            else:
                logger.error(f"Erreur FFmpeg: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la durée: {str(e)}")
            return None
    
    @staticmethod
    def create_video_thumbnail(video_path, output_path, time_position='00:00:01'):
        """Crée une miniature pour une vidéo"""
        try:
            cmd = [
                'ffmpeg', '-i', video_path, '-ss', time_position,
                '-vframes', '1', '-q:v', '2', output_path, '-y'
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"Erreur création thumbnail: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de la miniature: {str(e)}")
            return False
    
    @staticmethod
    def validate_video_duration(video_path, max_duration=60):
        """Valide que la vidéo ne dépasse pas la durée maximale"""
        duration = VideoProcessingService.get_video_duration(video_path)
        
        if duration:
            duration_seconds = duration.total_seconds()
            return {
                'is_valid': duration_seconds <= max_duration,
                'duration': duration,
                'duration_seconds': duration_seconds,
                'max_duration': max_duration
            }
        
        return {
            'is_valid': False,
            'duration': None,
            'duration_seconds': 0,
            'max_duration': max_duration,
            'error': 'Impossible de lire la durée de la vidéo'
        }

class LiveStreamingService:
    """Service pour gérer le live streaming"""
    
    @staticmethod
    def generate_stream_key(user_id):
        """Générer une clé de stream unique"""
        import uuid
        return f"live_{user_id}_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def start_stream(stream_key):
        """Démarrer un stream (simulation)"""
        # En production, cela démarrerait un vrai stream RTMP
        return True
    
    @staticmethod
    def stop_stream(stream_key):
        """Arrêter un stream (simulation)"""
        # En production, cela arrêterait un vrai stream RTMP
        return True
    
    @staticmethod
    def get_rtmp_url(stream_key):
        """Obtenir l'URL RTMP"""
        return f"rtmp://localhost/live/{stream_key}"
    
    @staticmethod
    def get_hls_url(stream_key):
        """Obtenir l'URL HLS"""
        return f"http://localhost:8080/hls/{stream_key}.m3u8"

class MediaCompressionService:
    """Service pour la compression des médias"""
    
    @staticmethod
    def compress_image(image_file, max_width=1920, max_height=1080, quality=85):
        """Compresse une image"""
        try:
            # Ouvrir l'image
            img = Image.open(image_file)
            
            # Redimensionner si nécessaire
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Sauvegarder en JPEG
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            return ContentFile(output.getvalue(), name=image_file.name)
            
        except Exception as e:
            logger.error(f"Erreur compression image: {str(e)}")
            return image_file
    
    @staticmethod
    def compress_video(video_path, output_path, target_bitrate='1M'):
        """Compresse une vidéo"""
        try:
            cmd = [
                'ffmpeg', '-i', video_path, '-c:v', 'libx264',
                '-b:v', target_bitrate, '-c:a', 'aac', '-b:a', '128k',
                output_path, '-y'
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"Erreur compression vidéo: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la compression: {str(e)}")
            return False 

class MediaCDNService:
    """
    Service pour la gestion des médias avec CDN Cloudinary
    Optimisation automatique des images et vidéos
    """
    
    @staticmethod
    def upload_media_to_cdn(file, title, description, user):
        """
        Upload un média vers Cloudinary avec optimisation automatique
        """
        try:
            # Configuration Cloudinary
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
            )
            
            # Préparer les options d'upload
            upload_options = {
                'resource_type': 'auto',
                'folder': f'communiconnect/{user.id}',
                'public_id': f'{title}_{user.id}_{os.path.splitext(file.name)[0]}',
                'tags': ['communiconnect', 'media', f'user_{user.id}'],
                'context': {
                    'title': title,
                    'description': description,
                    'user': user.username
                }
            }
            
            # Optimisation selon le type de fichier
            if file.content_type.startswith('image/'):
                upload_options.update({
                    'transformation': [
                        {'quality': 'auto:good', 'fetch_format': 'auto'},
                        {'width': 1920, 'height': 1080, 'crop': 'limit'}
                    ]
                })
            elif file.content_type.startswith('video/'):
                upload_options.update({
                    'resource_type': 'video',
                    'transformation': [
                        {'quality': 'auto:good', 'fetch_format': 'auto'},
                        {'width': 1280, 'height': 720, 'crop': 'limit'}
                    ]
                })
            
            # Upload vers Cloudinary
            result = cloudinary.uploader.upload(file, **upload_options)
            
            logger.info(f"Média uploadé vers CDN: {result['public_id']}")
            
            return {
                'success': True,
                'url': result['secure_url'],
                'public_id': result['public_id'],
                'format': result.get('format'),
                'bytes': result.get('bytes'),
                'width': result.get('width'),
                'height': result.get('height'),
                'duration': result.get('duration')  # Pour les vidéos
            }
            
        except Exception as e:
            logger.error(f"Erreur upload CDN: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def optimize_image_for_cdn(image_file, max_width=1920, quality=85):
        """
        Optimise une image avant upload vers CDN
        """
        try:
            with Image.open(image_file) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionner si trop grande
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Sauvegarder optimisé
                optimized_path = f"optimized_{image_file.name}"
                img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
                
                return optimized_path
                
        except Exception as e:
            logger.error(f"Erreur optimisation image: {str(e)}")
            return image_file
    
    @staticmethod
    def get_cdn_url(public_id, transformation=None):
        """
        Génère une URL CDN avec transformations
        """
        try:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
            )
            
            if transformation:
                return cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)
            else:
                return cloudinary.CloudinaryImage(public_id).build_url()
                
        except Exception as e:
            logger.error(f"Erreur génération URL CDN: {str(e)}")
            return None
    
    @staticmethod
    def delete_from_cdn(public_id):
        """
        Supprime un média du CDN
        """
        try:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
            )
            
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Média supprimé du CDN: {public_id}")
            return result
            
        except Exception as e:
            logger.error(f"Erreur suppression CDN: {str(e)}")
            return None

class MediaOptimizationService:
    """
    Service d'optimisation des médias
    """
    
    @staticmethod
    def compress_image(image_file, max_width=1920, quality=85):
        """
        Compresse une image pour réduire sa taille
        """
        try:
            with Image.open(image_file) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionner si trop grande
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Sauvegarder compressé
                compressed_path = f"compressed_{image_file.name}"
                img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
                
                return compressed_path
                
        except Exception as e:
            logger.error(f"Erreur compression image: {str(e)}")
            return image_file
    
    @staticmethod
    def validate_video_duration(video_file, max_duration=60):
        """
        Valide la durée d'une vidéo
        """
        try:
            # Utiliser ffprobe pour obtenir la durée
            import subprocess
            
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 
                'format=duration', '-of', 'csv=p=0', video_file.name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
            
            return duration <= max_duration
            
        except Exception as e:
            logger.error(f"Erreur validation durée vidéo: {str(e)}")
            return False 

class AnalyticsService:
    """Service pour gérer les analytics"""
    
    @staticmethod
    def create_or_update_post_analytics(post):
        """Créer ou mettre à jour les analytics d'un post"""
        from .models import PostAnalytics
        
        analytics, created = PostAnalytics.objects.get_or_create(
            post=post,
            defaults={
                'total_views': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0
            }
        )
        
        # Mettre à jour les compteurs
        analytics.total_views = post.views_count
        analytics.total_likes = post.likes.count()
        analytics.total_comments = post.comments.count()
        analytics.total_shares = post.shares.count()
        analytics.save()
        
        return analytics
    
    @staticmethod
    def get_user_analytics_summary(user, days=30):
        """Récupère le résumé des analytics d'un utilisateur"""
        from django.utils import timezone
        from datetime import timedelta
        from .models import PostAnalytics
        
        # Période
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Posts de l'utilisateur dans la période
        user_posts = user.posts.filter(created_at__range=(start_date, end_date))
        analytics = PostAnalytics.objects.filter(post__in=user_posts)
        
        if not analytics.exists():
            return {
                'total_posts': 0,
                'total_views': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'total_external_shares': 0,
                'average_viral_score': 0.0,
                'average_engagement_rate': 0.0,
                'top_performing_posts': [],
                'platform_breakdown': {},
                'viral_posts_count': 0,
                'popular_posts_count': 0
            }
        
        # Calculs
        total_posts = analytics.count()
        total_views = sum(a.total_views for a in analytics)
        total_likes = sum(a.total_likes for a in analytics)
        total_comments = sum(a.total_comments for a in analytics)
        total_shares = sum(a.total_shares for a in analytics)
        total_external_shares = sum(a.total_external_shares for a in analytics)
        
        average_viral_score = sum(a.viral_score for a in analytics) / total_posts
        average_engagement_rate = sum(a.engagement_rate for a in analytics) / total_posts
        
        # Posts performants
        top_performing_posts = analytics.order_by('-viral_score')[:5]
        
        # Répartition des plateformes
        platform_breakdown = {
            'whatsapp': sum(a.whatsapp_shares for a in analytics),
            'facebook': sum(a.facebook_shares for a in analytics),
            'twitter': sum(a.twitter_shares for a in analytics),
            'telegram': sum(a.telegram_shares for a in analytics),
            'email': sum(a.email_shares for a in analytics)
        }
        
        # Posts viraux et populaires
        viral_posts_count = analytics.filter(viral_score__gte=80).count()
        popular_posts_count = analytics.filter(viral_score__gte=50).count()
        
        return {
            'total_posts': total_posts,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_external_shares': total_external_shares,
            'average_viral_score': round(average_viral_score, 1),
            'average_engagement_rate': round(average_engagement_rate, 1),
            'top_performing_posts': top_performing_posts,
            'platform_breakdown': platform_breakdown,
            'viral_posts_count': viral_posts_count,
            'popular_posts_count': popular_posts_count
        }
    
    @staticmethod
    def get_community_analytics(quartier, days=30):
        """Récupère les analytics de la communauté"""
        from django.utils import timezone
        from datetime import timedelta
        from .models import PostAnalytics
        
        # Période
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Posts de la communauté dans la période
        community_posts = Post.objects.filter(
            quartier=quartier,
            created_at__range=(start_date, end_date)
        )
        analytics = PostAnalytics.objects.filter(post__in=community_posts)
        
        if not analytics.exists():
            return {
                'total_posts': 0,
                'total_views': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'total_external_shares': 0,
                'average_viral_score': 0.0,
                'average_engagement_rate': 0.0,
                'top_performing_posts': [],
                'platform_breakdown': {},
                'viral_posts_count': 0,
                'popular_posts_count': 0,
                'most_active_users': []
            }
        
        # Calculs similaires à get_user_analytics_summary
        total_posts = analytics.count()
        total_views = sum(a.total_views for a in analytics)
        total_likes = sum(a.total_likes for a in analytics)
        total_comments = sum(a.total_comments for a in analytics)
        total_shares = sum(a.total_shares for a in analytics)
        total_external_shares = sum(a.total_external_shares for a in analytics)
        
        average_viral_score = sum(a.viral_score for a in analytics) / total_posts
        average_engagement_rate = sum(a.engagement_rate for a in analytics) / total_posts
        
        # Posts performants
        top_performing_posts = analytics.order_by('-viral_score')[:10]
        
        # Répartition des plateformes
        platform_breakdown = {
            'whatsapp': sum(a.whatsapp_shares for a in analytics),
            'facebook': sum(a.facebook_shares for a in analytics),
            'twitter': sum(a.twitter_shares for a in analytics),
            'telegram': sum(a.telegram_shares for a in analytics),
            'email': sum(a.email_shares for a in analytics)
        }
        
        # Posts viraux et populaires
        viral_posts_count = analytics.filter(viral_score__gte=80).count()
        popular_posts_count = analytics.filter(viral_score__gte=50).count()
        
        # Utilisateurs les plus actifs
        from django.db.models import Count
        most_active_users = Post.objects.filter(
            quartier=quartier,
            created_at__range=(start_date, end_date)
        ).values('user__username', 'user__first_name', 'user__last_name').annotate(
            post_count=Count('id')
        ).order_by('-post_count')[:5]
        
        return {
            'total_posts': total_posts,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_external_shares': total_external_shares,
            'average_viral_score': round(average_viral_score, 1),
            'average_engagement_rate': round(average_engagement_rate, 1),
            'top_performing_posts': top_performing_posts,
            'platform_breakdown': platform_breakdown,
            'viral_posts_count': viral_posts_count,
            'popular_posts_count': popular_posts_count,
            'most_active_users': most_active_users
        } 

class CacheService:
    """Service pour gérer le cache des posts et médias"""
    
    @staticmethod
    def get_posts_cache_key(user_id, quartier_id=None, filters=None):
        """Génère une clé de cache unique pour les posts"""
        key_parts = [f"posts_list_{user_id}"]
        if quartier_id:
            key_parts.append(f"quartier_{quartier_id}")
        if filters:
            key_parts.append(f"filters_{hash(str(filters))}")
        return "_".join(key_parts)
    
    @staticmethod
    def get_post_detail_cache_key(post_id):
        """Génère une clé de cache pour les détails d'un post"""
        return f"post_detail_{post_id}"
    
    @staticmethod
    def invalidate_user_posts_cache(user_id, quartier_id=None):
        """Invalide le cache des posts d'un utilisateur"""
        cache_key = CacheService.get_posts_cache_key(user_id, quartier_id)
        cache.delete(cache_key)
        logger.info(f"Cache invalidé pour l'utilisateur {user_id}")
    
    @staticmethod
    def invalidate_post_cache(post_id):
        """Invalide le cache d'un post spécifique"""
        cache_key = CacheService.get_post_detail_cache_key(post_id)
        cache.delete(cache_key)
        logger.info(f"Cache invalidé pour le post {post_id}")
    
    @staticmethod
    def get_cached_posts(user, filters=None):
        """Récupère les posts depuis le cache ou la base de données"""
        cache_key = CacheService.get_posts_cache_key(
            user.id, 
            user.quartier.id if user.quartier else None,
            filters
        )
        
        # Essayer de récupérer depuis le cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f"Posts récupérés depuis le cache pour l'utilisateur {user.id}")
            return cached_data
        
        # Si pas en cache, récupérer depuis la base de données
        queryset = Post.objects.filter(
            quartier__commune=user.quartier.commune
        ).select_related(
            'author', 
            'quartier', 
            'quartier__commune'
        ).prefetch_related(
            'comments__author',
            'likes__user',
            'media_files'
        ).annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments', filter=Q(comments__parent_comment__isnull=True)),
            shares_count=Count('shares')
        ).order_by('-created_at')
        
        # Appliquer les filtres
        if filters:
            if filters.get('post_type'):
                queryset = queryset.filter(post_type=filters['post_type'])
        
        # Mettre en cache pour 5 minutes
        cache.set(cache_key, queryset, 300)
        logger.info(f"Posts mis en cache pour l'utilisateur {user.id}")
        
        return queryset
    
    @staticmethod
    def get_cached_post_detail(post_id):
        """Récupère les détails d'un post depuis le cache"""
        cache_key = CacheService.get_post_detail_cache_key(post_id)
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        
        return None


class PerformanceOptimizer:
    """Service pour optimiser les performances des requêtes"""
    
    @staticmethod
    def optimize_post_queryset(queryset):
        """Optimise un queryset de posts avec les bonnes relations"""
        return queryset.select_related(
            'author', 
            'quartier', 
            'quartier__commune'
        ).prefetch_related(
            'comments__author',
            'likes__user',
            'media_files'
        ).annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments', filter=Q(comments__parent_comment__isnull=True)),
            shares_count=Count('shares')
        )
    
    @staticmethod
    def batch_update_post_counts():
        """Met à jour en lot les compteurs des posts"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Mettre à jour les compteurs de likes
            cursor.execute("""
                UPDATE posts_post 
                SET likes_count = (
                    SELECT COUNT(*) 
                    FROM posts_postlike 
                    WHERE posts_postlike.post_id = posts_post.id
                )
            """)
            
            # Mettre à jour les compteurs de commentaires
            cursor.execute("""
                UPDATE posts_post 
                SET comments_count = (
                    SELECT COUNT(*) 
                    FROM posts_postcomment 
                    WHERE posts_postcomment.post_id = posts_post.id 
                    AND posts_postcomment.parent_comment_id IS NULL
                )
            """)
            
            # Mettre à jour les compteurs de partages
            cursor.execute("""
                UPDATE posts_post 
                SET shares_count = (
                    SELECT COUNT(*) 
                    FROM posts_postshare 
                    WHERE posts_postshare.post_id = posts_post.id
                )
            """)
        
        logger.info("Compteurs des posts mis à jour en lot")


class DatabaseOptimizer:
    """Service pour optimiser la base de données"""
    
    @staticmethod
    def create_database_indexes():
        """Crée les index nécessaires pour optimiser les requêtes"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Index pour les posts
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posts_author_created 
                ON posts_post(author_id, created_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posts_quartier_created 
                ON posts_post(quartier_id, created_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posts_type_created 
                ON posts_post(post_type, created_at DESC)
            """)
            
            # Index pour les likes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_postlike_post_user 
                ON posts_postlike(post_id, user_id)
            """)
            
            # Index pour les commentaires
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_postcomment_post_created 
                ON posts_postcomment(post_id, created_at DESC)
            """)
            
            # Index pour les médias
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_media_user_created 
                ON posts_media(user_id, created_at DESC)
            """)
        
        logger.info("Index de base de données créés") 


class AdvancedMediaOptimizationService:
    """Service avancé pour l'optimisation des médias"""
    
    @staticmethod
    def optimize_image(image_file, max_width=None, max_height=None, quality=None):
        """Optimise une image avec compression intelligente"""
        try:
            # Ouvrir l'image
            with Image.open(image_file) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionner si nécessaire
                if max_width or max_height:
                    img = AdvancedMediaOptimizationService._resize_image(
                        img, max_width, max_height
                    )
                
                # Optimiser la qualité
                if quality is None:
                    quality = settings.MEDIA_OPTIMIZATION.get('image_quality', 85)
                
                # Créer un buffer temporaire
                output_buffer = io.BytesIO()
                
                # Sauvegarder avec optimisation
                img.save(
                    output_buffer, 
                    format='JPEG', 
                    quality=quality, 
                    optimize=True,
                    progressive=True
                )
                
                output_buffer.seek(0)
                
                # Calculer la réduction de taille
                original_size = image_file.size
                optimized_size = output_buffer.tell()
                reduction = ((original_size - optimized_size) / original_size) * 100
                
                logger.info(f"Image optimisée: {reduction:.1f}% de réduction")
                
                return output_buffer, reduction
                
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation d'image: {str(e)}")
            return None, 0
    
    @staticmethod
    def _resize_image(img, max_width, max_height):
        """Redimensionne une image en conservant les proportions"""
        if max_width is None:
            max_width = settings.MEDIA_OPTIMIZATION.get('max_width', 1920)
        if max_height is None:
            max_height = settings.MEDIA_OPTIMIZATION.get('max_height', 1080)
        
        # Calculer les nouvelles dimensions
        width, height = img.size
        ratio = min(max_width / width, max_height / height)
        
        if ratio < 1:
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        return img
    
    @staticmethod
    def create_thumbnails(image_file, sizes=None):
        """Crée des miniatures de différentes tailles"""
        if sizes is None:
            sizes = settings.MEDIA_OPTIMIZATION.get('thumbnail_sizes', [150, 300, 600])
        
        thumbnails = {}
        
        try:
            with Image.open(image_file) as img:
                for size in sizes:
                    # Créer une copie pour la miniature
                    thumb = img.copy()
                    
                    # Redimensionner en conservant les proportions
                    thumb.thumbnail((size, size), Image.LANCZOS)
                    
                    # Sauvegarder la miniature
                    thumb_buffer = io.BytesIO()
                    thumb.save(thumb_buffer, format='JPEG', quality=85, optimize=True)
                    thumb_buffer.seek(0)
                    
                    thumbnails[f"thumb_{size}"] = thumb_buffer
                    
        except Exception as e:
            logger.error(f"Erreur lors de la création des miniatures: {str(e)}")
        
        return thumbnails
    
    @staticmethod
    def convert_to_webp(image_file):
        """Convertit une image en format WebP pour une meilleure compression"""
        try:
            with Image.open(image_file) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Créer le buffer WebP
                webp_buffer = io.BytesIO()
                img.save(webp_buffer, format='WEBP', quality=85, method=6)
                webp_buffer.seek(0)
                
                return webp_buffer
                
        except Exception as e:
            logger.error(f"Erreur lors de la conversion WebP: {str(e)}")
            return None
    
    @staticmethod
    def optimize_video(video_file, max_duration=60, max_size_mb=50):
        """Optimise une vidéo avec compression"""
        try:
            # Vérifier la durée
            duration = AdvancedMediaOptimizationService._get_video_duration(video_file)
            if duration > max_duration:
                logger.warning(f"Vidéo trop longue: {duration}s > {max_duration}s")
                return None, "Vidéo trop longue"
            
            # Vérifier la taille
            file_size = video_file.size / (1024 * 1024)  # MB
            if file_size > max_size_mb:
                logger.warning(f"Vidéo trop volumineuse: {file_size:.1f}MB > {max_size_mb}MB")
                return None, "Vidéo trop volumineuse"
            
            # Pour l'instant, on retourne le fichier original
            # En production, on utiliserait FFmpeg pour la compression
            return video_file, "OK"
            
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation vidéo: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def _get_video_duration(video_file):
        """Récupère la durée d'une vidéo"""
        try:
            # Utiliser FFmpeg pour obtenir la durée
            cmd = [
                'ffprobe', 
                '-v', 'quiet', 
                '-show_entries', 'format=duration', 
                '-of', 'csv=p=0', 
                video_file.temporary_file_path()
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la durée: {str(e)}")
            return 0


class ResponseOptimizationService:
    """Service pour optimiser les réponses API"""
    
    @staticmethod
    def optimize_json_response(data, max_items=None):
        """Optimise une réponse JSON"""
        if max_items and isinstance(data, list):
            data = data[:max_items]
        
        return data
    
    @staticmethod
    def add_performance_headers(response, processing_time):
        """Ajoute des en-têtes de performance à la réponse"""
        response['X-Processing-Time'] = f"{processing_time:.3f}s"
        response['X-Cache-Status'] = 'MISS'  # ou HIT si depuis le cache
        
        return response
    
    @staticmethod
    def compress_response(response, min_size=800):
        """Compresse une réponse si elle dépasse la taille minimale"""
        if hasattr(response, 'content'):
            content_size = len(response.content)
            if content_size > min_size:
                # La compression est gérée par le middleware GZip
                response['Content-Encoding'] = 'gzip'
                logger.info(f"Réponse compressée: {content_size} bytes")
        
        return response


class DatabaseQueryOptimizer:
    """Service pour optimiser les requêtes de base de données"""
    
    @staticmethod
    def optimize_post_queryset(queryset, include_related=True):
        """Optimise un queryset de posts"""
        if include_related:
            queryset = queryset.select_related(
                'author', 
                'quartier', 
                'quartier__commune'
            ).prefetch_related(
                'media_files',
                'comments__author',
                'likes__user'
            )
        
        # Ajouter les annotations pour les compteurs
        queryset = queryset.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments', filter=Q(comments__parent_comment__isnull=True)),
            shares_count=Count('shares')
        )
        
        return queryset
    
    @staticmethod
    def optimize_user_queryset(queryset):
        """Optimise un queryset d'utilisateurs"""
        return queryset.select_related(
            'quartier',
            'quartier__commune'
        ).prefetch_related(
            'posts',
            'friends'
        )
    
    @staticmethod
    def batch_update_counters():
        """Met à jour en lot tous les compteurs"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Mettre à jour les compteurs de posts
            cursor.execute("""
                UPDATE posts_post 
                SET likes_count = (
                    SELECT COUNT(*) 
                    FROM posts_postlike 
                    WHERE posts_postlike.post_id = posts_post.id
                ),
                comments_count = (
                    SELECT COUNT(*) 
                    FROM posts_postcomment 
                    WHERE posts_postcomment.post_id = posts_post.id 
                    AND posts_postcomment.parent_comment_id IS NULL
                ),
                shares_count = (
                    SELECT COUNT(*) 
                    FROM posts_postshare 
                    WHERE posts_postshare.post_id = posts_post.id
                )
            """)
        
        logger.info("Compteurs mis à jour en lot")


class CacheOptimizationService:
    """Service pour optimiser l'utilisation du cache"""
    
    @staticmethod
    def warm_cache_for_user(user_id, quartier_id):
        """Préchauffe le cache pour un utilisateur"""
        try:
            # Précharger les posts du quartier
            from posts.models import Post
            posts = Post.objects.filter(
                quartier__commune__quartiers__id=quartier_id
            ).select_related(
                'author', 'quartier'
            )[:50]  # Limiter à 50 posts
            
            # Mettre en cache
            cache_key = f"posts_list_{user_id}_{quartier_id}"
            cache.set(cache_key, list(posts), 300)
            
            logger.info(f"Cache préchauffé pour l'utilisateur {user_id}")
            
        except Exception as e:
            logger.error(f"Erreur lors du préchauffage: {str(e)}")
    
    @staticmethod
    def invalidate_related_caches(post_id, user_id, quartier_id):
        """Invalide tous les caches liés à un post"""
        cache_keys_to_delete = [
            f"post_detail_{post_id}",
            f"posts_list_{user_id}_{quartier_id}",
            f"user_posts_{user_id}",
            f"analytics_posts_{quartier_id}"
        ]
        
        for key in cache_keys_to_delete:
            cache.delete(key)
        
        logger.info(f"Caches invalidés pour le post {post_id}")
    
    @staticmethod
    def get_cache_statistics():
        """Récupère les statistiques du cache"""
        try:
            # Statistiques basiques (Redis nécessaire pour plus de détails)
            return {
                'cache_backend': settings.CACHES['default']['BACKEND'],
                'cache_timeout': settings.CACHE_TIMEOUTS,
                'cache_enabled': True
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {str(e)}")
            return {'cache_enabled': False} 

import os
import logging
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.conf import settings

logger = logging.getLogger(__name__)

class ImageCompressionService:
    """Service pour la compression automatique des images"""
    
    @staticmethod
    def compress_image(image_file, max_width=1920, max_height=1080, quality=85):
        """
        Compresse une image en conservant ses proportions
        
        Args:
            image_file: Fichier image à compresser
            max_width: Largeur maximale (défaut: 1920)
            max_height: Hauteur maximale (défaut: 1080)
            quality: Qualité JPEG (défaut: 85)
        
        Returns:
            BytesIO: Image compressée en mémoire
        """
        try:
            # Ouvrir l'image avec PIL
            img = Image.open(image_file)
            
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Redimensionner si nécessaire
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Compresser l'image
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            logger.info(f"Image compressée: {image_file.name} -> {len(output.getvalue())} bytes")
            return output
            
        except Exception as e:
            logger.error(f"Erreur lors de la compression de l'image {image_file.name}: {str(e)}")
            return None
    
    @staticmethod
    def create_thumbnail(image_file, size=(300, 300)):
        """
        Crée une miniature d'une image
        
        Args:
            image_file: Fichier image source
            size: Taille de la miniature (largeur, hauteur)
        
        Returns:
            BytesIO: Miniature en mémoire
        """
        try:
            img = Image.open(image_file)
            
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Créer la miniature
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la miniature: {str(e)}")
            return None 
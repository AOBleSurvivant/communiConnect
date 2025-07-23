import logging
import os
import subprocess
from datetime import timedelta
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Prefetch
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import time
from .models import Post, PostLike, PostComment, Media, PostShare, PostAnalytics, ExternalShare, LiveChatMessage
from .serializers import (
    PostSerializer, PostCreateSerializer, PostCommentSerializer,
    PostCommentCreateSerializer, PostLikeSerializer,
    MediaSerializer, MediaCreateSerializer, PostShareCreateSerializer, PostShareSerializer,
    ExternalShareSerializer, ExternalShareCreateSerializer,
    PostAnalyticsSerializer, PostAnalyticsSummarySerializer
)
from .services import ModerationService, VideoProcessingService, LiveStreamingService, MediaCDNService

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        summary="Uploader un média",
        description="""
        Upload un fichier média (image ou vidéo) avec :
        - Validation automatique du type et de la taille
        - Modération automatique avec Google Cloud Vision
        - Optimisation et compression automatique
        - Upload vers CDN Cloudinary si configuré
        
        **Types de fichiers supportés :**
        - Images : JPEG, PNG, GIF, WebP (max 10MB)
        - Vidéos : MP4, WebM, QuickTime, AVI (max 50MB, 60s)
        """,
        tags=['media'],
        examples=[
            OpenApiExample(
                'Upload image',
                value={
                    'file': 'image.jpg',
                    'title': 'Mon image',
                    'description': 'Description de l\'image'
                },
                request_only=True
            ),
            OpenApiExample(
                'Upload vidéo',
                value={
                    'file': 'video.mp4',
                    'title': 'Ma vidéo',
                    'description': 'Description de la vidéo'
                },
                request_only=True
            )
        ]
    )
)
class MediaUploadView(generics.CreateAPIView):
    """Vue pour uploader des médias avec modération automatique"""
    serializer_class = MediaCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'media'  # Rate limiting spécifique
    
    def perform_create(self, serializer):
        media = serializer.save()
        
        # Upload vers CDN si configuré
        if settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
            self.upload_to_cdn(media)
        
        # Analyser le contenu pour la modération
        self.analyze_content(media)
        
        # Si c'est une vidéo, vérifier la durée
        if media.media_type == 'video':
            self.check_video_duration(media)
    
    def analyze_content(self, media):
        """Analyse le contenu pour la modération"""
        try:
            if media.media_type == 'image':
                # Analyser l'image avec Google Cloud Vision
                analysis_result = ModerationService.analyze_image_with_vision_api(media.file)
                
                media.moderation_score = analysis_result['moderation_score']
                media.is_appropriate = analysis_result['is_appropriate']
                media.moderation_details = analysis_result['moderation_details']
                
                if media.is_appropriate:
                    media.approval_status = 'approved'
                else:
                    media.approval_status = 'rejected'
                    logger.warning(f"Contenu inapproprié détecté pour le média {media.id}")
                
            elif media.media_type == 'video':
                # Pour les vidéos, on simule l'analyse pour l'instant
                # Dans un vrai projet, vous utiliseriez une API de modération vidéo
                media.moderation_score = 0.2
                media.is_appropriate = True
                media.approval_status = 'approved'
            
            media.save()
            logger.info(f"Contenu analysé pour le média {media.id}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du contenu: {str(e)}")
            # En cas d'erreur, marquer comme en attente
            media.approval_status = 'pending'
            media.save()
    
    def check_video_duration(self, media):
        """Vérifie la durée de la vidéo"""
        try:
            file_path = media.file.path
            validation_result = VideoProcessingService.validate_video_duration(file_path, max_duration=60)
            
            if validation_result['is_valid']:
                media.duration = validation_result['duration']
                logger.info(f"Durée vidéo validée: {validation_result['duration_seconds']}s")
            else:
                media.approval_status = 'rejected'
                media.moderation_details = {
                    'reason': 'Vidéo trop longue',
                    'duration_seconds': validation_result['duration_seconds'],
                    'max_duration': validation_result['max_duration']
                }
                logger.warning(f"Vidéo rejetée: durée {validation_result['duration_seconds']}s > 60s")
            
            media.save()
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de la durée: {str(e)}")
    
    def upload_to_cdn(self, media):
        """Upload le média vers le CDN Cloudinary"""
        try:
            if not settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
                logger.warning("Cloudinary non disponible, upload CDN ignoré")
                return
            
            # Upload vers CDN
            cdn_result = MediaCDNService.upload_media_to_cdn(
                file=media.file,
                title=media.title,
                description=media.description,
                user=media.user
            )
            
            if cdn_result['success']:
                # Mettre à jour le média avec l'URL CDN
                media.cdn_url = cdn_result['url']
                media.cdn_public_id = cdn_result['public_id']
                media.file_size = cdn_result.get('bytes', 0)
                media.width = cdn_result.get('width')
                media.height = cdn_result.get('height')
                media.duration = cdn_result.get('duration')
                media.save()
                
                logger.info(f"Média {media.id} uploadé vers CDN: {cdn_result['url']}")
            else:
                logger.error(f"Erreur upload CDN pour média {media.id}: {cdn_result.get('error')}")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'upload CDN: {str(e)}")


class MediaListView(generics.ListAPIView):
    """Vue pour lister les médias de l'utilisateur"""
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Media.objects.filter(
            approval_status='approved',
            is_appropriate=True
        ).order_by('-created_at')


class MediaDetailView(generics.RetrieveAPIView):
    """Vue pour afficher un média spécifique"""
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Media.objects.all()


class LiveStreamView(generics.GenericAPIView):
    """Vue pour gérer les lives"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MediaSerializer
    
    def post(self, request):
        """Démarrer un live"""
        try:
            logger.info(f"Tentative de démarrage live pour {request.user.username}")
            
            # Vérifier que l'utilisateur a un quartier assigné
            if not request.user.quartier:
                logger.warning(f"Utilisateur {request.user.username} sans quartier")
                return Response(
                    {'error': 'Vous devez être assigné à un quartier pour démarrer un live'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Récupérer les données du live
            content = request.data.get('content', 'Live en cours')
            title = request.data.get('title', 'Live streaming')
            description = request.data.get('description', '')
            
            logger.info(f"Données live: content='{content}', title='{title}'")
            
            # Générer une clé de stream unique
            stream_key = LiveStreamingService.generate_stream_key(request.user.id)
            logger.info(f"Clé de stream générée: {stream_key}")
            
            # Créer un post live avec type 'info' au lieu de 'live'
            post = Post.objects.create(
                author=request.user,  # Utiliser 'author' au lieu de 'user'
                quartier=request.user.quartier,
                content=content,
                post_type='info',  # Utiliser 'info' au lieu de 'live'
                is_live_post=True
            )
            
            logger.info(f"Post live créé avec ID: {post.id}")
            
            # Démarrer le stream (simulation)
            LiveStreamingService.start_stream(stream_key)
            logger.info(f"Stream démarré pour la clé: {stream_key}")
            
            # Préparer la réponse
            response_data = {
                'live_id': post.id,
                'stream_key': stream_key,
                'post_id': post.id,
                'rtmp_url': LiveStreamingService.get_rtmp_url(stream_key),
                'hls_url': LiveStreamingService.get_hls_url(stream_key),
                'message': 'Live démarré avec succès'
            }
            
            logger.info(f"Live démarré avec succès: {response_data}")
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du live: {str(e)}")
            logger.error(f"Type d'erreur: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            return Response(
                {
                    'error': 'Erreur lors du démarrage du live. Veuillez réessayer.',
                    'details': str(e) if settings.DEBUG else None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, live_id):
        """Arrêter un live"""
        try:
            logger.info(f"Tentative d'arrêt du live {live_id}")
            
            # Chercher le post live
            try:
                post = Post.objects.get(id=live_id, is_live_post=True)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Live non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Arrêter le stream
            stream_key = f"live_{post.author.id}_"  # Utiliser author au lieu de user
            LiveStreamingService.stop_stream(stream_key)
            
            # Récupérer les données de la vidéo enregistrée
            video_data = request.data.get('video_data', {})
            video_url = video_data.get('url')
            video_duration = video_data.get('duration', 0)
            video_size = video_data.get('size', 0)
            
            # Si une vidéo a été enregistrée, la sauvegarder
            media = None
            if video_url:
                logger.info(f"Sauvegarde de la vidéo enregistrée pour le live {live_id}")
                
                try:
                    # Convertir la durée en secondes en timedelta
                    # S'assurer que video_duration est un nombre
                    if isinstance(video_duration, (int, float)):
                        duration_timedelta = timedelta(seconds=int(video_duration))
                    else:
                        # Valeur par défaut si la durée n'est pas valide
                        duration_timedelta = timedelta(seconds=1)
                        logger.warning(f"Durée vidéo invalide: {video_duration}, utilisation de la valeur par défaut")
                    
                    # Si c'est une URL blob, on va la convertir en fichier
                    if video_url.startswith('blob:'):
                        logger.info("Conversion de l'URL blob en fichier...")
                        
                        # Créer un nom de fichier unique
                        import uuid
                        import base64
                        from django.core.files.base import ContentFile
                        
                        # Extraire les données base64 de l'URL blob
                        # Note: En production, il faudrait recevoir les données directement
                        video_filename = f"live_video_{live_id}_{uuid.uuid4().hex[:8]}.webm"
                        
                        # Créer un objet Media avec un fichier temporaire
                        media = Media.objects.create(
                            title=f"Vidéo du live - {post.content}",
                            description=f"Vidéo enregistrée du live '{post.content}'",
                            media_type='video',
                            file_size=video_size,
                            duration=duration_timedelta,
                            is_live_recording=True,
                            live_post=post
                        )
                        
                        # Pour l'instant, on sauvegarde l'URL blob comme cdn_url
                        # En production, on ferait un vrai upload de fichier
                        media.cdn_url = video_url
                        media.save()
                        
                        logger.info(f"Vidéo sauvegardée avec ID: {media.id} (URL blob temporaire)")
                    else:
                        # Si c'est déjà une URL permanente
                        media = Media.objects.create(
                            title=f"Vidéo du live - {post.content}",
                            description=f"Vidéo enregistrée du live '{post.content}'",
                            media_type='video',
                            cdn_url=video_url,
                            file_size=video_size,
                            duration=duration_timedelta,
                            is_live_recording=True,
                            live_post=post
                        )
                        logger.info(f"Vidéo sauvegardée avec ID: {media.id}")
                    
                    # Associer la vidéo au post
                    post.media_files.add(media)
                    
                    # Mettre à jour le contenu du post
                    post.content = f"{post.content}\n\n📹 Vidéo enregistrée disponible"
                    
                except Exception as video_error:
                    logger.error(f"Erreur lors de la sauvegarde de la vidéo: {str(video_error)}")
                    # Continuer sans la vidéo plutôt que d'échouer complètement
            
            # Marquer le post comme non-live
            post.is_live_post = False
            post.save()
            
            # Invalider le cache des posts pour que la vidéo apparaisse immédiatement
            from django.core.cache import cache
            user = request.user
            cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
            cache.delete(cache_key)
            
            logger.info(f"Live {live_id} arrêté avec succès")
            return Response({
                'message': 'Live arrêté',
                'video_saved': bool(video_url),
                'video_id': media.id if media else None
            })
            
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du live: {str(e)}")
            return Response(
                {'error': 'Erreur lors de l\'arrêt du live'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Lister les posts",
        description="""
        Récupère la liste des posts avec :
        - Pagination automatique (20 posts par page)
        - Filtrage par quartier de l'utilisateur
        - Tri par date de création (plus récent en premier)
        - Inclut les médias, likes et commentaires
        """,
        tags=['posts'],
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Numéro de page'
            ),
            OpenApiParameter(
                name='post_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrer par type de post (info, event, help, etc.)'
            )
        ]
    ),
    post=extend_schema(
        summary="Créer un post",
        description="""
        Crée un nouveau post avec :
        - Contenu texte obligatoire ou médias
        - Support des médias multiples (max 5)
        - Types de posts : info, event, help, announcement, discussion
        - Option anonyme disponible
        """,
        tags=['posts'],
        examples=[
            OpenApiExample(
                'Post simple',
                value={
                    'content': 'Mon premier post sur CommuniConnect !',
                    'post_type': 'info',
                    'is_anonymous': False
                },
                request_only=True
            ),
            OpenApiExample(
                'Post avec médias',
                value={
                    'content': 'Post avec image et vidéo',
                    'post_type': 'event',
                    'media_files': [1, 2, 3],
                    'is_anonymous': False
                },
                request_only=True
            )
        ]
    )
)
@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache 5 minutes
class PostListView(generics.ListCreateAPIView):
    """Vue pour lister et créer des posts"""
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'posts'  # Rate limiting spécifique
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    
    def get_queryset(self):
        try:
            user = self.request.user
            
            # Clé de cache unique par utilisateur et paramètres
            cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
            
            # Essayer de récupérer depuis le cache
            cached_queryset = cache.get(cache_key)
            if cached_queryset is not None:
                return cached_queryset
            
            # Vérifier si l'utilisateur a un quartier
            if not user.quartier:
                # Si pas de quartier, retourner tous les posts
                queryset = Post.objects.all()
            else:
                # Requête optimisée avec prefetch intelligent
                queryset = Post.objects.filter(
                    quartier__commune=user.quartier.commune
                )
            
            # Appliquer les optimisations communes avec gestion d'erreur
            queryset = queryset.select_related(
                'author', 
                'quartier', 
                'quartier__commune'
            ).prefetch_related(
                Prefetch(
                    'comments',
                    queryset=PostComment.objects.select_related('author').filter(
                        parent_comment__isnull=True
                    ).order_by('-created_at')[:10],  # Limiter à 10 commentaires récents
                    to_attr='recent_comments'
                ),
                Prefetch(
                    'likes',
                    queryset=PostLike.objects.select_related('user').order_by('-created_at')[:20],
                    to_attr='recent_likes'
                ),
                'media_files'
            ).annotate(
                likes_count_annotated=Count('likes'),
                comments_count_annotated=Count('comments', filter=Q(comments__parent_comment__isnull=True)),
                shares_count_annotated=Count('shares')
            ).order_by('-created_at')
            
            # Mettre en cache pour 5 minutes
            cache.set(cache_key, queryset, 300)
            
            return queryset
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du queryset: {str(e)}")
            # Fallback vers une requête simple en cas d'erreur
            return Post.objects.select_related('author', 'quartier').order_by('-created_at')[:20]
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # Filtres
            post_type = request.GET.get('type')
            if post_type:
                if post_type == 'live':
                    # Pour les lives, filtrer par is_live_post=True
                    queryset = queryset.filter(is_live_post=True)
                else:
                    # Pour les autres types, filtrer par post_type
                    queryset = queryset.filter(post_type=post_type)
            
            # Tri
            sort_by = request.GET.get('sort', '-created_at')
            if sort_by in ['created_at', '-created_at', 'likes_count', '-likes_count']:
                queryset = queryset.order_by(sort_by)
            
            # Pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des posts: {str(e)}")
            return Response(
                {'error': 'Erreur lors du chargement des posts', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def perform_create(self, serializer):
        try:
            logger.info(f"Tentative de création de post par l'utilisateur {self.request.user.username}")
            post = serializer.save()
            
            # Invalider le cache des posts
            user = self.request.user
            cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
            cache.delete(cache_key)
            
            logger.info(f"Post créé avec succès: {post.id}")
            return post
        except Exception as e:
            logger.error(f"Erreur lors de la création du post: {str(e)}")
            raise

    def create(self, request, *args, **kwargs):
        """Créer un post et retourner les données complètes"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.perform_create(serializer)
        
        # Retourner le post complet avec tous les champs
        post_serializer = PostSerializer(post, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(post_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer un post"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.select_related(
            'author', 
            'quartier', 
            'quartier__commune'
        ).prefetch_related(
            Prefetch(
                'comments',
                queryset=PostComment.objects.select_related('author').order_by('-created_at'),
                to_attr='all_comments'
            ),
            'likes__user',
            'media_files'
        ).annotate(
            likes_count_annotated=Count('likes'),
            comments_count_annotated=Count('comments', filter=Q(comments__parent_comment__isnull=True)),
            shares_count_annotated=Count('shares')
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Cache pour les détails du post
        cache_key = f"post_detail_{instance.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Incrémenter le compteur de vues
            instance.increment_views()
            serializer = self.get_serializer(instance)
            cached_data = serializer.data
            # Mettre en cache pour 2 minutes
            cache.set(cache_key, cached_data, 120)
        
        return Response(cached_data)
    
    def perform_update(self, serializer):
        # Vérifier que l'utilisateur est l'auteur du post
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez modifier que vos propres posts")
        
        # Vérifier la limite de temps (30 minutes)
        from django.utils import timezone
        from datetime import timedelta
        
        time_limit = serializer.instance.created_at + timedelta(minutes=30)
        if timezone.now() > time_limit:
            raise permissions.PermissionDenied(
                "Vous ne pouvez plus modifier ce post. La limite de 30 minutes est dépassée."
            )
        
        post = serializer.save()
        
        # Invalider les caches
        cache.delete(f"post_detail_{post.id}")
        user = self.request.user
        cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
        cache.delete(cache_key)
    
    def perform_destroy(self, instance):
        # Vérifier que l'utilisateur est l'auteur du post
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez supprimer que vos propres posts")
        
        post_id = instance.id
        user = self.request.user
        
        instance.delete()
        
        # Invalider les caches
        cache.delete(f"post_detail_{post_id}")
        cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
        cache.delete(cache_key)


class PostLikeView(generics.CreateAPIView, generics.DestroyAPIView):
    """Vue pour liker/unliker un post"""
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        return get_object_or_404(PostLike, post=post, user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        
        # Vérifier si l'utilisateur a déjà liké ce post
        if PostLike.objects.filter(post=post, user=request.user).exists():
            return Response(
                {'detail': 'Vous avez déjà liké ce post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le like
        like = PostLike.objects.create(post=post, user=request.user)
        post.increment_likes()
        
        # Invalider les caches
        cache.delete(f"post_detail_{post_id}")
        user = request.user
        cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
        cache.delete(cache_key)
        
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        
        # Chercher le like de l'utilisateur pour ce post
        try:
            like = PostLike.objects.get(post=post, user=request.user)
            like.delete()
            post.decrement_likes()
            
            # Invalider les caches
            cache.delete(f"post_detail_{post_id}")
            user = request.user
            cache_key = f"posts_list_{user.id}_{user.quartier.id if user.quartier else 'none'}"
            cache.delete(cache_key)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            return Response(
                {'detail': 'Vous n\'avez pas liké ce post'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class PostCommentView(generics.ListCreateAPIView):
    """Vue pour lister et créer des commentaires sur un post"""
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        # Retourner seulement les commentaires de premier niveau (pas de parent)
        return PostComment.objects.filter(
            post_id=post_id, 
            parent_comment__isnull=True
        ).select_related('author').prefetch_related('replies__author')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCommentCreateSerializer
        return PostCommentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            post_id = self.kwargs.get('pk')
            post = get_object_or_404(Post, pk=post_id)
            context['post'] = post
        return context
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        comment = serializer.save(post=post, author=self.request.user)
        
        # Incrémenter le compteur de commentaires du post
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        
        return comment

    def create(self, request, *args, **kwargs):
        """Créer un commentaire et retourner les données complètes"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        
        # Retourner le commentaire complet avec tous les champs
        comment_serializer = PostCommentSerializer(comment, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour modifier et supprimer un commentaire"""
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PostComment.objects.select_related('author')
    
    def perform_update(self, serializer):
        # Vérifier que l'utilisateur est l'auteur du commentaire
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez modifier que vos propres commentaires")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Vérifier que l'utilisateur est l'auteur du commentaire
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez supprimer que vos propres commentaires")
        
        # Décrémenter le compteur de commentaires du post
        post = instance.post
        post.comments_count -= 1
        post.save(update_fields=['comments_count'])
        
        instance.delete()


class PostCommentReplyView(generics.CreateAPIView):
    """Vue pour répondre à un commentaire"""
    serializer_class = PostCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        comment_id = self.kwargs.get('comment_id')
        parent_comment = get_object_or_404(PostComment, pk=comment_id)
        context['post'] = parent_comment.post
        context['parent_comment'] = parent_comment
        return context
    
    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        parent_comment = get_object_or_404(PostComment, pk=comment_id)
        
        # Créer la réponse
        reply = serializer.save(
            post=parent_comment.post,
            author=self.request.user,
            parent_comment=parent_comment
        )
        
        # Incrémenter le compteur de commentaires du post
        post = parent_comment.post
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        
        return reply


class UserPostsView(generics.ListAPIView):
    """Vue pour lister les posts d'un utilisateur"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author_id=user_id).select_related('author', 'quartier').prefetch_related(
            'media_files', 'live_stream'
        )


class PostIncrementViewsView(generics.GenericAPIView):
    """Vue pour incrémenter les vues d'un post"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.views_count += 1
        post.save()
        return Response({'message': 'Vue incrémentée'}, status=status.HTTP_200_OK)


class PostShareView(generics.CreateAPIView, generics.DestroyAPIView):
    """Vue pour partager/unpartager un post"""
    serializer_class = PostShareCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        context['post'] = post
        return context
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        
        # Créer un partage simple sans serializer complexe
        from .models import PostShare
        
        # Vérifier si l'utilisateur a déjà partagé ce post
        existing_share = PostShare.objects.filter(
            user=request.user,
            post=post,
            share_type='share'
        ).first()
        
        if existing_share:
            return Response({
                'message': 'Vous avez déjà partagé ce post',
                'share_id': existing_share.id
            }, status=status.HTTP_200_OK)
        
        share = PostShare.objects.create(
            user=request.user,
            post=post,
            comment=request.data.get('message', '')
        )
        
        # Notifier l'auteur du post
        try:
            from notifications.services import create_notification
            create_notification(
                recipient=post.user,
                sender=request.user,
                notification_type='post_shared',
                title='Post partagé',
                message=f"{request.user.first_name} {request.user.last_name} a partagé votre publication",
                extra_data={'post_id': post.id, 'share_id': share.id}
            )
        except Exception as e:
            # Ignorer les erreurs de notification
            pass
        
        return Response({
            'message': 'Post partagé avec succès !',
            'share_id': share.id
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        share_type = request.data.get('share_type', 'share')
        
        try:
            share = PostShare.objects.get(
                user=request.user,
                post=post,
                share_type=share_type
            )
            share.delete()
            return Response({'message': 'Partage supprimé'}, status=status.HTTP_204_NO_CONTENT)
        except PostShare.DoesNotExist:
            return Response(
                {'error': 'Partage non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class PostSharesListView(generics.ListAPIView):
    """Vue pour lister les partages d'un post"""
    serializer_class = PostShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return PostShare.objects.filter(
            post_id=post_id
        ).select_related('user', 'post').order_by('-created_at') 


class ExternalShareView(generics.CreateAPIView):
    """Vue pour partager un post sur les réseaux sociaux externes"""
    serializer_class = ExternalShareCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        context['post'] = post
        return context
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        
        # Créer un partage externe simple
        from .models import ExternalShare
        
        platform = request.data.get('platform', 'whatsapp')
        
        # Créer un partage externe avec gestion d'erreur
        try:
            external_share = ExternalShare.objects.create(
                user=request.user,
                post=post,
                platform=platform
            )
        except Exception as e:
            # Si erreur de contrainte unique, récupérer l'existant
            existing_share = ExternalShare.objects.filter(
                user=request.user,
                post=post,
                platform=platform
            ).first()
            
            if existing_share:
                return Response({
                    'message': f'Vous avez déjà partagé ce post sur {existing_share.get_platform_display()}',
                    'platform': existing_share.platform,
                    'platform_display': existing_share.get_platform_display()
                }, status=status.HTTP_200_OK)
            else:
                raise e
        
        # Notifier l'auteur du post
        if post.author != request.user:
            try:
                from notifications.services import create_notification
                create_notification(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='post_shared_external',
                    title=f"{request.user.username} a partagé votre post",
                    message=f"Votre post a été partagé sur {external_share.get_platform_display()}",
                    extra_data={'post_id': post.id, 'external_share_id': external_share.id}
                )
            except Exception as e:
                # Ignorer les erreurs de notification
                pass
        
        return Response({
            'message': f'Post partagé sur {external_share.get_platform_display()}',
            'platform': external_share.platform,
            'platform_display': external_share.get_platform_display()
        }, status=201)

class ExternalSharesListView(generics.ListAPIView):
    """Vue pour lister les partages externes d'un post"""
    serializer_class = ExternalShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        return ExternalShare.objects.filter(post=post) 


class PostAnalyticsView(generics.RetrieveAPIView):
    """Vue pour récupérer les analytics d'un post"""
    serializer_class = PostAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        
        # Créer ou mettre à jour les analytics
        from .services import AnalyticsService
        analytics = AnalyticsService.create_or_update_post_analytics(post)
        
        return analytics

class UserAnalyticsView(generics.GenericAPIView):
    """Vue pour récupérer les analytics d'un utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Récupérer les statistiques de l'utilisateur
        user_posts = Post.objects.filter(author=user)
        total_posts = user_posts.count()
        
        # Calculer les totaux
        total_likes = sum(post.likes.count() for post in user_posts)
        total_comments = sum(post.comments.count() for post in user_posts)
        total_shares = sum(post.shares.count() for post in user_posts)
        total_views = sum(post.views_count for post in user_posts)
        
        # Analytics des posts récents
        recent_posts = user_posts.order_by('-created_at')[:5]
        recent_analytics = []
        
        for post in recent_posts:
            recent_analytics.append({
                'post_id': post.id,
                'content': post.content[:100] + '...' if len(post.content) > 100 else post.content,
                'likes_count': post.likes.count(),
                'comments_count': post.comments.count(),
                'shares_count': post.shares.count(),
                'views_count': post.views_count,
                'created_at': post.created_at
            })
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'total_posts': total_posts,
            'total_likes_received': total_likes,
            'total_comments_received': total_comments,
            'total_shares_received': total_shares,
            'total_views_received': total_views,
            'recent_posts_analytics': recent_analytics
        })


class CommunityAnalyticsView(generics.GenericAPIView):
    """Vue pour récupérer les analytics de la communauté"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostAnalyticsSummarySerializer
    
    def get(self, request):
        # Logique pour les analytics communautaires
        return Response({'message': 'Analytics communautaires'}) 


class LiveChatView(generics.GenericAPIView):
    """Vue pour gérer les messages de chat live"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        """Envoyer un message dans le chat live"""
        try:
            # Vérifier que le post existe et est un live
            post = Post.objects.get(id=post_id, is_live_post=True)
            
            content = request.data.get('content', '').strip()
            if not content:
                return Response(
                    {'error': 'Le contenu du message ne peut pas être vide'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer le message
            message = LiveChatMessage.objects.create(
                live_post=post,
                author=request.user,
                content=content,
                message_type=request.data.get('type', 'text')
            )
            
            # Sérialiser le message pour la réponse
            message_data = {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'author': {
                    'id': message.author.id,
                    'first_name': message.author.first_name,
                    'last_name': message.author.last_name,
                    'profile_picture': message.author.profile_picture.url if message.author.profile_picture else None
                }
            }
            
            return Response(message_data, status=status.HTTP_201_CREATED)
            
        except Post.DoesNotExist:
            return Response(
                {'error': 'Live non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erreur envoi message chat: {e}")
            return Response(
                {'error': 'Erreur lors de l\'envoi du message'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request, post_id):
        """Récupérer les messages d'un live"""
        try:
            # Vérifier que le post existe et est un live
            post = Post.objects.get(id=post_id, is_live_post=True)
            
            # Récupérer les messages avec pagination
            messages = LiveChatMessage.objects.filter(live_post=post).select_related('author')
            
            # Sérialiser les messages
            messages_data = []
            for message in messages:
                messages_data.append({
                    'id': message.id,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'author': {
                        'id': message.author.id,
                        'first_name': message.author.first_name,
                        'last_name': message.author.last_name,
                        'profile_picture': message.author.profile_picture.url if message.author.profile_picture else None
                    }
                })
            
            return Response(messages_data, status=status.HTTP_200_OK)
            
        except Post.DoesNotExist:
            return Response(
                {'error': 'Live non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erreur récupération messages chat: {e}")
            return Response(
                {'error': 'Erreur lors de la récupération des messages'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 


class LiveVideoUploadView(generics.GenericAPIView):
    """Vue pour uploader les vidéos de live enregistrées"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MediaSerializer
    
    def post(self, request, live_id):
        """Uploader une vidéo de live enregistrée"""
        try:
            logger.info(f"Tentative d'upload vidéo pour le live {live_id}")
            
            # Chercher le post live
            try:
                post = Post.objects.get(id=live_id, is_live_post=True)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Post live non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Récupérer le fichier vidéo
            video_file = request.FILES.get('video')
            if not video_file:
                return Response(
                    {'error': 'Fichier vidéo requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Vérifier le type de fichier
            allowed_types = ['video/webm', 'video/mp4', 'video/quicktime']
            if video_file.content_type not in allowed_types:
                return Response(
                    {'error': 'Type de fichier non supporté'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer le média
            media = Media.objects.create(
                title=f"Vidéo du live - {post.content}",
                description=f"Vidéo enregistrée du live '{post.content}'",
                media_type='video',
                file=video_file,  # Django gère automatiquement l'upload
                file_size=video_file.size,
                is_live_recording=True,
                live_post=post,
                duration=timedelta(seconds=5)  # Durée par défaut plus réaliste pour les lives
            )
            
            # Associer la vidéo au post
            post.media_files.add(media)
            
            # Associer la vidéo au champ live_stream du post
            post.live_stream = media
            post.save()
            
            # Mettre à jour le contenu du post
            post.content = f"{post.content}\n\n📹 Vidéo enregistrée disponible"
            post.save()
            
            logger.info(f"Vidéo uploadée avec succès: {media.id}")
            return Response({
                'message': 'Vidéo uploadée avec succès',
                'media_id': media.id,
                'file_url': media.file.url if media.file else None
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'upload vidéo: {str(e)}")
            return Response(
                {'error': 'Erreur lors de l\'upload de la vidéo'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
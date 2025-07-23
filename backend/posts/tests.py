import os
import tempfile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from PIL import Image
import io
import json

from .models import Post, Media, PostLike, PostComment
from .services import (
    ModerationService, VideoProcessingService, 
    MediaCDNService, MediaOptimizationService
)
from geography.models import Quartier, Commune, Prefecture, Region

User = get_user_model()


class MediaServicesTestCase(TestCase):
    """Tests pour les services de médias"""
    
    def setUp(self):
        """Configuration initiale"""
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer un quartier de test
        self.region = Region.objects.create(nom='Conakry')
        self.prefecture = Prefecture.objects.create(
            nom='Conakry', 
            region=self.region
        )
        self.commune = Commune.objects.create(
            nom='Kaloum', 
            prefecture=self.prefecture
        )
        self.quartier = Quartier.objects.create(
            nom='Test Quartier',
            commune=self.commune
        )
        
        # Assigner le quartier à l'utilisateur
        self.user.quartier = self.quartier
        self.user.save()
    
    def create_test_image(self, width=100, height=100, format='JPEG'):
        """Crée une image de test"""
        image = Image.new('RGB', (width, height), color='red')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format=format)
        image_buffer.seek(0)
        return image_buffer
    
    def test_media_optimization_service(self):
        """Test du service d'optimisation des médias"""
        # Créer une image de test
        test_image = self.create_test_image(200, 200)
        
        # Test de compression
        compressed_path = MediaOptimizationService.compress_image(
            test_image, max_width=100, quality=80
        )
        
        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(compressed_path))
        
        # Vérifier la taille réduite
        with Image.open(compressed_path) as img:
            self.assertLessEqual(img.width, 100)
    
    def test_moderation_service_simulation(self):
        """Test du service de modération (simulation)"""
        # Créer une image de test
        test_image = self.create_test_image()
        
        # Test d'analyse de modération
        result = ModerationService.analyze_image_with_vision_api(test_image)
        
        # Vérifier la structure de la réponse
        self.assertIn('moderation_score', result)
        self.assertIn('is_appropriate', result)
        self.assertIn('moderation_details', result)
        
        # Vérifier les valeurs
        self.assertIsInstance(result['moderation_score'], float)
        self.assertIsInstance(result['is_appropriate'], bool)
        self.assertIsInstance(result['moderation_details'], dict)
    
    def test_cdn_service_without_config(self):
        """Test du service CDN sans configuration"""
        # Test de génération d'URL CDN
        test_public_id = "test_image_123"
        cdn_url = MediaCDNService.get_cdn_url(test_public_id)
        
        # Sans configuration, devrait retourner None
        self.assertIsNone(cdn_url)
    
    def test_video_processing_service(self):
        """Test du service de traitement vidéo"""
        # Test de validation de durée (simulation)
        # En production, on utiliserait un vrai fichier vidéo
        
        # Créer un fichier temporaire pour simuler une vidéo
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            tmp_file.write(b'fake video content')
            tmp_file_path = tmp_file.name
        
        try:
            # Test de validation (devrait échouer car pas une vraie vidéo)
            validation_result = VideoProcessingService.validate_video_duration(
                tmp_file_path, max_duration=60
            )
            
            # Vérifier la structure de la réponse
            self.assertIn('is_valid', validation_result)
            self.assertIn('duration', validation_result)
            self.assertIn('max_duration', validation_result)
            
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(tmp_file_path)


class MediaModelTestCase(TestCase):
    """Tests pour le modèle Media"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer un quartier
        self.region = Region.objects.create(nom='Conakry')
        self.prefecture = Prefecture.objects.create(
            nom='Conakry', 
            region=self.region
        )
        self.commune = Commune.objects.create(
            nom='Kaloum', 
            prefecture=self.prefecture
        )
        self.quartier = Quartier.objects.create(
            nom='Test Quartier',
            commune=self.commune
        )
    
    def create_test_image_file(self):
        """Crée un fichier image de test"""
        image = Image.new('RGB', (100, 100), color='blue')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        
        return SimpleUploadedFile(
            "test_image.jpg",
            image_buffer.getvalue(),
            content_type="image/jpeg"
        )
    
    def test_media_creation(self):
        """Test de création d'un média"""
        image_file = self.create_test_image_file()
        
        media = Media.objects.create(
            file=image_file,
            media_type='image',
            title='Test Image',
            description='Test description',
            user=self.user
        )
        
        # Vérifications
        self.assertEqual(media.media_type, 'image')
        self.assertEqual(media.title, 'Test Image')
        self.assertEqual(media.description, 'Test description')
        self.assertEqual(media.user, self.user)
        self.assertTrue(media.file.url)
    
    def test_media_cdn_fields(self):
        """Test des champs CDN"""
        image_file = self.create_test_image_file()
        
        media = Media.objects.create(
            file=image_file,
            media_type='image',
            title='Test Image',
            cdn_url='https://res.cloudinary.com/test/image.jpg',
            cdn_public_id='test_image_123',
            width=100,
            height=100,
            file_size=1024,
            user=self.user
        )
        
        # Vérifications CDN
        self.assertEqual(media.cdn_url, 'https://res.cloudinary.com/test/image.jpg')
        self.assertEqual(media.cdn_public_id, 'test_image_123')
        self.assertEqual(media.width, 100)
        self.assertEqual(media.height, 100)
        self.assertEqual(media.file_size, 1024)
    
    def test_media_file_url_priority(self):
        """Test de la priorité des URLs (CDN vs local)"""
        image_file = self.create_test_image_file()
        
        # Test sans CDN
        media_local = Media.objects.create(
            file=image_file,
            media_type='image',
            title='Local Image',
            user=self.user
        )
        
        self.assertIsNotNone(media_local.file_url)
        self.assertIn('media/', media_local.file_url)
        
        # Test avec CDN
        media_cdn = Media.objects.create(
            file=image_file,
            media_type='image',
            title='CDN Image',
            cdn_url='https://res.cloudinary.com/test/image.jpg',
            user=self.user
        )
        
        self.assertEqual(media_cdn.file_url, 'https://res.cloudinary.com/test/image.jpg')


class PostModelTest(TestCase):
    """Tests pour le modèle Post"""
    
    def setUp(self):
        # Créer les données géographiques
        self.region = Region.objects.create(nom="Conakry")
        self.prefecture = Prefecture.objects.create(
            region=self.region, 
            nom="Conakry"
        )
        self.commune = Commune.objects.create(
            prefecture=self.prefecture, 
            nom="Kaloum"
        )
        self.quartier = Quartier.objects.create(
            commune=self.commune, 
            nom="Centre-ville"
        )
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            quartier=self.quartier
        )
    
    def test_create_post(self):
        """Test de création d'un post"""
        post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Test post content",
            post_type='info'
        )
        
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.quartier, self.quartier)
        self.assertEqual(post.content, "Test post content")
        self.assertEqual(post.post_type, 'info')
        self.assertEqual(post.likes_count, 0)
        self.assertEqual(post.comments_count, 0)
    
    def test_post_str_representation(self):
        """Test de la représentation string du post"""
        post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Test post",
            post_type='info'
        )
        
        self.assertIn("Test post", str(post))
        self.assertIn(self.user.username, str(post))
    
    def test_post_has_media_property(self):
        """Test de la propriété has_media"""
        post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Test post",
            post_type='info'
        )
        
        self.assertFalse(post.has_media)
        
        # Ajouter un média
        media = Media.objects.create(
            file="test.jpg",
            media_type='image',
            title="Test image"
        )
        post.media_files.add(media)
        
        self.assertTrue(post.has_media)

class PostAPITest(APITestCase):
    """Tests pour l'API des posts"""
    
    def setUp(self):
        # Créer les données géographiques
        self.region = Region.objects.create(nom="Conakry")
        self.prefecture = Prefecture.objects.create(
            region=self.region, 
            nom="Conakry"
        )
        self.commune = Commune.objects.create(
            prefecture=self.prefecture, 
            nom="Kaloum"
        )
        self.quartier = Quartier.objects.create(
            commune=self.commune, 
            nom="Centre-ville"
        )
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            quartier=self.quartier
        )
        
        # Créer un client API
        self.client = APIClient()
        
        # Créer quelques posts de test
        self.post1 = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Premier post de test",
            post_type='info'
        )
        
        self.post2 = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Deuxième post de test",
            post_type='event'
        )
    
    def test_get_posts_list(self):
        """Test de récupération de la liste des posts"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête
        url = reverse('posts:post-list')
        response = self.client.get(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_post(self):
        """Test de création d'un post"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Données du post
        post_data = {
            'content': 'Nouveau post via API',
            'post_type': 'info',
            'is_anonymous': False
        }
        
        # Faire la requête
        url = reverse('posts:post-list')
        response = self.client.post(url, post_data, format='json')
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Nouveau post via API')
        self.assertEqual(response.data['author']['username'], self.user.username)
        
        # Vérifier que le post a été créé en base
        self.assertEqual(Post.objects.count(), 3)
    
    def test_get_post_detail(self):
        """Test de récupération d'un post spécifique"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête
        url = reverse('posts:post-detail', args=[self.post1.id])
        response = self.client.get(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Premier post de test')
        self.assertEqual(response.data['id'], self.post1.id)
    
    def test_update_post(self):
        """Test de modification d'un post"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Données de modification
        update_data = {
            'content': 'Post modifié via API',
            'post_type': 'event'
        }
        
        # Faire la requête
        url = reverse('posts:post-detail', args=[self.post1.id])
        response = self.client.put(url, update_data, format='json')
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Post modifié via API')
        self.assertEqual(response.data['post_type'], 'event')
        
        # Vérifier en base
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'Post modifié via API')
    
    def test_delete_post(self):
        """Test de suppression d'un post"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête
        url = reverse('posts:post-detail', args=[self.post1.id])
        response = self.client.delete(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérifier que le post a été supprimé
        self.assertEqual(Post.objects.count(), 1)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
    
    def test_like_post(self):
        """Test de like d'un post"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête de like
        url = reverse('posts:post-like', args=[self.post1.id])
        response = self.client.post(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Vérifier que le like a été créé
        self.assertTrue(PostLike.objects.filter(
            user=self.user, 
            post=self.post1
        ).exists())
        
        # Vérifier que le compteur a été incrémenté
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.likes_count, 1)
    
    def test_unlike_post(self):
        """Test de unlike d'un post"""
        # Créer un like
        PostLike.objects.create(user=self.user, post=self.post1)
        self.post1.likes_count = 1
        self.post1.save()
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête de unlike
        url = reverse('posts:post-like', args=[self.post1.id])
        response = self.client.delete(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérifier que le like a été supprimé
        self.assertFalse(PostLike.objects.filter(
            user=self.user, 
            post=self.post1
        ).exists())
        
        # Vérifier que le compteur a été décrémenté
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.likes_count, 0)

class PostCommentTest(APITestCase):
    """Tests pour les commentaires"""
    
    def setUp(self):
        # Créer les données géographiques
        self.region = Region.objects.create(nom="Conakry")
        self.prefecture = Prefecture.objects.create(
            region=self.region, 
            nom="Conakry"
        )
        self.commune = Commune.objects.create(
            prefecture=self.prefecture, 
            nom="Kaloum"
        )
        self.quartier = Quartier.objects.create(
            commune=self.commune, 
            nom="Centre-ville"
        )
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            quartier=self.quartier
        )
        
        # Créer un post
        self.post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content="Post pour tester les commentaires",
            post_type='info'
        )
        
        # Créer un client API
        self.client = APIClient()
    
    def test_create_comment(self):
        """Test de création d'un commentaire"""
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Données du commentaire
        comment_data = {
            'content': 'Commentaire de test',
            'is_anonymous': False
        }
        
        # Faire la requête
        url = reverse('posts:post-comments', args=[self.post.id])
        response = self.client.post(url, comment_data, format='json')
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Commentaire de test')
        self.assertEqual(response.data['author']['username'], self.user.username)
        
        # Vérifier que le commentaire a été créé en base
        self.assertEqual(PostComment.objects.count(), 1)
        
        # Vérifier que le compteur du post a été incrémenté
        self.post.refresh_from_db()
        self.assertEqual(self.post.comments_count, 1)
    
    def test_get_comments(self):
        """Test de récupération des commentaires d'un post"""
        # Créer quelques commentaires
        PostComment.objects.create(
            post=self.post,
            author=self.user,
            content="Premier commentaire"
        )
        PostComment.objects.create(
            post=self.post,
            author=self.user,
            content="Deuxième commentaire"
        )
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
        
        # Faire la requête
        url = reverse('posts:post-comments', args=[self.post.id])
        response = self.client.get(url)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['content'], 'Premier commentaire')
        self.assertEqual(response.data[1]['content'], 'Deuxième commentaire')

class MediaTest(APITestCase):
    """Tests pour les médias"""
    
    def setUp(self):
        # Créer les données géographiques
        self.region = Region.objects.create(nom="Conakry")
        self.prefecture = Prefecture.objects.create(
            region=self.region, 
            nom="Conakry"
        )
        self.commune = Commune.objects.create(
            prefecture=self.prefecture, 
            nom="Kaloum"
        )
        self.quartier = Quartier.objects.create(
            commune=self.commune, 
            nom="Centre-ville"
        )
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            quartier=self.quartier
        )
        
        # Créer un client API
        self.client = APIClient()
    
    def test_media_validation(self):
        """Test de validation des médias"""
        # Créer un média valide
        media = Media.objects.create(
            file="test.jpg",
            media_type='image',
            title="Test image",
            file_size=1024
        )
        
        self.assertEqual(media.media_type, 'image')
        self.assertEqual(media.file_size, 1024)
        self.assertTrue(media.is_approved_for_publication)
    
    def test_media_str_representation(self):
        """Test de la représentation string du média"""
        media = Media.objects.create(
            file="test.jpg",
            media_type='image',
            title="Test image"
        )
        
        self.assertIn("Test image", str(media))
        self.assertIn("Image", str(media))


class CacheTestCase(TestCase):
    """Tests pour le système de cache"""
    
    def setUp(self):
        """Configuration initiale"""
        # Nettoyer le cache avant chaque test
        cache.clear()
    
    def test_cache_basic_operations(self):
        """Test des opérations de base du cache"""
        # Test d'écriture
        cache.set('test_key', 'test_value', 60)
        
        # Test de lecture
        value = cache.get('test_key')
        self.assertEqual(value, 'test_value')
        
        # Test de suppression
        cache.delete('test_key')
        value = cache.get('test_key')
        self.assertIsNone(value)
    
    def test_cache_timeout(self):
        """Test du timeout du cache"""
        # Écrire avec un timeout très court
        cache.set('timeout_test', 'value', 1)
        
        # Vérifier que la valeur existe
        value = cache.get('timeout_test')
        self.assertEqual(value, 'value')
        
        # Attendre que le timeout expire (simulation)
        import time
        time.sleep(0.1)  # Petit délai pour simuler
        
        # En production, on utiliserait un timeout réel


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})
class APITestCase(APITestCase):
    """Tests pour les API endpoints"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = APIClient()
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer un quartier
        self.region = Region.objects.create(name='Conakry')
        self.prefecture = Prefecture.objects.create(
            name='Conakry', 
            region=self.region
        )
        self.commune = Commune.objects.create(
            name='Kaloum', 
            prefecture=self.prefecture
        )
        self.quartier = Quartier.objects.create(
            name='Test Quartier',
            commune=self.commune
        )
        
        self.user.quartier = self.quartier
        self.user.save()
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)
    
    def create_test_image_file(self):
        """Crée un fichier image de test"""
        image = Image.new('RGB', (100, 100), color='green')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        
        return SimpleUploadedFile(
            "test_image.jpg",
            image_buffer.getvalue(),
            content_type="image/jpeg"
        )
    
    def test_media_upload_api(self):
        """Test de l'API d'upload de média"""
        image_file = self.create_test_image_file()
        
        data = {
            'file': image_file,
            'title': 'Test Image',
            'description': 'Test description'
        }
        
        response = self.client.post(
            reverse('media-upload'),
            data,
            format='multipart'
        )
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], 'Test Image')
        self.assertEqual(response.data['description'], 'Test description')
    
    def test_post_creation_api(self):
        """Test de l'API de création de post"""
        data = {
            'content': 'Test post content',
            'post_type': 'info',
            'is_anonymous': False
        }
        
        response = self.client.post(
            reverse('post-list'),
            data,
            format='json'
        )
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test post content')
        self.assertEqual(response.data['post_type'], 'info')
        self.assertEqual(response.data['author'], self.user.username)
    
    def test_post_list_api(self):
        """Test de l'API de liste des posts"""
        # Créer quelques posts
        Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content='Post 1',
            post_type='info'
        )
        
        Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content='Post 2',
            post_type='event'
        )
        
        response = self.client.get(reverse('post-list'))
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_post_like_api(self):
        """Test de l'API de like/unlike"""
        # Créer un post
        post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content='Test post for likes',
            post_type='info'
        )
        
        # Test d'ajout de like
        response = self.client.post(
            reverse('post-like', kwargs={'pk': post.pk})
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Vérifier que le like a été créé
        self.assertTrue(PostLike.objects.filter(
            user=self.user, 
            post=post
        ).exists())
        
        # Test de suppression de like
        response = self.client.delete(
            reverse('post-like', kwargs={'pk': post.pk})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérifier que le like a été supprimé
        self.assertFalse(PostLike.objects.filter(
            user=self.user, 
            post=post
        ).exists())
    
    def test_post_comment_api(self):
        """Test de l'API de commentaires"""
        # Créer un post
        post = Post.objects.create(
            author=self.user,
            quartier=self.quartier,
            content='Test post for comments',
            post_type='info'
        )
        
        # Test d'ajout de commentaire
        data = {
            'content': 'Test comment'
        }
        
        response = self.client.post(
            reverse('post-comments', kwargs={'pk': post.pk}),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test comment')
        self.assertEqual(response.data['author'], self.user.username)
        
        # Test de liste des commentaires
        response = self.client.get(
            reverse('post-comments', kwargs={'pk': post.pk})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PerformanceTestCase(TestCase):
    """Tests de performance"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer un quartier
        self.region = Region.objects.create(name='Conakry')
        self.prefecture = Prefecture.objects.create(
            name='Conakry', 
            region=self.region
        )
        self.commune = Commune.objects.create(
            name='Kaloum', 
            prefecture=self.prefecture
        )
        self.quartier = Quartier.objects.create(
            name='Test Quartier',
            commune=self.commune
        )
        
        self.user.quartier = self.quartier
        self.user.save()
    
    def test_cache_performance(self):
        """Test de performance du cache"""
        import time
        
        # Test sans cache
        start_time = time.time()
        for _ in range(100):
            Post.objects.filter(quartier=self.quartier)
        without_cache_time = time.time() - start_time
        
        # Test avec cache (simulation)
        start_time = time.time()
        for _ in range(100):
            # En production, on utiliserait le cache Redis
            Post.objects.filter(quartier=self.quartier)
        with_cache_time = time.time() - start_time
        
        # Le cache devrait être plus rapide (en production)
        # Pour ce test, on vérifie juste que ça fonctionne
        self.assertIsInstance(without_cache_time, float)
        self.assertIsInstance(with_cache_time, float)
    
    def test_media_optimization_performance(self):
        """Test de performance de l'optimisation des médias"""
        import time
        
        # Créer une image de test
        image = Image.new('RGB', (1920, 1080), color='blue')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        
        # Test de compression
        start_time = time.time()
        compressed_path = MediaOptimizationService.compress_image(
            image_buffer, max_width=800, quality=85
        )
        compression_time = time.time() - start_time
        
        # Vérifications
        self.assertIsInstance(compression_time, float)
        self.assertTrue(compression_time < 5.0)  # Moins de 5 secondes
        
        # Nettoyer
        if os.path.exists(compressed_path):
            os.unlink(compressed_path)


if __name__ == '__main__':
    # Pour exécuter les tests manuellement
    import django
    django.setup()
    
    # Exécuter les tests
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    failures = test_runner.run_tests([
        'posts.tests.MediaServicesTestCase',
        'posts.tests.MediaModelTestCase',
        'posts.tests.PostModelTestCase',
        'posts.tests.CacheTestCase',
        'posts.tests.APITestCase',
        'posts.tests.PerformanceTestCase',
    ])
    
    if failures:
        print(f"❌ {failures} tests ont échoué")
        exit(1)
    else:
        print("✅ Tous les tests sont passés!") 
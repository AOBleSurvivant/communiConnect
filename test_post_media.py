#!/usr/bin/env python3
"""
Script de test pour diagnostiquer les problèmes avec les posts et médias
"""

import os
import sys
import django
import requests
import json
from pathlib import Path

# Ajouter le chemin du backend au PYTHONPATH
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post, Media
from posts.serializers import PostCreateSerializer, MediaCreateSerializer
from rest_framework.test import APITestCase
from rest_framework import status
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

User = get_user_model()

class PostMediaTest:
    """Classe de test pour les posts avec médias"""
    
    def __init__(self):
        self.client = Client()
        self.api_client = APITestCase()
        self.base_url = 'http://localhost:8000'
        self.test_user = None
        self.test_media = None
        
    def setup_test_user(self):
        """Créer un utilisateur de test avec quartier"""
        try:
            # Vérifier si l'utilisateur existe déjà
            self.test_user = User.objects.filter(username='testuser').first()
            if not self.test_user:
                # Créer ou récupérer un quartier de test
                from geography.models import Region, Prefecture, Commune, Quartier
                
                # Créer une région de test si elle n'existe pas
                region, created = Region.objects.get_or_create(
                    nom='Conakry',
                    defaults={'code': 'CON'}
                )
                
                # Créer une préfecture de test
                prefecture, created = Prefecture.objects.get_or_create(
                    region=region,
                    nom='Conakry',
                    defaults={'code': 'CON'}
                )
                
                # Créer une commune de test
                commune, created = Commune.objects.get_or_create(
                    prefecture=prefecture,
                    nom='Kaloum',
                    defaults={'type': 'urbaine', 'code': 'KAL'}
                )
                
                # Créer un quartier de test
                quartier, created = Quartier.objects.get_or_create(
                    commune=commune,
                    nom='Centre-ville',
                    defaults={'code': 'CV'}
                )
                
                self.test_user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='testpass123',
                    first_name='Test',
                    last_name='User',
                    quartier=quartier
                )
                logger.info(f"Utilisateur de test créé: {self.test_user.username} avec quartier: {quartier.nom}")
            else:
                # S'assurer que l'utilisateur a un quartier
                if not self.test_user.quartier:
                    # Assigner un quartier existant
                    from geography.models import Quartier
                    quartier = Quartier.objects.first()
                    if quartier:
                        self.test_user.quartier = quartier
                        self.test_user.save()
                        logger.info(f"Quartier assigné à l'utilisateur: {quartier.nom}")
                    else:
                        logger.error("Aucun quartier disponible dans la base de données")
                        return False
                else:
                    logger.info(f"Utilisateur de test existant: {self.test_user.username} avec quartier: {self.test_user.quartier.nom}")
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur: {e}")
            return False
    
    def create_test_image(self):
        """Créer une image de test"""
        try:
            # Créer une image simple (1x1 pixel PNG)
            image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
            
            image_file = SimpleUploadedFile(
                name='test_image.png',
                content=image_data,
                content_type='image/png'
            )
            
            return image_file
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'image de test: {e}")
            return None
    
    def test_media_upload(self):
        """Tester l'upload de média"""
        logger.info("=== Test d'upload de média ===")
        
        if not self.setup_test_user():
            return False
        
        try:
            # Créer une image de test
            image_file = self.create_test_image()
            if not image_file:
                logger.error("Impossible de créer l'image de test")
                return False
            
            # Créer le média via le modèle
            media = Media.objects.create(
                file=image_file,
                media_type='image',
                title='Test Image',
                description='Image de test',
                approval_status='approved',
                is_appropriate=True
            )
            
            logger.info(f"Média créé avec succès: ID={media.id}, Type={media.media_type}")
            self.test_media = media
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'upload de média: {e}")
            return False
    
    def test_post_creation_with_media(self):
        """Tester la création de post avec média"""
        logger.info("=== Test de création de post avec média ===")
        
        if not self.test_media:
            logger.error("Aucun média de test disponible")
            return False
        
        try:
            # Créer un post avec média
            post_data = {
                'content': 'Test post avec média',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [self.test_media.id]
            }
            
            # Utiliser le sérialiseur
            serializer = PostCreateSerializer(
                data=post_data,
                context={'request': type('Request', (), {'user': self.test_user})()}
            )
            
            if serializer.is_valid():
                post = serializer.save()
                logger.info(f"Post créé avec succès: ID={post.id}")
                logger.info(f"Médias associés: {post.media_files.count()}")
                return True
            else:
                logger.error(f"Erreurs de validation: {serializer.errors}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la création du post: {e}")
            return False
    
    def test_api_endpoints(self):
        """Tester les endpoints API"""
        logger.info("=== Test des endpoints API ===")
        
        try:
            # S'assurer que l'utilisateur de test existe
            if not self.setup_test_user():
                return False
            
            # Authentifier l'utilisateur
            self.client.login(username='testuser', password='testpass123')
            
            # Test de l'endpoint de création de post
            post_data = {
                'content': 'Test post via API',
                'post_type': 'info',
                'is_anonymous': False
            }
            
            # Simuler une requête API avec le bon host
            response = self.client.post(
                '/api/posts/',
                data=json.dumps(post_data),
                content_type='application/json',
                HTTP_HOST='localhost:8000'
            )
            
            logger.info(f"Réponse API: Status={response.status_code}")
            if response.status_code in [200, 201]:
                logger.info(f"Données de réponse: {response.json()}")
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            logger.error(f"Erreur lors du test API: {e}")
            return False
    
    def test_media_serializer(self):
        """Tester le sérialiseur de média"""
        logger.info("=== Test du sérialiseur de média ===")
        
        try:
            image_file = self.create_test_image()
            if not image_file:
                return False
            
            # Tester le sérialiseur
            serializer = MediaCreateSerializer(data={
                'file': image_file,
                'title': 'Test via sérialiseur',
                'description': 'Test description'
            })
            
            if serializer.is_valid():
                media = serializer.save()
                logger.info(f"Média créé via sérialiseur: ID={media.id}")
                return True
            else:
                logger.error(f"Erreurs de validation média: {serializer.errors}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors du test du sérialiseur: {e}")
            return False
    
    def check_database_connection(self):
        """Vérifier la connexion à la base de données"""
        logger.info("=== Vérification de la base de données ===")
        
        try:
            # Compter les utilisateurs
            user_count = User.objects.count()
            logger.info(f"Nombre d'utilisateurs dans la DB: {user_count}")
            
            # Compter les posts
            post_count = Post.objects.count()
            logger.info(f"Nombre de posts dans la DB: {post_count}")
            
            # Compter les médias
            media_count = Media.objects.count()
            logger.info(f"Nombre de médias dans la DB: {media_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur de connexion à la DB: {e}")
            return False
    
    def check_media_settings(self):
        """Vérifier les paramètres de médias"""
        logger.info("=== Vérification des paramètres de médias ===")
        
        try:
            from django.conf import settings
            
            # Vérifier MEDIA_URL
            logger.info(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Non défini')}")
            
            # Vérifier MEDIA_ROOT
            logger.info(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Non défini')}")
            
            # Vérifier si le dossier media existe
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if media_root:
                media_path = Path(media_root)
                logger.info(f"Dossier media existe: {media_path.exists()}")
                if media_path.exists():
                    logger.info(f"Contenu du dossier media: {list(media_path.iterdir())}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des paramètres: {e}")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        logger.info("🚀 Démarrage des tests de posts et médias")
        
        results = {
            'database': self.check_database_connection(),
            'media_settings': self.check_media_settings(),
            'media_upload': self.test_media_upload(),
            'media_serializer': self.test_media_serializer(),
            'post_creation': self.test_post_creation_with_media(),
            'api_endpoints': self.test_api_endpoints()
        }
        
        logger.info("\n📊 Résultats des tests:")
        for test_name, result in results.items():
            status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
            logger.info(f"{test_name}: {status}")
        
        success_count = sum(results.values())
        total_count = len(results)
        
        logger.info(f"\n🎯 Résumé: {success_count}/{total_count} tests réussis")
        
        if success_count == total_count:
            logger.info("🎉 Tous les tests sont passés!")
        else:
            logger.warning("⚠️ Certains tests ont échoué. Vérifiez les logs ci-dessus.")
        
        return results

def main():
    """Fonction principale"""
    tester = PostMediaTest()
    results = tester.run_all_tests()
    
    # Retourner le code de sortie approprié
    success_count = sum(results.values())
    total_count = len(results)
    
    if success_count == total_count:
        sys.exit(0)  # Succès
    else:
        sys.exit(1)  # Échec

if __name__ == '__main__':
    main() 
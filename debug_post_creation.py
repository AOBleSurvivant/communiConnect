#!/usr/bin/env python3
"""
Script de debug pour capturer les problèmes de création de posts avec médias
"""

import os
import sys
import django
import json
import requests
from pathlib import Path

# Ajouter le chemin du backend au PYTHONPATH
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post, Media
from posts.serializers import PostCreateSerializer
from geography.models import Region, Prefecture, Commune, Quartier
import logging

# Configuration du logging détaillé
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

User = get_user_model()

class PostCreationDebugger:
    """Debugger pour la création de posts avec médias"""
    
    def __init__(self):
        self.test_user = None
        self.test_media = None
        self.api_url = "http://localhost:8000"
        
    def setup_test_environment(self):
        """Créer l'environnement de test"""
        logger.info("🔧 Configuration de l'environnement de test...")
        
        try:
            # Créer ou récupérer un quartier de test
            region, created = Region.objects.get_or_create(
                nom='Conakry',
                defaults={'code': 'CON'}
            )
            
            prefecture, created = Prefecture.objects.get_or_create(
                region=region,
                nom='Conakry',
                defaults={'code': 'CON'}
            )
            
            commune, created = Commune.objects.get_or_create(
                prefecture=prefecture,
                nom='Kaloum',
                defaults={'type': 'urbaine', 'code': 'KAL'}
            )
            
            quartier, created = Quartier.objects.get_or_create(
                commune=commune,
                nom='Centre-ville',
                defaults={'code': 'CV'}
            )
            
            # Créer ou récupérer l'utilisateur de test
            self.test_user = User.objects.filter(username='testuser').first()
            if not self.test_user:
                self.test_user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='testpass123',
                    first_name='Test',
                    last_name='User',
                    quartier=quartier
                )
                logger.info(f"✅ Utilisateur créé: {self.test_user.username}")
            else:
                # S'assurer que l'utilisateur a un quartier
                if not self.test_user.quartier:
                    self.test_user.quartier = quartier
                    self.test_user.save()
                    logger.info(f"✅ Quartier assigné: {quartier.nom}")
                else:
                    logger.info(f"✅ Utilisateur existant: {self.test_user.username} avec quartier: {self.test_user.quartier.nom}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur configuration: {e}")
            return False
    
    def create_test_media(self):
        """Créer un média de test"""
        logger.info("📸 Création d'un média de test...")
        
        try:
            # Créer une image simple
            image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
            
            image_file = SimpleUploadedFile(
                name='test_image.png',
                content=image_data,
                content_type='image/png'
            )
            
            # Créer le média
            self.test_media = Media.objects.create(
                file=image_file,
                media_type='image',
                title='Test Image',
                description='Image de test pour debug',
                approval_status='approved',
                is_appropriate=True
            )
            
            logger.info(f"✅ Média créé: ID={self.test_media.id}, Type={self.test_media.media_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur création média: {e}")
            return False
    
    def test_serializer_validation(self):
        """Tester la validation du sérialiseur"""
        logger.info("🔍 Test de validation du sérialiseur...")
        
        try:
            # Test 1: Post avec contenu seulement
            post_data_1 = {
                'content': 'Test post avec contenu seulement',
                'post_type': 'info',
                'is_anonymous': False
            }
            
            serializer_1 = PostCreateSerializer(
                data=post_data_1,
                context={'request': type('Request', (), {'user': self.test_user})()}
            )
            
            if serializer_1.is_valid():
                logger.info("✅ Validation OK: Post avec contenu seulement")
            else:
                logger.error(f"❌ Validation échouée: {serializer_1.errors}")
            
            # Test 2: Post avec média seulement
            post_data_2 = {
                'content': '',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [self.test_media.id]
            }
            
            serializer_2 = PostCreateSerializer(
                data=post_data_2,
                context={'request': type('Request', (), {'user': self.test_user})()}
            )
            
            if serializer_2.is_valid():
                logger.info("✅ Validation OK: Post avec média seulement")
            else:
                logger.error(f"❌ Validation échouée: {serializer_2.errors}")
            
            # Test 3: Post avec contenu et média
            post_data_3 = {
                'content': 'Test post avec contenu et média',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [self.test_media.id]
            }
            
            serializer_3 = PostCreateSerializer(
                data=post_data_3,
                context={'request': type('Request', (), {'user': self.test_user})()}
            )
            
            if serializer_3.is_valid():
                logger.info("✅ Validation OK: Post avec contenu et média")
                return True
            else:
                logger.error(f"❌ Validation échouée: {serializer_3.errors}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur test validation: {e}")
            return False
    
    def test_serializer_creation(self):
        """Tester la création via sérialiseur"""
        logger.info("🏗️ Test de création via sérialiseur...")
        
        try:
            post_data = {
                'content': 'Test post créé via sérialiseur',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [self.test_media.id]
            }
            
            serializer = PostCreateSerializer(
                data=post_data,
                context={'request': type('Request', (), {'user': self.test_user})()}
            )
            
            if serializer.is_valid():
                post = serializer.save()
                logger.info(f"✅ Post créé via sérialiseur: ID={post.id}")
                logger.info(f"✅ Médias associés: {post.media_files.count()}")
                return post
            else:
                logger.error(f"❌ Erreur validation: {serializer.errors}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur création: {e}")
            return None
    
    def test_api_endpoint(self):
        """Tester l'endpoint API"""
        logger.info("🌐 Test de l'endpoint API...")
        
        try:
            # D'abord, obtenir un token JWT
            login_data = {
                'email': 'test@example.com',
                'password': 'testpass123'
            }
            
            login_response = requests.post(
                f"{self.api_url}/api/users/login/",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if login_response.status_code != 200:
                logger.error(f"❌ Échec login: {login_response.status_code} - {login_response.text}")
                return False
            
            token_data = login_response.json()
            logger.info(f"📊 Réponse login: {token_data}")
            
            # Vérifier la structure de la réponse
            if 'tokens' in token_data:
                access_token = token_data['tokens'].get('access')
            else:
                access_token = token_data.get('access')
            
            if not access_token:
                logger.error("❌ Token d'accès non trouvé dans la réponse")
                return False
            
            logger.info("✅ Authentification réussie")
            
            # Tester la création de post via API
            post_data = {
                'content': 'Test post via API',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [self.test_media.id]
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.post(
                f"{self.api_url}/api/posts/",
                json=post_data,
                headers=headers
            )
            
            logger.info(f"📊 Réponse API: Status={response.status_code}")
            logger.info(f"📊 Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                response_data = response.json()
                logger.info(f"✅ Post créé via API: {response_data}")
                return True
            else:
                logger.error(f"❌ Erreur API: {response.status_code}")
                logger.error(f"❌ Réponse: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur test API: {e}")
            return False
    
    def simulate_frontend_request(self):
        """Simuler une requête frontend"""
        logger.info("🖥️ Simulation d'une requête frontend...")
        
        try:
            # Simuler l'upload de média
            image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
            
            # Login
            login_data = {
                'email': 'test@example.com',
                'password': 'testpass123'
            }
            
            login_response = requests.post(
                f"{self.api_url}/api/users/login/",
                json=login_data
            )
            
            if login_response.status_code != 200:
                logger.error("❌ Échec login")
                return False
            
            token_data = login_response.json()
            logger.info(f"📊 Réponse login: {token_data}")
            
            # Vérifier la structure de la réponse
            if 'tokens' in token_data:
                access_token = token_data['tokens'].get('access')
            else:
                access_token = token_data.get('access')
            
            # Upload média
            files = {
                'file': ('test_image.png', image_data, 'image/png')
            }
            data = {
                'title': 'Test Image',
                'description': 'Test description'
            }
            
            upload_headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            upload_response = requests.post(
                f"{self.api_url}/api/posts/media/upload/",
                files=files,
                data=data,
                headers=upload_headers
            )
            
            logger.info(f"📤 Upload status: {upload_response.status_code}")
            
            if upload_response.status_code != 201:
                logger.error(f"❌ Échec upload: {upload_response.text}")
                return False
            
            upload_data = upload_response.json()
            logger.info(f"📊 Réponse upload: {upload_data}")
            media_id = upload_data.get('id')
            
            logger.info(f"✅ Média uploadé: ID={media_id}")
            
            # Créer post avec média
            post_data = {
                'content': 'Test post avec média uploadé',
                'post_type': 'info',
                'is_anonymous': False,
                'media_files': [media_id]
            }
            
            post_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            post_response = requests.post(
                f"{self.api_url}/api/posts/",
                json=post_data,
                headers=post_headers
            )
            
            logger.info(f"📝 Création post status: {post_response.status_code}")
            
            if post_response.status_code == 201:
                logger.info("✅ Post créé avec succès!")
                return True
            else:
                logger.error(f"❌ Échec création post: {post_response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur simulation frontend: {e}")
            return False
    
    def run_complete_debug(self):
        """Exécuter le debug complet"""
        logger.info("🚀 Démarrage du debug complet...")
        
        results = {
            'setup': self.setup_test_environment(),
            'media_creation': self.create_test_media(),
            'validation': self.test_serializer_validation(),
            'creation': self.test_serializer_creation() is not None,
            'api_test': self.test_api_endpoint(),
            'frontend_simulation': self.simulate_frontend_request()
        }
        
        logger.info("\n📊 Résultats du debug:")
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
    debugger = PostCreationDebugger()
    results = debugger.run_complete_debug()
    
    success_count = sum(results.values())
    total_count = len(results)
    
    if success_count == total_count:
        sys.exit(0)  # Succès
    else:
        sys.exit(1)  # Échec

if __name__ == '__main__':
    main() 
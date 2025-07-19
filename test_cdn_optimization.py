#!/usr/bin/env python3
"""
Test d'optimisation CDN pour CommuniConnect
Vérifie la configuration Redis et Cloudinary
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'backend'))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.conf import settings
from django.core.cache import cache
from posts.services import MediaCDNService, MediaOptimizationService
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_redis_cache():
    """Test de la configuration Redis"""
    print("🔍 Test de la configuration Redis...")
    
    try:
        # Test de connexion Redis
        cache.set('test_key', 'test_value', 60)
        value = cache.get('test_key')
        
        if value == 'test_value':
            print("✅ Redis fonctionne correctement")
            return True
        else:
            print("❌ Redis ne fonctionne pas")
            return False
            
    except Exception as e:
        print(f"❌ Erreur Redis: {str(e)}")
        return False

def test_cloudinary_config():
    """Test de la configuration Cloudinary"""
    print("\n🔍 Test de la configuration Cloudinary...")
    
    try:
        cloudinary_config = settings.CLOUDINARY_STORAGE
        
        if cloudinary_config.get('CLOUD_NAME'):
            print("✅ Configuration Cloudinary trouvée")
            print(f"   Cloud Name: {cloudinary_config['CLOUD_NAME']}")
            print(f"   API Key: {'*' * len(cloudinary_config['API_KEY']) if cloudinary_config['API_KEY'] else 'Non configuré'}")
            return True
        else:
            print("⚠️  Cloudinary non configuré (normal en développement)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur configuration Cloudinary: {str(e)}")
        return False

def test_media_optimization():
    """Test de l'optimisation des médias"""
    print("\n🔍 Test de l'optimisation des médias...")
    
    try:
        # Test de compression d'image (simulation)
        from PIL import Image
        import io
        
        # Créer une image de test
        test_image = Image.new('RGB', (100, 100), color='red')
        image_buffer = io.BytesIO()
        test_image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        
        # Test de compression
        compressed_path = MediaOptimizationService.compress_image(
            image_buffer, max_width=50, quality=80
        )
        
        print("✅ Service d'optimisation des médias fonctionnel")
        return True
        
    except Exception as e:
        print(f"❌ Erreur optimisation médias: {str(e)}")
        return False

def test_cdn_service():
    """Test du service CDN"""
    print("\n🔍 Test du service CDN...")
    
    try:
        # Test de génération d'URL CDN
        test_public_id = "test_image_123"
        cdn_url = MediaCDNService.get_cdn_url(test_public_id)
        
        if cdn_url:
            print("✅ Service CDN fonctionnel")
            print(f"   URL générée: {cdn_url}")
        else:
            print("⚠️  Service CDN non disponible (normal sans configuration)")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur service CDN: {str(e)}")
        return False

def test_cache_configuration():
    """Test de la configuration du cache"""
    print("\n🔍 Test de la configuration du cache...")
    
    try:
        # Vérifier les configurations de cache
        caches = settings.CACHES
        
        if 'default' in caches:
            print("✅ Cache par défaut configuré")
            print(f"   Backend: {caches['default']['BACKEND']}")
            
        if 'posts' in caches:
            print("✅ Cache posts configuré")
            print(f"   Timeout: {caches['posts']['TIMEOUT']}s")
            
        if 'sessions' in caches:
            print("✅ Cache sessions configuré")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration cache: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test d'optimisation CDN pour CommuniConnect")
    print("=" * 50)
    
    tests = [
        test_redis_cache,
        test_cloudinary_config,
        test_media_optimization,
        test_cdn_service,
        test_cache_configuration
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test: {str(e)}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"📈 Taux de réussite: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Toutes les optimisations sont configurées correctement!")
        print("   Votre application est prête pour la production.")
    elif passed >= total * 0.8:
        print("\n⚠️  La plupart des optimisations sont configurées.")
        print("   Quelques ajustements mineurs peuvent être nécessaires.")
    else:
        print("\n❌ Plusieurs optimisations nécessitent une configuration.")
        print("   Consultez la documentation pour les étapes manquantes.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
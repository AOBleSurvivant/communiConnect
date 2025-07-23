#!/usr/bin/env python
import requests
import json
import os
from PIL import Image
import io

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def create_test_image():
    """Créer une image de test"""
    # Créer une image simple de 100x100 pixels
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_login():
    """Test de connexion utilisateur"""
    print("🔐 Test de connexion...")
    
    login_data = {
        "email": "mariam.diallo@test.gn",
        "password": "test123456"
    }
    
    response = requests.post(f"{API_URL}/users/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('tokens', {}).get('access')
        print(f"✅ Connexion réussie pour mariam_diallo")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        return None

def test_media_upload(token):
    """Test de l'upload de médias"""
    print("\n📸 Test de l'upload de médias...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer une image de test
    img_bytes = create_test_image()
    
    # Préparer les données pour l'upload
    files = {
        'file': ('test_image.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'title': 'Image de test',
        'description': 'Image créée automatiquement pour les tests'
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/media/upload/",
            files=files,
            data=data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 201:
            media_data = response.json()
            print(f"✅ Média uploadé avec succès!")
            print(f"📸 ID: {media_data.get('id')}")
            print(f"📸 URL: {media_data.get('file')}")
            return media_data
        else:
            print(f"❌ Erreur upload média: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors de l'upload: {str(e)}")
        return None

def test_live_streaming(token):
    """Test du live streaming"""
    print("\n🔴 Test du live streaming...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    live_data = {
        "title": "Test de live streaming",
        "description": "Test automatique du live streaming",
        "is_public": True
    }
    
    try:
        # Démarrer un live
        response = requests.post(
            f"{API_URL}/posts/live/start/",
            json=live_data,
            headers=headers
        )
        
        print(f"Status start live: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 201:
            live_data = response.json()
            live_id = live_data.get('id')
            print(f"✅ Live démarré avec succès!")
            print(f"🔴 ID: {live_id}")
            
            # Arrêter le live
            stop_response = requests.put(
                f"{API_URL}/posts/live/{live_id}/stop/",
                headers=headers
            )
            
            print(f"Status stop live: {stop_response.status_code}")
            if stop_response.status_code == 200:
                print(f"✅ Live arrêté avec succès!")
                return True
            else:
                print(f"❌ Erreur arrêt live: {stop_response.status_code}")
                return False
        else:
            print(f"❌ Erreur démarrage live: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors du live: {str(e)}")
        return False

def test_post_with_media(token, media_id):
    """Test de création d'un post avec média"""
    print("\n📝 Test de création de post avec média...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Post de test avec image uploadée via API ! 📸",
        "post_type": "info",
        "is_anonymous": False,
        "media_files": [media_id]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/",
            json=post_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post avec média créé avec succès!")
            print(f"📝 ID: {post_data.get('id')}")
            return True
        else:
            print(f"❌ Erreur création post avec média: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors de la création: {str(e)}")
        return False

def test_media_endpoints(token):
    """Test des endpoints de médias"""
    print("\n📋 Test des endpoints de médias...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Lister les médias
    try:
        response = requests.get(f"{API_URL}/posts/media/", headers=headers)
        print(f"Status GET media: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            media_count = len(data.get('results', []))
            print(f"✅ {media_count} médias récupérés")
            return True
        else:
            print(f"❌ Erreur récupération médias: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors de la récupération: {str(e)}")
        return False

def main():
    """Test complet des fonctionnalités médias"""
    print("🚀 Test des fonctionnalités médias et live streaming")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Test upload média
    media_data = test_media_upload(token)
    
    # Test live streaming
    live_ok = test_live_streaming(token)
    
    # Test post avec média
    post_with_media_ok = False
    if media_data:
        post_with_media_ok = test_post_with_media(token, media_data.get('id'))
    
    # Test endpoints médias
    media_endpoints_ok = test_media_endpoints(token)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS MÉDIAS")
    print("=" * 60)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"📸 Upload Média: {'✅' if media_data else '❌'}")
    print(f"🔴 Live Streaming: {'✅' if live_ok else '❌'}")
    print(f"📝 Post avec Média: {'✅' if post_with_media_ok else '❌'}")
    print(f"📋 Endpoints Médias: {'✅' if media_endpoints_ok else '❌'}")
    
    if all([token, media_data, live_ok, post_with_media_ok, media_endpoints_ok]):
        print("\n🎉 TOUS LES TESTS MÉDIAS SONT PASSÉS!")
        print("Les fonctionnalités médias sont 100% fonctionnelles!")
    else:
        print("\n⚠️ Certains tests médias ont échoué")
        print("Vérifiez les logs ci-dessus pour plus de détails")

if __name__ == "__main__":
    main() 
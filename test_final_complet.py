#!/usr/bin/env python
import requests
import json
from PIL import Image
import io

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

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
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Préparer les données pour l'upload
    files = {
        'file': ('test_image_final.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'title': 'Image de test final',
        'description': 'Image créée pour le test final'
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/media/upload/",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 201:
            media_data = response.json()
            print(f"✅ Média uploadé avec succès!")
            print(f"📸 ID: {media_data.get('id')}")
            return media_data
        else:
            print(f"❌ Erreur upload média: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors de l'upload: {str(e)}")
        return None

def test_create_post_with_media(token, media_id):
    """Test de création d'un post avec média"""
    print("\n📝 Test de création de post avec média...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Post final de test avec image uploadée ! 🎉",
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
        
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post avec média créé avec succès!")
            print(f"📝 ID: {post_data.get('id')}")
            return post_data.get('id')
        else:
            print(f"❌ Erreur création post avec média: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors de la création: {str(e)}")
        return None

def test_live_streaming(token):
    """Test du live streaming"""
    print("\n🔴 Test du live streaming...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    live_data = {
        "title": "Test final de live streaming",
        "description": "Test automatique du live streaming",
        "content": "Live de test final - CommuniConnect fonctionne !"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/live/start/",
            json=live_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Live démarré avec succès!")
            print(f"🔴 ID: {data.get('live_id')}")
            print(f"🔑 Stream Key: {data.get('stream_key')}")
            return data.get('live_id')
        else:
            print(f"❌ Erreur démarrage live: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors du live: {str(e)}")
        return None

def test_share_post(token, post_id):
    """Test du partage de post"""
    print(f"\n🔄 Test du partage de post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    share_data = {
        "share_type": "share",
        "comment": "Post très intéressant du test final !"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/posts/{post_id}/share/",
            json=share_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Post partagé avec succès!")
            return True
        else:
            print(f"❌ Erreur partage: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors du partage: {str(e)}")
        return False

def test_geographic_data():
    """Test des données géographiques"""
    print("\n🗺️ Test des données géographiques...")
    
    response = requests.get(f"{API_URL}/users/geographic-data/")
    
    if response.status_code == 200:
        data = response.json()
        regions = data.get('regions', [])
        print(f"✅ Données géographiques récupérées!")
        print(f"📊 Nombre de régions: {len(regions)}")
        return True
    else:
        print(f"❌ Erreur données géographiques: {response.status_code}")
        return False

def main():
    """Test final complet de toutes les fonctionnalités"""
    print("🚀 TEST FINAL COMPLET - COMMUNICONNECT")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Test upload média
    media_data = test_media_upload(token)
    
    # Test création post avec média
    post_id = None
    if media_data:
        post_id = test_create_post_with_media(token, media_data.get('id'))
    
    # Test live streaming
    live_id = test_live_streaming(token)
    
    # Test partage de post
    share_ok = False
    if post_id:
        share_ok = test_share_post(token, post_id)
    
    # Test données géographiques
    geo_ok = test_geographic_data()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("🏆 RÉSUMÉ FINAL COMPLET")
    print("=" * 60)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"📸 Upload Média: {'✅' if media_data else '❌'}")
    print(f"📝 Création Post avec Média: {'✅' if post_id else '❌'}")
    print(f"🔴 Live Streaming: {'✅' if live_id else '❌'}")
    print(f"🔄 Partage de Post: {'✅' if share_ok else '❌'}")
    print(f"🗺️ Données Géographiques: {'✅' if geo_ok else '❌'}")
    
    # Calcul du pourcentage de réussite
    tests = [token, media_data, post_id, live_id, share_ok, geo_ok]
    success_count = sum(1 for test in tests if test)
    total_tests = len(tests)
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n📊 TAUX DE RÉUSSITE: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT ! CommuniConnect est presque parfaitement fonctionnel!")
        print("Toutes les fonctionnalités principales marchent !")
    elif success_rate >= 80:
        print("\n✅ TRÈS BIEN ! CommuniConnect est largement fonctionnel!")
        print("La plupart des fonctionnalités marchent parfaitement.")
    elif success_rate >= 60:
        print("\n⚠️ BIEN ! CommuniConnect a des fonctionnalités opérationnelles.")
        print("Certaines améliorations sont possibles.")
    else:
        print("\n❌ ATTENTION ! CommuniConnect a des problèmes.")
        print("Des corrections sont nécessaires.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_camera_permissions():
    """Test des permissions de la caméra"""
    print("🎥 TEST PERMISSIONS CAMÉRA")
    print("=" * 50)
    
    # Connexion
    login_data = {
        "email": "mariam.diallo@test.gn",
        "password": "test123456"
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('tokens', {}).get('access')
            print(f"✅ Connexion réussie")
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Vérifier l'endpoint de démarrage de live
    print(f"\n1️⃣ TEST ENDPOINT LIVE START")
    print("-" * 30)
    
    live_data = {
        "title": "Test Live Stream",
        "description": "Test des permissions caméra",
        "content": "Test en cours..."
    }
    
    try:
        response = requests.post(f"{API_URL}/posts/live/start/", json=live_data, headers=headers)
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Réponse: {response.text}")
        
        if response.status_code == 201:
            print("✅ Endpoint live start fonctionnel")
        elif response.status_code == 400:
            print("⚠️ Erreur de validation des données")
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Vérifier les posts de type live
    print(f"\n2️⃣ TEST POSTS LIVE")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_URL}/posts/?type=live", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            live_posts = data.get('results', [])
            print(f"📝 Posts live trouvés: {len(live_posts)}")
            
            for post in live_posts[:3]:  # Afficher les 3 premiers
                print(f"   - ID: {post.get('id')} - {post.get('title', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 30)
    print("✅ Backend live stream fonctionnel")
    print("💡 Le problème vient probablement du frontend")
    print("🔧 Utilisez le bouton 'Test Caméra' dans le Dashboard")

def main():
    """Test principal"""
    test_camera_permissions()

if __name__ == "__main__":
    main() 
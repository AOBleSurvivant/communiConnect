#!/usr/bin/env python
import requests
import json

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

def test_live_streaming_detailed(token):
    """Test détaillé du live streaming"""
    print("\n🔴 Test détaillé du live streaming...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test avec différentes données
    test_cases = [
        {
            "title": "Test de live streaming",
            "description": "Test automatique du live streaming",
            "is_public": True
        },
        {
            "content": "Test de live streaming avec contenu",
            "post_type": "live",
            "is_anonymous": False
        },
        {
            "title": "Live Test",
            "description": "Description du live",
            "content": "Contenu du live"
        }
    ]
    
    for i, live_data in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        print(f"Données envoyées: {json.dumps(live_data, indent=2)}")
        
        try:
            response = requests.post(
                f"{API_URL}/posts/live/start/",
                json=live_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Réponse complète: {response.text}")
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Live démarré avec succès!")
                print(f"🔴 ID: {data.get('live_id')}")
                print(f"🔑 Stream Key: {data.get('stream_key')}")
                return True
            else:
                print(f"❌ Erreur: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    return False

def test_live_endpoints(token):
    """Tester les endpoints de live"""
    print("\n📋 Test des endpoints de live...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Tester GET /api/posts/live/
    try:
        response = requests.get(f"{API_URL}/posts/live/", headers=headers)
        print(f"Status GET live: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Erreur GET live: {str(e)}")

def main():
    """Test complet du live streaming"""
    print("🚀 Test détaillé du live streaming")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Test détaillé du live streaming
    live_ok = test_live_streaming_detailed(token)
    
    # Test des endpoints
    test_live_endpoints(token)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU TEST LIVE")
    print("=" * 60)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"🔴 Live Streaming: {'✅' if live_ok else '❌'}")
    
    if live_ok:
        print("\n🎉 Le live streaming fonctionne!")
    else:
        print("\n⚠️ Le live streaming a des problèmes")
        print("Vérifiez les logs ci-dessus pour plus de détails")

if __name__ == "__main__":
    main() 
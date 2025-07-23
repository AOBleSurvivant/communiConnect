#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def nettoyer_streams_camera():
    """Nettoyer les streams de caméra bloqués"""
    print("🧹 NETTOYAGE STREAMS CAMÉRA")
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
    
    # Vérifier les lives actifs
    print(f"\n📺 VÉRIFICATION LIVES ACTIFS")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_URL}/posts/?type=live", headers=headers)
        if response.status_code == 200:
            data = response.json()
            live_posts = data.get('results', [])
            
            print(f"📊 Lives trouvés: {len(live_posts)}")
            
            for post in live_posts:
                print(f"   - ID: {post.get('id')} - {post.get('title', 'N/A')}")
                print(f"     Status: {post.get('is_live', False)}")
                
                # Arrêter les lives actifs
                if post.get('is_live', False):
                    try:
                        stop_response = requests.post(f"{API_URL}/posts/live/{post.get('id')}/stop/", headers=headers)
                        if stop_response.status_code == 200:
                            print(f"     ✅ Live arrêté")
                        else:
                            print(f"     ❌ Erreur arrêt: {stop_response.status_code}")
                    except Exception as e:
                        print(f"     ❌ Erreur: {e}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n💡 INSTRUCTIONS POUR L'UTILISATEUR:")
    print("=" * 40)
    print("1. Fermez complètement le navigateur")
    print("2. Redémarrez le navigateur")
    print("3. Allez sur http://localhost:3001")
    print("4. Testez la caméra avec le bouton 'Test Caméra'")
    print("5. Si le problème persiste, redémarrez l'ordinateur")

def main():
    """Test principal"""
    nettoyer_streams_camera()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_stop_live():
    """Tester l'arrêt de live"""
    print("🛑 TEST ARRÊT LIVE")
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
            
            if len(live_posts) == 0:
                print("❌ Aucun live actif trouvé")
                print("💡 Pour tester l'arrêt, démarrez d'abord un live")
                return
            
            for post in live_posts:
                print(f"   - ID: {post.get('id')} - {post.get('title', 'N/A')}")
                print(f"     Status: {post.get('is_live', False)}")
                print(f"     Live ID: {post.get('live_id', 'N/A')}")
                
                # Tester l'arrêt du live
                if post.get('is_live', False) and post.get('live_id'):
                    print(f"\n🛑 TEST ARRÊT LIVE ID: {post.get('live_id')}")
                    print("-" * 30)
                    
                    try:
                        stop_response = requests.put(f"{API_URL}/posts/live/{post.get('live_id')}/stop/", headers=headers)
                        print(f"📊 Status Code: {stop_response.status_code}")
                        print(f"📊 Response: {stop_response.text}")
                        
                        if stop_response.status_code == 200:
                            print("✅ Live arrêté avec succès")
                        else:
                            print(f"❌ Erreur arrêt: {stop_response.status_code}")
                            
                    except Exception as e:
                        print(f"❌ Erreur: {e}")
                        
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n💡 INSTRUCTIONS POUR L'UTILISATEUR:")
    print("=" * 40)
    print("1. Si aucun live actif, démarrez un live d'abord")
    print("2. Utilisez le bouton 'Arrêt forcé' dans l'interface")
    print("3. Vérifiez la console du navigateur pour les logs")
    print("4. Si le problème persiste, redémarrez l'application")

def main():
    """Test principal"""
    test_stop_live()

if __name__ == "__main__":
    main() 
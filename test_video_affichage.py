#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_video_affichage():
    """Tester l'affichage de la vidéo après enregistrement"""
    print("🎥 TEST AFFICHAGE VIDÉO")
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
    
    # Vérifier les lives récents
    print(f"\n📺 VÉRIFICATION LIVES RÉCENTS")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_URL}/posts/?type=info&is_live_post=false", headers=headers)
        if response.status_code == 200:
            data = response.json()
            recent_posts = data.get('results', [])
            
            print(f"📊 Posts récents trouvés: {len(recent_posts)}")
            
            # Chercher des posts qui étaient des lives
            live_posts = [p for p in recent_posts if p.get('content', '').startswith('Live')]
            
            if len(live_posts) > 0:
                print(f"🎯 Posts de live trouvés: {len(live_posts)}")
                
                for i, post in enumerate(live_posts[:3]):  # Afficher les 3 premiers
                    print(f"   {i+1}. ID: {post.get('id')} - {post.get('content', 'N/A')}")
                    print(f"      Créé: {post.get('created_at', 'N/A')}")
                    print(f"      Auteur: {post.get('author', {}).get('first_name', 'N/A')}")
            else:
                print("❌ Aucun post de live trouvé")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n💡 DIAGNOSTIC AFFICHAGE VIDÉO:")
    print("=" * 40)
    print("1. Vérifiez que la vidéo est bien enregistrée")
    print("2. Regardez les logs dans la console F12")
    print("3. Cherchez le message '✅ Vidéo configurée pour la lecture'")
    print("4. Vérifiez que recordedVideo est défini")
    print("5. Vérifiez que videoDuration > 0")
    print("6. Assurez-vous que l'interface affiche les contrôles de lecture")

def main():
    """Test principal"""
    test_video_affichage()

if __name__ == "__main__":
    main() 
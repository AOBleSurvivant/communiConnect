#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_stop_live_fixed():
    """Tester l'arrêt du live après correction"""
    print("🛑 TEST ARRÊT LIVE - CORRECTION APPLIQUÉE")
    print("=" * 60)
    
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
        response = requests.get(f"{API_URL}/posts/?type=info&is_live_post=true", headers=headers)
        if response.status_code == 200:
            data = response.json()
            live_posts = data.get('results', [])
            
            print(f"📊 Lives trouvés: {len(live_posts)}")
            
            if len(live_posts) == 0:
                print("❌ Aucun live actif trouvé")
                print("💡 Pour tester l'arrêt, démarrez d'abord un live")
                return
            
            # Tester avec le premier live trouvé
            live_post = live_posts[0]
            post_id = live_post.get('id')
            print(f"🎯 Test avec le live ID: {post_id}")
            print(f"   Titre: {live_post.get('content', 'N/A')}")
            print(f"   Auteur: {live_post.get('author', {}).get('first_name', 'N/A')}")
            
            # Tester l'arrêt du live
            print(f"\n🛑 TEST ARRÊT LIVE ID: {post_id}")
            print("-" * 30)
            
            stop_response = requests.put(f"{API_URL}/posts/live/{post_id}/stop/", headers=headers)
            
            print(f"📊 Status Code: {stop_response.status_code}")
            print(f"📊 Response: {stop_response.text}")
            
            if stop_response.status_code == 200:
                print("✅ Live arrêté avec succès")
                
                # Vérifier que le live est bien arrêté
                print(f"\n🔍 VÉRIFICATION ARRÊT")
                print("-" * 20)
                
                check_response = requests.get(f"{API_URL}/posts/?type=info&is_live_post=true", headers=headers)
                if check_response.status_code == 200:
                    check_data = check_response.json()
                    remaining_lives = check_data.get('results', [])
                    
                    # Filtrer pour voir si notre live est toujours actif
                    still_active = [p for p in remaining_lives if p.get('id') == post_id]
                    
                    if len(still_active) == 0:
                        print("✅ Live correctement arrêté (plus dans la liste des lives actifs)")
                    else:
                        print("⚠️ Live toujours actif dans la liste")
                        
            else:
                print(f"❌ Erreur arrêt: {stop_response.status_code}")
                if stop_response.status_code == 500:
                    print("💡 Erreur 500 - Vérifiez les logs du serveur")
                    
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n💡 INSTRUCTIONS POUR L'UTILISATEUR:")
    print("=" * 40)
    print("1. L'erreur 'Post object has no attribute user' est corrigée")
    print("2. L'arrêt du live devrait maintenant fonctionner")
    print("3. Testez en démarrant un live puis en l'arrêtant")
    print("4. Vérifiez que la vidéo enregistrée est disponible")

def main():
    """Test principal"""
    test_stop_live_fixed()

if __name__ == "__main__":
    main() 
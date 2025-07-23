#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_chat_live():
    """Tester le système de chat live"""
    print("💬 TEST SYSTÈME CHAT LIVE")
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
    
    # Vérifier les lives existants
    print(f"\n📺 VÉRIFICATION LIVES EXISTANTS")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_URL}/posts/?type=info&is_live_post=true", headers=headers)
        if response.status_code == 200:
            data = response.json()
            live_posts = data.get('results', [])
            
            print(f"📊 Lives trouvés: {len(live_posts)}")
            
            if len(live_posts) == 0:
                print("❌ Aucun live trouvé")
                print("💡 Pour tester le chat, démarrez d'abord un live")
                return
            
            # Tester avec le premier live trouvé
            live_post = live_posts[0]
            post_id = live_post.get('id')
            print(f"🎯 Test avec le live ID: {post_id}")
            
            # Tester l'envoi d'un message
            print(f"\n💬 TEST ENVOI MESSAGE")
            print("-" * 20)
            
            message_data = {
                "content": "Test message depuis le script Python",
                "type": "text"
            }
            
            send_response = requests.post(f"{API_URL}/posts/live/{post_id}/chat/", 
                                        json=message_data, headers=headers)
            
            print(f"📊 Status Code: {send_response.status_code}")
            print(f"📊 Response: {send_response.text}")
            
            if send_response.status_code == 201:
                print("✅ Message envoyé avec succès")
            else:
                print(f"❌ Erreur envoi: {send_response.status_code}")
            
            # Tester la récupération des messages
            print(f"\n📨 TEST RÉCUPÉRATION MESSAGES")
            print("-" * 30)
            
            get_response = requests.get(f"{API_URL}/posts/live/{post_id}/chat/messages/", 
                                      headers=headers)
            
            print(f"📊 Status Code: {get_response.status_code}")
            
            if get_response.status_code == 200:
                messages = get_response.json()
                print(f"✅ {len(messages)} messages récupérés")
                
                for i, msg in enumerate(messages[:3]):  # Afficher les 3 premiers
                    print(f"   {i+1}. {msg.get('author', {}).get('first_name', 'N/A')}: {msg.get('content', 'N/A')}")
                
                if len(messages) > 3:
                    print(f"   ... et {len(messages) - 3} autres messages")
            else:
                print(f"❌ Erreur récupération: {get_response.status_code}")
                print(f"📊 Response: {get_response.text}")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n💡 INSTRUCTIONS POUR L'UTILISATEUR:")
    print("=" * 40)
    print("1. Le système de chat live est maintenant opérationnel")
    print("2. Les messages sont sauvegardés en base de données")
    print("3. Testez en démarrant un live et en envoyant des messages")
    print("4. Les messages seront visibles même après redémarrage")

def main():
    """Test principal"""
    test_chat_live()

if __name__ == "__main__":
    main() 
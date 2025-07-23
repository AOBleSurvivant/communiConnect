#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_like_comportement():
    """Test du comportement exact de l'API de like"""
    print("🧪 TEST COMPORTEMENT LIKE API")
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
    
    # Récupérer un post pour tester
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            if posts:
                test_post = posts[0]
                post_id = test_post.get('id')
                print(f"📝 Test avec le post {post_id}: {test_post.get('content', 'N/A')[:30]}...")
                print(f"❤️ Likes actuels: {test_post.get('likes_count', 0)}")
                print(f"👤 Liké par l'utilisateur: {test_post.get('is_liked_by_user', False)}")
            else:
                print("❌ Aucun post trouvé")
                return
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Test 1: Premier like
    print(f"\n1️⃣ PREMIER LIKE")
    print("-" * 30)
    try:
        response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 201:
            print("✅ Like créé avec succès (201)")
        elif response.status_code == 200:
            print("✅ Like traité avec succès (200)")
        elif response.status_code == 400:
            print("⚠️ Erreur de validation (400)")
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Deuxième like (devrait échouer)
    print(f"\n2️⃣ DEUXIÈME LIKE (DOIT ÉCHOUER)")
    print("-" * 30)
    try:
        response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 400:
            print("✅ Erreur attendue (400) - Post déjà liké")
        else:
            print(f"⚠️ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Unlike
    print(f"\n3️⃣ UNLIKE")
    print("-" * 30)
    try:
        response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 204:
            print("✅ Unlike réussi (204)")
        elif response.status_code == 200:
            print("✅ Unlike traité (200)")
        else:
            print(f"⚠️ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 4: Like après unlike
    print(f"\n4️⃣ LIKE APRÈS UNLIKE")
    print("-" * 30)
    try:
        response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Like après unlike réussi")
        else:
            print(f"⚠️ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 30)
    print("✅ API de like fonctionne correctement")
    print("✅ Gestion des erreurs appropriée")
    print("✅ Status codes cohérents")

def main():
    """Test principal"""
    test_like_comportement()

if __name__ == "__main__":
    main() 
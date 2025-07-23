#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def obtenir_token():
    """Obtenir un token d'authentification"""
    login_data = {
        "email": "mariam.diallo@test.gn",
        "password": "test123456"
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('tokens', {}).get('access')
            print(f"✅ Connexion réussie, token obtenu")
            return token
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def verifier_post_411(token):
    """Vérifier si le post 411 existe et tester les likes"""
    print("🔍 VÉRIFICATION POST 411")
    print("=" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Vérifier si le post 411 existe
    try:
        response = requests.get(f"{API_URL}/posts/411/", headers=headers)
        print(f"📊 Status post 411: {response.status_code}")
        
        if response.status_code == 200:
            post = response.json()
            print(f"✅ Post 411 trouvé: {post.get('content', 'N/A')[:50]}...")
            print(f"📝 Auteur: {post.get('author', {}).get('first_name', 'N/A')}")
            print(f"❤️ Likes: {post.get('likes_count', 0)}")
            
            # Test 2: Tester le like sur le post 411
            try:
                like_response = requests.post(f"{API_URL}/posts/411/like/", headers=headers)
                print(f"📊 Status like post 411: {like_response.status_code}")
                
                if like_response.status_code == 200:
                    like_data = like_response.json()
                    print(f"✅ Like réussi: {like_data}")
                elif like_response.status_code == 400:
                    print(f"⚠️ Post déjà liké ou erreur de validation")
                    print(f"📝 Réponse: {like_response.text}")
                else:
                    print(f"❌ Erreur like: {like_response.status_code}")
                    print(f"📝 Réponse: {like_response.text}")
                    
            except Exception as e:
                print(f"❌ Erreur lors du like: {e}")
                
        elif response.status_code == 404:
            print(f"❌ Post 411 n'existe pas")
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

def lister_posts_disponibles(token):
    """Lister les posts disponibles"""
    print("\n📝 POSTS DISPONIBLES")
    print("=" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            print(f"📊 Total posts: {len(posts)}")
            
            for i, post in enumerate(posts[:5]):  # Afficher les 5 premiers
                print(f"{i+1}. Post ID: {post.get('id')} - {post.get('content', 'N/A')[:30]}...")
                
            if len(posts) > 5:
                print(f"... et {len(posts) - 5} autres posts")
                
            # Retourner le premier post pour test
            if posts:
                return posts[0].get('id')
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    return None

def tester_like_post(post_id, token):
    """Tester le like sur un post spécifique"""
    print(f"\n❤️ TEST LIKE POST {post_id}")
    print("=" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        like_response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        print(f"📊 Status like post {post_id}: {like_response.status_code}")
        
        if like_response.status_code == 200:
            like_data = like_response.json()
            print(f"✅ Like réussi: {like_data}")
        elif like_response.status_code == 400:
            print(f"⚠️ Post déjà liké ou erreur de validation")
            print(f"📝 Réponse: {like_response.text}")
        else:
            print(f"❌ Erreur like: {like_response.status_code}")
            print(f"📝 Réponse: {like_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du like: {e}")

def main():
    """Test principal"""
    print("🧪 TEST POST 411 ET LIKES")
    print("=" * 50)
    
    # Obtenir un token
    token = obtenir_token()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier le post 411
    post_411_ok = verifier_post_411(token)
    
    # Lister les posts disponibles
    premier_post_id = lister_posts_disponibles(token)
    
    # Tester le like sur le premier post disponible
    if premier_post_id:
        tester_like_post(premier_post_id, token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 30)
    if post_411_ok:
        print("✅ Post 411 existe et est testable")
    else:
        print("❌ Post 411 n'existe pas")
        if premier_post_id:
            print(f"✅ Testé le like sur le post {premier_post_id} à la place")

if __name__ == "__main__":
    main() 
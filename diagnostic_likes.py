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

def verifier_posts_avec_likes(token):
    """Vérifier les posts avec likes"""
    print("\n❤️ VÉRIFICATION POSTS AVEC LIKES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            posts_avec_likes = [p for p in posts if p.get('likes_count', 0) > 0]
            print(f"📋 Posts avec likes: {len(posts_avec_likes)}")
            
            for post in posts_avec_likes[:5]:
                print(f"\n📝 Post ID: {post.get('id')}")
                print(f"   Contenu: {post.get('content', '')[:50]}...")
                print(f"   Likes count: {post.get('likes_count', 0)}")
                print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")
                
                # Vérifier les likes détaillés
                likes = post.get('likes', [])
                if likes:
                    print(f"   📊 Likes détaillés:")
                    for like in likes[:3]:
                        print(f"      - User: {like.get('user', {}).get('username', 'Inconnu')}")
                        print(f"        Date: {like.get('created_at')}")
            
            # Afficher un post sans likes pour test
            posts_sans_likes = [p for p in posts if p.get('likes_count', 0) == 0]
            if posts_sans_likes:
                test_post = posts_sans_likes[0]
                print(f"\n🧪 POST DE TEST (sans likes):")
                print(f"   ID: {test_post.get('id')}")
                print(f"   Contenu: {test_post.get('content', '')[:50]}...")
                print(f"   Likes count: {test_post.get('likes_count', 0)}")
                print(f"   Is liked by user: {test_post.get('is_liked_by_user', False)}")
                return test_post.get('id')
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_like_post(token, post_id):
    """Tester le like d'un post"""
    print(f"\n❤️ TEST LIKE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Tester le like
        response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Like ajouté avec succès")
            print(f"📊 Données retournées: {data}")
            return True
        else:
            print(f"❌ Erreur ajout like: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def tester_unlike_post(token, post_id):
    """Tester l'unlike d'un post"""
    print(f"\n💔 TEST UNLIKE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Tester l'unlike
        response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        
        if response.status_code == 204:
            print(f"✅ Unlike réussi")
            return True
        else:
            print(f"❌ Erreur unlike: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def verifier_etat_post_apres_like(token, post_id):
    """Vérifier l'état du post après like/unlike"""
    print(f"\n🔍 VÉRIFICATION ÉTAT POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
        
        if response.status_code == 200:
            post = response.json()
            print(f"📝 Post ID: {post.get('id')}")
            print(f"   Likes count: {post.get('likes_count', 0)}")
            print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")
            
            # Vérifier les likes détaillés
            likes = post.get('likes', [])
            print(f"   📊 Nombre de likes détaillés: {len(likes)}")
            
            for like in likes:
                print(f"      - User: {like.get('user', {}).get('username', 'Inconnu')}")
                print(f"        Date: {like.get('created_at')}")
            
            return post
        else:
            print(f"❌ Erreur récupération post: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_endpoints_likes():
    """Vérifier les endpoints de likes"""
    print("\n🔗 VÉRIFICATION ENDPOINTS LIKES")
    print("=" * 60)
    
    endpoints = [
        f"{API_URL}/posts/1/like/",
        f"{API_URL}/posts/1/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)}")

def main():
    """Diagnostic complet du système de likes"""
    print("❤️ DIAGNOSTIC SYSTÈME DE LIKES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier les endpoints
    verifier_endpoints_likes()
    
    # Vérifier les posts avec likes
    post_id = verifier_posts_avec_likes(token)
    
    if post_id:
        # Tester le like
        like_success = tester_like_post(token, post_id)
        
        if like_success:
            # Vérifier l'état après like
            verifier_etat_post_apres_like(token, post_id)
            
            # Tester l'unlike
            unlike_success = tester_unlike_post(token, post_id)
            
            if unlike_success:
                # Vérifier l'état après unlike
                verifier_etat_post_apres_like(token, post_id)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ Posts récupérés")
    print(f"✅ Endpoints likes vérifiés")
    print(f"✅ Tests like/unlike effectués")
    print(f"💡 Si les likes ne fonctionnent pas:")
    print(f"   1. Vérifiez les endpoints API")
    print(f"   2. Vérifiez la base de données")
    print(f"   3. Vérifiez les permissions")
    print(f"   4. Vérifiez le frontend")

if __name__ == "__main__":
    main() 
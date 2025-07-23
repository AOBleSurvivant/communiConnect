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

def verifier_posts_recents(token):
    """Vérifier les posts récents"""
    print("\n📝 VÉRIFICATION POSTS RÉCENTS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            print(f"📋 Total posts: {len(posts)}")
            
            if posts:
                print(f"\n📊 5 DERNIERS POSTS:")
                for i, post in enumerate(posts[:5]):
                    print(f"\n{i+1}. 📝 Post ID: {post.get('id')}")
                    print(f"   Auteur: {post.get('author', {}).get('username', 'Inconnu')}")
                    print(f"   Contenu: {post.get('content', '')[:100]}...")
                    print(f"   Type: {post.get('post_type', 'info')}")
                    print(f"   Date: {post.get('created_at', 'Inconnue')}")
                    print(f"   Médias: {len(post.get('media_files', []))}")
                    print(f"   Likes: {post.get('likes_count', 0)}")
                    print(f"   Commentaires: {post.get('comments_count', 0)}")
                    print(f"   Vues: {post.get('views_count', 0)}")
                    
                    # Vérifier les médias
                    media_files = post.get('media_files', [])
                    if media_files:
                        print(f"   📸 Médias:")
                        for media in media_files:
                            print(f"      - ID: {media.get('id')}")
                            print(f"        Type: {media.get('media_type')}")
                            print(f"        Titre: {media.get('title')}")
                            print(f"        URL: {media.get('file_url')}")
                            print(f"        URL complète: {media.get('file')}")
                            
                            # Tester l'accessibilité
                            if media.get('file'):
                                try:
                                    img_response = requests.head(media['file'])
                                    print(f"        ✅ Accessible: {img_response.status_code}")
                                except Exception as e:
                                    print(f"        ❌ Erreur: {str(e)}")
            else:
                print("❌ Aucun post trouvé")
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def tester_creation_post_simple(token):
    """Tester la création d'un post simple sans média"""
    print("\n📝 TEST CRÉATION POST SIMPLE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Test de post simple sans image - Vérification affichage ! 🔍",
        "post_type": "info",
        "is_anonymous": False
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/",
            json=post_data,
            headers=headers
        )
        
        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data.get('id')
            print(f"✅ Post simple créé - ID: {post_id}")
            print(f"   Contenu: {post_data.get('content')}")
            print(f"   Auteur: {post_data.get('author', {}).get('username')}")
            print(f"   Date: {post_data.get('created_at')}")
            return post_id
        else:
            print(f"❌ Erreur création post: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_creation_post_avec_image(token):
    """Tester la création d'un post avec image"""
    print("\n📸 TEST CRÉATION POST AVEC IMAGE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer une image de test
    from PIL import Image
    import io
    
    img = Image.new('RGB', (400, 300), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {
        'file': ('test_verification.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'title': 'Image de test vérification',
        'description': 'Test pour vérifier l\'affichage des posts avec images'
    }
    
    try:
        # Upload de l'image
        response = requests.post(
            f"{API_URL}/posts/media/upload/",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 201:
            media_data = response.json()
            media_id = media_data.get('id')
            print(f"✅ Upload réussi - ID: {media_id}")
            
            # Créer un post avec l'image
            post_data = {
                "content": "Test de post avec image - Vérification affichage ! 📸",
                "post_type": "info",
                "is_anonymous": False,
                "media_files": [media_id]
            }
            
            headers_json = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{API_URL}/posts/",
                json=post_data,
                headers=headers_json
            )
            
            if response.status_code == 201:
                post_data = response.json()
                post_id = post_data.get('id')
                print(f"✅ Post avec image créé - ID: {post_id}")
                
                # Vérifier les médias du post
                media_files = post_data.get('media_files', [])
                print(f"   Médias dans le post: {len(media_files)}")
                
                for media in media_files:
                    print(f"     📸 Média ID: {media.get('id')}")
                    print(f"        URL: {media.get('file_url')}")
                    print(f"        URL complète: {media.get('file')}")
                
                return post_id
            else:
                print(f"❌ Erreur création post: {response.status_code}")
                print(f"Réponse: {response.text}")
                return None
        else:
            print(f"❌ Erreur upload: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_api_endpoints():
    """Vérifier les endpoints API"""
    print("\n🔗 VÉRIFICATION ENDPOINTS API")
    print("=" * 60)
    
    endpoints = [
        f"{API_URL}/health/",
        f"{API_URL}/posts/",
        f"{API_URL}/users/",
        f"{BASE_URL}/admin/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)}")

def verifier_frontend_access():
    """Vérifier l'accès au frontend"""
    print("\n🌐 VÉRIFICATION ACCÈS FRONTEND")
    print("=" * 60)
    
    frontend_urls = [
        "http://localhost:3002",
        "http://127.0.0.1:3002"
    ]
    
    for url in frontend_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: Erreur - {str(e)}")

def main():
    """Vérification complète du système"""
    print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier les endpoints API
    verifier_api_endpoints()
    
    # Vérifier l'accès frontend
    verifier_frontend_access()
    
    # Vérifier les posts récents
    verifier_posts_recents(token)
    
    # Tester création post simple
    post_simple_id = tester_creation_post_simple(token)
    
    # Tester création post avec image
    post_image_id = tester_creation_post_avec_image(token)
    
    # Vérifier à nouveau les posts
    print(f"\n🔄 VÉRIFICATION FINALE")
    print("=" * 60)
    verifier_posts_recents(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ API accessible")
    print(f"✅ Posts récupérés")
    print(f"✅ Post simple créé: {'Oui' if post_simple_id else 'Non'}")
    print(f"✅ Post avec image créé: {'Oui' if post_image_id else 'Non'}")
    print(f"💡 Si vous ne voyez rien, vérifiez:")
    print(f"   1. Le frontend est-il démarré sur http://localhost:3002 ?")
    print(f"   2. Les posts apparaissent-ils dans la console ?")
    print(f"   3. Y a-t-il des erreurs dans la console du navigateur ?")

if __name__ == "__main__":
    main() 
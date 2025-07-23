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

def examiner_posts_avec_images(token):
    """Examiner les posts avec images"""
    print("\n📸 EXAMEN DES POSTS AVEC IMAGES")
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
            
            posts_avec_images = []
            for post in posts:
                media_files = post.get('media_files', [])
                if media_files:
                    posts_avec_images.append(post)
                    print(f"\n📝 Post ID: {post.get('id')}")
                    print(f"   Contenu: {post.get('content', '')[:50]}...")
                    print(f"   Médias: {len(media_files)} fichiers")
                    
                    for media in media_files:
                        print(f"     📸 Média ID: {media.get('id')}")
                        print(f"        Type: {media.get('media_type')}")
                        print(f"        Titre: {media.get('title')}")
                        print(f"        URL: {media.get('file_url')}")
                        print(f"        CDN URL: {media.get('cdn_url')}")
                        print(f"        Thumbnail: {media.get('thumbnail_url')}")
                        
                        # Tester l'accessibilité de l'URL
                        if media.get('file_url'):
                            test_url = f"{BASE_URL}{media['file_url']}"
                            try:
                                img_response = requests.head(test_url)
                                print(f"        ✅ Accessible: {img_response.status_code}")
                            except Exception as e:
                                print(f"        ❌ Erreur accès: {str(e)}")
            
            print(f"\n📊 STATISTIQUES:")
            print(f"   Posts avec images: {len(posts_avec_images)}")
            print(f"   Posts total: {len(posts)}")
            
            return posts_avec_images
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def examiner_media_direct(token):
    """Examiner directement les médias"""
    print("\n📸 EXAMEN DIRECT DES MÉDIAS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/media/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            media_list = data.get('results', [])
            
            print(f"📋 Total médias: {len(media_list)}")
            
            for media in media_list:
                print(f"\n📸 Média ID: {media.get('id')}")
                print(f"   Titre: {media.get('title')}")
                print(f"   Type: {media.get('media_type')}")
                print(f"   File URL: {media.get('file_url')}")
                print(f"   CDN URL: {media.get('cdn_url')}")
                print(f"   Thumbnail: {media.get('thumbnail_url')}")
                
                # Tester l'accessibilité
                if media.get('file_url'):
                    test_url = f"{BASE_URL}{media['file_url']}"
                    try:
                        img_response = requests.head(test_url)
                        print(f"   ✅ Accessible: {img_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Erreur accès: {str(e)}")
            
            return media_list
            
        else:
            print(f"❌ Erreur récupération médias: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def tester_upload_image(token):
    """Tester l'upload d'une nouvelle image"""
    print("\n📤 TEST UPLOAD D'IMAGE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer une image de test
    from PIL import Image
    import io
    
    img = Image.new('RGB', (200, 200), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {
        'file': ('test_image_diagnostic.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'title': 'Image de test diagnostic',
        'description': 'Test pour diagnostiquer le problème d\'affichage'
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/media/upload/",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 201:
            media_data = response.json()
            print(f"✅ Upload réussi")
            print(f"   ID: {media_data.get('id')}")
            print(f"   URL: {media_data.get('file_url')}")
            print(f"   CDN URL: {media_data.get('cdn_url')}")
            
            # Tester l'accessibilité
            if media_data.get('file_url'):
                test_url = f"{BASE_URL}{media_data['file_url']}"
                try:
                    img_response = requests.head(test_url)
                    print(f"   ✅ Accessible: {img_response.status_code}")
                except Exception as e:
                    print(f"   ❌ Erreur accès: {str(e)}")
            
            return media_data.get('id')
        else:
            print(f"❌ Erreur upload: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception upload: {str(e)}")
        return None

def creer_post_avec_image(token, media_id):
    """Créer un post avec l'image uploadée"""
    print(f"\n📝 CRÉATION POST AVEC IMAGE {media_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Post de test pour diagnostiquer l'affichage des images ! 🔍",
        "post_type": "info",
        "is_anonymous": False,
        "media_files": [media_id]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/",
            json=post_data,
            headers=headers
        )
        
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post créé avec succès")
            print(f"   ID: {post_data.get('id')}")
            
            # Vérifier les médias du post
            media_files = post_data.get('media_files', [])
            print(f"   Médias: {len(media_files)}")
            
            for media in media_files:
                print(f"     📸 Média ID: {media.get('id')}")
                print(f"        URL: {media.get('file_url')}")
                print(f"        CDN URL: {media.get('cdn_url')}")
            
            return post_data.get('id')
        else:
            print(f"❌ Erreur création post: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception création post: {str(e)}")
        return None

def main():
    """Diagnostic complet des images"""
    print("🔍 DIAGNOSTIC DES PROBLÈMES D'IMAGES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Examiner les posts existants avec images
    posts_images = examiner_posts_avec_images(token)
    
    # Examiner directement les médias
    media_list = examiner_media_direct(token)
    
    # Tester l'upload d'une nouvelle image
    media_id = tester_upload_image(token)
    
    # Créer un post avec l'image
    if media_id:
        post_id = creer_post_avec_image(token, media_id)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DU DIAGNOSTIC:")
    print("=" * 60)
    print(f"   Posts avec images: {len(posts_images)}")
    print(f"   Médias total: {len(media_list)}")
    print(f"   Upload test: {'✅' if media_id else '❌'}")
    print(f"   Post test: {'✅' if media_id and post_id else '❌'}")

if __name__ == "__main__":
    main() 
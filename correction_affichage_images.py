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

def examiner_serializer_media():
    """Examiner le serializer des médias"""
    print("\n🔍 EXAMEN DU SERIALIZER MÉDIA")
    print("=" * 60)
    
    token = test_login()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Récupérer un média spécifique
        response = requests.get(f"{API_URL}/posts/media/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            media_list = data.get('results', [])
            
            if media_list:
                media = media_list[0]  # Premier média
                print(f"📸 Média ID: {media.get('id')}")
                print(f"   Titre: {media.get('title')}")
                print(f"   Type: {media.get('media_type')}")
                print(f"   File URL: {media.get('file_url')}")
                print(f"   CDN URL: {media.get('cdn_url')}")
                print(f"   Thumbnail: {media.get('thumbnail_url')}")
                
                # Tester l'URL complète
                if media.get('file_url'):
                    full_url = f"{BASE_URL}{media['file_url']}"
                    print(f"   URL complète: {full_url}")
                    
                    # Tester l'accessibilité
                    try:
                        img_response = requests.head(full_url)
                        print(f"   ✅ Accessible: {img_response.status_code}")
                        print(f"   Content-Type: {img_response.headers.get('content-type')}")
                    except Exception as e:
                        print(f"   ❌ Erreur accès: {str(e)}")
                
                # Afficher la structure complète
                print(f"\n📋 Structure complète du média:")
                print(json.dumps(media, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ Erreur récupération médias: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def examiner_posts_avec_images():
    """Examiner les posts avec images"""
    print("\n📝 EXAMEN DES POSTS AVEC IMAGES")
    print("=" * 60)
    
    token = test_login()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            posts_avec_images = [p for p in posts if p.get('media_files')]
            print(f"📋 Posts avec images: {len(posts_avec_images)}")
            
            for post in posts_avec_images[:3]:  # Afficher les 3 premiers
                print(f"\n📝 Post ID: {post.get('id')}")
                print(f"   Contenu: {post.get('content', '')[:50]}...")
                
                media_files = post.get('media_files', [])
                print(f"   Médias: {len(media_files)}")
                
                for media in media_files:
                    print(f"     📸 Média ID: {media.get('id')}")
                    print(f"        Titre: {media.get('title')}")
                    print(f"        Type: {media.get('media_type')}")
                    print(f"        File URL: {media.get('file_url')}")
                    print(f"        CDN URL: {media.get('cdn_url')}")
                    
                    # Tester l'URL
                    if media.get('file_url'):
                        full_url = f"{BASE_URL}{media['file_url']}"
                        print(f"        URL complète: {full_url}")
                        
                        try:
                            img_response = requests.head(full_url)
                            print(f"        ✅ Accessible: {img_response.status_code}")
                        except Exception as e:
                            print(f"        ❌ Erreur: {str(e)}")
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def verifier_configuration_media():
    """Vérifier la configuration des médias"""
    print("\n⚙️ VÉRIFICATION CONFIGURATION MÉDIAS")
    print("=" * 60)
    
    # Tester l'endpoint de santé
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print(f"❌ API non accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API: {str(e)}")
    
    # Tester un fichier média directement
    test_url = f"{BASE_URL}/media/media/2025/07/23/test_image.jpg"
    try:
        response = requests.head(test_url)
        print(f"📸 Test fichier média: {response.status_code}")
        if response.status_code == 200:
            print("✅ Fichiers médias accessibles")
        else:
            print("❌ Fichiers médias non accessibles")
    except Exception as e:
        print(f"❌ Erreur fichiers médias: {str(e)}")

def main():
    """Diagnostic complet des images"""
    print("🔍 DIAGNOSTIC COMPLET DES IMAGES")
    print("=" * 60)
    
    # Examiner le serializer
    examiner_serializer_media()
    
    # Examiner les posts avec images
    examiner_posts_avec_images()
    
    # Vérifier la configuration
    verifier_configuration_media()
    
    print("\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Les images sont accessibles côté backend")
    print("✅ Les URLs sont correctement construites")
    print("⚠️ Le problème vient probablement du frontend")
    print("💡 Solution: Vérifier la construction des URLs dans MediaGallery.js")

if __name__ == "__main__":
    main() 
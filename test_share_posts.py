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

def test_get_posts(token):
    """Récupérer des posts pour les tests"""
    print("\n📝 Récupération des posts...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posts = data.get('results', [])
        if posts:
            post_id = posts[0].get('id')
            print(f"✅ Post trouvé: ID {post_id}")
            return post_id
        else:
            print("❌ Aucun post disponible")
            return None
    else:
        print(f"❌ Erreur récupération posts: {response.status_code}")
        return None

def test_share_post(token, post_id):
    """Test du partage de post"""
    print(f"\n🔄 Test du partage de post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    share_data = {
        "share_type": "share",
        "comment": "Post très intéressant !"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/posts/{post_id}/share/",
            json=share_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Post partagé avec succès!")
            print(f"🔄 ID du partage: {data.get('id')}")
            return True
        else:
            print(f"❌ Erreur partage: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors du partage: {str(e)}")
        return False

def test_external_share(token, post_id):
    """Test du partage externe"""
    print(f"\n🌐 Test du partage externe du post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    external_share_data = {
        "platform": "whatsapp"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/posts/{post_id}/share-external/",
            json=external_share_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Partage externe réussi!")
            print(f"🌐 Plateforme: {data.get('platform')}")
            return True
        else:
            print(f"❌ Erreur partage externe: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors du partage externe: {str(e)}")
        return False

def test_get_shares(token, post_id):
    """Test de récupération des partages"""
    print(f"\n📋 Test de récupération des partages du post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{API_URL}/posts/posts/{post_id}/shares/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            shares_count = len(data.get('results', []))
            print(f"✅ {shares_count} partages récupérés")
            return True
        else:
            print(f"❌ Erreur récupération partages: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors de la récupération: {str(e)}")
        return False

def main():
    """Test complet du partage de posts"""
    print("🚀 Test du partage de posts")
    print("=" * 50)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Récupérer un post pour les tests
    post_id = test_get_posts(token)
    if not post_id:
        print("❌ Impossible de continuer sans post")
        return
    
    # Test du partage de post
    share_ok = test_share_post(token, post_id)
    
    # Test du partage externe
    external_share_ok = test_external_share(token, post_id)
    
    # Test de récupération des partages
    get_shares_ok = test_get_shares(token, post_id)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS DE PARTAGE")
    print("=" * 50)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"📝 Récupération posts: {'✅' if post_id else '❌'}")
    print(f"🔄 Partage de post: {'✅' if share_ok else '❌'}")
    print(f"🌐 Partage externe: {'✅' if external_share_ok else '❌'}")
    print(f"📋 Récupération partages: {'✅' if get_shares_ok else '❌'}")
    
    if all([token, post_id, share_ok, external_share_ok, get_shares_ok]):
        print("\n🎉 TOUS LES TESTS DE PARTAGE SONT PASSÉS!")
        print("Le partage de posts fonctionne parfaitement!")
    else:
        print("\n⚠️ Certains tests de partage ont échoué")
        print("Vérifiez les logs ci-dessus pour plus de détails")

if __name__ == "__main__":
    main() 
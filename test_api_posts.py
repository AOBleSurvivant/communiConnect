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
        print(f"Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        print(f"Réponse: {response.text}")
        return None

def test_posts_api(token):
    """Test de l'API posts avec authentification"""
    print("\n📝 Test de l'API posts...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET /api/posts/
    response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posts = data.get('results', [])
        print(f"✅ API posts fonctionnelle!")
        print(f"📊 Nombre de posts récupérés: {len(posts)}")
        print(f"📊 Total de posts: {data.get('count', 0)}")
        
        if posts:
            print("\n📋 Posts disponibles:")
            for i, post in enumerate(posts[:3], 1):  # Afficher les 3 premiers
                print(f"  {i}. {post.get('content', '')[:50]}...")
                print(f"     Auteur: {post.get('author', {}).get('username', 'N/A')}")
                print(f"     Type: {post.get('post_type', 'N/A')}")
                print(f"     Likes: {post.get('likes_count', 0)}")
                print()
        
        return True
    else:
        print(f"❌ Erreur API posts: {response.status_code}")
        print(f"Réponse: {response.text}")
        return False

def test_create_post(token):
    """Test de création d'un post"""
    print("\n✏️ Test de création de post...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Test de création de post via API - CommuniConnect fonctionne parfaitement ! 🎉",
        "post_type": "info",
        "is_anonymous": False
    }
    
    response = requests.post(f"{API_URL}/posts/", json=post_data, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Post créé avec succès!")
        print(f"📝 ID: {data.get('id')}")
        print(f"📝 Contenu: {data.get('content')}")
        return True
    else:
        print(f"❌ Erreur création post: {response.status_code}")
        print(f"Réponse: {response.text}")
        return False

def test_user_profile(token):
    """Test du profil utilisateur"""
    print("\n👤 Test du profil utilisateur...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{API_URL}/users/my-profile/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Profil récupéré avec succès!")
        print(f"👤 Utilisateur: {data.get('username')}")
        print(f"📧 Email: {data.get('email')}")
        
        # Gérer le quartier (peut être un int ou un dict)
        quartier = data.get('quartier')
        if isinstance(quartier, dict):
            quartier_name = quartier.get('name', 'Non assigné')
        elif isinstance(quartier, int):
            quartier_name = f"Quartier ID: {quartier}"
        else:
            quartier_name = 'Non assigné'
        print(f"📍 Quartier: {quartier_name}")
        return True
    else:
        print(f"❌ Erreur profil: {response.status_code}")
        print(f"Réponse: {response.text}")
        return False

def test_geographic_data():
    """Test des données géographiques"""
    print("\n🗺️ Test des données géographiques...")
    
    response = requests.get(f"{API_URL}/users/geographic-data/")
    
    if response.status_code == 200:
        data = response.json()
        regions = data.get('regions', [])
        print(f"✅ Données géographiques récupérées!")
        print(f"📊 Nombre de régions: {len(regions)}")
        return True
    else:
        print(f"❌ Erreur données géographiques: {response.status_code}")
        print(f"Réponse: {response.text}")
        return False

def main():
    """Test complet de l'API"""
    print("🚀 Test complet de l'API CommuniConnect")
    print("=" * 50)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Test de l'API posts
    posts_ok = test_posts_api(token)
    
    # Test de création de post
    create_ok = test_create_post(token)
    
    # Test du profil utilisateur
    profile_ok = test_user_profile(token)
    
    # Test des données géographiques
    geo_ok = test_geographic_data()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"📝 API Posts: {'✅' if posts_ok else '❌'}")
    print(f"✏️ Création Post: {'✅' if create_ok else '❌'}")
    print(f"👤 Profil Utilisateur: {'✅' if profile_ok else '❌'}")
    print(f"🗺️ Données Géographiques: {'✅' if geo_ok else '❌'}")
    
    if all([token, posts_ok, create_ok, profile_ok, geo_ok]):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("CommuniConnect est 100% fonctionnel!")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("Vérifiez les logs ci-dessus pour plus de détails")

if __name__ == "__main__":
    main() 
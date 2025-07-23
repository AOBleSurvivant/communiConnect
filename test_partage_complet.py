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

def test_get_posts_for_sharing(token):
    """Récupérer des posts pour les tests de partage"""
    print("\n📝 Récupération des posts pour les tests de partage...")
    
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

def test_share_post_detailed(token, post_id):
    """Test détaillé du partage de post"""
    print(f"\n🔄 Test détaillé du partage de post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test avec différentes données de partage
    share_test_cases = [
        {
            "share_type": "share",
            "comment": "Post très intéressant !"
        },
        {
            "share_type": "like",
            "comment": "J'aime beaucoup ce post"
        },
        {
            "share_type": "recommend",
            "comment": "Je recommande ce post"
        }
    ]
    
    success_count = 0
    
    for i, share_data in enumerate(share_test_cases, 1):
        print(f"\n--- Test de partage {i} ---")
        print(f"Données: {json.dumps(share_data, indent=2)}")
        
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
                print(f"✅ Partage {i} réussi!")
                print(f"🔄 Share ID: {data.get('share_id')}")
                success_count += 1
            else:
                print(f"❌ Erreur partage {i}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception partage {i}: {str(e)}")
    
    return success_count > 0

def test_external_share_detailed(token, post_id):
    """Test détaillé du partage externe"""
    print(f"\n🌐 Test détaillé du partage externe du post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test avec différentes plateformes
    platform_test_cases = [
        {"platform": "whatsapp"},
        {"platform": "facebook"},
        {"platform": "twitter"},
        {"platform": "telegram"}
    ]
    
    success_count = 0
    
    for i, platform_data in enumerate(platform_test_cases, 1):
        print(f"\n--- Test plateforme {i}: {platform_data['platform']} ---")
        
        try:
            response = requests.post(
                f"{API_URL}/posts/posts/{post_id}/share-external/",
                json=platform_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            print(f"Réponse: {response.text[:200]}...")
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Partage externe {i} réussi!")
                print(f"🌐 Plateforme: {data.get('platform')}")
                success_count += 1
            else:
                print(f"❌ Erreur partage externe {i}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception partage externe {i}: {str(e)}")
    
    return success_count > 0

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
        print(f"Réponse: {response.text[:300]}...")
        
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

def test_get_external_shares(token, post_id):
    """Test de récupération des partages externes"""
    print(f"\n🌐 Test de récupération des partages externes du post {post_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{API_URL}/posts/posts/{post_id}/external-shares/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text[:300]}...")
        
        if response.status_code == 200:
            data = response.json()
            external_shares_count = len(data.get('results', []))
            print(f"✅ {external_shares_count} partages externes récupérés")
            return True
        else:
            print(f"❌ Erreur récupération partages externes: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors de la récupération: {str(e)}")
        return False

def main():
    """Test complet des fonctionnalités de partage"""
    print("🚀 TEST COMPLET DES FONCTIONNALITÉS DE PARTAGE")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token d'authentification")
        return
    
    # Récupérer un post pour les tests
    post_id = test_get_posts_for_sharing(token)
    if not post_id:
        print("❌ Impossible de continuer sans post")
        return
    
    # Test du partage de post
    share_ok = test_share_post_detailed(token, post_id)
    
    # Test du partage externe
    external_share_ok = test_external_share_detailed(token, post_id)
    
    # Test de récupération des partages
    get_shares_ok = test_get_shares(token, post_id)
    
    # Test de récupération des partages externes
    get_external_shares_ok = test_get_external_shares(token, post_id)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS DE PARTAGE")
    print("=" * 60)
    print(f"🔐 Authentification: {'✅' if token else '❌'}")
    print(f"📝 Récupération posts: {'✅' if post_id else '❌'}")
    print(f"🔄 Partage de post: {'✅' if share_ok else '❌'}")
    print(f"🌐 Partage externe: {'✅' if external_share_ok else '❌'}")
    print(f"📋 Récupération partages: {'✅' if get_shares_ok else '❌'}")
    print(f"🌐 Récupération partages externes: {'✅' if get_external_shares_ok else '❌'}")
    
    # Calcul du taux de réussite
    tests = [token, post_id, share_ok, external_share_ok, get_shares_ok, get_external_shares_ok]
    success_count = sum(1 for test in tests if test)
    total_tests = len(tests)
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n📊 TAUX DE RÉUSSITE: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT ! Les fonctionnalités de partage fonctionnent parfaitement!")
    elif success_rate >= 80:
        print("\n✅ TRÈS BIEN ! La plupart des fonctionnalités de partage marchent!")
    elif success_rate >= 60:
        print("\n⚠️ BIEN ! Certaines fonctionnalités de partage marchent.")
    else:
        print("\n❌ ATTENTION ! Les fonctionnalités de partage ont des problèmes.")

if __name__ == "__main__":
    main() 
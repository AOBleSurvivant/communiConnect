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

def verifier_posts_avec_partages(token):
    """Vérifier les posts avec partages"""
    print("\n📤 VÉRIFICATION POSTS AVEC PARTAGES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            posts_avec_partages = [p for p in posts if p.get('shares_count', 0) > 0]
            print(f"📋 Posts avec partages: {len(posts_avec_partages)}")
            
            for post in posts_avec_partages[:3]:
                print(f"\n📝 Post ID: {post.get('id')}")
                print(f"   Contenu: {post.get('content', '')[:50]}...")
                print(f"   Shares count: {post.get('shares_count', 0)}")
            
            # Afficher un post sans partages pour test
            posts_sans_partages = [p for p in posts if p.get('shares_count', 0) == 0]
            if posts_sans_partages:
                test_post = posts_sans_partages[0]
                print(f"\n🧪 POST DE TEST (sans partages):")
                print(f"   ID: {test_post.get('id')}")
                print(f"   Contenu: {test_post.get('content', '')[:50]}...")
                print(f"   Shares count: {test_post.get('shares_count', 0)}")
                return test_post.get('id')
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_endpoints_partages():
    """Vérifier les endpoints de partages"""
    print("\n🔗 VÉRIFICATION ENDPOINTS PARTAGES")
    print("=" * 60)
    
    endpoints = [
        f"{API_URL}/posts/posts/1/share/",
        f"{API_URL}/posts/posts/1/shares/",
        f"{API_URL}/posts/posts/1/share-external/",
        f"{API_URL}/posts/posts/1/external-shares/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)}")

def tester_partage_post(token, post_id):
    """Tester le partage d'un post"""
    print(f"\n📤 TEST PARTAGE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    share_data = {
        "share_type": "share",
        "comment": "Test de partage - Vérification système ! 📤"
    }
    
    try:
        # Tester le partage
        response = requests.post(
            f"{API_URL}/posts/posts/{post_id}/share/",
            json=share_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Partage créé avec succès")
            print(f"📊 Données retournées: {data}")
            return data.get('id')
        else:
            print(f"❌ Erreur création partage: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_unshare_post(token, post_id):
    """Tester l'unshare d'un post"""
    print(f"\n❌ TEST UNSHARE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Tester l'unshare
        response = requests.delete(f"{API_URL}/posts/posts/{post_id}/share/", headers=headers)
        
        if response.status_code == 204:
            print(f"✅ Unshare réussi")
            return True
        else:
            print(f"❌ Erreur unshare: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def verifier_partages_post(token, post_id):
    """Vérifier les partages d'un post"""
    print(f"\n📋 VÉRIFICATION PARTAGES POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/posts/{post_id}/shares/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            shares = data.get('results', []) if isinstance(data, dict) else data
            
            print(f"📊 Nombre de partages: {len(shares)}")
            
            for i, share in enumerate(shares):
                print(f"\n{i+1}. Partage ID: {share.get('id')}")
                print(f"   Utilisateur: {share.get('user', {}).get('username', 'Inconnu')}")
                print(f"   Type: {share.get('share_type')}")
                print(f"   Commentaire: {share.get('comment', '')}")
                print(f"   Date: {share.get('created_at')}")
            
            return shares
        else:
            print(f"❌ Erreur récupération partages: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_partage_externe(token, post_id):
    """Tester le partage externe"""
    print(f"\n🌐 TEST PARTAGE EXTERNE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    external_share_data = {
        "platform": "whatsapp"
    }
    
    try:
        # Tester le partage externe
        response = requests.post(
            f"{API_URL}/posts/posts/{post_id}/share-external/",
            json=external_share_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Partage externe créé avec succès")
            print(f"📊 Données retournées: {data}")
            return data.get('id')
        else:
            print(f"❌ Erreur création partage externe: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_partages_externes_post(token, post_id):
    """Vérifier les partages externes d'un post"""
    print(f"\n🌐 VÉRIFICATION PARTAGES EXTERNES POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/posts/{post_id}/external-shares/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            external_shares = data.get('results', []) if isinstance(data, dict) else data
            
            print(f"📊 Nombre de partages externes: {len(external_shares)}")
            
            for i, share in enumerate(external_shares):
                print(f"\n{i+1}. Partage externe ID: {share.get('id')}")
                print(f"   Utilisateur: {share.get('user', {}).get('username', 'Inconnu')}")
                print(f"   Plateforme: {share.get('platform')}")
                print(f"   Date: {share.get('shared_at')}")
            
            return external_shares
        else:
            print(f"❌ Erreur récupération partages externes: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def main():
    """Diagnostic complet du système de partages"""
    print("📤 DIAGNOSTIC SYSTÈME DE PARTAGES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier les endpoints
    verifier_endpoints_partages()
    
    # Vérifier les posts avec partages
    post_id = verifier_posts_avec_partages(token)
    
    if post_id:
        # Vérifier les partages existants
        shares = verifier_partages_post(token, post_id)
        
        # Tester la création d'un partage
        share_id = tester_partage_post(token, post_id)
        
        if share_id:
            # Vérifier les partages après création
            verifier_partages_post(token, post_id)
            
            # Tester l'unshare
            unshare_success = tester_unshare_post(token, post_id)
            
            if unshare_success:
                # Vérifier les partages après unshare
                verifier_partages_post(token, post_id)
        
        # Tester le partage externe
        external_share_id = tester_partage_externe(token, post_id)
        
        if external_share_id:
            # Vérifier les partages externes
            verifier_partages_externes_post(token, post_id)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ Posts récupérés")
    print(f"✅ Endpoints partages vérifiés")
    print(f"✅ Tests partages effectués")
    print(f"✅ Tests partages externes effectués")
    print(f"💡 Si les partages ne fonctionnent pas:")
    print(f"   1. Vérifiez les endpoints API")
    print(f"   2. Vérifiez la base de données")
    print(f"   3. Vérifiez les permissions")
    print(f"   4. Vérifiez le frontend")

if __name__ == "__main__":
    main() 
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

def nettoyer_likes_utilisateur(token, post_id):
    """Nettoyer les likes de l'utilisateur sur un post"""
    print(f"\n🧹 NETTOYAGE LIKES POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Vérifier l'état actuel
    response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    if response.status_code == 200:
        post = response.json()
        print(f"📊 État actuel du post:")
        print(f"   Likes count: {post.get('likes_count', 0)}")
        print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")
        
        # Si l'utilisateur a liké le post, le unliker
        if post.get('is_liked_by_user', False):
            print("🔄 Suppression du like existant...")
            response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
            if response.status_code == 204:
                print("✅ Like supprimé avec succès")
            else:
                print(f"❌ Erreur suppression like: {response.status_code}")
        else:
            print("ℹ️ Aucun like à supprimer")
    
    # Vérifier l'état après nettoyage
    response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    if response.status_code == 200:
        post = response.json()
        print(f"📊 État après nettoyage:")
        print(f"   Likes count: {post.get('likes_count', 0)}")
        print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")

def tester_like_cycle(token, post_id):
    """Tester un cycle complet like/unlike"""
    print(f"\n🔄 TEST CYCLE LIKE/UNLIKE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 1. Nettoyer d'abord
    nettoyer_likes_utilisateur(token, post_id)
    
    # 2. Tester le like
    print("\n❤️ Test du like...")
    response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    if response.status_code == 201:
        print("✅ Like ajouté avec succès")
    else:
        print(f"❌ Erreur ajout like: {response.status_code}")
        print(f"Réponse: {response.text}")
        return False
    
    # 3. Vérifier l'état après like
    response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    if response.status_code == 200:
        post = response.json()
        print(f"📊 État après like:")
        print(f"   Likes count: {post.get('likes_count', 0)}")
        print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")
    
    # 4. Tester l'unlike
    print("\n💔 Test de l'unlike...")
    response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    if response.status_code == 204:
        print("✅ Unlike réussi")
    else:
        print(f"❌ Erreur unlike: {response.status_code}")
        return False
    
    # 5. Vérifier l'état final
    response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    if response.status_code == 200:
        post = response.json()
        print(f"📊 État final:")
        print(f"   Likes count: {post.get('likes_count', 0)}")
        print(f"   Is liked by user: {post.get('is_liked_by_user', False)}")
    
    return True

def main():
    """Nettoyage et test des likes"""
    print("🧹 NETTOYAGE ET TEST DES LIKES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Posts à tester
    posts_to_test = [410, 406, 407, 409]
    
    for post_id in posts_to_test:
        print(f"\n{'='*60}")
        print(f"📝 TEST POST {post_id}")
        print(f"{'='*60}")
        
        success = tester_like_cycle(token, post_id)
        if success:
            print(f"✅ Post {post_id}: Cycle like/unlike réussi")
        else:
            print(f"❌ Post {post_id}: Échec du cycle like/unlike")
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Nettoyage des likes effectué")
    print("✅ Tests de cycle like/unlike effectués")
    print("💡 Le frontend devrait maintenant fonctionner correctement")

if __name__ == "__main__":
    main() 
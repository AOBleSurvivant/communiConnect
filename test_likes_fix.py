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

def test_likes(token):
    """Test des fonctionnalités de like"""
    print(f"\n❤️ TEST FONCTIONNALITÉS LIKE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 1. Récupérer un post pour tester
    print("\n1️⃣ Récupération d'un post pour test...")
    posts_response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    if posts_response.status_code != 200:
        print(f"❌ Erreur récupération posts: {posts_response.status_code}")
        return
    
    posts_data = posts_response.json()
    if not posts_data.get('results'):
        print("❌ Aucun post disponible pour test")
        return
    
    post = posts_data['results'][0]
    post_id = post['id']
    print(f"✅ Post sélectionné: ID {post_id}")
    
    # 2. Tester le like
    print(f"\n2️⃣ Test like sur post {post_id}...")
    like_response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status like: {like_response.status_code}")
    
    if like_response.status_code == 201:
        print("✅ Like ajouté avec succès")
        like_data = like_response.json()
        print(f"📊 Données like: {like_data}")
    elif like_response.status_code == 200:
        print("✅ Like mis à jour avec succès")
        like_data = like_response.json()
        print(f"📊 Données like: {like_data}")
    else:
        print(f"❌ Erreur like: {like_response.status_code}")
        print(f"📊 Réponse: {like_response.text}")
        return
    
    # 3. Tester l'unlike
    print(f"\n3️⃣ Test unlike sur post {post_id}...")
    unlike_response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status unlike: {unlike_response.status_code}")
    
    if unlike_response.status_code == 204:
        print("✅ Unlike réussi")
    else:
        print(f"❌ Erreur unlike: {unlike_response.status_code}")
        print(f"📊 Réponse: {unlike_response.text}")
    
    # 4. Tester le like à nouveau
    print(f"\n4️⃣ Test like à nouveau sur post {post_id}...")
    like_response2 = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status like (2ème): {like_response2.status_code}")
    
    if like_response2.status_code in [200, 201]:
        print("✅ Like à nouveau réussi")
    else:
        print(f"❌ Erreur like (2ème): {like_response2.status_code}")
        print(f"📊 Réponse: {like_response2.text}")

def test_comments(token):
    """Test des fonctionnalités de commentaires"""
    print(f"\n💬 TEST FONCTIONNALITÉS COMMENTAIRES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 1. Récupérer un post pour tester
    print("\n1️⃣ Récupération d'un post pour test commentaires...")
    posts_response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    if posts_response.status_code != 200:
        print(f"❌ Erreur récupération posts: {posts_response.status_code}")
        return
    
    posts_data = posts_response.json()
    if not posts_data.get('results'):
        print("❌ Aucun post disponible pour test")
        return
    
    post = posts_data['results'][0]
    post_id = post['id']
    print(f"✅ Post sélectionné: ID {post_id}")
    
    # 2. Tester l'ajout de commentaire
    print(f"\n2️⃣ Test ajout commentaire sur post {post_id}...")
    comment_data = {
        "content": "Test commentaire automatique"
    }
    
    comment_response = requests.post(
        f"{API_URL}/posts/{post_id}/comments/", 
        headers=headers,
        json=comment_data
    )
    
    print(f"📊 Status commentaire: {comment_response.status_code}")
    
    if comment_response.status_code == 201:
        print("✅ Commentaire ajouté avec succès")
        comment_data = comment_response.json()
        print(f"📊 Données commentaire: {comment_data}")
    else:
        print(f"❌ Erreur commentaire: {comment_response.status_code}")
        print(f"📊 Réponse: {comment_response.text}")

def main():
    """Test complet des fonctionnalités sociales"""
    print("🧪 TEST FONCTIONNALITÉS SOCIALES APRÈS CORRECTION")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Test des likes
    test_likes(token)
    
    # Test des commentaires
    test_comments(token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Likes: Testé")
    print("✅ Commentaires: Testé")
    print("💡 Vérifiez les résultats ci-dessus")

if __name__ == "__main__":
    main() 
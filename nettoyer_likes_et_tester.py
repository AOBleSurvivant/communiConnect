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
        print(f"✅ Connexion réussie pour alphaoumarb67")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        return None

def nettoyer_likes_existants(token):
    """Nettoyer tous les likes existants pour éviter les conflits"""
    print(f"\n🧹 NETTOYAGE DES LIKES EXISTANTS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Récupérer tous les posts
    posts_response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    if posts_response.status_code != 200:
        print(f"❌ Erreur récupération posts: {posts_response.status_code}")
        return
    
    posts_data = posts_response.json()
    posts = posts_data.get('results', [])
    
    print(f"📊 {len(posts)} posts trouvés")
    
    # Pour chaque post, essayer de supprimer le like s'il existe
    for post in posts:
        post_id = post['id']
        print(f"🧹 Nettoyage likes pour post {post_id}...")
        
        # Essayer de supprimer le like (DELETE ne fait rien si pas de like)
        unlike_response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
        
        if unlike_response.status_code == 204:
            print(f"✅ Like supprimé pour post {post_id}")
        elif unlike_response.status_code == 404:
            print(f"ℹ️ Aucun like à supprimer pour post {post_id}")
        else:
            print(f"⚠️ Erreur {unlike_response.status_code} pour post {post_id}")

def test_likes_complet(token):
    """Test complet du système de likes"""
    print(f"\n❤️ TEST COMPLET SYSTÈME DE LIKES")
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
    
    # Vérifier l'état initial du post
    print(f"📊 État initial - is_liked_by_user: {post.get('is_liked_by_user', 'Non défini')}")
    print(f"📊 État initial - likes_count: {post.get('likes_count', 0)}")
    
    # 2. Premier like
    print(f"\n2️⃣ Premier like sur post {post_id}...")
    like_response1 = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status premier like: {like_response1.status_code}")
    
    if like_response1.status_code == 201:
        print("✅ Premier like ajouté avec succès")
        like_data = like_response1.json()
        print(f"📊 Données like: {like_data}")
    else:
        print(f"❌ Erreur premier like: {like_response1.status_code}")
        print(f"📊 Réponse: {like_response1.text}")
        return
    
    # 3. Vérifier l'état après le premier like
    print(f"\n3️⃣ Vérification état après premier like...")
    post_response = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    
    if post_response.status_code == 200:
        post_data = post_response.json()
        print(f"📊 is_liked_by_user: {post_data.get('is_liked_by_user')}")
        print(f"📊 likes_count: {post_data.get('likes_count')}")
    else:
        print(f"❌ Erreur récupération post: {post_response.status_code}")
    
    # 4. Deuxième like (devrait échouer)
    print(f"\n4️⃣ Deuxième like sur post {post_id} (devrait échouer)...")
    like_response2 = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status deuxième like: {like_response2.status_code}")
    
    if like_response2.status_code == 400:
        print("✅ Deuxième like correctement rejeté (400)")
        error_data = like_response2.json()
        print(f"📊 Message d'erreur: {error_data.get('detail', 'Aucun message')}")
    else:
        print(f"⚠️ Comportement inattendu: {like_response2.status_code}")
        print(f"📊 Réponse: {like_response2.text}")
    
    # 5. Unlike
    print(f"\n5️⃣ Unlike sur post {post_id}...")
    unlike_response = requests.delete(f"{API_URL}/posts/{post_id}/like/", headers=headers)
    
    print(f"📊 Status unlike: {unlike_response.status_code}")
    
    if unlike_response.status_code == 204:
        print("✅ Unlike réussi")
    else:
        print(f"❌ Erreur unlike: {unlike_response.status_code}")
        print(f"📊 Réponse: {unlike_response.text}")
    
    # 6. Vérifier l'état final
    print(f"\n6️⃣ Vérification état final...")
    post_response_final = requests.get(f"{API_URL}/posts/{post_id}/", headers=headers)
    
    if post_response_final.status_code == 200:
        post_data_final = post_response_final.json()
        print(f"📊 is_liked_by_user final: {post_data_final.get('is_liked_by_user')}")
        print(f"📊 likes_count final: {post_data_final.get('likes_count')}")
    else:
        print(f"❌ Erreur récupération post final: {post_response_final.status_code}")

def main():
    """Test complet du système de likes"""
    print("🧪 TEST COMPLET SYSTÈME DE LIKES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Nettoyer les likes existants
    nettoyer_likes_existants(token)
    
    # Test complet du système de likes
    test_likes_complet(token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Nettoyage: Effectué")
    print("✅ Test likes: Terminé")
    print("💡 Vérifiez les résultats ci-dessus")

if __name__ == "__main__":
    main() 
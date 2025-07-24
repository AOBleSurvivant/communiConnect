#!/usr/bin/env python3
"""
Test de diagnostic pour le problème de disparition des posts après like
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api"
LOGIN_URL = f"{API_URL}/auth/login/"
POSTS_URL = f"{API_URL}/posts/"

def login_user():
    """Se connecter avec un utilisateur de test"""
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            token = response.json().get('access')
            print(f"✅ Connexion réussie - Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Échec connexion: {response.status_code}")
            print(f"📝 Réponse: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return None

def get_posts(token):
    """Récupérer les posts"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(POSTS_URL, headers=headers)
        print(f"📊 Status récupération posts: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Structure réponse: {type(data)}")
            
            if isinstance(data, dict):
                print(f"📊 Clés disponibles: {list(data.keys())}")
                if 'results' in data:
                    posts = data['results']
                    print(f"📊 Posts dans 'results': {len(posts)}")
                elif 'data' in data:
                    posts = data['data']
                    print(f"📊 Posts dans 'data': {len(posts)}")
                else:
                    posts = []
                    print(f"📊 Aucune clé 'results' ou 'data' trouvée")
            elif isinstance(data, list):
                posts = data
                print(f"📊 Posts dans liste directe: {len(posts)}")
            else:
                posts = []
                print(f"📊 Type de réponse inattendu: {type(data)}")
            
            return posts
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            print(f"📝 Réponse: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des posts: {e}")
        return []

def like_post(post_id, token):
    """Liker un post"""
    headers = {"Authorization": f"Bearer {token}"}
    like_url = f"{POSTS_URL}{post_id}/like/"
    
    try:
        response = requests.post(like_url, headers=headers)
        print(f"📊 Status like post {post_id}: {response.status_code}")
        
        if response.status_code == 201:
            print(f"✅ Like réussi pour post {post_id}")
            return True
        elif response.status_code == 400:
            print(f"⚠️ Post {post_id} déjà liké ou erreur validation")
            print(f"📝 Réponse: {response.text}")
            return True  # Considéré comme "succès" car l'état est correct
        else:
            print(f"❌ Erreur like post {post_id}: {response.status_code}")
            print(f"📝 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du like: {e}")
        return False

def unlike_post(post_id, token):
    """Unliker un post"""
    headers = {"Authorization": f"Bearer {token}"}
    like_url = f"{POSTS_URL}{post_id}/like/"
    
    try:
        response = requests.delete(like_url, headers=headers)
        print(f"📊 Status unlike post {post_id}: {response.status_code}")
        
        if response.status_code == 204:
            print(f"✅ Unlike réussi pour post {post_id}")
            return True
        else:
            print(f"❌ Erreur unlike post {post_id}: {response.status_code}")
            print(f"📝 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'unlike: {e}")
        return False

def test_like_disappearance():
    """Test complet du problème de disparition des posts"""
    print("🧪 TEST DIAGNOSTIC - DISPARITION POSTS APRÈS LIKE")
    print("=" * 60)
    
    # 1. Connexion
    token = login_user()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # 2. Récupération posts initiaux
    print("\n📋 ÉTAPE 1: Posts initiaux")
    print("-" * 30)
    initial_posts = get_posts(token)
    print(f"📊 Nombre de posts initiaux: {len(initial_posts)}")
    
    if not initial_posts:
        print("❌ Aucun post trouvé, impossible de tester")
        return
    
    # Afficher les premiers posts
    for i, post in enumerate(initial_posts[:3]):
        print(f"📝 Post {i+1}: ID {post.get('id')} - {post.get('content', '')[:50]}...")
        print(f"   Likes: {post.get('likes_count', 0)} | Liké par user: {post.get('is_liked_by_user', False)}")
    
    # 3. Tester le like sur le premier post
    if initial_posts:
        first_post = initial_posts[0]
        post_id = first_post.get('id')
        
        print(f"\n❤️ ÉTAPE 2: Test like sur post {post_id}")
        print("-" * 30)
        
        # Vérifier l'état initial
        initial_liked = first_post.get('is_liked_by_user', False)
        print(f"📊 État initial - Liké par user: {initial_liked}")
        
        if not initial_liked:
            # Liker le post
            like_success = like_post(post_id, token)
            if like_success:
                print("⏳ Attente 2 secondes...")
                time.sleep(2)
        else:
            print("ℹ️ Post déjà liké, test d'unlike")
            unlike_success = unlike_post(post_id, token)
            if unlike_success:
                print("⏳ Attente 2 secondes...")
                time.sleep(2)
    
    # 4. Récupération posts après like
    print(f"\n📋 ÉTAPE 3: Posts après like")
    print("-" * 30)
    posts_after_like = get_posts(token)
    print(f"📊 Nombre de posts après like: {len(posts_after_like)}")
    
    # Comparaison
    if len(posts_after_like) != len(initial_posts):
        print(f"⚠️ DIFFÉRENCE DÉTECTÉE!")
        print(f"   Posts initiaux: {len(initial_posts)}")
        print(f"   Posts après like: {len(posts_after_like)}")
        print(f"   Différence: {len(initial_posts) - len(posts_after_like)} posts")
    else:
        print("✅ Nombre de posts inchangé")
    
    # Vérifier si le post liké est toujours présent
    if initial_posts and posts_after_like:
        first_post_id = initial_posts[0].get('id')
        post_still_exists = any(post.get('id') == first_post_id for post in posts_after_like)
        
        if post_still_exists:
            print(f"✅ Post {first_post_id} toujours présent")
            
            # Vérifier l'état du like
            updated_post = next(post for post in posts_after_like if post.get('id') == first_post_id)
            updated_liked = updated_post.get('is_liked_by_user', False)
            print(f"📊 État like après mise à jour: {updated_liked}")
            
        else:
            print(f"❌ Post {first_post_id} a disparu!")
    
    # 5. Test de rechargement multiple
    print(f"\n🔄 ÉTAPE 4: Test rechargement multiple")
    print("-" * 30)
    
    for i in range(3):
        print(f"🔄 Rechargement {i+1}/3...")
        posts = get_posts(token)
        print(f"   Posts trouvés: {len(posts)}")
        time.sleep(1)
    
    print(f"\n🎯 CONCLUSION")
    print("=" * 30)
    if len(posts_after_like) == len(initial_posts):
        print("✅ Aucun problème de disparition détecté")
        print("💡 Le problème pourrait être côté frontend")
    else:
        print("❌ Problème de disparition confirmé")
        print("💡 Le problème est côté backend/API")

if __name__ == "__main__":
    test_like_disappearance() 
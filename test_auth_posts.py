#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post
from users.models import User
from geography.models import Quartier

def test_auth_posts_api():
    """Test l'API posts avec authentification"""
    print("🔍 Test de l'API posts avec authentification...")
    
    # 1. Créer un utilisateur de test et obtenir un token
    print("👤 Création d'un utilisateur de test...")
    
    # Créer un utilisateur de test
    user_data = {
        "username": "test_user_posts",
        "email": "test.posts@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "first_name": "Test",
        "last_name": "Posts",
        "quartier": 676  # Boké Centre
    }
    
    try:
        # Inscription
        response = requests.post('http://localhost:8000/api/users/register/', json=user_data)
        print(f"Status inscription: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            access_token = data['tokens']['access']
            print("✅ Utilisateur créé et token obtenu")
        else:
            print(f"❌ Erreur inscription: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'inscription: {e}")
        return False
    
    # 2. Tester l'API posts avec authentification
    print("\n🌐 Test de l'API posts avec token...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://localhost:8000/api/posts/', headers=headers)
        print(f"Status API posts: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API posts fonctionnelle avec authentification!")
            print(f"Posts retournés: {len(data.get('results', []))}")
            return True
        else:
            print(f"❌ Erreur API posts: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def create_test_post_with_auth():
    """Crée un post de test avec authentification"""
    print("\n📝 Création d'un post de test avec authentification...")
    
    # Données de connexion
    login_data = {
        "email": "test.posts@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Connexion
        response = requests.post('http://localhost:8000/api/users/login/', json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            access_token = data['tokens']['access']
            print("✅ Connexion réussie")
            
            # Créer un post
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            post_data = {
                "content": "Post de test créé via API avec authentification",
                "post_type": "info",
                "is_anonymous": False
            }
            
            response = requests.post('http://localhost:8000/api/posts/', json=post_data, headers=headers)
            print(f"Status création post: {response.status_code}")
            
            if response.status_code == 201:
                print("✅ Post créé avec succès via API!")
                return True
            else:
                print(f"❌ Erreur création post: {response.text}")
                return False
        else:
            print(f"❌ Erreur connexion: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'API posts avec authentification")
    print("=" * 60)
    
    # Tester l'API posts avec authentification
    if test_auth_posts_api():
        print("\n✅ Test de l'API posts avec authentification réussi!")
    else:
        print("\n❌ Test de l'API posts avec authentification échoué")
    
    # Créer un post de test avec authentification
    if create_test_post_with_auth():
        print("\n✅ Création de post avec authentification réussie!")
    else:
        print("\n❌ Création de post avec authentification échouée") 
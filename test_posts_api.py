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
from posts.serializers import PostSerializer

def test_posts_api():
    """Test l'API posts pour diagnostiquer l'erreur 500"""
    print("🔍 Test de l'API posts...")
    
    # 1. Vérifier les posts existants
    posts_count = Post.objects.count()
    print(f"📊 Posts dans la DB: {posts_count}")
    
    # 2. Créer un post de test si nécessaire
    if posts_count == 0:
        print("📝 Création d'un post de test...")
        user = User.objects.first()
        quartier = Quartier.objects.first()
        
        if user and quartier:
            post = Post.objects.create(
                author=user,
                quartier=quartier,
                content="Post de test pour diagnostiquer l'API",
                post_type="info",
                is_anonymous=False
            )
            print(f"✅ Post créé: {post.id}")
        else:
            print("❌ Utilisateur ou quartier non trouvé")
            return False
    
    # 3. Tester la sérialisation
    print("🔧 Test de sérialisation...")
    try:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        print(f"✅ Sérialisation réussie: {len(serializer.data)} posts")
    except Exception as e:
        print(f"❌ Erreur de sérialisation: {e}")
        return False
    
    # 4. Tester l'API endpoint
    print("🌐 Test de l'endpoint API...")
    try:
        response = requests.get('http://localhost:8000/api/posts/')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API posts fonctionnelle!")
            data = response.json()
            print(f"Posts retournés: {len(data.get('results', []))}")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    return True

def create_test_posts():
    """Crée des posts de test"""
    print("\n📝 Création de posts de test...")
    
    user = User.objects.first()
    quartier = Quartier.objects.first()
    
    if not user or not quartier:
        print("❌ Utilisateur ou quartier non trouvé")
        return False
    
    test_posts = [
        {
            'content': 'Bienvenue sur CommuniConnect ! 🎉',
            'post_type': 'info',
            'is_anonymous': False
        },
        {
            'content': 'Test de post avec contenu simple',
            'post_type': 'discussion',
            'is_anonymous': False
        },
        {
            'content': 'Post de test pour vérifier l\'API',
            'post_type': 'info',
            'is_anonymous': True
        }
    ]
    
    for i, post_data in enumerate(test_posts):
        try:
            post = Post.objects.create(
                author=user,
                quartier=quartier,
                **post_data
            )
            print(f"✅ Post {i+1} créé: {post.id}")
        except Exception as e:
            print(f"❌ Erreur création post {i+1}: {e}")
    
    return True

if __name__ == "__main__":
    print("🚀 Test de l'API posts CommuniConnect")
    print("=" * 50)
    
    # Créer des posts de test
    if create_test_posts():
        print("\n✅ Posts de test créés avec succès!")
    else:
        print("\n❌ Erreur lors de la création des posts")
    
    # Tester l'API
    if test_posts_api():
        print("\n🎉 Test de l'API posts réussi!")
    else:
        print("\n❌ Test de l'API posts échoué") 
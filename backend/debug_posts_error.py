#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post
from users.models import User
from geography.models import Quartier
from posts.views import PostListView
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory

def debug_posts_error():
    """Diagnostiquer l'erreur ValueError dans l'API posts"""
    print("🔍 Diagnostic de l'erreur ValueError...")
    
    try:
        # 1. Vérifier l'utilisateur
        user = User.objects.get(email='test.posts@example.com')
        print(f"✅ Utilisateur trouvé: {user.username}")
        print(f"📍 Quartier: {user.quartier}")
        
        if user.quartier:
            print(f"🏘️ Commune: {user.quartier.commune}")
            print(f"🏘️ Région: {user.quartier.commune.prefecture.region}")
        
        # 2. Vérifier les posts
        posts_count = Post.objects.count()
        print(f"📊 Posts dans la DB: {posts_count}")
        
        # 3. Tester la méthode get_queryset
        print("\n🔧 Test de get_queryset...")
        factory = APIRequestFactory()
        request = factory.get('/api/posts/')
        request.user = user
        
        view = PostListView()
        view.request = request
        
        try:
            queryset = view.get_queryset()
            print(f"✅ get_queryset réussi: {queryset.count()} posts")
        except Exception as e:
            print(f"❌ Erreur get_queryset: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 4. Tester la sérialisation
        print("\n🔧 Test de sérialisation...")
        try:
            from posts.serializers import PostSerializer
            serializer = PostSerializer(queryset, many=True)
            print(f"✅ Sérialisation réussie: {len(serializer.data)} posts")
        except Exception as e:
            print(f"❌ Erreur sérialisation: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 5. Tester la méthode list
        print("\n🔧 Test de la méthode list...")
        try:
            response = view.list(request)
            print(f"✅ Méthode list réussie: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur méthode list: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Diagnostic de l'erreur ValueError - CommuniConnect")
    print("=" * 60)
    
    if debug_posts_error():
        print("\n✅ Diagnostic terminé avec succès!")
    else:
        print("\n❌ Diagnostic échoué - Erreur identifiée") 
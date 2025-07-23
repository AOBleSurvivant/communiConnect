#!/usr/bin/env python
import os
import sys
import django

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from geography.models import Quartier
from posts.models import Post, Media
from posts.services import LiveStreamingService

User = get_user_model()

def check_user_quartier():
    """Vérifier si l'utilisateur a un quartier assigné"""
    print("🔍 Vérification du quartier de l'utilisateur...")
    
    try:
        user = User.objects.get(username='mariam_diallo')
        print(f"👤 Utilisateur: {user.username}")
        print(f"📧 Email: {user.email}")
        
        if user.quartier:
            print(f"✅ Quartier assigné: {user.quartier.name}")
            print(f"📍 Commune: {user.quartier.commune.name}")
            print(f"🏛️ Préfecture: {user.quartier.commune.prefecture.name}")
            return True
        else:
            print("❌ Aucun quartier assigné")
            
            # Assigner un quartier
            quartiers = Quartier.objects.all()[:5]
            if quartiers:
                user.quartier = quartiers[0]
                user.save()
                print(f"✅ Quartier assigné: {user.quartier.name}")
                return True
            else:
                print("❌ Aucun quartier disponible")
                return False
                
    except User.DoesNotExist:
        print("❌ Utilisateur mariam_diallo non trouvé")
        return False

def test_live_streaming_service():
    """Tester le service de live streaming"""
    print("\n🔴 Test du service LiveStreamingService...")
    
    try:
        # Générer une clé de stream
        stream_key = LiveStreamingService.generate_stream_key(1)
        print(f"✅ Clé de stream générée: {stream_key}")
        
        # Tester le démarrage
        start_result = LiveStreamingService.start_stream(stream_key)
        print(f"✅ Démarrage stream: {start_result}")
        
        # Tester l'arrêt
        stop_result = LiveStreamingService.stop_stream(stream_key)
        print(f"✅ Arrêt stream: {stop_result}")
        
        # Tester les URLs
        rtmp_url = LiveStreamingService.get_rtmp_url(stream_key)
        hls_url = LiveStreamingService.get_hls_url(stream_key)
        print(f"✅ RTMP URL: {rtmp_url}")
        print(f"✅ HLS URL: {hls_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur service live streaming: {str(e)}")
        return False

def create_test_live_post():
    """Créer un post de test pour le live"""
    print("\n📝 Création d'un post de test pour le live...")
    
    try:
        user = User.objects.get(username='mariam_diallo')
        
        if not user.quartier:
            print("❌ Utilisateur sans quartier")
            return None
        
        # Créer un post live
        post = Post.objects.create(
            user=user,
            quartier=user.quartier,
            content="Test de live streaming - CommuniConnect",
            post_type='live',
            is_live_post=True
        )
        
        print(f"✅ Post live créé: ID {post.id}")
        print(f"📝 Contenu: {post.content}")
        print(f"🔴 Type: {post.post_type}")
        print(f"🎯 Live: {post.is_live_post}")
        
        return post
        
    except Exception as e:
        print(f"❌ Erreur création post live: {str(e)}")
        return None

def main():
    """Diagnostic complet du live streaming"""
    print("🚀 Diagnostic du live streaming")
    print("=" * 50)
    
    # Vérifier le quartier de l'utilisateur
    quartier_ok = check_user_quartier()
    
    # Tester le service de live streaming
    service_ok = test_live_streaming_service()
    
    # Créer un post de test
    post = create_test_live_post()
    post_ok = post is not None
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    print(f"📍 Quartier utilisateur: {'✅' if quartier_ok else '❌'}")
    print(f"🔴 Service live streaming: {'✅' if service_ok else '❌'}")
    print(f"📝 Post de test: {'✅' if post_ok else '❌'}")
    
    if all([quartier_ok, service_ok, post_ok]):
        print("\n🎉 Le live streaming devrait fonctionner maintenant!")
        print("Testez à nouveau avec le script de test.")
    else:
        print("\n⚠️ Problèmes détectés")
        if not quartier_ok:
            print("- L'utilisateur n'a pas de quartier assigné")
        if not service_ok:
            print("- Le service de live streaming a des problèmes")
        if not post_ok:
            print("- Impossible de créer un post de test")

if __name__ == "__main__":
    main() 
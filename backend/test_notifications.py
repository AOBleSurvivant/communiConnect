#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, PostComment, PostLike
from notifications.services import NotificationService
from notifications.models import Notification

User = get_user_model()

def create_test_notifications():
    """Crée des notifications de test"""
    
    # Récupérer les utilisateurs existants
    users = User.objects.all()
    if users.count() < 2:
        print("❌ Il faut au moins 2 utilisateurs pour tester les notifications")
        return
    
    user1 = users.first()
    user2 = users.last()
    
    print(f"👤 Utilisateur 1: {user1.username}")
    print(f"👤 Utilisateur 2: {user2.username}")
    
    # Créer un post de test
    post, created = Post.objects.get_or_create(
        author=user1,
        title="Post de test pour notifications",
        content="Ceci est un post de test pour vérifier le système de notifications.",
        defaults={'quartier': user1.quartier}
    )
    
    if created:
        print(f"✅ Post créé: {post.title}")
    else:
        print(f"📝 Post existant: {post.title}")
    
    # Créer un like de test
    like, created = PostLike.objects.get_or_create(
        user=user2,
        post=post
    )
    
    if created:
        print("✅ Like créé")
        # Créer la notification
        notification = NotificationService.notify_like(like)
        if notification:
            print(f"🔔 Notification de like créée: {notification.title}")
        else:
            print("⚠️ Pas de notification de like (probablement like sur son propre post)")
    else:
        print("📝 Like existant")
    
    # Créer un commentaire de test
    comment, created = PostComment.objects.get_or_create(
        author=user2,
        post=post,
        content="Commentaire de test pour les notifications!"
    )
    
    if created:
        print("✅ Commentaire créé")
        # Créer la notification
        notification = NotificationService.notify_comment(comment)
        if notification:
            print(f"🔔 Notification de commentaire créée: {notification.title}")
        else:
            print("⚠️ Pas de notification de commentaire (probablement commentaire sur son propre post)")
    else:
        print("📝 Commentaire existant")
    
    # Créer une notification de live
    notification = NotificationService.notify_live_started(user1, "Live de test")
    if notification:
        print(f"🔔 Notification de live créée: {notification.title}")
    
    # Créer une notification de mention
    notification = NotificationService.notify_mention(
        user2, 
        user1, 
        f"Salut @{user1.username}, comment ça va?",
        post
    )
    if notification:
        print(f"🔔 Notification de mention créée: {notification.title}")
    
    # Afficher les statistiques
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    
    print(f"\n📊 Statistiques:")
    print(f"   Total notifications: {total_notifications}")
    print(f"   Notifications non lues: {unread_notifications}")
    
    # Afficher les notifications récentes
    recent_notifications = Notification.objects.order_by('-created_at')[:5]
    print(f"\n🔔 Notifications récentes:")
    for notif in recent_notifications:
        status = "🔴" if not notif.is_read else "⚪"
        print(f"   {status} {notif.title} ({notif.notification_type})")

if __name__ == '__main__':
    print("🧪 Test du système de notifications")
    print("=" * 40)
    create_test_notifications()
    print("\n✅ Test terminé!") 
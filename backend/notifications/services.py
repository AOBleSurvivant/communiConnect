from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification, NotificationPreference
from posts.models import Post, PostComment, PostLike
import json

User = get_user_model()

class NotificationService:
    @staticmethod
    def create_notification(
        recipient,
        notification_type,
        title,
        message,
        sender=None,
        content_object=None,
        extra_data=None
    ):
        """
        Crée une notification pour un utilisateur
        """
        # Vérifier les préférences de l'utilisateur
        if not NotificationService._should_send_notification(recipient, notification_type):
            return None
        
        # Préparer les données
        content_type = None
        object_id = None
        
        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = content_object.id
        
        # Créer la notification
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            content_type=content_type,
            object_id=object_id,
            extra_data=extra_data or {}
        )
        
        # Envoyer la notification en temps réel (WebSocket)
        NotificationService._send_realtime_notification(notification)
        
        return notification
    
    @staticmethod
    def _should_send_notification(user, notification_type):
        """
        Vérifie si l'utilisateur veut recevoir ce type de notification
        """
        try:
            preferences = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            # Créer des préférences par défaut
            preferences = NotificationPreference.objects.create(user=user)
        
        # Mapping des types vers les préférences
        preference_mapping = {
            'like': 'likes_notifications',
            'comment': 'comments_notifications',
            'follow': 'follows_notifications',
            'live_started': 'live_notifications',
            'live_ended': 'live_notifications',
            'mention': 'mention_notifications',
            'system': 'system_notifications',
        }
        
        preference_field = preference_mapping.get(notification_type)
        if not preference_field:
            return True  # Par défaut, envoyer si pas de mapping
        
        return getattr(preferences, preference_field, True)
    
    @staticmethod
    def _send_realtime_notification(notification):
        """
        Envoie la notification en temps réel via WebSocket
        """
        # TODO: Implémenter l'envoi WebSocket
        # Pour l'instant, on utilise un système simple
        pass
    
    @staticmethod
    def notify_like(post_like):
        """
        Crée une notification pour un like
        """
        post = post_like.post
        liker = post_like.user
        
        # Ne pas notifier si l'utilisateur like son propre post
        if liker == post.author:
            return None
        
        title = f"{liker.first_name} a aimé votre publication"
        message = f"{liker.first_name} {liker.last_name} a aimé votre publication"
        
        return NotificationService.create_notification(
            recipient=post.author,
            notification_type='like',
            title=title,
            message=message,
            sender=liker,
            content_object=post,
            extra_data={
                'post_id': post.id,
                'post_title': post.title[:50] + '...' if len(post.title) > 50 else post.title
            }
        )
    
    @staticmethod
    def notify_comment(comment):
        """
        Crée une notification pour un commentaire
        """
        post = comment.post
        commenter = comment.author
        
        # Ne pas notifier si l'utilisateur commente son propre post
        if commenter == post.author:
            return None
        
        title = f"{commenter.first_name} a commenté votre publication"
        message = f"{commenter.first_name} {commenter.last_name} a commenté votre publication"
        
        return NotificationService.create_notification(
            recipient=post.author,
            notification_type='comment',
            title=title,
            message=message,
            sender=commenter,
            content_object=post,
            extra_data={
                'post_id': post.id,
                'comment_id': comment.id,
                'comment_content': comment.content[:100] + '...' if len(comment.content) > 100 else comment.content
            }
        )
    
    @staticmethod
    def notify_follow(follower, followed):
        """
        Crée une notification pour un nouveau follower
        """
        title = f"{follower.first_name} vous suit maintenant"
        message = f"{follower.first_name} {follower.last_name} a commencé à vous suivre"
        
        return NotificationService.create_notification(
            recipient=followed,
            notification_type='follow',
            title=title,
            message=message,
            sender=follower,
            extra_data={
                'follower_id': follower.id,
                'follower_name': f"{follower.first_name} {follower.last_name}"
            }
        )
    
    @staticmethod
    def notify_live_started(user, live_title):
        """
        Crée une notification pour un live démarré
        """
        title = f"{user.first_name} a démarré un live"
        message = f"{user.first_name} {user.last_name} a démarré un live : {live_title}"
        
        # Notifier tous les followers
        # TODO: Implémenter le système de followers
        # Pour l'instant, on notifie seulement l'utilisateur lui-même
        return NotificationService.create_notification(
            recipient=user,
            notification_type='live_started',
            title=title,
            message=message,
            sender=user,
            extra_data={
                'live_title': live_title,
                'user_id': user.id
            }
        )
    
    @staticmethod
    def notify_mention(user, mentioned_user, content, content_object=None):
        """
        Crée une notification pour une mention
        """
        title = f"{user.first_name} vous a mentionné"
        message = f"{user.first_name} {user.last_name} vous a mentionné dans une publication"
        
        return NotificationService.create_notification(
            recipient=mentioned_user,
            notification_type='mention',
            title=title,
            message=message,
            sender=user,
            content_object=content_object,
            extra_data={
                'content': content[:100] + '...' if len(content) > 100 else content,
                'mentioner_id': user.id
            }
        )
    
    @staticmethod
    def get_unread_count(user):
        """
        Retourne le nombre de notifications non lues
        """
        return Notification.objects.filter(recipient=user, is_read=False).count()
    
    @staticmethod
    def mark_as_read(user, notification_ids=None, mark_all=False):
        """
        Marque les notifications comme lues
        """
        queryset = Notification.objects.filter(recipient=user, is_read=False)
        
        if mark_all:
            queryset.update(is_read=True)
        elif notification_ids:
            queryset.filter(id__in=notification_ids).update(is_read=True)
        
        return queryset.count() 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PostLike, PostComment, Post, Media
from notifications.services import NotificationService


@receiver(post_save, sender=PostLike)
def notify_post_like(sender, instance, created, **kwargs):
    """
    Déclenche une notification quand quelqu'un like un post
    """
    if created:
        NotificationService.notify_like(instance)


@receiver(post_save, sender=PostComment)
def notify_post_comment(sender, instance, created, **kwargs):
    """
    Déclenche une notification quand quelqu'un commente un post
    """
    if created:
        NotificationService.notify_comment(instance)


@receiver(post_save, sender=Media)
def notify_live_started(sender, instance, created, **kwargs):
    """
    Déclenche une notification quand un live démarre
    """
    if created and instance.is_live and instance.media_type == 'live':
        NotificationService.notify_live_started(
            instance.posts.first().author if instance.posts.exists() else None,
            instance.title or "Live en cours"
        ) 
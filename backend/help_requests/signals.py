from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import HelpRequest, HelpResponse


@receiver(post_save, sender=HelpRequest)
def help_request_created(sender, instance, created, **kwargs):
    """Signal déclenché lors de la création d'une demande d'aide"""
    if created:
        # Envoyer une notification par email à l'auteur (optionnel)
        if hasattr(settings, 'SEND_HELP_REQUEST_NOTIFICATIONS') and settings.SEND_HELP_REQUEST_NOTIFICATIONS:
            try:
                context = {
                    'help_request': instance,
                    'user': instance.author,
                }
                
                subject = f'Votre demande d\'aide "{instance.title}" a été créée'
                html_message = render_to_string('help_requests/email/request_created.html', context)
                plain_message = render_to_string('help_requests/email/request_created.txt', context)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.author.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Erreur envoi email notification demande d'aide: {e}")


@receiver(post_save, sender=HelpResponse)
def help_response_created(sender, instance, created, **kwargs):
    """Signal déclenché lors de la création d'une réponse"""
    if created:
        # Envoyer une notification par email à l'auteur de la demande
        if hasattr(settings, 'SEND_HELP_RESPONSE_NOTIFICATIONS') and settings.SEND_HELP_RESPONSE_NOTIFICATIONS:
            try:
                context = {
                    'help_request': instance.help_request,
                    'response': instance,
                    'user': instance.help_request.author,
                }
                
                subject = f'Nouvelle réponse à votre demande "{instance.help_request.title}"'
                html_message = render_to_string('help_requests/email/response_received.html', context)
                plain_message = render_to_string('help_requests/email/response_received.txt', context)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.help_request.author.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Erreur envoi email notification réponse: {e}")


@receiver(post_save, sender=HelpResponse)
def help_response_status_changed(sender, instance, **kwargs):
    """Signal déclenché lors du changement de statut d'une réponse"""
    if instance.is_accepted or instance.is_rejected:
        # Envoyer une notification à l'auteur de la réponse
        if hasattr(settings, 'SEND_HELP_RESPONSE_STATUS_NOTIFICATIONS') and settings.SEND_HELP_RESPONSE_STATUS_NOTIFICATIONS:
            try:
                context = {
                    'help_request': instance.help_request,
                    'response': instance,
                    'user': instance.author,
                    'status': 'acceptée' if instance.is_accepted else 'rejetée'
                }
                
                subject = f'Votre réponse a été {context["status"]}'
                html_message = render_to_string('help_requests/email/response_status_changed.html', context)
                plain_message = render_to_string('help_requests/email/response_status_changed.txt', context)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.author.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Erreur envoi email notification statut réponse: {e}")


@receiver(post_save, sender=HelpRequest)
def help_request_status_changed(sender, instance, **kwargs):
    """Signal déclenché lors du changement de statut d'une demande"""
    if instance.status in ['completed', 'cancelled']:
        # Notifier les personnes qui ont répondu
        if hasattr(settings, 'SEND_HELP_REQUEST_STATUS_NOTIFICATIONS') and settings.SEND_HELP_REQUEST_STATUS_NOTIFICATIONS:
            try:
                responses = instance.responses.filter(is_accepted=True)
                for response in responses:
                    context = {
                        'help_request': instance,
                        'response': response,
                        'user': response.author,
                        'status': instance.get_status_display()
                    }
                    
                    subject = f'Demande "{instance.title}" {instance.get_status_display().lower()}'
                    html_message = render_to_string('help_requests/email/request_status_changed.html', context)
                    plain_message = render_to_string('help_requests/email/request_status_changed.txt', context)
                    
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[response.author.email],
                        html_message=html_message,
                        fail_silently=True
                    )
            except Exception as e:
                print(f"Erreur envoi email notification statut demande: {e}")


# Fonction pour nettoyer les demandes expirées (peut être appelée par une tâche cron)
def cleanup_expired_requests():
    """Nettoyer les demandes expirées"""
    expired_requests = HelpRequest.objects.filter(
        expires_at__lt=timezone.now(),
        status='open'
    )
    
    count = expired_requests.count()
    expired_requests.update(status='expired')
    
    print(f"{count} demande(s) d'aide expirée(s) nettoyée(s)")
    return count 
"""
Service de notifications push intelligentes pour les alertes communautaires
"""

import logging
from typing import List, Dict, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CommunityAlert, AlertNotification
from .services import AlertNotificationService

User = get_user_model()
logger = logging.getLogger(__name__)

try:
    import firebase_admin
    from firebase_admin import messaging, credentials
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logger.warning("Firebase Admin SDK non installé. Les notifications push ne fonctionneront pas.")

class PushNotificationService:
    """Service pour les notifications push avancées"""
    
    def __init__(self):
        if FIREBASE_AVAILABLE and not firebase_admin._apps:
            try:
                # Initialiser Firebase avec les credentials
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialisé avec succès")
            except Exception as e:
                logger.error(f"Erreur initialisation Firebase: {e}")
                FIREBASE_AVAILABLE = False
    
    def send_push_notification(self, notification: AlertNotification) -> bool:
        """Envoyer une notification push via Firebase"""
        if not FIREBASE_AVAILABLE:
            logger.warning("Firebase non disponible pour les notifications push")
            return False
        
        try:
            # Récupérer le token FCM de l'utilisateur
            fcm_token = getattr(notification.recipient.profile, 'fcm_token', None)
            
            if not fcm_token:
                logger.info(f"Pas de token FCM pour l'utilisateur {notification.recipient.username}")
                return False
            
            # Créer le message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.message
                ),
                data={
                    'alert_id': str(notification.alert.alert_id),
                    'category': notification.alert.category,
                    'type': notification.notification_type,
                    'urgency': 'high' if notification.alert.is_urgent else 'normal'
                },
                token=fcm_token,
                android=messaging.AndroidConfig(
                    priority='high' if notification.alert.is_urgent else 'normal',
                    notification=messaging.AndroidNotification(
                        icon='ic_notification',
                        color='#FF0000' if notification.alert.is_urgent else '#2196F3',
                        sound='default'
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound='default',
                            badge=1
                        )
                    )
                )
            )
            
            # Envoyer la notification
            response = messaging.send(message)
            logger.info(f"Push notification envoyée: {response} à {notification.recipient.username}")
            
            # Marquer comme envoyée
            notification.is_sent = True
            notification.save()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur push notification: {e}")
            return False
    
    def send_urgent_alert_push(self, alert: CommunityAlert) -> int:
        """Envoyer une notification push urgente à tous les utilisateurs à proximité"""
        if not FIREBASE_AVAILABLE:
            return 0
        
        try:
            # Trouver tous les utilisateurs à proximité
            nearby_users = AlertNotificationService.get_nearby_users(
                alert.latitude, alert.longitude, 10.0
            )
            
            # Créer les messages en lot
            messages = []
            for user in nearby_users:
                fcm_token = getattr(user.profile, 'fcm_token', None)
                if fcm_token and user.notification_preferences.push_notifications:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=f"🚨 URGENT: {alert.get_category_display()}",
                            body=f"{alert.title} - {alert.neighborhood or alert.city}"
                        ),
                        data={
                            'alert_id': str(alert.alert_id),
                            'category': alert.category,
                            'urgent': 'true',
                            'distance': str(alert.extra_data.get('distance_km', 0))
                        },
                        token=fcm_token,
                        android=messaging.AndroidConfig(
                            priority='high',
                            notification=messaging.AndroidNotification(
                                icon='ic_urgent_alert',
                                color='#FF0000',
                                sound='urgent_alert.wav',
                                channel_id='urgent_alerts'
                            )
                        ),
                        apns=messaging.APNSConfig(
                            payload=messaging.APNSPayload(
                                aps=messaging.Aps(
                                    sound='urgent_alert.wav',
                                    badge=1,
                                    category='URGENT_ALERT'
                                )
                            )
                        )
                    )
                    messages.append(message)
            
            # Envoyer en lot
            if messages:
                response = messaging.send_all(messages)
                logger.info(f"Notifications urgentes envoyées: {response.success_count}/{len(messages)}")
                return response.success_count
            else:
                logger.info("Aucun utilisateur à proximité avec notifications push activées")
                return 0
                
        except Exception as e:
            logger.error(f"Erreur notifications urgentes: {e}")
            return 0
    
    def send_bulk_notifications(self, notifications: List[AlertNotification]) -> Dict:
        """Envoyer des notifications en lot"""
        if not FIREBASE_AVAILABLE:
            return {'success': 0, 'failed': len(notifications)}
        
        try:
            messages = []
            for notification in notifications:
                fcm_token = getattr(notification.recipient.profile, 'fcm_token', None)
                if fcm_token and notification.recipient.notification_preferences.push_notifications:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=notification.title,
                            body=notification.message
                        ),
                        data={
                            'alert_id': str(notification.alert.alert_id),
                            'category': notification.alert.category,
                            'type': notification.notification_type
                        },
                        token=fcm_token
                    )
                    messages.append(message)
            
            if messages:
                response = messaging.send_all(messages)
                logger.info(f"Notifications en lot envoyées: {response.success_count}/{len(messages)}")
                
                # Marquer les notifications comme envoyées
                for notification in notifications:
                    if notification.recipient.profile.fcm_token:
                        notification.is_sent = True
                        notification.save()
                
                return {
                    'success': response.success_count,
                    'failed': response.failure_count,
                    'total': len(messages)
                }
            else:
                return {'success': 0, 'failed': 0, 'total': 0}
                
        except Exception as e:
            logger.error(f"Erreur notifications en lot: {e}")
            return {'success': 0, 'failed': len(notifications), 'total': len(notifications)}
    
    def send_scheduled_notification(self, alert: CommunityAlert, delay_minutes: int = 30):
        """Envoyer une notification programmée (pour rappels)"""
        from django.utils import timezone
        from datetime import timedelta
        
        scheduled_time = timezone.now() + timedelta(minutes=delay_minutes)
        
        # Créer une notification programmée
        notification = AlertNotification.objects.create(
            alert=alert,
            recipient=alert.author,
            notification_type='reminder',
            title=f"⏰ Rappel: {alert.title}",
            message=f"Votre alerte n'a pas encore été confirmée. Vérifiez la situation.",
            extra_data={'scheduled': True, 'scheduled_time': scheduled_time.isoformat()}
        )
        
        # TODO: Utiliser Celery ou un autre système de tâches pour la programmation
        logger.info(f"Notification programmée créée pour {scheduled_time}")
        return notification
    
    def update_user_fcm_token(self, user: User, fcm_token: str) -> bool:
        """Mettre à jour le token FCM d'un utilisateur"""
        try:
            if hasattr(user, 'profile'):
                user.profile.fcm_token = fcm_token
                user.profile.save()
                logger.info(f"Token FCM mis à jour pour {user.username}")
                return True
            else:
                logger.error(f"Profil non trouvé pour {user.username}")
                return False
        except Exception as e:
            logger.error(f"Erreur mise à jour token FCM: {e}")
            return False
    
    def remove_user_fcm_token(self, user: User) -> bool:
        """Supprimer le token FCM d'un utilisateur"""
        try:
            if hasattr(user, 'profile'):
                user.profile.fcm_token = None
                user.profile.save()
                logger.info(f"Token FCM supprimé pour {user.username}")
                return True
            else:
                logger.error(f"Profil non trouvé pour {user.username}")
                return False
        except Exception as e:
            logger.error(f"Erreur suppression token FCM: {e}")
            return False

# Instance globale du service
push_service = PushNotificationService() 
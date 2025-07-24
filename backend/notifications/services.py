from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification, NotificationPreference
from posts.models import Post, PostComment, PostLike
import json
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Count, Avg, F
from datetime import datetime, timedelta
import logging
import math
from typing import List, Dict, Optional
from .models import (
    Notification, 
    NotificationPreference, 
    CommunityAlert, 
    AlertNotification,
    User
)

User = get_user_model()

logger = logging.getLogger(__name__)

class NotificationService:
    """Service pour gérer les notifications"""
    
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
        """Créer une nouvelle notification"""
        try:
            notification = Notification.objects.create(
                recipient=recipient,
                sender=sender,
                notification_type=notification_type,
                title=title,
                message=message,
                content_object=content_object,
                extra_data=extra_data or {}
            )
            
            # Envoyer par email si activé
            if recipient.notification_preferences.email_notifications:
                NotificationService.send_email_notification(notification)
            
            # Envoyer push notification si activé
            if recipient.notification_preferences.push_notifications:
                NotificationService.send_push_notification(notification)
            
            logger.info(f"Notification créée: {notification.id} pour {recipient.username}")
            return notification
            
        except Exception as e:
            logger.error(f"Erreur création notification: {e}")
            return None
    
    @staticmethod
    def send_email_notification(notification):
        """Envoyer une notification par email"""
        try:
            subject = f"CommuniConnect - {notification.title}"
            message = f"""
            {notification.message}
            
            Connectez-vous sur CommuniConnect pour plus de détails.
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                fail_silently=True
            )
            
            logger.info(f"Email notification envoyé à {notification.recipient.email}")
            
        except Exception as e:
            logger.error(f"Erreur envoi email notification: {e}")
    
    @staticmethod
    def send_push_notification(notification):
        """Envoyer une notification push (à implémenter avec FCM ou autre)"""
        try:
            # TODO: Implémenter l'envoi de push notifications
            # Exemple avec Firebase Cloud Messaging (FCM)
            pass
            
        except Exception as e:
            logger.error(f"Erreur envoi push notification: {e}")
    
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


class AlertNotificationService:
    """Service spécialisé pour les notifications d'alertes communautaires"""
    
    @staticmethod
    def notify_nearby_users(alert: CommunityAlert, radius_km: float = 5.0):
        """Notifier les utilisateurs à proximité d'une alerte"""
        if not alert.latitude or not alert.longitude:
            logger.warning(f"Alerte {alert.alert_id} sans coordonnées géographiques")
            return
        
        try:
            # Trouver les utilisateurs dans le rayon spécifié
            nearby_users = AlertNotificationService.get_nearby_users(
                alert.latitude, 
                alert.longitude, 
                radius_km
            )
            
            # Filtrer les utilisateurs qui veulent recevoir des alertes
            users_to_notify = [
                user for user in nearby_users 
                if user.notification_preferences.community_alert_notifications
            ]
            
            # Créer les notifications
            notifications = []
            for user in users_to_notify:
                if user.id == alert.author.id:  # Ne pas notifier l'auteur
                    continue
                
                distance = AlertNotificationService.calculate_distance(
                    alert.latitude, alert.longitude,
                    user.profile.latitude, user.profile.longitude
                )
                
                notification = AlertNotification(
                    alert=alert,
                    recipient=user,
                    notification_type='nearby_alert',
                    title=f"🚨 Alerte à proximité: {alert.get_category_display()}",
                    message=f"{alert.title} - {alert.neighborhood or alert.city} ({distance:.1f} km)",
                    extra_data={
                        'distance_km': distance,
                        'category': alert.category,
                        'is_urgent': alert.is_urgent
                    }
                )
                notifications.append(notification)
            
            # Créer en lot pour optimiser les performances
            if notifications:
                AlertNotification.objects.bulk_create(notifications)
                logger.info(f"Notifications d'alerte envoyées à {len(notifications)} utilisateurs")
            
        except Exception as e:
            logger.error(f"Erreur notification utilisateurs à proximité: {e}")
    
    @staticmethod
    def notify_alert_status_change(alert: CommunityAlert, old_status: str):
        """Notifier les changements de statut d'une alerte"""
        try:
            # Utilisateurs à notifier: auteur + personnes qui ont offert leur aide
            recipients = set([alert.author])
            recipients.update(alert.help_offers.all())
            
            notifications = []
            for user in recipients:
                if not user.notification_preferences.community_alert_notifications:
                    continue
                
                status_emoji = {
                    'confirmed': '✅',
                    'in_progress': '🔄',
                    'resolved': '✅',
                    'false_alarm': '❌'
                }.get(alert.status, '📋')
                
                notification = AlertNotification(
                    alert=alert,
                    recipient=user,
                    notification_type='status_update',
                    title=f"{status_emoji} Statut mis à jour: {alert.get_status_display()}",
                    message=f"L'alerte '{alert.title}' est maintenant {alert.get_status_display().lower()}",
                    extra_data={
                        'old_status': old_status,
                        'new_status': alert.status,
                        'status_emoji': status_emoji
                    }
                )
                notifications.append(notification)
            
            if notifications:
                AlertNotification.objects.bulk_create(notifications)
                logger.info(f"Notifications de changement de statut envoyées à {len(notifications)} utilisateurs")
            
        except Exception as e:
            logger.error(f"Erreur notification changement statut: {e}")
    
    @staticmethod
    def notify_help_offer(help_offer):
        """Notifier l'auteur de l'alerte d'une nouvelle offre d'aide"""
        try:
            alert = help_offer.alert
            helper = help_offer.helper
            
            notification = AlertNotification(
                alert=alert,
                recipient=alert.author,
                notification_type='help_needed',
                title=f"🤝 Nouvelle offre d'aide",
                message=f"{helper.first_name or helper.username} propose son aide pour votre alerte",
                extra_data={
                    'helper_id': helper.id,
                    'helper_name': helper.first_name or helper.username,
                    'offer_type': help_offer.offer_type,
                    'help_offer_id': help_offer.id
                }
            )
            notification.save()
            
            logger.info(f"Notification d'offre d'aide envoyée à {alert.author.username}")
            
        except Exception as e:
            logger.error(f"Erreur notification offre d'aide: {e}")
    
    @staticmethod
    def get_nearby_users(lat: float, lon: float, radius_km: float) -> List[User]:
        """Récupérer les utilisateurs dans un rayon donné"""
        try:
            # Approximation: 1 degré ≈ 111 km
            radius_degrees = radius_km / 111.0
            
            nearby_users = User.objects.filter(
                profile__latitude__isnull=False,
                profile__longitude__isnull=False,
                profile__latitude__range=(
                    lat - radius_degrees,
                    lat + radius_degrees
                ),
                profile__longitude__range=(
                    lon - radius_degrees,
                    lon + radius_degrees
                )
            )
            
            # Calculer les distances exactes et filtrer
            users_with_distance = []
            for user in nearby_users:
                distance = AlertNotificationService.calculate_distance(
                    lat, lon,
                    user.profile.latitude, user.profile.longitude
                )
                
                if distance <= radius_km:
                    user.distance_km = distance
                    users_with_distance.append(user)
            
            # Trier par distance
            users_with_distance.sort(key=lambda x: x.distance_km)
            
            return users_with_distance
            
        except Exception as e:
            logger.error(f"Erreur récupération utilisateurs à proximité: {e}")
            return []
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculer la distance entre deux points géographiques (formule de Haversine)"""
        R = 6371  # Rayon de la Terre en km
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @staticmethod
    def send_urgent_alert_notifications(alert: CommunityAlert):
        """Envoyer des notifications spéciales pour les alertes urgentes"""
        if not alert.is_urgent:
            return
        
        try:
            # Notifier tous les utilisateurs dans un rayon plus large pour les alertes urgentes
            AlertNotificationService.notify_nearby_users(alert, radius_km=10.0)
            
            # Notification spéciale pour les autorités (si configuré)
            AlertNotificationService.notify_authorities(alert)
            
            logger.info(f"Notifications d'urgence envoyées pour l'alerte {alert.alert_id}")
            
        except Exception as e:
            logger.error(f"Erreur notifications d'urgence: {e}")
    
    @staticmethod
    def notify_authorities(alert: CommunityAlert):
        """Notifier les autorités locales (à implémenter selon les besoins)"""
        try:
            # TODO: Implémenter la notification des autorités
            # Cela pourrait inclure:
            # - Envoi d'emails aux services d'urgence
            # - Intégration avec des APIs de services d'urgence
            # - Notifications aux administrateurs de la plateforme
            
            logger.info(f"Notification aux autorités pour l'alerte {alert.alert_id}")
            
        except Exception as e:
            logger.error(f"Erreur notification autorités: {e}")


class AlertReliabilityService:
    """Service pour gérer la fiabilité des alertes"""
    
    @staticmethod
    def update_user_reliability_score(user: User):
        """Mettre à jour le score de fiabilité d'un utilisateur basé sur ses alertes"""
        try:
            user_alerts = CommunityAlert.objects.filter(author=user)
            
            if not user_alerts.exists():
                return
            
            # Calculer le score basé sur:
            # - Pourcentage d'alertes confirmées
            # - Pourcentage de fausses alertes
            # - Temps moyen de résolution
            
            confirmed_alerts = user_alerts.filter(status='confirmed').count()
            false_alarms = user_alerts.filter(status='false_alarm').count()
            total_alerts = user_alerts.count()
            
            if total_alerts > 0:
                confirmation_rate = (confirmed_alerts / total_alerts) * 100
                false_alarm_rate = (false_alarms / total_alerts) * 100
                
                # Score de base: 100 - taux de fausses alertes
                base_score = max(0, 100 - false_alarm_rate)
                
                # Bonus pour les alertes confirmées
                bonus = confirmation_rate * 0.2
                
                final_score = min(100, base_score + bonus)
                
                # Mettre à jour le profil utilisateur (si le champ existe)
                if hasattr(user, 'profile') and hasattr(user.profile, 'reliability_score'):
                    user.profile.reliability_score = final_score
                    user.profile.save()
                
                logger.info(f"Score de fiabilité mis à jour pour {user.username}: {final_score:.1f}")
            
        except Exception as e:
            logger.error(f"Erreur mise à jour score fiabilité: {e}")
    
    @staticmethod
    def flag_unreliable_user(user: User):
        """Marquer un utilisateur comme peu fiable"""
        try:
            # Réduire le score de fiabilité
            if hasattr(user, 'profile') and hasattr(user.profile, 'reliability_score'):
                user.profile.reliability_score = max(0, user.profile.reliability_score - 20)
                user.profile.save()
            
            # Créer une notification d'avertissement
            NotificationService.create_notification(
                recipient=user,
                notification_type='system',
                title='Avertissement - Fiabilité des alertes',
                message='Votre score de fiabilité a été réduit en raison de fausses alertes. Veuillez être plus vigilant.',
                extra_data={'warning_type': 'reliability_reduced'}
            )
            
            logger.warning(f"Utilisateur {user.username} marqué comme peu fiable")
            
        except Exception as e:
            logger.error(f"Erreur marquage utilisateur peu fiable: {e}")


class AlertStatisticsService:
    """Service pour générer les statistiques d'alertes"""
    
    @staticmethod
    def generate_daily_statistics():
        """Générer les statistiques quotidiennes"""
        try:
            today = timezone.now().date()
            start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            
            AlertStatisticsService._generate_statistics('daily', start_date, end_date)
            
        except Exception as e:
            logger.error(f"Erreur génération statistiques quotidiennes: {e}")
    
    @staticmethod
    def generate_weekly_statistics():
        """Générer les statistiques hebdomadaires"""
        try:
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            start_date = timezone.make_aware(datetime.combine(start_of_week, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_of_week, datetime.max.time()))
            
            AlertStatisticsService._generate_statistics('weekly', start_date, end_date)
            
        except Exception as e:
            logger.error(f"Erreur génération statistiques hebdomadaires: {e}")
    
    @staticmethod
    def _generate_statistics(statistic_type: str, start_date, end_date):
        """Générer les statistiques pour une période donnée"""
        try:
            alerts = CommunityAlert.objects.filter(
                created_at__range=[start_date, end_date]
            )
            
            # Vérifier si les statistiques existent déjà
            existing_stats = AlertStatistics.objects.filter(
                statistic_type=statistic_type,
                period_start=start_date,
                period_end=end_date
            ).first()
            
            if existing_stats:
                stats = existing_stats
            else:
                stats = AlertStatistics(
                    statistic_type=statistic_type,
                    period_start=start_date,
                    period_end=end_date
                )
            
            # Calculer les statistiques
            stats.total_alerts = alerts.count()
            stats.resolved_alerts = alerts.filter(status='resolved').count()
            stats.false_alarms = alerts.filter(status='false_alarm').count()
            
            # Statistiques par catégorie
            for category, _ in CommunityAlert.ALERT_CATEGORIES:
                count = alerts.filter(category=category).count()
                setattr(stats, f'{category}_count', count)
            
            # Statistiques géographiques
            city_stats = alerts.values('city').annotate(count=Count('id'))
            stats.cities_data = {item['city']: item['count'] for item in city_stats if item['city']}
            
            neighborhood_stats = alerts.values('neighborhood').annotate(count=Count('id'))
            stats.neighborhoods_data = {item['neighborhood']: item['count'] for item in neighborhood_stats if item['neighborhood']}
            
            # Score de fiabilité moyen
            avg_reliability = alerts.aggregate(avg=Avg('reliability_score'))['avg']
            stats.avg_reliability_score = avg_reliability or 0.0
            stats.reliable_alerts_count = alerts.filter(reliability_score__gte=70.0).count()
            
            # Temps de résolution moyen
            resolved_alerts = alerts.filter(status='resolved', resolved_at__isnull=False)
            if resolved_alerts.exists():
                avg_time = resolved_alerts.aggregate(
                    avg_time=Avg(F('resolved_at') - F('created_at'))
                )['avg_time']
                stats.avg_resolution_time_hours = avg_time.total_seconds() / 3600 if avg_time else 0
            else:
                stats.avg_resolution_time_hours = 0
            
            stats.save()
            
            logger.info(f"Statistiques {statistic_type} générées pour {start_date.date()}")
            
        except Exception as e:
            logger.error(f"Erreur génération statistiques: {e}") 


class PushNotificationService:
    """Service pour les notifications push avancées"""
    
    def __init__(self):
        self.fcm_available = self._check_fcm_availability()
    
    def _check_fcm_availability(self):
        """Vérifier si Firebase est disponible"""
        try:
            # Vérifier si les variables d'environnement sont configurées
            from django.conf import settings
            return hasattr(settings, 'FIREBASE_CREDENTIALS') or hasattr(settings, 'FIREBASE_API_KEY')
        except:
            return False
    
    @staticmethod
    def send_push_notification(user, title, message, data=None, priority='normal'):
        """Envoyer une notification push à un utilisateur"""
        try:
            if not user.fcm_token:
                logger.warning(f"Utilisateur {user.id} n'a pas de token FCM")
                return False
            
            # Préparer les données de notification
            notification_data = {
                'title': title,
                'body': message,
                'data': data or {},
                'priority': priority,
                'timestamp': timezone.now().isoformat()
            }
            
            # Simuler l'envoi (en développement)
            if settings.DEBUG:
                logger.info(f"Notification push simulée pour {user.username}: {title}")
                return True
            
            # En production, utiliser Firebase
            if PushNotificationService().fcm_available:
                return PushNotificationService._send_via_firebase(user.fcm_token, notification_data)
            else:
                logger.warning("Firebase non configuré, notification simulée")
                return True
                
        except Exception as e:
            logger.error(f"Erreur envoi notification push: {e}")
            return False
    
    @staticmethod
    def send_urgent_alert_push(alert):
        """Envoyer une notification push urgente pour une alerte"""
        try:
            # Récupérer les utilisateurs à proximité
            nearby_users = PushNotificationService._get_nearby_users(alert)
            
            # Préparer le message
            title = f"🚨 Alerte {alert.get_category_display()}"
            message = f"{alert.title} - {alert.neighborhood or alert.city}"
            
            # Données supplémentaires
            data = {
                'alert_id': str(alert.alert_id),
                'category': alert.category,
                'latitude': str(alert.latitude) if alert.latitude else '',
                'longitude': str(alert.longitude) if alert.longitude else '',
                'type': 'urgent_alert'
            }
            
            # Envoyer aux utilisateurs à proximité
            success_count = 0
            for user in nearby_users:
                if PushNotificationService.send_push_notification(
                    user, title, message, data, priority='high'
                ):
                    success_count += 1
            
            logger.info(f"Notifications urgentes envoyées: {success_count}/{len(nearby_users)}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Erreur notification alerte urgente: {e}")
            return False
    
    @staticmethod
    def send_bulk_notifications(notifications_data):
        """Envoyer des notifications en lot"""
        try:
            success_count = 0
            total_count = len(notifications_data)
            
            for notification in notifications_data:
                user = notification.get('user')
                title = notification.get('title')
                message = notification.get('message')
                data = notification.get('data', {})
                priority = notification.get('priority', 'normal')
                
                if PushNotificationService.send_push_notification(user, title, message, data, priority):
                    success_count += 1
            
            logger.info(f"Notifications en lot: {success_count}/{total_count} envoyées")
            return success_count / max(total_count, 1) * 100
            
        except Exception as e:
            logger.error(f"Erreur notifications en lot: {e}")
            return 0
    
    @staticmethod
    def update_user_fcm_token(user, token):
        """Mettre à jour le token FCM d'un utilisateur"""
        try:
            if token and token != user.fcm_token:
                user.fcm_token = token
                user.save(update_fields=['fcm_token'])
                logger.info(f"Token FCM mis à jour pour {user.username}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erreur mise à jour token FCM: {e}")
            return False
    
    @staticmethod
    def _get_nearby_users(alert, radius_km=5.0):
        """Récupérer les utilisateurs à proximité d'une alerte"""
        try:
            if not alert.latitude or not alert.longitude:
                return []
            
            # Calculer la boîte de recherche
            lat_delta = radius_km / 111.0  # 1 degré ≈ 111 km
            lon_delta = radius_km / (111.0 * math.cos(math.radians(alert.latitude)))
            
            # Filtrer les utilisateurs dans la zone
            nearby_users = User.objects.filter(
                latitude__range=(alert.latitude - lat_delta, alert.latitude + lat_delta),
                longitude__range=(alert.longitude - lon_delta, alert.longitude + lon_delta),
                fcm_token__isnull=False
            ).exclude(fcm_token='')
            
            # Filtrer par distance exacte
            filtered_users = []
            for user in nearby_users:
                distance = PushNotificationService._calculate_distance(
                    alert.latitude, alert.longitude,
                    user.latitude, user.longitude
                )
                if distance <= radius_km:
                    filtered_users.append(user)
            
            return filtered_users
            
        except Exception as e:
            logger.error(f"Erreur récupération utilisateurs proximité: {e}")
            return []
    
    @staticmethod
    def _calculate_distance(lat1, lon1, lat2, lon2):
        """Calculer la distance entre deux points (formule de Haversine)"""
        try:
            R = 6371  # Rayon de la Terre en km
            
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return R * c
        except:
            return float('inf')
    
    @staticmethod
    def _send_via_firebase(token, notification_data):
        """Envoyer via Firebase Cloud Messaging"""
        try:
            # En développement, simuler l'envoi
            if settings.DEBUG:
                logger.info(f"Notification Firebase simulée: {notification_data['title']}")
                return True
            
            # En production, utiliser Firebase
            import firebase_admin
            from firebase_admin import messaging
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification_data['title'],
                    body=notification_data['body']
                ),
                data=notification_data['data'],
                token=token,
                android=messaging.AndroidConfig(
                    priority='high' if notification_data['priority'] == 'high' else 'normal'
                )
            )
            
            response = messaging.send(message)
            logger.info(f"Notification Firebase envoyée: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur Firebase: {e}")
            return False 
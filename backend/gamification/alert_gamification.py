"""
Système de gamification pour les alertes communautaires
"""

import logging
from typing import Dict, List, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from notifications.models import CommunityAlert, AlertNotification
from django.db.models import Count
from datetime import timedelta

User = get_user_model()
logger = logging.getLogger(__name__)

class AlertAchievement(models.Model):
    """Réalisations pour les alertes communautaires"""
    
    ACHIEVEMENT_TYPES = [
        ('first_alert', 'Première Alerte'),
        ('reliable_user', 'Utilisateur Fiable'),
        ('helpful_user', 'Utilisateur Serviable'),
        ('urgent_responder', 'Répondeur d\'Urgence'),
        ('community_guardian', 'Gardien de la Communauté'),
        ('verified_expert', 'Expert Vérifié'),
        ('quick_responder', 'Répondeur Rapide'),
        ('neighborhood_watch', 'Veilleur de Quartier'),
        ('emergency_hero', 'Héros d\'Urgence'),
        ('community_leader', 'Leader Communautaire'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    earned_at = models.DateTimeField(auto_now_add=True)
    points_earned = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'achievement_type']
        ordering = ['-earned_at']
        verbose_name = "Réalisation d'Alerte"
        verbose_name_plural = "Réalisations d'Alertes"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_achievement_type_display()}"

class UserLevel(models.Model):
    """Niveaux d'utilisateur basés sur les points"""
    
    LEVELS = [
        (1, 'Débutant'),
        (2, 'Actif'),
        (3, 'Fiable'),
        (4, 'Expert'),
        (5, 'Maître'),
        (6, 'Légende'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alert_level')
    level = models.IntegerField(choices=LEVELS, default=1)
    points = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Niveau d'Utilisateur"
        verbose_name_plural = "Niveaux d'Utilisateurs"
    
    def __str__(self):
        return f"{self.user.username} - Niveau {self.level} ({self.points} points)"

class AlertGamificationService:
    """Service de gamification pour les alertes"""
    
    def __init__(self):
        self.achievement_configs = {
            'first_alert': {
                'points': 50,
                'description': 'Vous avez créé votre première alerte !'
            },
            'reliable_user': {
                'points': 100,
                'description': '80% de vos alertes ont été confirmées'
            },
            'helpful_user': {
                'points': 75,
                'description': 'Vous avez offert de l\'aide 5 fois'
            },
            'urgent_responder': {
                'points': 150,
                'description': 'Vous avez répondu à 3 alertes urgentes'
            },
            'community_guardian': {
                'points': 200,
                'description': 'Vous avez créé 20 alertes confirmées'
            },
            'verified_expert': {
                'points': 300,
                'description': 'Vous êtes un expert vérifié avec 95% de fiabilité'
            },
            'quick_responder': {
                'points': 125,
                'description': 'Vous avez répondu à une alerte en moins de 5 minutes'
            },
            'neighborhood_watch': {
                'points': 175,
                'description': 'Vous surveillez activement votre quartier'
            },
            'emergency_hero': {
                'points': 250,
                'description': 'Vous avez aidé lors de 10 situations d\'urgence'
            },
            'community_leader': {
                'points': 500,
                'description': 'Vous êtes un leader reconnu de la communauté'
            }
        }
    
    def check_achievements(self, user: User, alert: CommunityAlert = None) -> List[AlertAchievement]:
        """Vérifier et attribuer les réalisations"""
        achievements = []
        
        try:
            # Première alerte
            if not user.alert_achievements.filter(achievement_type='first_alert').exists():
                if CommunityAlert.objects.filter(author=user).count() >= 1:
                    achievement = self._create_achievement(user, 'first_alert')
                    achievements.append(achievement)
            
            # Utilisateur fiable
            if not user.alert_achievements.filter(achievement_type='reliable_user').exists():
                user_alerts = CommunityAlert.objects.filter(author=user)
                if user_alerts.count() >= 10:
                    confirmed_alerts = user_alerts.filter(status='confirmed').count()
                    if confirmed_alerts >= 8:  # 80% de confirmation
                        achievement = self._create_achievement(user, 'reliable_user')
                        achievements.append(achievement)
            
            # Utilisateur serviable
            if not user.alert_achievements.filter(achievement_type='helpful_user').exists():
                help_offers = user.offered_help_alerts.count()
                if help_offers >= 5:
                    achievement = self._create_achievement(user, 'helpful_user')
                    achievements.append(achievement)
            
            # Répondeur d'urgence
            if not user.alert_achievements.filter(achievement_type='urgent_responder').exists():
                urgent_alerts = CommunityAlert.objects.filter(
                    category__in=['fire', 'medical', 'security', 'gas_leak'],
                    author=user,
                    status='confirmed'
                ).count()
                if urgent_alerts >= 3:
                    achievement = self._create_achievement(user, 'urgent_responder')
                    achievements.append(achievement)
            
            # Gardien de la communauté
            if not user.alert_achievements.filter(achievement_type='community_guardian').exists():
                confirmed_alerts = CommunityAlert.objects.filter(
                    author=user,
                    status='confirmed'
                ).count()
                if confirmed_alerts >= 20:
                    achievement = self._create_achievement(user, 'community_guardian')
                    achievements.append(achievement)
            
            # Expert vérifié
            if not user.alert_achievements.filter(achievement_type='verified_expert').exists():
                user_alerts = CommunityAlert.objects.filter(author=user)
                if user_alerts.count() >= 50:
                    confirmed_alerts = user_alerts.filter(status='confirmed').count()
                    false_alarms = user_alerts.filter(status='false_alarm').count()
                    if confirmed_alerts >= 47 and false_alarms <= 2:  # 95% de fiabilité
                        achievement = self._create_achievement(user, 'verified_expert')
                        achievements.append(achievement)
            
            # Répondeur rapide
            if not user.alert_achievements.filter(achievement_type='quick_responder').exists():
                if alert and alert.created_at:
                    # Vérifier si l'utilisateur a répondu rapidement à cette alerte
                    response_time = self._check_quick_response(user, alert)
                    if response_time and response_time < 300:  # 5 minutes
                        achievement = self._create_achievement(user, 'quick_responder')
                        achievements.append(achievement)
            
            # Veilleur de quartier
            if not user.alert_achievements.filter(achievement_type='neighborhood_watch').exists():
                neighborhood_alerts = CommunityAlert.objects.filter(
                    author=user,
                    neighborhood__isnull=False
                ).values('neighborhood').annotate(
                    count=Count('id')
                ).filter(count__gte=5).count()
                if neighborhood_alerts >= 3:
                    achievement = self._create_achievement(user, 'neighborhood_watch')
                    achievements.append(achievement)
            
            # Héros d'urgence
            if not user.alert_achievements.filter(achievement_type='emergency_hero').exists():
                emergency_help = user.offered_help_alerts.filter(
                    alert__category__in=['fire', 'medical', 'security', 'gas_leak']
                ).count()
                if emergency_help >= 10:
                    achievement = self._create_achievement(user, 'emergency_hero')
                    achievements.append(achievement)
            
            # Leader communautaire
            if not user.alert_achievements.filter(achievement_type='community_leader').exists():
                total_points = self.calculate_user_score(user)
                if total_points >= 1000:
                    achievement = self._create_achievement(user, 'community_leader')
                    achievements.append(achievement)
            
            # Mettre à jour le niveau de l'utilisateur
            if achievements:
                self._update_user_level(user)
            
            return achievements
            
        except Exception as e:
            logger.error(f"Erreur vérification réalisations: {e}")
            return []
    
    def calculate_user_score(self, user: User) -> int:
        """Calculer le score total d'un utilisateur"""
        try:
            # Points de base des réalisations
            base_score = user.alert_achievements.aggregate(
                total_points=models.Sum('points_earned')
            )['total_points'] or 0
            
            # Bonus pour la fiabilité
            user_alerts = CommunityAlert.objects.filter(author=user)
            if user_alerts.count() > 0:
                reliability_bonus = user_alerts.aggregate(
                    avg_reliability=models.Avg('reliability_score')
                )['avg_reliability'] or 0
                base_score += int(reliability_bonus * 0.5)
            
            # Bonus pour l'aide
            help_bonus = user.offered_help_alerts.count() * 10
            base_score += help_bonus
            
            # Bonus pour les alertes confirmées
            confirmed_bonus = user_alerts.filter(status='confirmed').count() * 5
            base_score += confirmed_bonus
            
            # Malus pour les fausses alertes
            false_alarm_malus = user_alerts.filter(status='false_alarm').count() * 20
            base_score = max(0, base_score - false_alarm_malus)
            
            return base_score
            
        except Exception as e:
            logger.error(f"Erreur calcul score utilisateur: {e}")
            return 0
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Obtenir le classement des utilisateurs"""
        try:
            # Calculer les scores pour tous les utilisateurs actifs
            active_users = User.objects.filter(
                authored_alerts__created_at__gte=timezone.now() - timedelta(days=30)
            ).distinct()
            
            leaderboard = []
            for user in active_users:
                score = self.calculate_user_score(user)
                if score > 0:
                    leaderboard.append({
                        'username': user.username,
                        'score': score,
                        'achievements_count': user.alert_achievements.count(),
                        'alerts_count': user.authored_alerts.count(),
                        'help_offers_count': user.offered_help_alerts.count(),
                        'level': self._get_user_level(user)
                    })
            
            # Trier par score décroissant
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Erreur leaderboard: {e}")
            return []
    
    def get_user_stats(self, user: User) -> Dict:
        """Obtenir les statistiques détaillées d'un utilisateur"""
        try:
            user_alerts = CommunityAlert.objects.filter(author=user)
            user_achievements = user.alert_achievements.all()
            
            stats = {
                'total_alerts': user_alerts.count(),
                'confirmed_alerts': user_alerts.filter(status='confirmed').count(),
                'false_alarms': user_alerts.filter(status='false_alarm').count(),
                'resolved_alerts': user_alerts.filter(status='resolved').count(),
                'urgent_alerts': user_alerts.filter(
                    category__in=['fire', 'medical', 'security', 'gas_leak']
                ).count(),
                'help_offers': user.offered_help_alerts.count(),
                'achievements': user_achievements.count(),
                'total_score': self.calculate_user_score(user),
                'level': self._get_user_level(user),
                'reliability_score': user_alerts.aggregate(
                    avg_reliability=models.Avg('reliability_score')
                )['avg_reliability'] or 0,
                'achievements_list': [
                    {
                        'type': achievement.achievement_type,
                        'name': achievement.get_achievement_type_display(),
                        'points': achievement.points_earned,
                        'earned_at': achievement.earned_at.isoformat()
                    }
                    for achievement in user_achievements
                ]
            }
            
            # Calculer les pourcentages
            if stats['total_alerts'] > 0:
                stats['confirmation_rate'] = (stats['confirmed_alerts'] / stats['total_alerts']) * 100
                stats['false_alarm_rate'] = (stats['false_alarms'] / stats['total_alerts']) * 100
            else:
                stats['confirmation_rate'] = 0
                stats['false_alarm_rate'] = 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur stats utilisateur: {e}")
            return {}
    
    def _create_achievement(self, user: User, achievement_type: str) -> AlertAchievement:
        """Créer une réalisation"""
        config = self.achievement_configs.get(achievement_type, {})
        
        achievement = AlertAchievement.objects.create(
            user=user,
            achievement_type=achievement_type,
            points_earned=config.get('points', 50),
            description=config.get('description', '')
        )
        
        logger.info(f"Réalisation '{achievement_type}' attribuée à {user.username}")
        return achievement
    
    def _update_user_level(self, user: User):
        """Mettre à jour le niveau de l'utilisateur"""
        try:
            score = self.calculate_user_score(user)
            level, created = UserLevel.objects.get_or_create(user=user)
            
            # Calculer le nouveau niveau
            new_level = 1
            if score >= 1000:
                new_level = 6  # Légende
            elif score >= 500:
                new_level = 5  # Maître
            elif score >= 250:
                new_level = 4  # Expert
            elif score >= 100:
                new_level = 3  # Fiable
            elif score >= 50:
                new_level = 2  # Actif
            
            if level.level != new_level:
                level.level = new_level
                level.points = score
                level.save()
                logger.info(f"Niveau mis à jour pour {user.username}: {new_level}")
            
        except Exception as e:
            logger.error(f"Erreur mise à jour niveau: {e}")
    
    def _get_user_level(self, user: User) -> int:
        """Obtenir le niveau d'un utilisateur"""
        try:
            level_obj = UserLevel.objects.get(user=user)
            return level_obj.level
        except UserLevel.DoesNotExist:
            return 1
    
    def _check_quick_response(self, user: User, alert: CommunityAlert) -> Optional[int]:
        """Vérifier si l'utilisateur a répondu rapidement à une alerte"""
        try:
            # Chercher les offres d'aide de l'utilisateur pour cette alerte
            help_offers = user.offered_help_alerts.filter(alert=alert)
            if help_offers.exists():
                first_offer = help_offers.earliest('created_at')
                response_time = (first_offer.created_at - alert.created_at).total_seconds()
                return response_time
            return None
        except Exception as e:
            logger.error(f"Erreur vérification réponse rapide: {e}")
            return None

# Instance globale du service
gamification_service = AlertGamificationService() 
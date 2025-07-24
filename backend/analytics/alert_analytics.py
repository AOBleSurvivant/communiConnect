"""
Service d'analytics avancées et prédictives pour les alertes communautaires
"""

import logging
from typing import Dict, List, Optional, Tuple
from django.db.models import Count, Avg, Q, F, Sum
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from notifications.models import CommunityAlert, AlertNotification, AlertReport
import json

User = get_user_model()
logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logger.warning("Pandas/Scikit-learn non installé. Les analytics prédictives ne fonctionneront pas.")

class AlertAnalyticsService:
    """Service d'analytics avancées pour les alertes"""
    
    def __init__(self):
        self.ml_available = ML_AVAILABLE
    
    def get_alert_trends(self, days: int = 30) -> Dict:
        """Analyser les tendances des alertes"""
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=days)
            
            # Données par jour
            daily_alerts = CommunityAlert.objects.filter(
                created_at__range=(start_date, end_date)
            ).extra(
                select={'day': 'date(created_at)'}
            ).values('day').annotate(
                count=Count('id'),
                urgent_count=Count('id', filter=Q(category__in=['fire', 'medical', 'security', 'gas_leak'])),
                confirmed_count=Count('id', filter=Q(status='confirmed')),
                false_alarm_count=Count('id', filter=Q(status='false_alarm')),
                resolved_count=Count('id', filter=Q(status='resolved'))
            ).order_by('day')
            
            # Tendances par catégorie
            category_trends = CommunityAlert.objects.filter(
                created_at__range=(start_date, end_date)
            ).values('category').annotate(
                count=Count('id'),
                avg_reliability=Avg('reliability_score'),
                false_alarm_rate=Count('id', filter=Q(status='false_alarm')) * 100.0 / Count('id'),
                avg_resolution_time=Avg(F('resolved_at') - F('created_at'))
            )
            
            # Prédictions
            predictions = self._predict_future_alerts(daily_alerts) if self.ml_available else {}
            
            # Statistiques globales
            total_alerts = sum(d['count'] for d in daily_alerts)
            urgent_alerts = sum(d['urgent_count'] for d in daily_alerts)
            confirmed_alerts = sum(d['confirmed_count'] for d in daily_alerts)
            false_alarms = sum(d['false_alarm_count'] for d in daily_alerts)
            
            return {
                'daily_trends': list(daily_alerts),
                'category_trends': list(category_trends),
                'predictions': predictions,
                'summary': {
                    'total_alerts': total_alerts,
                    'urgent_alerts': urgent_alerts,
                    'confirmed_alerts': confirmed_alerts,
                    'false_alarms': false_alarms,
                    'accuracy_rate': ((confirmed_alerts - false_alarms) / total_alerts * 100) if total_alerts > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse tendances: {e}")
            return {}
    
    def get_hotspots(self, days: int = 7) -> List[Dict]:
        """Identifier les zones à forte activité d'alertes"""
        try:
            start_date = timezone.now() - timedelta(days=days)
            
            hotspots = CommunityAlert.objects.filter(
                created_at__gte=start_date
            ).values('neighborhood', 'city').annotate(
                alert_count=Count('id'),
                urgent_count=Count('id', filter=Q(category__in=['fire', 'medical', 'security', 'gas_leak'])),
                avg_lat=Avg('latitude'),
                avg_lng=Avg('longitude'),
                avg_reliability=Avg('reliability_score'),
                false_alarm_rate=Count('id', filter=Q(status='false_alarm')) * 100.0 / Count('id')
            ).filter(alert_count__gte=3).order_by('-alert_count')
            
            return list(hotspots)
            
        except Exception as e:
            logger.error(f"Erreur analyse hotspots: {e}")
            return []
    
    def get_user_reliability_insights(self) -> Dict:
        """Analyser la fiabilité des utilisateurs"""
        try:
            # Utilisateurs les plus fiables
            reliable_users = User.objects.annotate(
                alert_count=Count('authored_alerts'),
                confirmed_alerts=Count('authored_alerts', filter=Q(authored_alerts__status='confirmed')),
                false_alarms=Count('authored_alerts', filter=Q(authored_alerts__status='false_alarm')),
                resolved_alerts=Count('authored_alerts', filter=Q(authored_alerts__status='resolved'))
            ).filter(alert_count__gte=5).order_by('-confirmed_alerts')
            
            # Statistiques globales
            total_users = User.objects.count()
            active_users = User.objects.filter(
                authored_alerts__created_at__gte=timezone.now() - timedelta(days=30)
            ).distinct().count()
            
            # Top utilisateurs fiables
            top_reliable = []
            for user in reliable_users[:10]:
                if user.alert_count > 0:
                    reliability_score = (user.confirmed_alerts / user.alert_count) * 100
                    top_reliable.append({
                        'username': user.username,
                        'alert_count': user.alert_count,
                        'confirmed_alerts': user.confirmed_alerts,
                        'false_alarms': user.false_alarms,
                        'resolved_alerts': user.resolved_alerts,
                        'reliability_score': reliability_score
                    })
            
            return {
                'reliable_users': top_reliable,
                'total_users': total_users,
                'active_users': active_users,
                'engagement_rate': (active_users / total_users * 100) if total_users > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse fiabilité utilisateurs: {e}")
            return {}
    
    def get_response_time_analytics(self) -> Dict:
        """Analyser les temps de réponse aux alertes"""
        try:
            # Alertes avec temps de résolution
            resolved_alerts = CommunityAlert.objects.filter(
                status='resolved',
                resolved_at__isnull=False
            ).annotate(
                resolution_time=F('resolved_at') - F('created_at')
            )
            
            # Statistiques de temps de réponse
            avg_resolution_time = resolved_alerts.aggregate(
                avg_time=Avg('resolution_time')
            )['avg_time']
            
            # Temps de réponse par catégorie
            response_by_category = resolved_alerts.values('category').annotate(
                avg_time=Avg('resolution_time'),
                count=Count('id')
            )
            
            # Temps de réponse par urgence
            urgent_response = resolved_alerts.filter(
                category__in=['fire', 'medical', 'security', 'gas_leak']
            ).aggregate(avg_time=Avg('resolution_time'))['avg_time']
            
            normal_response = resolved_alerts.exclude(
                category__in=['fire', 'medical', 'security', 'gas_leak']
            ).aggregate(avg_time=Avg('resolution_time'))['avg_time']
            
            return {
                'overall_avg_response': avg_resolution_time,
                'urgent_avg_response': urgent_response,
                'normal_avg_response': normal_response,
                'by_category': list(response_by_category)
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse temps de réponse: {e}")
            return {}
    
    def get_community_engagement_metrics(self) -> Dict:
        """Métriques d'engagement communautaire"""
        try:
            # Statistiques d'engagement
            total_alerts = CommunityAlert.objects.count()
            total_help_offers = CommunityAlert.objects.aggregate(
                total_offers=Sum('help_offers_count')
            )['total_offers'] or 0
            
            # Utilisateurs actifs
            active_users_7d = User.objects.filter(
                authored_alerts__created_at__gte=timezone.now() - timedelta(days=7)
            ).distinct().count()
            
            active_users_30d = User.objects.filter(
                authored_alerts__created_at__gte=timezone.now() - timedelta(days=30)
            ).distinct().count()
            
            # Taux de participation
            participation_rate = (active_users_30d / User.objects.count() * 100) if User.objects.count() > 0 else 0
            
            # Alertes par utilisateur actif
            avg_alerts_per_user = total_alerts / active_users_30d if active_users_30d > 0 else 0
            
            return {
                'total_alerts': total_alerts,
                'total_help_offers': total_help_offers,
                'active_users_7d': active_users_7d,
                'active_users_30d': active_users_30d,
                'participation_rate': participation_rate,
                'avg_alerts_per_user': avg_alerts_per_user,
                'help_engagement_rate': (total_help_offers / total_alerts * 100) if total_alerts > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Erreur métriques engagement: {e}")
            return {}
    
    def get_geographic_insights(self) -> Dict:
        """Analyses géographiques des alertes"""
        try:
            # Alertes par région
            alerts_by_region = CommunityAlert.objects.values('city').annotate(
                alert_count=Count('id'),
                urgent_count=Count('id', filter=Q(category__in=['fire', 'medical', 'security', 'gas_leak'])),
                avg_reliability=Avg('reliability_score')
            ).order_by('-alert_count')
            
            # Densité d'alertes
            total_alerts = CommunityAlert.objects.count()
            alerts_with_location = CommunityAlert.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            ).count()
            
            # Zones les plus actives
            active_zones = alerts_by_region.filter(alert_count__gte=5)[:10]
            
            return {
                'alerts_by_region': list(alerts_by_region),
                'active_zones': list(active_zones),
                'location_coverage': (alerts_with_location / total_alerts * 100) if total_alerts > 0 else 0,
                'total_regions': alerts_by_region.count()
            }
            
        except Exception as e:
            logger.error(f"Erreur insights géographiques: {e}")
            return {}
    
    def _predict_future_alerts(self, daily_data: List[Dict]) -> Dict:
        """Prédire les alertes futures"""
        if not self.ml_available:
            return {}
        
        try:
            # Préparer les données
            df = pd.DataFrame(daily_data)
            if df.empty or len(df) < 7:
                return {}
            
            df['day'] = pd.to_datetime(df['day'])
            df = df.sort_values('day')
            
            # Créer les features
            df['day_of_week'] = df['day'].dt.dayofweek
            df['month'] = df['day'].dt.month
            df['day_of_month'] = df['day'].dt.day
            
            # Modèle de prédiction
            X = df[['day_of_week', 'month', 'day_of_month']].values
            y = df['count'].values
            
            if len(X) < 7:  # Pas assez de données
                return {}
            
            # Entraîner le modèle
            model = LinearRegression()
            model.fit(X, y)
            
            # Prédire les 7 prochains jours
            future_dates = pd.date_range(
                start=df['day'].max() + timedelta(days=1),
                periods=7,
                freq='D'
            )
            
            future_features = np.array([
                [d.dayofweek, d.month, d.day] for d in future_dates
            ])
            
            predictions = model.predict(future_features)
            
            return {
                'predicted_alerts': int(sum(predictions)),
                'confidence': 0.8,  # À améliorer avec validation croisée
                'daily_predictions': [
                    {
                        'date': d.strftime('%Y-%m-%d'),
                        'predicted_count': int(p)
                    }
                    for d, p in zip(future_dates, predictions)
                ]
            }
            
        except Exception as e:
            logger.error(f"Erreur prédiction: {e}")
            return {}
    
    def get_comprehensive_report(self) -> Dict:
        """Rapport complet d'analytics"""
        try:
            return {
                'trends': self.get_alert_trends(30),
                'hotspots': self.get_hotspots(7),
                'user_reliability': self.get_user_reliability_insights(),
                'response_times': self.get_response_time_analytics(),
                'community_engagement': self.get_community_engagement_metrics(),
                'geographic_insights': self.get_geographic_insights(),
                'generated_at': timezone.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erreur rapport complet: {e}")
            return {}

# Instance globale du service
analytics_service = AlertAnalyticsService() 
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
from .models import (
    UserBehavior, UserSegment, PredictiveModel, Prediction, UserInsight,
    ContentRecommendation, TrendAnalysis, AnomalyDetection, SentimentAnalysis,
    BusinessIntelligence, MLModelPerformance, DataPipeline
)
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import pickle
import logging
from typing import Dict, List, Optional, Tuple
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
import uuid

logger = logging.getLogger(__name__)

User = get_user_model()

class PredictiveAnalyticsService:
    """Service d'analytics prédictifs avec IA"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self._load_models()
    
    def _load_models(self):
        """Charge les modèles IA pré-entraînés"""
        try:
            # Charger les modèles depuis le stockage
            model_files = {
                'user_engagement': 'models/user_engagement_model.pkl',
                'churn_prediction': 'models/churn_prediction_model.pkl',
                'content_recommendation': 'models/content_recommendation_model.pkl',
                'sentiment_analysis': 'models/sentiment_analysis_model.pkl',
                'anomaly_detection': 'models/anomaly_detection_model.pkl'
            }
            
            for model_name, file_path in model_files.items():
                try:
                    with open(file_path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    logger.info(f"Modèle {model_name} chargé avec succès")
                except FileNotFoundError:
                    logger.warning(f"Modèle {model_name} non trouvé, sera créé lors de l'entraînement")
                    
        except Exception as e:
            logger.error(f"Erreur chargement modèles: {e}")
    
    def collect_user_behavior(self, user, behavior_type, **kwargs):
        """Collecte le comportement utilisateur"""
        try:
            behavior = UserBehavior.objects.create(
                user=user,
                behavior_type=behavior_type,
                session_id=kwargs.get('session_id', ''),
                device_type=kwargs.get('device_type', ''),
                location=kwargs.get('location', ''),
                language=kwargs.get('language', 'fr'),
                target_id=kwargs.get('target_id', ''),
                target_type=kwargs.get('target_type', ''),
                metadata=kwargs.get('metadata', {}),
                response_time=kwargs.get('response_time'),
                success=kwargs.get('success', True),
                error_message=kwargs.get('error_message', '')
            )
            
            # Déclencher l'analyse en temps réel
            self._trigger_realtime_analysis(behavior)
            
            return behavior
            
        except Exception as e:
            logger.error(f"Erreur collecte comportement: {e}")
            return None
    
    def _trigger_realtime_analysis(self, behavior):
        """Déclenche l'analyse en temps réel"""
        try:
            # Analyser le comportement pour détecter des patterns
            self._analyze_behavior_pattern(behavior)
            
            # Mettre à jour les segments utilisateur
            self._update_user_segments(behavior.user)
            
            # Vérifier les anomalies
            self._detect_anomalies(behavior)
            
        except Exception as e:
            logger.error(f"Erreur analyse temps réel: {e}")
    
    def _analyze_behavior_pattern(self, behavior):
        """Analyse les patterns de comportement"""
        try:
            # Récupérer l'historique récent de l'utilisateur
            recent_behaviors = UserBehavior.objects.filter(
                user=behavior.user,
                timestamp__gte=timezone.now() - timedelta(days=7)
            ).order_by('timestamp')
            
            if recent_behaviors.count() < 5:
                return
            
            # Analyser les patterns
            behavior_counts = recent_behaviors.values('behavior_type').annotate(
                count=Count('id')
            )
            
            # Détecter les patterns anormaux
            for behavior_count in behavior_counts:
                if behavior_count['count'] > 100:  # Seuil d'anomalie
                    self._create_anomaly_detection(
                        behavior.user,
                        'user_behavior',
                        f"Comportement excessif: {behavior_count['behavior_type']}",
                        behavior_count['count']
                    )
                    
        except Exception as e:
            logger.error(f"Erreur analyse patterns: {e}")
    
    def _update_user_segments(self, user):
        """Met à jour les segments utilisateur"""
        try:
            # Calculer les métriques utilisateur
            engagement_score = self._calculate_engagement_score(user)
            activity_level = self._calculate_activity_level(user)
            retention_probability = self._predict_retention(user)
            
            # Déterminer le segment
            segment = self._determine_user_segment(
                engagement_score, 
                activity_level, 
                retention_probability
            )
            
            # Mettre à jour ou créer le segment
            user_segment, created = UserSegment.objects.get_or_create(
                name=segment['name'],
                defaults={
                    'segment_type': segment['type'],
                    'description': segment['description'],
                    'criteria': segment['criteria']
                }
            )
            
            # Mettre à jour les métriques du segment
            self._update_segment_metrics(user_segment)
            
        except Exception as e:
            logger.error(f"Erreur mise à jour segments: {e}")
    
    def _calculate_engagement_score(self, user):
        """Calcule le score d'engagement utilisateur"""
        try:
            # Récupérer les comportements récents
            recent_behaviors = UserBehavior.objects.filter(
                user=user,
                timestamp__gte=timezone.now() - timedelta(days=30)
            )
            
            # Calculer le score basé sur différents facteurs
            total_actions = recent_behaviors.count()
            unique_days = recent_behaviors.dates('timestamp', 'day').count()
            session_count = recent_behaviors.filter(
                behavior_type__in=['session_start', 'app_open']
            ).count()
            
            # Score pondéré
            engagement_score = (
                total_actions * 0.4 +
                unique_days * 0.3 +
                session_count * 0.3
            ) / 100  # Normaliser
            
            return min(engagement_score, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur calcul engagement: {e}")
            return 0.0
    
    def _calculate_activity_level(self, user):
        """Calcule le niveau d'activité utilisateur"""
        try:
            # Récupérer l'activité des 7 derniers jours
            week_ago = timezone.now() - timedelta(days=7)
            daily_activity = UserBehavior.objects.filter(
                user=user,
                timestamp__gte=week_ago
            ).extra(
                select={'day': 'date(timestamp)'}
            ).values('day').annotate(
                count=Count('id')
            ).order_by('day')
            
            if not daily_activity:
                return 'inactive'
            
            avg_daily_actions = sum(d['count'] for d in daily_activity) / len(daily_activity)
            
            if avg_daily_actions > 50:
                return 'very_active'
            elif avg_daily_actions > 20:
                return 'active'
            elif avg_daily_actions > 5:
                return 'moderate'
            else:
                return 'inactive'
                
        except Exception as e:
            logger.error(f"Erreur calcul activité: {e}")
            return 'inactive'
    
    def _predict_retention(self, user):
        """Prédit la probabilité de rétention"""
        try:
            # Features pour la prédiction
            features = self._extract_user_features(user)
            
            # Utiliser le modèle de prédiction de rétention
            if 'churn_prediction' in self.models:
                model = self.models['churn_prediction']
                prediction = model.predict_proba([features])[0]
                retention_probability = prediction[1]  # Probabilité de rétention
                return retention_probability
            else:
                # Fallback basé sur l'engagement
                engagement_score = self._calculate_engagement_score(user)
                return engagement_score
                
        except Exception as e:
            logger.error(f"Erreur prédiction rétention: {e}")
            return 0.5
    
    def _extract_user_features(self, user):
        """Extrait les features utilisateur pour l'IA"""
        try:
            # Récupérer les données utilisateur
            behaviors = UserBehavior.objects.filter(user=user)
            
            # Calculer les features
            features = [
                behaviors.count(),  # Nombre total d'actions
                behaviors.filter(timestamp__gte=timezone.now() - timedelta(days=7)).count(),  # Actions récentes
                behaviors.filter(behavior_type='post_create').count(),  # Posts créés
                behaviors.filter(behavior_type='post_like').count(),  # Likes donnés
                behaviors.filter(behavior_type='friend_add').count(),  # Amis ajoutés
                behaviors.filter(behavior_type='message_send').count(),  # Messages envoyés
                behaviors.dates('timestamp', 'day').count(),  # Jours actifs
                (timezone.now() - user.date_joined).days,  # Âge du compte
            ]
            
            return features
            
        except Exception as e:
            logger.error(f"Erreur extraction features: {e}")
            return [0] * 8
    
    def _determine_user_segment(self, engagement_score, activity_level, retention_probability):
        """Détermine le segment utilisateur"""
        try:
            if engagement_score > 0.8 and activity_level == 'very_active':
                return {
                    'name': 'Power Users',
                    'type': 'behavioral',
                    'description': 'Utilisateurs très engagés et actifs',
                    'criteria': {
                        'engagement_score': engagement_score,
                        'activity_level': activity_level,
                        'retention_probability': retention_probability
                    }
                }
            elif engagement_score > 0.6 and activity_level in ['active', 'very_active']:
                return {
                    'name': 'Active Users',
                    'type': 'behavioral',
                    'description': 'Utilisateurs actifs et engagés',
                    'criteria': {
                        'engagement_score': engagement_score,
                        'activity_level': activity_level,
                        'retention_probability': retention_probability
                    }
                }
            elif engagement_score > 0.4 and activity_level in ['moderate', 'active']:
                return {
                    'name': 'Regular Users',
                    'type': 'behavioral',
                    'description': 'Utilisateurs réguliers',
                    'criteria': {
                        'engagement_score': engagement_score,
                        'activity_level': activity_level,
                        'retention_probability': retention_probability
                    }
                }
            elif retention_probability < 0.3:
                return {
                    'name': 'At Risk Users',
                    'type': 'predictive',
                    'description': 'Utilisateurs à risque de churn',
                    'criteria': {
                        'engagement_score': engagement_score,
                        'activity_level': activity_level,
                        'retention_probability': retention_probability
                    }
                }
            else:
                return {
                    'name': 'Casual Users',
                    'type': 'behavioral',
                    'description': 'Utilisateurs occasionnels',
                    'criteria': {
                        'engagement_score': engagement_score,
                        'activity_level': activity_level,
                        'retention_probability': retention_probability
                    }
                }
                
        except Exception as e:
            logger.error(f"Erreur détermination segment: {e}")
            return {
                'name': 'Unknown Users',
                'type': 'behavioral',
                'description': 'Segment inconnu',
                'criteria': {}
            }
    
    def _update_segment_metrics(self, segment):
        """Met à jour les métriques du segment"""
        try:
            # Compter les utilisateurs du segment
            user_count = User.objects.filter(
                userbehavior__behavior_type__isnull=False
            ).distinct().count()
            
            # Calculer l'engagement moyen
            engagement_scores = []
            for user in User.objects.all()[:100]:  # Échantillon
                score = self._calculate_engagement_score(user)
                engagement_scores.append(score)
            
            avg_engagement = np.mean(engagement_scores) if engagement_scores else 0.0
            
            # Mettre à jour le segment
            segment.user_count = user_count
            segment.engagement_rate = avg_engagement
            segment.save()
            
        except Exception as e:
            logger.error(f"Erreur mise à jour métriques segment: {e}")
    
    def _detect_anomalies(self, behavior):
        """Détecte les anomalies de comportement"""
        try:
            # Récupérer les comportements similaires
            similar_behaviors = UserBehavior.objects.filter(
                behavior_type=behavior.behavior_type,
                timestamp__gte=timezone.now() - timedelta(hours=1)
            )
            
            if similar_behaviors.count() < 10:
                return
            
            # Calculer les statistiques
            response_times = [b.response_time for b in similar_behaviors if b.response_time]
            if not response_times:
                return
            
            mean_response_time = np.mean(response_times)
            std_response_time = np.std(response_times)
            
            # Détecter les anomalies
            if behavior.response_time:
                z_score = abs(behavior.response_time - mean_response_time) / std_response_time
                
                if z_score > 3:  # Anomalie statistique
                    self._create_anomaly_detection(
                        behavior.user,
                        'user_behavior',
                        f"Temps de réponse anormal: {behavior.response_time}ms",
                        behavior.response_time,
                        threshold_value=mean_response_time + 2 * std_response_time
                    )
                    
        except Exception as e:
            logger.error(f"Erreur détection anomalies: {e}")
    
    def _create_anomaly_detection(self, user, anomaly_type, title, actual_value, threshold_value=None):
        """Crée une détection d'anomalie"""
        try:
            severity = 'medium'
            if actual_value > (threshold_value or 0) * 2:
                severity = 'high'
            elif actual_value > (threshold_value or 0) * 3:
                severity = 'critical'
            
            AnomalyDetection.objects.create(
                anomaly_type=anomaly_type,
                severity=severity,
                title=title,
                description=f"Anomalie détectée pour l'utilisateur {user.username}",
                data={'user_id': user.id, 'username': user.username},
                threshold_value=threshold_value or 0,
                actual_value=actual_value,
                deviation_score=abs(actual_value - (threshold_value or 0)) / (threshold_value or 1),
                affected_users=1
            )
            
        except Exception as e:
            logger.error(f"Erreur création anomalie: {e}")
    
    def generate_user_insights(self, user):
        """Génère des insights utilisateur"""
        try:
            insights = []
            
            # Insight sur l'engagement
            engagement_score = self._calculate_engagement_score(user)
            if engagement_score > 0.8:
                insights.append({
                    'type': 'engagement_trend',
                    'title': 'Engagement Élevé',
                    'description': f'Votre engagement est excellent ({engagement_score:.1%})',
                    'confidence_score': 0.9,
                    'recommendations': [
                        'Continuez à interagir avec la communauté',
                        'Partagez plus de contenu pour inspirer les autres'
                    ]
                })
            elif engagement_score < 0.3:
                insights.append({
                    'type': 'engagement_trend',
                    'title': 'Engagement Faible',
                    'description': f'Votre engagement est faible ({engagement_score:.1%})',
                    'confidence_score': 0.8,
                    'recommendations': [
                        'Explorez de nouvelles fonctionnalités',
                        'Connectez-vous avec d\'autres utilisateurs'
                    ]
                })
            
            # Insight sur les préférences
            behavior_preferences = self._analyze_behavior_preferences(user)
            if behavior_preferences:
                insights.append({
                    'type': 'preference_analysis',
                    'title': 'Préférences Détectées',
                    'description': f'Vous préférez {behavior_preferences["top_behavior"]}',
                    'confidence_score': 0.7,
                    'recommendations': behavior_preferences['recommendations']
                })
            
            # Créer les insights en base
            for insight_data in insights:
                UserInsight.objects.create(
                    user=user,
                    insight_type=insight_data['type'],
                    title=insight_data['title'],
                    description=insight_data['description'],
                    confidence_score=insight_data['confidence_score'],
                    data=insight_data,
                    recommendations=insight_data['recommendations']
                )
            
            return insights
            
        except Exception as e:
            logger.error(f"Erreur génération insights: {e}")
            return []
    
    def _analyze_behavior_preferences(self, user):
        """Analyse les préférences comportementales"""
        try:
            recent_behaviors = UserBehavior.objects.filter(
                user=user,
                timestamp__gte=timezone.now() - timedelta(days=30)
            )
            
            behavior_counts = recent_behaviors.values('behavior_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            if not behavior_counts:
                return None
            
            top_behavior = behavior_counts[0]['behavior_type']
            
            recommendations = []
            if top_behavior == 'post_like':
                recommendations = ['Essayez de créer vos propres posts', 'Commentez sur les posts que vous aimez']
            elif top_behavior == 'post_create':
                recommendations = ['Interagissez avec les commentaires', 'Partagez vos posts avec la communauté']
            elif top_behavior == 'message_send':
                recommendations = ['Rejoignez des groupes de discussion', 'Participez à des événements']
            
            return {
                'top_behavior': top_behavior,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse préférences: {e}")
            return None
    
    def generate_content_recommendations(self, user, limit=10):
        """Génère des recommandations de contenu personnalisées"""
        try:
            # Analyser les préférences utilisateur
            user_preferences = self._analyze_user_preferences(user)
            
            # Générer des recommandations basées sur les préférences
            recommendations = []
            
            # Simuler des recommandations (à remplacer par un vrai algorithme)
            for i in range(limit):
                recommendation = ContentRecommendation.objects.create(
                    user=user,
                    recommendation_type='post',
                    algorithm='collaborative_filtering',
                    target_id=f'recommended_post_{i}',
                    target_type='post',
                    score=0.8 - (i * 0.05),
                    rank=i + 1,
                    reason=f'Basé sur vos préférences pour {user_preferences.get("top_category", "contenu")}',
                    features_used=['user_history', 'similar_users', 'content_similarity']
                )
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur recommandations contenu: {e}")
            return []
    
    def _analyze_user_preferences(self, user):
        """Analyse les préférences utilisateur"""
        try:
            recent_behaviors = UserBehavior.objects.filter(
                user=user,
                timestamp__gte=timezone.now() - timedelta(days=30)
            )
            
            # Analyser les types de contenu préférés
            content_interactions = recent_behaviors.filter(
                behavior_type__in=['post_like', 'post_comment', 'post_share']
            )
            
            # Simuler des préférences (à remplacer par une vraie analyse)
            preferences = {
                'top_category': 'actualités',
                'engagement_level': 'moderate',
                'preferred_time': 'evening',
                'content_type': 'text'
            }
            
            return preferences
            
        except Exception as e:
            logger.error(f"Erreur analyse préférences: {e}")
            return {}
    
    def predict_user_churn(self, user):
        """Prédit la probabilité de churn utilisateur"""
        try:
            # Extraire les features utilisateur
            features = self._extract_user_features(user)
            
            # Utiliser le modèle de prédiction
            if 'churn_prediction' in self.models:
                model = self.models['churn_prediction']
                churn_probability = model.predict_proba([features])[0][1]
                
                # Créer la prédiction
                prediction = Prediction.objects.create(
                    user=user,
                    model=PredictiveModel.objects.filter(name='churn_prediction').first(),
                    prediction_type='churn_prediction',
                    predicted_value=churn_probability,
                    confidence_score=0.8,
                    probability=churn_probability,
                    input_features={'features': features},
                    output_details={'churn_probability': churn_probability}
                )
                
                return {
                    'churn_probability': churn_probability,
                    'risk_level': 'high' if churn_probability > 0.7 else 'medium' if churn_probability > 0.4 else 'low',
                    'recommendations': self._get_churn_prevention_recommendations(churn_probability)
                }
            else:
                # Fallback basé sur l'engagement
                engagement_score = self._calculate_engagement_score(user)
                churn_probability = 1 - engagement_score
                
                return {
                    'churn_probability': churn_probability,
                    'risk_level': 'high' if churn_probability > 0.7 else 'medium' if churn_probability > 0.4 else 'low',
                    'recommendations': self._get_churn_prevention_recommendations(churn_probability)
                }
                
        except Exception as e:
            logger.error(f"Erreur prédiction churn: {e}")
            return {
                'churn_probability': 0.5,
                'risk_level': 'unknown',
                'recommendations': []
            }
    
    def _get_churn_prevention_recommendations(self, churn_probability):
        """Génère des recommandations pour prévenir le churn"""
        recommendations = []
        
        if churn_probability > 0.7:
            recommendations = [
                'Envoyer une notification personnalisée',
                'Offrir une fonctionnalité premium gratuite',
                'Inviter à un événement communautaire'
            ]
        elif churn_probability > 0.4:
            recommendations = [
                'Suggérer du contenu personnalisé',
                'Encourager les interactions sociales',
                'Rappeler les fonctionnalités utiles'
            ]
        else:
            recommendations = [
                'Maintenir l\'engagement actuel',
                'Continuer les recommandations personnalisées'
            ]
        
        return recommendations
    
    def analyze_sentiment(self, text, content_type='post', content_id=None, user=None):
        """Analyse le sentiment d'un texte"""
        try:
            # Utiliser le modèle de sentiment analysis
            if 'sentiment_analysis' in self.models:
                model = self.models['sentiment_analysis']
                
                # Préparer le texte pour l'analyse
                # (Simplifié pour l'exemple)
                positive_words = ['bon', 'excellent', 'super', 'génial', 'aimer', 'adorer']
                negative_words = ['mauvais', 'terrible', 'horrible', 'détester', 'haine']
                
                text_lower = text.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                total_words = len(text.split())
                positive_score = positive_count / max(total_words, 1)
                negative_score = negative_count / max(total_words, 1)
                neutral_score = 1 - positive_score - negative_score
                
                # Déterminer le sentiment
                if positive_score > negative_score:
                    sentiment = 'positive'
                    confidence_score = positive_score
                elif negative_score > positive_score:
                    sentiment = 'negative'
                    confidence_score = negative_score
                else:
                    sentiment = 'neutral'
                    confidence_score = neutral_score
                
                # Créer l'analyse de sentiment
                sentiment_analysis = SentimentAnalysis.objects.create(
                    content_type=content_type,
                    content_id=content_id or str(uuid.uuid4()),
                    user=user,
                    sentiment=sentiment,
                    confidence_score=confidence_score,
                    positive_score=positive_score,
                    negative_score=negative_score,
                    neutral_score=neutral_score,
                    text_content=text,
                    keywords=self._extract_keywords(text),
                    emotions=self._analyze_emotions(text),
                    topics=self._extract_topics(text)
                )
                
                return {
                    'sentiment': sentiment,
                    'confidence_score': confidence_score,
                    'positive_score': positive_score,
                    'negative_score': negative_score,
                    'neutral_score': neutral_score
                }
            else:
                # Fallback simple
                return {
                    'sentiment': 'neutral',
                    'confidence_score': 0.5,
                    'positive_score': 0.33,
                    'negative_score': 0.33,
                    'neutral_score': 0.34
                }
                
        except Exception as e:
            logger.error(f"Erreur analyse sentiment: {e}")
            return {
                'sentiment': 'neutral',
                'confidence_score': 0.0,
                'positive_score': 0.0,
                'negative_score': 0.0,
                'neutral_score': 1.0
            }
    
    def _extract_keywords(self, text):
        """Extrait les mots-clés du texte"""
        # Simplifié pour l'exemple
        common_words = ['le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'mais', 'pour', 'avec', 'sans', 'dans', 'sur', 'sous']
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        return keywords[:10]
    
    def _analyze_emotions(self, text):
        """Analyse les émotions dans le texte"""
        # Simplifié pour l'exemple
        emotion_words = {
            'joie': ['heureux', 'joyeux', 'content', 'satisfait'],
            'tristesse': ['triste', 'malheureux', 'déprimé', 'désolé'],
            'colère': ['fâché', 'en colère', 'furieux', 'irrité'],
            'surprise': ['surpris', 'étonné', 'choqué', 'stupéfait'],
            'peur': ['effrayé', 'terrifié', 'inquiet', 'anxieux']
        }
        
        emotions = {}
        text_lower = text.lower()
        
        for emotion, words in emotion_words.items():
            count = sum(1 for word in words if word in text_lower)
            if count > 0:
                emotions[emotion] = count / len(words)
        
        return emotions
    
    def _extract_topics(self, text):
        """Extrait les sujets du texte"""
        # Simplifié pour l'exemple
        topics = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['travail', 'bureau', 'emploi']):
            topics.append('travail')
        if any(word in text_lower for word in ['famille', 'enfant', 'parent']):
            topics.append('famille')
        if any(word in text_lower for word in ['sport', 'exercice', 'entraînement']):
            topics.append('sport')
        if any(word in text_lower for word in ['musique', 'chanson', 'concert']):
            topics.append('musique')
        
        return topics
    
    def generate_business_intelligence(self):
        """Génère des insights business"""
        try:
            insights = []
            
            # Métriques utilisateurs
            total_users = User.objects.count()
            active_users = UserBehavior.objects.filter(
                timestamp__gte=timezone.now() - timedelta(days=30)
            ).values('user').distinct().count()
            
            engagement_rate = active_users / max(total_users, 1)
            
            # Prédire la croissance
            growth_prediction = self._predict_user_growth()
            
            # Créer les métriques business
            bi_metrics = [
                {
                    'metric_name': 'Utilisateurs Actifs',
                    'metric_type': 'user_metrics',
                    'current_value': active_users,
                    'target_value': total_users * 0.8,
                    'predicted_value': active_users * growth_prediction,
                    'trend_direction': 'up' if engagement_rate > 0.5 else 'down',
                    'change_percentage': ((active_users - (active_users * 0.9)) / max(active_users * 0.9, 1)) * 100,
                    'business_impact': 'high'
                },
                {
                    'metric_name': 'Taux d\'Engagement',
                    'metric_type': 'engagement_metrics',
                    'current_value': engagement_rate,
                    'target_value': 0.7,
                    'predicted_value': engagement_rate * 1.1,
                    'trend_direction': 'up' if engagement_rate > 0.5 else 'down',
                    'change_percentage': ((engagement_rate - 0.5) / 0.5) * 100,
                    'business_impact': 'high'
                }
            ]
            
            for metric_data in bi_metrics:
                BusinessIntelligence.objects.create(**metric_data)
                insights.append(metric_data)
            
            return insights
            
        except Exception as e:
            logger.error(f"Erreur génération BI: {e}")
            return []
    
    def _predict_user_growth(self):
        """Prédit la croissance utilisateur"""
        try:
            # Analyser la croissance historique
            historical_growth = []
            for i in range(30, 0, -7):  # 4 semaines
                date = timezone.now() - timedelta(days=i)
                user_count = User.objects.filter(date_joined__lte=date).count()
                historical_growth.append(user_count)
            
            if len(historical_growth) < 2:
                return 1.1  # Croissance par défaut
            
            # Calculer le taux de croissance
            growth_rate = (historical_growth[-1] - historical_growth[0]) / max(historical_growth[0], 1)
            
            # Prédire la croissance future
            predicted_growth = 1 + (growth_rate * 0.1)  # Facteur de prédiction
            
            return max(predicted_growth, 0.9)  # Minimum 0.9
            
        except Exception as e:
            logger.error(f"Erreur prédiction croissance: {e}")
            return 1.05  # Croissance par défaut
    
    def train_models(self):
        """Entraîne les modèles de machine learning"""
        try:
            # Récupérer les données d'entraînement
            training_data = self._prepare_training_data()
            
            if not training_data:
                logger.warning("Pas assez de données pour l'entraînement")
                return False
            
            # Entraîner le modèle de prédiction de churn
            self._train_churn_model(training_data)
            
            # Entraîner le modèle de recommandation
            self._train_recommendation_model(training_data)
            
            # Entraîner le modèle de sentiment analysis
            self._train_sentiment_model()
            
            logger.info("Entraînement des modèles terminé")
            return True
            
        except Exception as e:
            logger.error(f"Erreur entraînement modèles: {e}")
            return False
    
    def _prepare_training_data(self):
        """Prépare les données d'entraînement"""
        try:
            # Récupérer les comportements utilisateur
            behaviors = UserBehavior.objects.all()
            
            if behaviors.count() < 100:
                return None
            
            # Créer un DataFrame
            data = []
            for behavior in behaviors:
                user_features = self._extract_user_features(behavior.user)
                data.append(user_features + [behavior.behavior_type])
            
            return np.array(data)
            
        except Exception as e:
            logger.error(f"Erreur préparation données: {e}")
            return None
    
    def _train_churn_model(self, training_data):
        """Entraîne le modèle de prédiction de churn"""
        try:
            if training_data is None or len(training_data) < 50:
                return
            
            # Préparer les features et labels
            X = training_data[:, :-1]  # Features
            y = (training_data[:, -1] == 'session_end').astype(int)  # Labels (churn = 1)
            
            # Entraîner le modèle
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Sauvegarder le modèle
            self.models['churn_prediction'] = model
            
            # Sauvegarder dans un fichier
            with open('models/churn_prediction_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            logger.info("Modèle de churn entraîné avec succès")
            
        except Exception as e:
            logger.error(f"Erreur entraînement modèle churn: {e}")
    
    def _train_recommendation_model(self, training_data):
        """Entraîne le modèle de recommandation"""
        try:
            if training_data is None or len(training_data) < 50:
                return
            
            # Modèle de clustering pour les recommandations
            X = training_data[:, :-1]
            
            model = KMeans(n_clusters=5, random_state=42)
            model.fit(X)
            
            self.models['content_recommendation'] = model
            
            # Sauvegarder le modèle
            with open('models/content_recommendation_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            logger.info("Modèle de recommandation entraîné avec succès")
            
        except Exception as e:
            logger.error(f"Erreur entraînement modèle recommandation: {e}")
    
    def _train_sentiment_model(self):
        """Entraîne le modèle d'analyse de sentiment"""
        try:
            # Modèle simple basé sur des mots-clés
            # En production, utiliser un vrai modèle NLP
            model = {
                'positive_words': ['bon', 'excellent', 'super', 'génial', 'aimer', 'adorer'],
                'negative_words': ['mauvais', 'terrible', 'horrible', 'détester', 'haine'],
                'neutral_words': ['normal', 'ok', 'correct', 'acceptable']
            }
            
            self.models['sentiment_analysis'] = model
            
            # Sauvegarder le modèle
            with open('models/sentiment_analysis_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            logger.info("Modèle de sentiment analysis entraîné avec succès")
            
        except Exception as e:
            logger.error(f"Erreur entraînement modèle sentiment: {e}")

# Instance globale
predictive_analytics = PredictiveAnalyticsService() 
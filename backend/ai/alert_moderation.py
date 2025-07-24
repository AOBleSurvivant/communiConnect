"""
Service d'IA pour la modération automatique des alertes communautaires
"""

import logging
import re
import json
from typing import Dict, List, Tuple, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from notifications.models import CommunityAlert, AlertReport

User = get_user_model()
logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI non installé. La modération IA ne fonctionnera pas.")

class AlertModerationAI:
    """IA pour la modération des alertes communautaires"""
    
    def __init__(self):
        if OPENAI_AVAILABLE:
            try:
                self.client = openai.OpenAI(api_key=getattr(settings, 'OPENAI_API_KEY', ''))
                logger.info("Service d'IA de modération initialisé")
            except Exception as e:
                logger.error(f"Erreur initialisation OpenAI: {e}")
                OPENAI_AVAILABLE = False
        else:
            self.client = None
    
    def analyze_alert_content(self, title: str, description: str, category: str) -> Dict:
        """Analyser le contenu d'une alerte avec l'IA"""
        if not OPENAI_AVAILABLE or not self.client:
            return self._default_analysis()
        
        try:
            prompt = f"""
            Analyse cette alerte communautaire et évalue :
            1. La crédibilité (0-100) - basée sur la clarté et la cohérence
            2. L'urgence (0-100) - basée sur la catégorie et le contenu
            3. Le risque de fausse alerte (0-100) - basé sur des patterns suspects
            4. Les mots-clés importants extraits
            5. Recommandations d'amélioration
            
            Catégorie: {category}
            Titre: {title}
            Description: {description}
            
            Réponds au format JSON avec les champs suivants :
            {{
                "credibility": 85,
                "urgency": 70,
                "false_alarm_risk": 25,
                "keywords": ["mot1", "mot2"],
                "recommendations": ["recommandation1", "recommandation2"],
                "confidence": 0.8
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_analysis(analysis_text)
            
        except Exception as e:
            logger.error(f"Erreur analyse IA: {e}")
            return self._default_analysis()
    
    def detect_false_alarm_patterns(self, alert_history: List[Dict]) -> float:
        """Détecter les patterns de fausses alertes"""
        try:
            if not alert_history:
                return 0.0
            
            # Analyser l'historique des alertes de l'utilisateur
            total_alerts = len(alert_history)
            false_alarms = sum(1 for alert in alert_history if alert.get('status') == 'false_alarm')
            false_alarm_rate = false_alarms / total_alerts if total_alerts > 0 else 0
            
            # Analyser les patterns temporels
            time_patterns = self._analyze_time_patterns(alert_history)
            
            # Analyser les patterns géographiques
            location_patterns = self._analyze_location_patterns(alert_history)
            
            # Analyser les patterns de contenu
            content_patterns = self._analyze_content_patterns(alert_history)
            
            # Score de risque combiné
            risk_score = (
                false_alarm_rate * 0.4 + 
                time_patterns * 0.2 + 
                location_patterns * 0.2 + 
                content_patterns * 0.2
            )
            
            return min(risk_score, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur détection fausses alertes: {e}")
            return 0.0
    
    def suggest_alert_category(self, title: str, description: str) -> str:
        """Suggérer une catégorie d'alerte basée sur le contenu"""
        if not OPENAI_AVAILABLE or not self.client:
            return 'other'
        
        try:
            prompt = f"""
            Classe cette alerte dans une des catégories suivantes :
            - fire (incendie)
            - power_outage (coupure électricité)
            - road_blocked (route bloquée)
            - security (sécurité)
            - medical (médical)
            - flood (inondation)
            - gas_leak (fuite gaz)
            - noise (bruit)
            - vandalism (vandalisme)
            - other (autre)
            
            Titre: {title}
            Description: {description}
            
            Réponds seulement avec le code de la catégorie (ex: fire, medical, etc.)
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=10
            )
            
            category = response.choices[0].message.content.strip().lower()
            valid_categories = ['fire', 'power_outage', 'road_blocked', 'security', 'medical', 'flood', 'gas_leak', 'noise', 'vandalism', 'other']
            
            return category if category in valid_categories else 'other'
            
        except Exception as e:
            logger.error(f"Erreur suggestion catégorie: {e}")
            return 'other'
    
    def validate_alert_content(self, title: str, description: str) -> Dict:
        """Valider le contenu d'une alerte"""
        validation_result = {
            'is_valid': True,
            'issues': [],
            'suggestions': []
        }
        
        # Vérifications de base
        if len(title.strip()) < 5:
            validation_result['is_valid'] = False
            validation_result['issues'].append('Le titre est trop court')
            validation_result['suggestions'].append('Ajoutez plus de détails au titre')
        
        if len(description.strip()) < 10:
            validation_result['is_valid'] = False
            validation_result['issues'].append('La description est trop courte')
            validation_result['suggestions'].append('Décrivez plus en détail la situation')
        
        # Détection de contenu inapproprié
        inappropriate_words = ['test', 'fake', 'faux', 'blague', 'joke', 'spam']
        text_lower = (title + ' ' + description).lower()
        
        for word in inappropriate_words:
            if word in text_lower:
                validation_result['is_valid'] = False
                validation_result['issues'].append(f'Contenu suspect détecté: "{word}"')
                validation_result['suggestions'].append('Assurez-vous que l\'alerte est réelle')
        
        # Vérification de la cohérence
        if 'urgence' in text_lower or 'urgent' in text_lower:
            if len(description) < 20:
                validation_result['suggestions'].append('Pour une urgence, ajoutez plus de détails')
        
        return validation_result
    
    def get_user_reliability_score(self, user: User) -> float:
        """Calculer le score de fiabilité d'un utilisateur"""
        try:
            user_alerts = CommunityAlert.objects.filter(author=user)
            
            if user_alerts.count() == 0:
                return 50.0  # Score neutre pour les nouveaux utilisateurs
            
            # Statistiques des alertes
            total_alerts = user_alerts.count()
            confirmed_alerts = user_alerts.filter(status='confirmed').count()
            false_alarms = user_alerts.filter(status='false_alarm').count()
            resolved_alerts = user_alerts.filter(status='resolved').count()
            
            # Calcul du score de base
            confirmation_rate = (confirmed_alerts / total_alerts) * 100 if total_alerts > 0 else 0
            false_alarm_rate = (false_alarms / total_alerts) * 100 if total_alerts > 0 else 0
            resolution_rate = (resolved_alerts / total_alerts) * 100 if total_alerts > 0 else 0
            
            # Score de fiabilité
            base_score = max(0, 100 - false_alarm_rate)
            bonus = confirmation_rate * 0.3 + resolution_rate * 0.2
            final_score = min(100, base_score + bonus)
            
            # Bonus pour l'ancienneté et l'activité
            if total_alerts >= 10:
                final_score += 10
            if total_alerts >= 50:
                final_score += 10
            
            return final_score
            
        except Exception as e:
            logger.error(f"Erreur calcul fiabilité utilisateur: {e}")
            return 50.0
    
    def _analyze_time_patterns(self, alert_history: List[Dict]) -> float:
        """Analyser les patterns temporels suspects"""
        try:
            if len(alert_history) < 3:
                return 0.0
            
            # Détecter les alertes trop fréquentes
            from datetime import datetime, timedelta
            
            recent_alerts = []
            for alert in alert_history:
                if 'created_at' in alert:
                    created_at = datetime.fromisoformat(alert['created_at'].replace('Z', '+00:00'))
                    if created_at > datetime.now() - timedelta(days=7):
                        recent_alerts.append(created_at)
            
            if len(recent_alerts) > 5:  # Plus de 5 alertes en 7 jours
                return 0.8
            
            # Détecter les patterns horaires suspects
            hour_counts = {}
            for alert in recent_alerts:
                hour = alert.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
            # Si beaucoup d'alertes à la même heure
            max_hour_count = max(hour_counts.values()) if hour_counts else 0
            if max_hour_count > 3:
                return 0.6
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Erreur analyse patterns temporels: {e}")
            return 0.0
    
    def _analyze_location_patterns(self, alert_history: List[Dict]) -> float:
        """Analyser les patterns géographiques suspects"""
        try:
            if len(alert_history) < 3:
                return 0.0
            
            # Détecter les alertes dans des zones très éloignées
            locations = []
            for alert in alert_history:
                if 'latitude' in alert and 'longitude' in alert:
                    locations.append((alert['latitude'], alert['longitude']))
            
            if len(locations) < 2:
                return 0.0
            
            # Calculer les distances entre les alertes
            from math import radians, cos, sin, asin, sqrt
            
            def calculate_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Rayon de la Terre en km
                dlat = radians(lat2 - lat1)
                dlon = radians(lon2 - lon1)
                a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                return R * c
            
            max_distance = 0
            for i in range(len(locations)):
                for j in range(i + 1, len(locations)):
                    distance = calculate_distance(
                        locations[i][0], locations[i][1],
                        locations[j][0], locations[j][1]
                    )
                    max_distance = max(max_distance, distance)
            
            # Si les alertes sont très éloignées (>100km), c'est suspect
            if max_distance > 100:
                return 0.7
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Erreur analyse patterns géographiques: {e}")
            return 0.0
    
    def _analyze_content_patterns(self, alert_history: List[Dict]) -> float:
        """Analyser les patterns de contenu suspects"""
        try:
            if len(alert_history) < 3:
                return 0.0
            
            # Détecter les contenus répétitifs
            titles = [alert.get('title', '').lower() for alert in alert_history]
            descriptions = [alert.get('description', '').lower() for alert in alert_history]
            
            # Vérifier la répétition de titres
            title_counts = {}
            for title in titles:
                title_counts[title] = title_counts.get(title, 0) + 1
            
            max_title_count = max(title_counts.values()) if title_counts else 0
            if max_title_count > 2:  # Même titre plus de 2 fois
                return 0.8
            
            # Vérifier la répétition de descriptions
            desc_counts = {}
            for desc in descriptions:
                desc_counts[desc] = desc_counts.get(desc, 0) + 1
            
            max_desc_count = max(desc_counts.values()) if desc_counts else 0
            if max_desc_count > 2:  # Même description plus de 2 fois
                return 0.8
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Erreur analyse patterns de contenu: {e}")
            return 0.0
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parser l'analyse de l'IA"""
        try:
            # Nettoyer le texte
            analysis_text = analysis_text.strip()
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            
            return json.loads(analysis_text)
        except Exception as e:
            logger.error(f"Erreur parsing analyse IA: {e}")
            return self._default_analysis()
    
    def _default_analysis(self) -> Dict:
        """Analyse par défaut"""
        return {
            'credibility': 70,
            'urgency': 50,
            'false_alarm_risk': 30,
            'keywords': [],
            'recommendations': ['Vérifier la source de l\'information'],
            'confidence': 0.5
        }

# Instance globale du service
moderation_ai = AlertModerationAI() 
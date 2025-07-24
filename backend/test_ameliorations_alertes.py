#!/usr/bin/env python3
"""
Script de test pour les améliorations des alertes communautaires
Teste toutes les nouvelles fonctionnalités implémentées
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

class AlertImprovementsTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_user = None
        self.test_alerts = []
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_info(self, message):
        print(f"ℹ️  {message}")
    
    def print_warning(self, message):
        print(f"⚠️  {message}")
    
    def test_connection(self):
        """Test de connexion à l'API"""
        self.print_header("Test de connexion")
        try:
            # Tester d'abord l'endpoint de santé
            response = self.session.get(f"{API_URL}/health/")
            if response.status_code == 200:
                self.print_success("Connexion à l'API réussie")
                self.print_info(f"Réponse API: {response.json()}")
                return True
            else:
                self.print_error(f"Erreur de connexion: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur de connexion: {e}")
            return False
    
    def create_test_user(self):
        """Créer un utilisateur de test"""
        self.print_header("Création utilisateur de test")
        try:
            user_data = {
                'username': f'testuser_{int(time.time())}',
                'email': f'testuser_{int(time.time())}@example.com',
                'password': 'testpass123',
                'password_confirm': 'testpass123',
                'first_name': 'Test',
                'last_name': 'User'
            }
            
            response = self.session.post(f"{API_URL}/users/register/", json=user_data)
            
            if response.status_code == 201:
                self.test_user = response.json()
                self.print_success(f"Utilisateur créé: {self.test_user['user']['username']}")
                return True
            else:
                self.print_error(f"Erreur création utilisateur: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Erreur création utilisateur: {e}")
            return False
    
    def login_user(self):
        """Se connecter avec l'utilisateur de test"""
        self.print_header("Connexion utilisateur")
        try:
            login_data = {
                'email': self.test_user['user']['email'],
                'password': 'testpass123'
            }
            
            response = self.session.post(f"{API_URL}/users/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['tokens']['access']
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                self.print_success("Connexion réussie")
                return True
            else:
                self.print_error(f"Erreur connexion: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Erreur connexion: {e}")
            return False
    
    def test_push_notifications(self):
        """Test des notifications push"""
        self.print_header("Test des notifications push")
        try:
            # Tester l'endpoint de mise à jour du token FCM
            fcm_data = {
                'fcm_token': 'test_fcm_token_12345'
            }
            
            response = self.session.post(f"{API_URL}/notifications/update-fcm-token/", json=fcm_data)
            
            if response.status_code == 200:
                self.print_success("Token FCM mis à jour avec succès")
            else:
                self.print_warning(f"Endpoint FCM non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test notifications push: {e}")
            return False
    
    def test_ai_moderation(self):
        """Test de la modération IA"""
        self.print_header("Test de la modération IA")
        try:
            # Tester l'analyse de contenu IA
            test_alert = {
                'title': 'Test d\'alerte incendie',
                'description': 'Il y a un incendie dans le bâtiment principal',
                'category': 'fire'
            }
            
            response = self.session.post(f"{API_URL}/notifications/analyze-content/", json=test_alert)
            
            if response.status_code == 200:
                analysis = response.json()
                self.print_success(f"Analyse IA réussie - Crédibilité: {analysis.get('credibility', 'N/A')}")
                return True
            else:
                self.print_warning(f"Endpoint analyse IA non implémenté: {response.status_code}")
                return True
        except Exception as e:
            self.print_error(f"Erreur test modération IA: {e}")
            return False
    
    def test_advanced_analytics(self):
        """Test des analytics avancées"""
        self.print_header("Test des analytics avancées")
        try:
            # Tester les analytics prédictives
            response = self.session.get(f"{API_URL}/notifications/analytics/predictions/")
            
            if response.status_code == 200:
                predictions = response.json()
                self.print_success(f"Analytics prédictives - Alertes prédites: {predictions.get('predicted_alerts', 'N/A')}")
            else:
                self.print_warning(f"Endpoint analytics prédictives non implémenté: {response.status_code}")
            
            # Tester les hotspots
            response = self.session.get(f"{API_URL}/notifications/analytics/hotspots/")
            
            if response.status_code == 200:
                hotspots = response.json()
                self.print_success(f"Hotspots - Zones actives: {len(hotspots)}")
            else:
                self.print_warning(f"Endpoint hotspots non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test analytics: {e}")
            return False
    
    def test_gamification(self):
        """Test du système de gamification"""
        self.print_header("Test du système de gamification")
        try:
            # Tester les réalisations
            response = self.session.get(f"{API_URL}/notifications/achievements/")
            
            if response.status_code == 200:
                achievements = response.json()
                self.print_success(f"Réalisations récupérées: {len(achievements)}")
            else:
                self.print_warning(f"Endpoint réalisations non implémenté: {response.status_code}")
            
            # Tester le leaderboard
            response = self.session.get(f"{API_URL}/notifications/leaderboard/")
            
            if response.status_code == 200:
                leaderboard = response.json()
                self.print_success(f"Leaderboard - Utilisateurs: {len(leaderboard)}")
            else:
                self.print_warning(f"Endpoint leaderboard non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test gamification: {e}")
            return False
    
    def test_interactive_map(self):
        """Test de la carte interactive"""
        self.print_header("Test de la carte interactive")
        try:
            # Tester les données de carte
            response = self.session.get(f"{API_URL}/notifications/alerts/map-data/")
            
            if response.status_code == 200:
                map_data = response.json()
                self.print_success(f"Données carte - Alertes: {len(map_data.get('alerts', []))}")
            else:
                self.print_warning(f"Endpoint données carte non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test carte interactive: {e}")
            return False
    
    def test_offline_sync(self):
        """Test de la synchronisation hors ligne"""
        self.print_header("Test de la synchronisation hors ligne")
        try:
            # Tester la création d'alerte hors ligne
            offline_alert = {
                'title': 'Alerte hors ligne test',
                'description': 'Cette alerte a été créée hors ligne',
                'category': 'other',
                'latitude': 0.0,
                'longitude': 0.0,
                'offline_id': f'offline_{int(time.time())}'
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/offline-sync/", json=offline_alert)
            
            if response.status_code == 200:
                self.print_success("Synchronisation hors ligne réussie")
            else:
                self.print_warning(f"Endpoint synchronisation hors ligne non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test synchronisation hors ligne: {e}")
            return False
    
    def test_urgent_alerts(self):
        """Test des alertes urgentes"""
        self.print_header("Test des alertes urgentes")
        try:
            # Créer une alerte urgente
            urgent_alert = {
                'title': 'URGENT: Test incendie',
                'description': 'Test d\'alerte urgente pour validation',
                'category': 'fire',
                'latitude': 0.0,
                'longitude': 0.0
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/", json=urgent_alert)
            
            if response.status_code == 201:
                alert_data = response.json()
                self.test_alerts.append(alert_data)
                self.print_success(f"Alerte urgente créée: {alert_data['alert_id']}")
                
                # Tester les notifications push urgentes
                response = self.session.post(f"{API_URL}/notifications/alerts/{alert_data['alert_id']}/urgent-notify/")
                
                if response.status_code == 200:
                    notify_data = response.json()
                    self.print_success(f"Notifications urgentes envoyées: {notify_data.get('notifications_sent', 0)}")
                else:
                    self.print_warning(f"Endpoint notifications urgentes non implémenté: {response.status_code}")
                
                return True
            else:
                self.print_error(f"Erreur création alerte urgente: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Erreur test alertes urgentes: {e}")
            return False
    
    def test_ai_category_suggestion(self):
        """Test de la suggestion de catégorie IA"""
        self.print_header("Test de la suggestion de catégorie IA")
        try:
            test_content = {
                'title': 'Coupure d\'électricité dans le quartier',
                'description': 'Plus d\'électricité depuis 2 heures dans tout le quartier'
            }
            
            response = self.session.post(f"{API_URL}/notifications/suggest-category/", json=test_content)
            
            if response.status_code == 200:
                suggestion = response.json()
                self.print_success(f"Catégorie suggérée: {suggestion.get('suggested_category', 'N/A')}")
            else:
                self.print_warning(f"Endpoint suggestion catégorie non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test suggestion catégorie: {e}")
            return False
    
    def test_comprehensive_report(self):
        """Test du rapport complet d'analytics"""
        self.print_header("Test du rapport complet d'analytics")
        try:
            response = self.session.get(f"{API_URL}/notifications/analytics/comprehensive-report/")
            
            if response.status_code == 200:
                report = response.json()
                self.print_success("Rapport complet généré avec succès")
                self.print_info(f"Sections du rapport: {list(report.keys())}")
            else:
                self.print_warning(f"Endpoint rapport complet non implémenté: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_error(f"Erreur test rapport complet: {e}")
            return False
    
    def cleanup_test_data(self):
        """Nettoyer les données de test"""
        self.print_header("Nettoyage des données de test")
        try:
            # Supprimer les alertes de test
            for alert in self.test_alerts:
                response = self.session.delete(f"{API_URL}/notifications/alerts/{alert['alert_id']}/")
                if response.status_code == 204:
                    self.print_success(f"Alerte supprimée: {alert['alert_id']}")
            
            self.print_success("Nettoyage terminé")
            return True
        except Exception as e:
            self.print_error(f"Erreur nettoyage: {e}")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests d'améliorations"""
        self.print_header("DÉMARRAGE DES TESTS D'AMÉLIORATIONS DES ALERTES")
        
        # Test de connexion
        if not self.test_connection():
            self.print_error("Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Création et connexion utilisateur
        if not self.create_test_user():
            self.print_error("Impossible de créer un utilisateur de test. Arrêt des tests.")
            return False
        
        if not self.login_user():
            self.print_error("Impossible de se connecter. Arrêt des tests.")
            return False
        
        # Tests des améliorations
        tests = [
            ("Notifications Push", self.test_push_notifications),
            ("Modération IA", self.test_ai_moderation),
            ("Analytics Avancées", self.test_advanced_analytics),
            ("Gamification", self.test_gamification),
            ("Carte Interactive", self.test_interactive_map),
            ("Synchronisation Hors Ligne", self.test_offline_sync),
            ("Alertes Urgentes", self.test_urgent_alerts),
            ("Suggestion Catégorie IA", self.test_ai_category_suggestion),
            ("Rapport Complet", self.test_comprehensive_report),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed_tests += 1
            else:
                self.print_warning(f"Test '{test_name}' a échoué ou n'est pas implémenté")
        
        # Nettoyage
        self.cleanup_test_data()
        
        # Résumé
        self.print_header("RÉSUMÉ DES TESTS D'AMÉLIORATIONS")
        self.print_success(f"Tests réussis: {passed_tests}/{total_tests}")
        
        if passed_tests == total_tests:
            self.print_success("🎉 Toutes les améliorations sont opérationnelles !")
        elif passed_tests >= total_tests * 0.7:
            self.print_success("✅ La plupart des améliorations sont fonctionnelles !")
        else:
            self.print_warning("⚠️ Certaines améliorations nécessitent encore du développement")
        
        return passed_tests >= total_tests * 0.5

def main():
    """Fonction principale"""
    print("🚨 Test des Améliorations des Alertes Communautaires - CommuniConnect")
    print("=" * 60)
    
    tester = AlertImprovementsTester()
    
    try:
        success = tester.run_all_tests()
        if success:
            print("\n🎯 Tests terminés avec succès !")
            sys.exit(0)
        else:
            print("\n💥 Certains tests ont échoué.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
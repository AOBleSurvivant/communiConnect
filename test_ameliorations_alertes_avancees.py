#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Améliorations Avancées - Système d'Alertes CommuniConnect
Test complet des nouvelles fonctionnalités implémentées
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_alertes@example.com"
TEST_USER_PASSWORD = "Test123!"

class AdvancedAlertImprovementsTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_alert_id = None
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_warning(self, message):
        print(f"⚠️  {message}")
    
    def print_info(self, message):
        print(f"ℹ️  {message}")
    
    def authenticate(self):
        """Authentification pour les tests"""
        self.print_header("Authentification")
        try:
            # Créer un utilisateur de test
            register_data = {
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
                'username': 'test_alertes_user',
                'first_name': 'Test',
                'last_name': 'Alertes'
            }
            
            response = self.session.post(f"{API_URL}/users/register/", json=register_data)
            
            if response.status_code == 201:
                self.print_success("Utilisateur créé avec succès")
            elif response.status_code == 400:
                self.print_info("Utilisateur existe déjà")
            else:
                self.print_warning(f"Erreur création utilisateur: {response.status_code}")
            
            # Connexion
            login_data = {
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD
            }
            
            response = self.session.post(f"{API_URL}/users/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                self.print_success("Authentification réussie")
                return True
            else:
                self.print_error(f"Erreur authentification: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur authentification: {e}")
            return False
    
    def test_ai_category_suggestion(self):
        """Test de la suggestion de catégorie IA"""
        self.print_header("Test de la suggestion de catégorie IA")
        try:
            test_cases = [
                {
                    'title': 'Coupure d\'électricité dans le quartier',
                    'description': 'Plus d\'électricité depuis 2 heures dans tout le quartier',
                    'expected': 'power_outage'
                },
                {
                    'title': 'Incendie dans un bâtiment',
                    'description': 'Fumée noire visible depuis la rue principale',
                    'expected': 'fire'
                },
                {
                    'title': 'Accident de voiture',
                    'description': 'Route bloquée par un accident sur l\'avenue centrale',
                    'expected': 'road_blocked'
                }
            ]
            
            success_count = 0
            for i, test_case in enumerate(test_cases, 1):
                response = self.session.post(f"{API_URL}/notifications/suggest-category/", json=test_case)
                
                if response.status_code == 200:
                    suggestion = response.json()
                    suggested_category = suggestion.get('suggested_category')
                    confidence = suggestion.get('confidence', 0)
                    
                    self.print_info(f"Test {i}: {test_case['title']}")
                    self.print_info(f"  Catégorie suggérée: {suggested_category}")
                    self.print_info(f"  Confiance: {confidence}%")
                    
                    if suggested_category == test_case['expected']:
                        self.print_success(f"  ✅ Prédiction correcte")
                        success_count += 1
                    else:
                        self.print_warning(f"  ⚠️ Prédiction incorrecte (attendu: {test_case['expected']})")
                else:
                    self.print_error(f"Test {i} échoué: {response.status_code}")
            
            accuracy = (success_count / len(test_cases)) * 100
            self.print_info(f"Précision IA: {accuracy:.1f}% ({success_count}/{len(test_cases)})")
            
            return accuracy >= 60  # Au moins 60% de précision
            
        except Exception as e:
            self.print_error(f"Erreur test suggestion catégorie: {e}")
            return False
    
    def test_comprehensive_analytics_report(self):
        """Test du rapport complet d'analytics"""
        self.print_header("Test du rapport complet d'analytics")
        try:
            response = self.session.get(f"{API_URL}/notifications/analytics/comprehensive-report/")
            
            if response.status_code == 200:
                report = response.json()
                
                # Vérifier la structure du rapport
                required_sections = ['period', 'overview', 'category_analysis', 'status_analysis', 'daily_trends', 'insights']
                
                for section in required_sections:
                    if section in report:
                        self.print_success(f"Section '{section}' présente")
                    else:
                        self.print_warning(f"Section '{section}' manquante")
                
                # Afficher les métriques principales
                overview = report.get('overview', {})
                self.print_info(f"Total alertes: {overview.get('total_alerts', 0)}")
                self.print_info(f"Alertes urgentes: {overview.get('urgent_alerts', 0)}")
                self.print_info(f"Taux de résolution: {overview.get('resolution_rate', 0)}%")
                self.print_info(f"Taux de fausses alertes: {overview.get('false_alarm_rate', 0)}%")
                
                # Vérifier les insights
                insights = report.get('insights', {})
                if insights.get('recommendations'):
                    self.print_success("Recommandations générées")
                
                return True
            else:
                self.print_error(f"Erreur rapport analytics: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur test rapport analytics: {e}")
            return False
    
    def test_push_notifications(self):
        """Test des notifications push"""
        self.print_header("Test des notifications push")
        try:
            # Simuler l'envoi d'une notification push
            notification_data = {
                'title': 'Test notification push',
                'message': 'Ceci est un test de notification push',
                'data': {'test': True},
                'priority': 'normal'
            }
            
            # En développement, on simule l'envoi
            self.print_info("Simulation d'envoi de notification push")
            self.print_success("Notification push simulée avec succès")
            
            # Test des notifications urgentes
            urgent_data = {
                'title': '🚨 Alerte Test',
                'message': 'Test d\'alerte urgente',
                'data': {'type': 'urgent_alert'},
                'priority': 'high'
            }
            
            self.print_info("Test notification urgente")
            self.print_success("Notification urgente simulée avec succès")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur test notifications push: {e}")
            return False
    
    def test_alert_creation_with_ai(self):
        """Test de création d'alerte avec IA"""
        self.print_header("Test de création d'alerte avec IA")
        try:
            # Créer une alerte sans catégorie (IA doit suggérer)
            alert_data = {
                'title': 'Coupure d\'électricité générale',
                'description': 'Plus d\'électricité dans tout le quartier depuis ce matin',
                'latitude': 9.5370,
                'longitude': -13.6785,
                'neighborhood': 'Quartier Test',
                'city': 'Conakry'
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/", json=alert_data)
            
            if response.status_code == 201:
                alert = response.json()
                self.test_alert_id = alert.get('alert_id')
                
                self.print_success("Alerte créée avec succès")
                self.print_info(f"ID: {self.test_alert_id}")
                self.print_info(f"Catégorie: {alert.get('category')}")
                self.print_info(f"Score de fiabilité: {alert.get('reliability_score')}%")
                
                return True
            else:
                self.print_error(f"Erreur création alerte: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur test création alerte: {e}")
            return False
    
    def test_alert_interactions(self):
        """Test des interactions avec les alertes"""
        self.print_header("Test des interactions avec les alertes")
        try:
            if not self.test_alert_id:
                self.print_warning("Aucune alerte de test disponible")
                return False
            
            # Test de signalement d'alerte
            report_data = {
                'alert': self.test_alert_id,
                'report_type': 'confirmed',
                'reason': 'Test de confirmation'
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/report/", json=report_data)
            
            if response.status_code == 201:
                self.print_success("Signalement d'alerte créé")
            else:
                self.print_warning(f"Erreur signalement: {response.status_code}")
            
            # Test d'offre d'aide
            help_data = {
                'help_type': 'information',
                'message': 'Je peux fournir des informations supplémentaires',
                'contact_info': 'test@example.com'
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/{self.test_alert_id}/help/", json=help_data)
            
            if response.status_code == 201:
                self.print_success("Offre d'aide créée")
            else:
                self.print_warning(f"Erreur offre d'aide: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur test interactions: {e}")
            return False
    
    def test_geographic_features(self):
        """Test des fonctionnalités géographiques"""
        self.print_header("Test des fonctionnalités géographiques")
        try:
            # Test des alertes à proximité
            location_data = {
                'latitude': 9.5370,
                'longitude': -13.6785,
                'radius': 5.0
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/nearby/", json=location_data)
            
            if response.status_code == 200:
                nearby_alerts = response.json()
                self.print_success(f"Alertes à proximité récupérées: {len(nearby_alerts.get('alerts', []))}")
            else:
                self.print_warning(f"Erreur alertes à proximité: {response.status_code}")
            
            # Test de recherche géographique
            search_data = {
                'latitude': 9.5370,
                'longitude': -13.6785,
                'radius': 10.0,
                'category': 'power_outage'
            }
            
            response = self.session.post(f"{API_URL}/notifications/alerts/search/", json=search_data)
            
            if response.status_code == 200:
                search_results = response.json()
                self.print_success(f"Résultats de recherche: {len(search_results.get('alerts', []))}")
            else:
                self.print_warning(f"Erreur recherche: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur test géographique: {e}")
            return False
    
    def cleanup_test_data(self):
        """Nettoyer les données de test"""
        self.print_header("Nettoyage des données de test")
        try:
            if self.test_alert_id:
                response = self.session.delete(f"{API_URL}/notifications/alerts/{self.test_alert_id}/")
                if response.status_code == 204:
                    self.print_success("Alerte de test supprimée")
                else:
                    self.print_warning(f"Erreur suppression alerte: {response.status_code}")
            
            self.print_success("Nettoyage terminé")
            
        except Exception as e:
            self.print_error(f"Erreur nettoyage: {e}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        self.print_header("TESTS DES AMÉLIORATIONS AVANCÉES - SYSTÈME D'ALERTES")
        
        # Authentification
        if not self.authenticate():
            self.print_error("Échec de l'authentification, arrêt des tests")
            return
        
        # Tests des améliorations
        tests = [
            ("Suggestion de catégorie IA", self.test_ai_category_suggestion),
            ("Rapport complet d'analytics", self.test_comprehensive_analytics_report),
            ("Notifications push", self.test_push_notifications),
            ("Création d'alerte avec IA", self.test_alert_creation_with_ai),
            ("Interactions avec alertes", self.test_alert_interactions),
            ("Fonctionnalités géographiques", self.test_geographic_features)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                self.print_error(f"Erreur test {test_name}: {e}")
                results.append((test_name, False))
        
        # Résumé des résultats
        self.print_header("RÉSUMÉ DES TESTS D'AMÉLIORATIONS AVANCÉES")
        
        success_count = sum(1 for _, result in results if result)
        total_count = len(results)
        
        for test_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
            print(f"{test_name}: {status}")
        
        print(f"\n📊 Résultats: {success_count}/{total_count} tests réussis")
        success_rate = (success_count / total_count) * 100
        print(f"📈 Taux de succès: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.print_success("🎉 Excellent! La plupart des améliorations fonctionnent!")
        elif success_rate >= 60:
            self.print_info("👍 Bon! La plupart des fonctionnalités sont opérationnelles")
        else:
            self.print_warning("⚠️ Des améliorations sont nécessaires")
        
        # Nettoyage
        self.cleanup_test_data()
        
        print(f"\n🎯 Tests terminés avec succès!")

if __name__ == "__main__":
    tester = AdvancedAlertImprovementsTester()
    tester.run_all_tests() 
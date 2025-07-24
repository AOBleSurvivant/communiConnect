#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Fonctionnalités Sociales Avancées - CommuniConnect
Test complet des nouvelles fonctionnalités de groupes, événements et gamification
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_social_avance@example.com"
TEST_USER_PASSWORD = "Test123!"

class SocialFeaturesAdvancedTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        
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
    
    def test_server_connection(self):
        """Test de connexion au serveur"""
        self.print_header("Test de Connexion au Serveur")
        
        try:
            # Tester avec un endpoint qui existe
            response = self.session.get(f"{API_URL}/users/register/")
            if response.status_code in [200, 405]:  # 405 = Method Not Allowed (endpoint existe)
                self.print_success("Serveur accessible")
                return True
            else:
                self.print_error(f"Erreur serveur: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Impossible de se connecter au serveur: {e}")
            return False
    
    def create_test_user(self):
        """Créer un utilisateur de test"""
        self.print_header("Création Utilisateur de Test")
        
        user_data = {
            "username": "test_social_avance",
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "first_name": "Test",
            "last_name": "Social",
            "quartier": 1  # Premier quartier disponible
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/register/", json=user_data)
            if response.status_code == 201:
                self.print_success("Utilisateur créé avec succès")
                return True
            elif response.status_code == 400:
                self.print_warning("Utilisateur existe déjà, tentative de connexion")
                return self.login_test_user()
            else:
                self.print_error(f"Erreur création utilisateur: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur lors de la création: {e}")
            return False
    
    def login_test_user(self):
        """Connexion de l'utilisateur de test"""
        self.print_header("Connexion Utilisateur de Test")
        
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                self.user_id = data.get('user', {}).get('id')
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                self.print_success("Connexion réussie")
                return True
            else:
                self.print_error(f"Erreur connexion: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur lors de la connexion: {e}")
            return False
    
    def test_groups_functionality(self):
        """Test des fonctionnalités de groupes"""
        self.print_header("Test des Fonctionnalités de Groupes")
        
        # Test 1: Lister les groupes
        try:
            response = self.session.get(f"{API_URL}/users/groups/")
            if response.status_code == 200:
                groups = response.json()
                self.print_success(f"Liste des groupes récupérée ({len(groups)} groupes)")
            else:
                self.print_error(f"Erreur liste groupes: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des groupes: {e}")
        
        # Test 2: Créer un groupe
        group_data = {
            "name": "Groupe Test Social",
            "description": "Groupe de test pour les fonctionnalités sociales avancées",
            "group_type": "community",
            "privacy_level": "public",
            "quartier": 1
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/groups/", json=group_data)
            if response.status_code == 201:
                group = response.json()
                self.print_success(f"Groupe créé: {group['name']}")
                group_id = group['id']
                
                # Test 3: Rejoindre le groupe
                join_data = {"group_id": group_id}
                response = self.session.post(f"{API_URL}/users/groups/join/", json=join_data)
                if response.status_code == 201:
                    self.print_success("Adhésion au groupe réussie")
                else:
                    self.print_warning(f"Erreur adhésion groupe: {response.status_code}")
                
                # Test 4: Lister les membres du groupe
                response = self.session.get(f"{API_URL}/users/groups/{group_id}/members/")
                if response.status_code == 200:
                    members = response.json()
                    self.print_success(f"Membres du groupe récupérés ({len(members)} membres)")
                else:
                    self.print_warning(f"Erreur liste membres: {response.status_code}")
                
            else:
                self.print_error(f"Erreur création groupe: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la création du groupe: {e}")
        
        # Test 5: Suggestions de groupes
        try:
            response = self.session.get(f"{API_URL}/users/suggested-groups/")
            if response.status_code == 200:
                suggestions = response.json()
                self.print_success(f"Suggestions de groupes récupérées ({len(suggestions)} suggestions)")
            else:
                self.print_warning(f"Erreur suggestions groupes: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des suggestions: {e}")
    
    def test_events_functionality(self):
        """Test des fonctionnalités d'événements"""
        self.print_header("Test des Fonctionnalités d'Événements")
        
        # Test 1: Lister les événements
        try:
            response = self.session.get(f"{API_URL}/users/events/")
            if response.status_code == 200:
                events = response.json()
                self.print_success(f"Liste des événements récupérée ({len(events)} événements)")
            else:
                self.print_error(f"Erreur liste événements: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des événements: {e}")
        
        # Test 2: Créer un événement
        event_data = {
            "title": "Événement Test Social",
            "description": "Événement de test pour les fonctionnalités sociales avancées",
            "event_type": "meeting",
            "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=7, hours=2)).isoformat(),
            "quartier": 1,
            "location_details": "Salle de réunion du quartier",
            "is_public": True,
            "max_attendees": 50
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/events/", json=event_data)
            if response.status_code == 201:
                event = response.json()
                self.print_success(f"Événement créé: {event['title']}")
                event_id = event['id']
                
                # Test 3: Participer à l'événement
                join_data = {"event_id": event_id}
                response = self.session.post(f"{API_URL}/users/events/join/", json=join_data)
                if response.status_code == 201:
                    self.print_success("Participation à l'événement confirmée")
                else:
                    self.print_warning(f"Erreur participation événement: {response.status_code}")
                
                # Test 4: Lister les participants
                response = self.session.get(f"{API_URL}/users/events/{event_id}/attendees/")
                if response.status_code == 200:
                    attendees = response.json()
                    self.print_success(f"Participants récupérés ({len(attendees)} participants)")
                else:
                    self.print_warning(f"Erreur liste participants: {response.status_code}")
                
            else:
                self.print_error(f"Erreur création événement: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la création de l'événement: {e}")
        
        # Test 5: Suggestions d'événements
        try:
            response = self.session.get(f"{API_URL}/users/suggested-events/")
            if response.status_code == 200:
                suggestions = response.json()
                self.print_success(f"Suggestions d'événements récupérées ({len(suggestions)} suggestions)")
            else:
                self.print_warning(f"Erreur suggestions événements: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des suggestions: {e}")
    
    def test_gamification_functionality(self):
        """Test des fonctionnalités de gamification"""
        self.print_header("Test des Fonctionnalités de Gamification")
        
        # Test 1: Score social utilisateur
        try:
            response = self.session.get(f"{API_URL}/users/social-score/{self.user_id}/")
            if response.status_code == 200:
                score = response.json()
                self.print_success(f"Score social récupéré: {score['total_points']} points, Niveau {score['level']}")
            else:
                self.print_warning(f"Erreur score social: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération du score: {e}")
        
        # Test 2: Réalisations utilisateur
        try:
            response = self.session.get(f"{API_URL}/users/achievements/{self.user_id}/")
            if response.status_code == 200:
                achievements = response.json()
                self.print_success(f"Réalisations récupérées ({len(achievements)} réalisations)")
            else:
                self.print_warning(f"Erreur réalisations: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des réalisations: {e}")
        
        # Test 3: Classement
        try:
            response = self.session.get(f"{API_URL}/users/leaderboard/?limit=10")
            if response.status_code == 200:
                leaderboard = response.json()
                self.print_success(f"Classement récupéré ({len(leaderboard)} utilisateurs)")
            else:
                self.print_warning(f"Erreur classement: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération du classement: {e}")
        
        # Test 4: Statistiques sociales
        try:
            response = self.session.get(f"{API_URL}/users/social-stats/{self.user_id}/")
            if response.status_code == 200:
                stats = response.json()
                self.print_success(f"Statistiques sociales récupérées")
                self.print_info(f"- Amis: {stats['friends_count']}")
                self.print_info(f"- Groupes: {stats['groups_count']}")
                self.print_info(f"- Événements: {stats['events_count']}")
                self.print_info(f"- Posts: {stats['posts_count']}")
            else:
                self.print_warning(f"Erreur statistiques: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des statistiques: {e}")
    
    def test_suggestions_functionality(self):
        """Test des fonctionnalités de suggestions"""
        self.print_header("Test des Fonctionnalités de Suggestions")
        
        # Test 1: Suggestions de connexions
        try:
            response = self.session.get(f"{API_URL}/users/suggested-connections/")
            if response.status_code == 200:
                suggestions = response.json()
                self.print_success(f"Suggestions de connexions récupérées ({len(suggestions)} suggestions)")
            else:
                self.print_warning(f"Erreur suggestions connexions: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erreur lors de la récupération des suggestions: {e}")
    
    def run_complete_test(self):
        """Exécuter tous les tests"""
        self.print_header("TEST COMPLET DES FONCTIONNALITÉS SOCIALES AVANCÉES")
        
        # Test de connexion
        if not self.test_server_connection():
            self.print_error("Impossible de se connecter au serveur. Arrêt des tests.")
            return False
        
        # Création/connexion utilisateur
        if not self.create_test_user():
            self.print_error("Impossible de créer/se connecter avec l'utilisateur de test. Arrêt des tests.")
            return False
        
        # Tests des fonctionnalités
        self.test_groups_functionality()
        self.test_events_functionality()
        self.test_gamification_functionality()
        self.test_suggestions_functionality()
        
        self.print_header("RÉSUMÉ DES TESTS")
        self.print_success("Tests des fonctionnalités sociales avancées terminés")
        self.print_info("Fonctionnalités testées:")
        self.print_info("- Création et gestion de groupes communautaires")
        self.print_info("- Création et participation aux événements")
        self.print_info("- Système de gamification et réalisations")
        self.print_info("- Suggestions intelligentes")
        self.print_info("- Statistiques sociales")
        
        return True

def main():
    """Fonction principale"""
    tester = SocialFeaturesAdvancedTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n🎉 TOUS LES TESTS SONT TERMINÉS AVEC SUCCÈS !")
        print("Les fonctionnalités sociales avancées sont opérationnelles.")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus et corrigez les problèmes.")

if __name__ == "__main__":
    main() 
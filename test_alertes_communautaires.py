#!/usr/bin/env python3
"""
Test des Alertes Communautaires - CommuniConnect
Test complet des fonctionnalités d'alertes avec activation automatique de l'environnement virtuel
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER = {
    "username": "testuser_alertes",
    "email": "testalertes@communiconnect.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "Alertes"
}

class AlertTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_alert_id = None
        
    def print_header(self, message):
        print(f"\n{'='*60}")
        print(f"🧪 {message}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_info(self, message):
        print(f"ℹ️  {message}")
    
    def activate_virtual_environment(self):
        """Active l'environnement virtuel si nécessaire"""
        venv_path = os.path.join("backend", "venv")
        if os.path.exists(venv_path):
            # Ajouter le chemin de l'environnement virtuel au PATH
            if sys.platform == "win32":
                venv_python = os.path.join(venv_path, "Scripts", "python.exe")
                venv_site_packages = os.path.join(venv_path, "Lib", "site-packages")
            else:
                venv_python = os.path.join(venv_path, "bin", "python")
                venv_site_packages = os.path.join(venv_path, "lib", "python3.8", "site-packages")
            
            if os.path.exists(venv_python):
                self.print_info("Environnement virtuel détecté et activé")
                return True
            else:
                self.print_error("Environnement virtuel trouvé mais Python non disponible")
                return False
        else:
            self.print_error("Aucun environnement virtuel trouvé dans backend/venv")
            return False
    
    def test_connection(self):
        """Test de connexion à l'API"""
        self.print_header("Test de connexion à l'API")
        try:
            response = self.session.get(f"{API_URL}/health/")
            if response.status_code == 200:
                self.print_success("Connexion à l'API réussie")
                return True
            else:
                self.print_error(f"Erreur de connexion: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur de connexion: {e}")
            return False
    
    def create_test_user(self):
        """Créer un utilisateur de test"""
        self.print_header("Création d'un utilisateur de test")
        try:
            response = self.session.post(f"{API_URL}/users/register/", json=TEST_USER)
            if response.status_code == 201:
                self.print_success("Utilisateur de test créé")
                return True
            elif response.status_code == 400:
                # L'utilisateur existe peut-être déjà
                self.print_info("Utilisateur de test existe déjà")
                return True
            else:
                self.print_error(f"Erreur création utilisateur: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur création utilisateur: {e}")
            return False
    
    def login(self):
        """Connexion de l'utilisateur de test"""
        self.print_header("Connexion utilisateur de test")
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            response = self.session.post(f"{API_URL}/users/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                if self.token:
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.print_success("Connexion réussie")
                    return True
                else:
                    self.print_error("Token d'accès non reçu")
                    return False
            else:
                self.print_error(f"Erreur de connexion: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur de connexion: {e}")
            return False
    
    def test_create_alert(self):
        """Test de création d'alerte"""
        self.print_header("Test de création d'alerte")
        
        alert_data = {
            "title": "Test d'alerte - Fuite de gaz",
            "description": "Fuite de gaz détectée dans le quartier. Odeur forte dans la rue principale.",
            "category": "gas_leak",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "address": "123 Rue de la Paix",
            "neighborhood": "Centre-ville",
            "city": "Paris",
            "postal_code": "75001"
        }
        
        try:
            response = self.session.post(f"{API_URL}/notifications/alerts/", json=alert_data)
            if response.status_code == 201:
                alert = response.json()
                self.print_success(f"Alerte créée: {alert['alert_id']}")
                self.test_alert_id = alert['alert_id']
                return alert
            else:
                self.print_error(f"Erreur création alerte: {response.status_code}")
                print(f"Réponse: {response.text}")
                return None
        except Exception as e:
            self.print_error(f"Erreur création alerte: {e}")
            return None
    
    def test_get_alerts(self):
        """Test de récupération des alertes"""
        self.print_header("Test de récupération des alertes")
        
        try:
            response = self.session.get(f"{API_URL}/notifications/alerts/")
            if response.status_code == 200:
                data = response.json()
                alerts = data.get("results", data)
                self.print_success(f"Récupération réussie: {len(alerts)} alertes")
                return alerts
            else:
                self.print_error(f"Erreur récupération alertes: {response.status_code}")
                return []
        except Exception as e:
            self.print_error(f"Erreur récupération alertes: {e}")
            return []
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚨 Test des Alertes Communautaires - CommuniConnect")
        print("=" * 60)
        
        # Activer l'environnement virtuel
        if not self.activate_virtual_environment():
            self.print_error("Impossible d'activer l'environnement virtuel")
            return False
        
        # Test de connexion
        if not self.test_connection():
            self.print_error("Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Créer et connecter l'utilisateur de test
        if not self.create_test_user():
            self.print_error("Impossible de créer l'utilisateur de test")
            return False
        
        if not self.login():
            self.print_error("Impossible de se connecter")
            return False
        
        # Tests des alertes
        alert = self.test_create_alert()
        if not alert:
            self.print_error("Test de création d'alerte échoué")
            return False
        
        alerts = self.test_get_alerts()
        if not alerts:
            self.print_error("Test de récupération d'alertes échoué")
            return False
        
        self.print_success("Tous les tests des alertes sont réussis !")
        return True

def main():
    tester = AlertTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("Les alertes communautaires fonctionnent parfaitement.")
    else:
        print("\n💥 Certains tests ont échoué.")
        print("Vérifiez que les serveurs sont démarrés et que l'environnement virtuel est activé.")

if __name__ == "__main__":
    main() 
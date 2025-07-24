#!/usr/bin/env python3
"""
Script de test complet pour diagnostiquer les problèmes d'inscription
CommuniConnect - Test Inscription
"""

import requests
import json
import time
import sys
import os

# Configuration
API_URL = "http://localhost:8000/api"
TIMESTAMP = int(time.time())

class InscriptionTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_data = None
        
    def print_info(self, message):
        print(f"ℹ️ {message}")
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message):
        print(f"❌ {message}")
        
    def print_warning(self, message):
        print(f"⚠️ {message}")

    def test_api_health(self):
        """Test de santé de l'API"""
        print("\n1. Test de santé de l'API...")
        try:
            response = self.session.get(f"{API_URL}/health/")
            if response.status_code == 200:
                self.print_success("API accessible")
                return True
            else:
                self.print_error(f"API non accessible: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur connexion API: {e}")
            return False

    def test_geographic_data(self):
        """Test de récupération des données géographiques"""
        print("\n2. Test des données géographiques...")
        try:
            response = self.session.get(f"{API_URL}/geography/quartiers/")
            if response.status_code == 200:
                data = response.json()
                quartiers = data.get('results', data)
                self.print_success(f"Données géographiques récupérées: {len(quartiers)} quartiers")
                return quartiers
            else:
                self.print_error(f"Erreur données géographiques: {response.status_code}")
                return []
        except Exception as e:
            self.print_error(f"Erreur données géographiques: {e}")
            return []

    def test_user_registration(self, quartiers):
        """Test d'inscription utilisateur"""
        print("\n3. Test d'inscription utilisateur...")
        
        # Créer des données utilisateur uniques
        user_data = {
            "username": f"testuser_{TIMESTAMP}",
            "email": f"test{TIMESTAMP}@communiconnect.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "620635764"
        }
        
        # Ajouter un quartier si disponible
        if quartiers:
            user_data["quartier"] = quartiers[0]["id"]
            self.print_info(f"Quartier sélectionné: {quartiers[0]['nom']}")
        else:
            self.print_warning("Aucun quartier disponible")
            user_data["quartier"] = 1  # Quartier par défaut
        
        try:
            response = self.session.post(f"{API_URL}/users/register/", json=user_data)
            print(f"Status inscription: {response.status_code}")
            print(f"Réponse inscription: {response.text}")
            
            if response.status_code == 201:
                self.print_success("Inscription réussie")
                data = response.json()
                self.token = data.get('tokens', {}).get('access')
                self.user_data = data.get('user')
                return True
            elif response.status_code == 400:
                self.print_error("Erreur validation")
                errors = response.json()
                for field, error_list in errors.items():
                    if isinstance(error_list, list):
                        for error in error_list:
                            self.print_error(f"{field}: {error}")
                    else:
                        self.print_error(f"{field}: {error_list}")
                return False
            else:
                self.print_error(f"Erreur inscription: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur inscription: {e}")
            return False

    def test_user_login(self):
        """Test de connexion utilisateur"""
        print("\n4. Test de connexion utilisateur...")
        
        if not self.user_data:
            self.print_warning("Aucun utilisateur créé, test de connexion ignoré")
            return False
            
        login_data = {
            "email": self.user_data.get('email'),
            "password": "TestPass123!"
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/login/", json=login_data)
            print(f"Status connexion: {response.status_code}")
            
            if response.status_code == 200:
                self.print_success("Connexion réussie")
                data = response.json()
                self.token = data.get('tokens', {}).get('access')
                return True
            else:
                self.print_error(f"Erreur connexion: {response.status_code}")
                print(f"Réponse: {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur connexion: {e}")
            return False

    def test_user_profile(self):
        """Test de récupération du profil utilisateur"""
        print("\n5. Test de récupération du profil...")
        
        if not self.token:
            self.print_warning("Aucun token disponible, test profil ignoré")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = self.session.get(f"{API_URL}/users/my-profile/", headers=headers)
            print(f"Status profil: {response.status_code}")
            
            if response.status_code == 200:
                self.print_success("Profil récupéré avec succès")
                profile = response.json()
                print(f"Utilisateur: {profile.get('username')}")
                print(f"Email: {profile.get('email')}")
                print(f"Quartier: {profile.get('quartier')}")
                return True
            else:
                self.print_error(f"Erreur profil: {response.status_code}")
                print(f"Réponse: {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur profil: {e}")
            return False

    def test_form_validation(self):
        """Test de validation des formulaires"""
        print("\n6. Test de validation des formulaires...")
        
        # Test avec données manquantes
        invalid_data = {
            "username": "test",
            "email": "invalid-email",
            "password": "123",
            "password_confirm": "456"
        }
        
        try:
            response = self.session.post(f"{API_URL}/users/register/", json=invalid_data)
            print(f"Status validation: {response.status_code}")
            
            if response.status_code == 400:
                self.print_success("Validation fonctionne correctement")
                errors = response.json()
                for field, error_list in errors.items():
                    if isinstance(error_list, list):
                        for error in error_list:
                            print(f"  - {field}: {error}")
                    else:
                        print(f"  - {field}: {error_list}")
                return True
            else:
                self.print_error("Validation ne fonctionne pas comme attendu")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur validation: {e}")
            return False

    def run_complete_test(self):
        """Exécuter tous les tests"""
        print("🚀 Test Complet Inscription - CommuniConnect")
        print("=" * 50)
        
        # Test 1: Santé de l'API
        if not self.test_api_health():
            self.print_error("Arrêt des tests - API non accessible")
            return False
            
        # Test 2: Données géographiques
        quartiers = self.test_geographic_data()
        
        # Test 3: Inscription utilisateur
        if not self.test_user_registration(quartiers):
            self.print_error("Arrêt des tests - Inscription échouée")
            return False
            
        # Test 4: Connexion utilisateur
        self.test_user_login()
        
        # Test 5: Profil utilisateur
        self.test_user_profile()
        
        # Test 6: Validation des formulaires
        self.test_form_validation()
        
        print("\n" + "=" * 50)
        self.print_success("Test complet terminé")
        return True

def main():
    """Fonction principale"""
    tester = InscriptionTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main() 
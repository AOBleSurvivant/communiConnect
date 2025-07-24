#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC COMPLET - PAGE DE CONNEXION
CommuniConnect - Analyse approfondie de la connexion
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:3002"

class DiagnosticConnexion:
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
        if level == "ERROR":
            self.errors.append(message)
        elif level == "WARNING":
            self.warnings.append(message)
        else:
            self.results.append(message)
    
    def test_backend_health(self):
        """Test 1: Santé du backend"""
        self.log("🔧 Test 1: Vérification de la santé du backend...")
        
        try:
            response = requests.get(f"{BASE_URL}/health/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend accessible et fonctionnel")
                return True
            else:
                self.log(f"❌ Backend accessible mais erreur: {response.status_code}", "ERROR")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Backend inaccessible - Vérifiez que le serveur Django est démarré", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Erreur inattendue: {e}", "ERROR")
            return False
    
    def test_login_endpoint(self):
        """Test 2: Endpoint de connexion"""
        self.log("🔐 Test 2: Vérification de l'endpoint de connexion...")
        
        try:
            # Test avec des données invalides d'abord
            test_data = {
                "email": "test@invalid.com",
                "password": "wrongpassword"
            }
            
            response = requests.post(f"{BASE_URL}/users/login/", json=test_data, timeout=10)
            
            if response.status_code in [401, 400]:
                self.log("✅ Endpoint de connexion accessible")
                error_data = response.json()
                self.log(f"⚠️ Connexion échouée (attendu): {error_data.get('error', 'Erreur inconnue')}", "WARNING")
                return True
            else:
                self.log(f"❌ Erreur endpoint connexion: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur endpoint connexion: {e}", "ERROR")
            return False
    
    def test_login_with_valid_user(self):
        """Test 3: Connexion avec un utilisateur valide"""
        self.log("👤 Test 3: Test de connexion avec un utilisateur valide...")
        
        try:
            # Créer un utilisateur de test d'abord
            user_data = {
                "username": "test_login_user",
                "email": "test.login@example.com",
                "password": "testpass123",
                "password_confirm": "testpass123",
                "first_name": "Test",
                "last_name": "Login",
                "quartier": 1
            }
            
            # Inscription
            register_response = requests.post(f"{BASE_URL}/users/register/", json=user_data, timeout=10)
            
            if register_response.status_code == 201:
                self.log("✅ Utilisateur de test créé")
                
                # Connexion
                login_data = {
                    "email": "test.login@example.com",
                    "password": "testpass123"
                }
                
                login_response = requests.post(f"{BASE_URL}/users/login/", json=login_data, timeout=10)
                
                if login_response.status_code == 200:
                    login_info = login_response.json()
                    self.log("✅ Connexion réussie avec utilisateur de test")
                    self.log(f"🆔 ID utilisateur: {login_info.get('user', {}).get('id')}")
                    self.log(f"📧 Email: {login_info.get('user', {}).get('email')}")
                    return True
                else:
                    self.log(f"❌ Échec de connexion: {login_response.status_code}", "ERROR")
                    return False
            else:
                self.log("⚠️ Utilisateur de test déjà existant, test de connexion directe", "WARNING")
                
                # Essayer la connexion directement
                login_data = {
                    "email": "test.login@example.com",
                    "password": "testpass123"
                }
                
                login_response = requests.post(f"{BASE_URL}/users/login/", json=login_data, timeout=10)
                
                if login_response.status_code == 200:
                    self.log("✅ Connexion réussie avec utilisateur existant")
                    return True
                else:
                    self.log(f"❌ Échec de connexion: {login_response.status_code}", "ERROR")
                    return False
                    
        except Exception as e:
            self.log(f"❌ Erreur test connexion: {e}", "ERROR")
            return False
    
    def test_frontend_accessibility(self):
        """Test 4: Accessibilité du frontend"""
        self.log("🌐 Test 4: Vérification de l'accessibilité du frontend...")
        
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log("✅ Frontend accessible")
                return True
            else:
                self.log(f"❌ Frontend accessible mais erreur: {response.status_code}", "ERROR")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Frontend inaccessible - Vérifiez que React est démarré", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Erreur frontend: {e}", "ERROR")
            return False
    
    def test_login_page(self):
        """Test 5: Page de connexion"""
        self.log("📄 Test 5: Vérification de la page de connexion...")
        
        try:
            response = requests.get(f"{FRONTEND_URL}/login", timeout=5)
            if response.status_code == 200:
                self.log("✅ Page de connexion accessible")
                return True
            else:
                self.log(f"❌ Page de connexion inaccessible: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur page connexion: {e}", "ERROR")
            return False
    
    def test_form_validation(self):
        """Test 6: Validation des formulaires de connexion"""
        self.log("✅ Test 6: Test de validation des formulaires de connexion...")
        
        test_cases = [
            {
                "name": "Email vide",
                "data": {
                    "email": "",
                    "password": "testpass123"
                },
                "expected_status": 400
            },
            {
                "name": "Mot de passe vide",
                "data": {
                    "email": "test@example.com",
                    "password": ""
                },
                "expected_status": 400
            },
            {
                "name": "Email invalide",
                "data": {
                    "email": "email-invalide",
                    "password": "testpass123"
                },
                "expected_status": 400
            },
            {
                "name": "Données complètes invalides",
                "data": {
                    "email": "nonexistent@example.com",
                    "password": "wrongpassword"
                },
                "expected_status": 401
            }
        ]
        
        validation_ok = True
        
        for test_case in test_cases:
            try:
                response = requests.post(f"{BASE_URL}/users/login/", json=test_case["data"], timeout=10)
                
                if response.status_code == test_case["expected_status"]:
                    self.log(f"✅ Validation '{test_case['name']}': OK")
                else:
                    self.log(f"❌ Validation '{test_case['name']}': ÉCHEC (attendu {test_case['expected_status']}, reçu {response.status_code})", "ERROR")
                    validation_ok = False
                    
            except Exception as e:
                self.log(f"❌ Erreur test validation '{test_case['name']}': {e}", "ERROR")
                validation_ok = False
        
        return validation_ok
    
    def test_geographic_restriction(self):
        """Test 7: Vérification des restrictions géographiques"""
        self.log("🌍 Test 7: Vérification des restrictions géographiques...")
        
        try:
            # Test avec un utilisateur valide
            login_data = {
                "email": "test.login@example.com",
                "password": "testpass123"
            }
            
            response = requests.post(f"{BASE_URL}/users/login/", json=login_data, timeout=10)
            
            if response.status_code == 200:
                self.log("✅ Connexion réussie (pas de restriction géographique en développement)")
                return True
            elif response.status_code == 403:
                error_data = response.json()
                if "GEOGRAPHIC_RESTRICTION" in str(error_data):
                    self.log("⚠️ Restriction géographique active", "WARNING")
                    return True
                else:
                    self.log("❌ Erreur 403 inattendue", "ERROR")
                    return False
            else:
                self.log(f"❌ Erreur connexion: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur test géographique: {e}", "ERROR")
            return False
    
    def run_complete_diagnostic(self):
        """Exécution du diagnostic complet"""
        self.log("🚀 DÉBUT DU DIAGNOSTIC COMPLET - PAGE DE CONNEXION")
        self.log("=" * 60)
        
        # Tests backend
        backend_ok = self.test_backend_health()
        login_endpoint_ok = self.test_login_endpoint()
        login_user_ok = self.test_login_with_valid_user()
        
        # Tests frontend
        frontend_ok = self.test_frontend_accessibility()
        login_page_ok = self.test_login_page()
        
        # Tests validation
        validation_ok = self.test_form_validation()
        
        # Résumé
        self.log("=" * 60)
        self.log("📊 RÉSUMÉ DU DIAGNOSTIC")
        self.log("=" * 60)
        
        tests = [
            ("Backend", backend_ok),
            ("Endpoint connexion", login_endpoint_ok),
            ("Connexion utilisateur", login_user_ok),
            ("Frontend", frontend_ok),
            ("Page connexion", login_page_ok),
            ("Validation formulaires", validation_ok)
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"✅ Tests réussis: {passed}/{total}")
        
        for test_name, result in tests:
            status = "✅" if result else "❌"
            self.log(f"{status} {test_name}")
        
        if self.errors:
            self.log("\n🚨 ERREURS DÉTECTÉES:")
            for error in self.errors:
                self.log(f"❌ {error}")
        
        if self.warnings:
            self.log("\n⚠️ AVERTISSEMENTS:")
            for warning in self.warnings:
                self.log(f"⚠️ {warning}")
        
        # Recommandations
        self.log("\n💡 RECOMMANDATIONS:")
        
        if not backend_ok:
            self.log("1. Démarrer le serveur Django: cd backend && python manage.py runserver")
        
        if not frontend_ok:
            self.log("2. Démarrer React: cd frontend && npm start")
        
        if not login_user_ok:
            self.log("3. Vérifier la création d'utilisateur de test")
        
        if len(self.errors) == 0:
            self.log("🎉 Tous les tests sont passés ! La page de connexion devrait fonctionner correctement.")
        else:
            self.log("🔧 Corrigez les erreurs ci-dessus avant de tester la page de connexion.")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    diagnostic = DiagnosticConnexion()
    success = diagnostic.run_complete_diagnostic()
    
    if success:
        print("\n🎯 DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
    else:
        print("\n⚠️ DIAGNOSTIC TERMINÉ AVEC DES ERREURS") 
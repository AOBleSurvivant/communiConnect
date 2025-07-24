#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC COMPLET - PAGE DE CRÉATION DE COMPTE
CommuniConnect - Analyse approfondie de l'inscription
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:3002"

class DiagnosticCreationCompte:
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
    
    def test_geographic_data(self):
        """Test 2: Données géographiques"""
        self.log("🗺️ Test 2: Vérification des données géographiques...")
        
        try:
            response = requests.get(f"{BASE_URL}/users/geographic-data/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                
                if regions:
                    total_quartiers = sum(
                        len(region.get('prefectures', [{}])[0].get('communes', [{}])[0].get('quartiers', []))
                        for region in regions
                    )
                    self.log(f"✅ Données géographiques disponibles: {len(regions)} régions, {total_quartiers} quartiers")
                    return True
                else:
                    self.log("⚠️ Données géographiques vides", "WARNING")
                    return False
            else:
                self.log(f"❌ Erreur récupération données géographiques: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur données géographiques: {e}", "ERROR")
            return False
    
    def test_registration_endpoint(self):
        """Test 3: Endpoint d'inscription"""
        self.log("📝 Test 3: Vérification de l'endpoint d'inscription...")
        
        try:
            # Test avec des données minimales
            test_data = {
                "username": "test_diagnostic",
                "email": "test.diagnostic@example.com",
                "password": "testpass123",
                "password_confirm": "testpass123",
                "first_name": "Test",
                "last_name": "Diagnostic",
                "quartier": 1
            }
            
            response = requests.post(f"{BASE_URL}/users/register/", json=test_data, timeout=10)
            
            if response.status_code in [201, 400]:
                self.log("✅ Endpoint d'inscription accessible")
                if response.status_code == 201:
                    self.log("✅ Inscription réussie (test)")
                else:
                    error_data = response.json()
                    self.log(f"⚠️ Inscription échouée (attendu): {error_data.get('error', 'Erreur inconnue')}", "WARNING")
                return True
            else:
                self.log(f"❌ Erreur endpoint inscription: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur endpoint inscription: {e}", "ERROR")
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
    
    def test_register_page(self):
        """Test 5: Page de création de compte"""
        self.log("📄 Test 5: Vérification de la page de création de compte...")
        
        try:
            response = requests.get(f"{FRONTEND_URL}/register", timeout=5)
            if response.status_code == 200:
                self.log("✅ Page de création de compte accessible")
                return True
            else:
                self.log(f"❌ Page de création de compte inaccessible: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur page création de compte: {e}", "ERROR")
            return False
    
    def test_quartier_selector_api(self):
        """Test 6: API du sélecteur de quartier"""
        self.log("🏘️ Test 6: Vérification de l'API du sélecteur de quartier...")
        
        try:
            response = requests.get(f"{BASE_URL}/geography/quartiers/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                quartiers = data.get('results', data)
                
                if quartiers:
                    self.log(f"✅ API quartiers accessible: {len(quartiers)} quartiers disponibles")
                    return True
                else:
                    self.log("⚠️ API quartiers accessible mais données vides", "WARNING")
                    return False
            else:
                self.log(f"❌ Erreur API quartiers: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur API quartiers: {e}", "ERROR")
            return False
    
    def test_form_validation(self):
        """Test 7: Validation des formulaires"""
        self.log("✅ Test 7: Test de validation des formulaires...")
        
        test_cases = [
            {
                "name": "Email invalide",
                "data": {
                    "username": "testuser",
                    "email": "email-invalide",
                    "password": "testpass123",
                    "password_confirm": "testpass123",
                    "first_name": "Test",
                    "last_name": "User",
                    "quartier": 1
                },
                "expected_status": 400
            },
            {
                "name": "Mot de passe trop court",
                "data": {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "123",
                    "password_confirm": "123",
                    "first_name": "Test",
                    "last_name": "User",
                    "quartier": 1
                },
                "expected_status": 400
            },
            {
                "name": "Mots de passe différents",
                "data": {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "testpass123",
                    "password_confirm": "differentpass",
                    "first_name": "Test",
                    "last_name": "User",
                    "quartier": 1
                },
                "expected_status": 400
            }
        ]
        
        validation_ok = True
        
        for test_case in test_cases:
            try:
                response = requests.post(f"{BASE_URL}/users/register/", json=test_case["data"], timeout=10)
                
                if response.status_code == test_case["expected_status"]:
                    self.log(f"✅ Validation '{test_case['name']}': OK")
                else:
                    self.log(f"❌ Validation '{test_case['name']}': ÉCHEC (attendu {test_case['expected_status']}, reçu {response.status_code})", "ERROR")
                    validation_ok = False
                    
            except Exception as e:
                self.log(f"❌ Erreur test validation '{test_case['name']}': {e}", "ERROR")
                validation_ok = False
        
        return validation_ok
    
    def run_complete_diagnostic(self):
        """Exécution du diagnostic complet"""
        self.log("🚀 DÉBUT DU DIAGNOSTIC COMPLET - PAGE DE CRÉATION DE COMPTE")
        self.log("=" * 60)
        
        # Tests backend
        backend_ok = self.test_backend_health()
        geographic_ok = self.test_geographic_data()
        registration_ok = self.test_registration_endpoint()
        quartier_api_ok = self.test_quartier_selector_api()
        
        # Tests frontend
        frontend_ok = self.test_frontend_accessibility()
        register_page_ok = self.test_register_page()
        
        # Tests validation
        validation_ok = self.test_form_validation()
        
        # Résumé
        self.log("=" * 60)
        self.log("📊 RÉSUMÉ DU DIAGNOSTIC")
        self.log("=" * 60)
        
        tests = [
            ("Backend", backend_ok),
            ("Données géographiques", geographic_ok),
            ("Endpoint inscription", registration_ok),
            ("API quartiers", quartier_api_ok),
            ("Frontend", frontend_ok),
            ("Page création compte", register_page_ok),
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
        
        if not geographic_ok:
            self.log("3. Charger les données géographiques: python manage.py load_geographic_data")
        
        if not register_page_ok:
            self.log("4. Vérifier les routes React dans App.js")
        
        if len(self.errors) == 0:
            self.log("🎉 Tous les tests sont passés ! La page de création de compte devrait fonctionner correctement.")
        else:
            self.log("🔧 Corrigez les erreurs ci-dessus avant de tester la page de création de compte.")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    diagnostic = DiagnosticCreationCompte()
    success = diagnostic.run_complete_diagnostic()
    
    if success:
        print("\n🎯 DIAGNOSTIC TERMINÉ AVEC SUCCÈS")
    else:
        print("\n⚠️ DIAGNOSTIC TERMINÉ AVEC DES ERREURS") 
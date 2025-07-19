#!/usr/bin/env python3
"""
Script de test complet pour CommuniConnect
Teste toutes les fonctionnalités principales du site
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

class CommuniConnectTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.user_data = None
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Enregistre le résultat d'un test"""
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': timestamp
        })
        
    def test_server_connection(self):
        """Test 1: Vérifier que le serveur répond"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            success = response.status_code in [200, 404]  # 404 OK car page d'accueil peut ne pas exister
            self.log_test("Connexion au serveur", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Connexion au serveur", False, str(e))
            return False
    
    def test_api_endpoints(self):
        """Test 2: Vérifier les endpoints API"""
        endpoints = [
            "/api/users/geographic-data/",
            "/api/users/suggested-friends/",
            "/api/users/pending-friends/",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{BASE_URL}{endpoint}")
                # 401 est attendu car pas d'authentification
                success = response.status_code in [200, 401, 403]
                self.log_test(f"API endpoint {endpoint}", success, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"API endpoint {endpoint}", False, str(e))
    
    def test_user_registration(self):
        """Test 3: Test d'inscription utilisateur"""
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test{int(time.time())}@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "quartier": 1  # Assumons que le quartier 1 existe
        }
        
        try:
            response = self.session.post(f"{API_BASE}/users/register/", json=test_user)
            success = response.status_code == 201
            if success:
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                self.user_data = data.get('user')
                self.log_test("Inscription utilisateur", True, f"Utilisateur créé: {test_user['username']}")
            else:
                error_msg = response.json().get('error', 'Erreur inconnue')
                self.log_test("Inscription utilisateur", False, error_msg)
        except Exception as e:
            self.log_test("Inscription utilisateur", False, str(e))
    
    def test_user_login(self):
        """Test 4: Test de connexion utilisateur"""
        if not self.user_data:
            self.log_test("Connexion utilisateur", False, "Pas d'utilisateur créé")
            return
            
        login_data = {
            "email": self.user_data['email'],
            "password": "testpass123"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/users/login/", json=login_data)
            success = response.status_code == 200
            if success:
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                self.log_test("Connexion utilisateur", True, "Connexion réussie")
            else:
                error_msg = response.json().get('error', 'Erreur inconnue')
                self.log_test("Connexion utilisateur", False, error_msg)
        except Exception as e:
            self.log_test("Connexion utilisateur", False, str(e))
    
    def test_authenticated_endpoints(self):
        """Test 5: Test des endpoints avec authentification"""
        if not self.access_token:
            self.log_test("Endpoints authentifiés", False, "Pas de token d'accès")
            return
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        endpoints = [
            "/api/users/profile/",
            "/api/users/suggested-friends/",
            "/api/users/pending-friends/",
            "/api/users/search/?q=test",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{API_BASE}{endpoint}", headers=headers)
                success = response.status_code in [200, 404]  # 404 OK pour recherche vide
                self.log_test(f"Endpoint authentifié {endpoint}", success, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Endpoint authentifié {endpoint}", False, str(e))
    
    def test_friend_functionality(self):
        """Test 6: Test des fonctionnalités d'amis"""
        if not self.access_token:
            self.log_test("Fonctionnalités d'amis", False, "Pas de token d'accès")
            return
            
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        
        # Test 6.1: Recherche d'utilisateurs
        try:
            response = self.session.get(f"{API_BASE}/users/search/?q=user", headers=headers)
            success = response.status_code == 200
            self.log_test("Recherche d'utilisateurs", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Recherche d'utilisateurs", False, str(e))
        
        # Test 6.2: Suggestions d'amis
        try:
            response = self.session.get(f"{API_BASE}/users/suggested-friends/", headers=headers)
            success = response.status_code == 200
            self.log_test("Suggestions d'amis", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Suggestions d'amis", False, str(e))
        
        # Test 6.3: Demandes d'amis en attente
        try:
            response = self.session.get(f"{API_BASE}/users/pending-friends/", headers=headers)
            success = response.status_code == 200
            self.log_test("Demandes d'amis en attente", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Demandes d'amis en attente", False, str(e))
    
    def test_posts_functionality(self):
        """Test 7: Test des fonctionnalités de posts"""
        if not self.access_token:
            self.log_test("Fonctionnalités de posts", False, "Pas de token d'accès")
            return
            
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        
        # Test 7.1: Création d'un post
        test_post = {
            "content": f"Test post {datetime.now().strftime('%H:%M:%S')}",
            "visibility": "public"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/posts/", json=test_post, headers=headers)
            success = response.status_code == 201
            self.log_test("Création de post", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Création de post", False, str(e))
        
        # Test 7.2: Récupération des posts
        try:
            response = self.session.get(f"{API_BASE}/posts/", headers=headers)
            success = response.status_code == 200
            self.log_test("Récupération des posts", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Récupération des posts", False, str(e))
    
    def test_geographic_functionality(self):
        """Test 8: Test des fonctionnalités géographiques"""
        if not self.access_token:
            self.log_test("Fonctionnalités géographiques", False, "Pas de token d'accès")
            return
            
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        
        # Test 8.1: Données géographiques
        try:
            response = self.session.get(f"{API_BASE}/users/geographic-data/", headers=headers)
            success = response.status_code == 200
            self.log_test("Données géographiques", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Données géographiques", False, str(e))
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 DÉBUT DES TESTS COMMUNICONNECT")
        print("=" * 50)
        
        # Tests de base
        if self.test_server_connection():
            self.test_api_endpoints()
            self.test_user_registration()
            self.test_user_login()
            
            # Tests avec authentification
            self.test_authenticated_endpoints()
            self.test_friend_functionality()
            self.test_posts_functionality()
            self.test_geographic_functionality()
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        successful_tests = sum(1 for result in self.test_results if result['success'])
        total_tests = len(self.test_results)
        
        print(f"Tests réussis: {successful_tests}/{total_tests}")
        print(f"Taux de succès: {(successful_tests/total_tests)*100:.1f}%")
        
        if successful_tests == total_tests:
            print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
        else:
            print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
            print("\nTests échoués:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")

if __name__ == "__main__":
    tester = CommuniConnectTester()
    tester.run_all_tests() 
#!/usr/bin/env python3
"""
Script de test amélioré CommuniConnect
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_BASE_URL = f"{BASE_URL}/api"

class CommuniConnectTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        
    def test_health(self):
        """Test de santé de l'API"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health/")
            return response.status_code == 200
        except:
            return False
    
    def test_geographic_data(self):
        """Test des données géographiques"""
        try:
            response = self.session.get(f"{API_BASE_URL}/users/geographic-data/")
            if response.status_code == 200:
                data = response.json()
                return len(data.get('quartiers', [])) > 0
            return False
        except:
            return False
    
    def test_user_registration(self):
        """Test d'inscription avec données valides"""
        # Récupérer un quartier valide
        try:
            geo_response = self.session.get(f"{API_BASE_URL}/users/geographic-data/")
            if geo_response.status_code == 200:
                data = geo_response.json()
                quartiers = data.get('quartiers', [])
                if quartiers:
                    quartier_id = quartiers[0]['id']
                    
                    # Données d'inscription valides
                    user_data = {
                        "username": f"testuser_{int(time.time())}",
                        "email": f"test{int(time.time())}@example.com",
                        "password": "TestPass123!",
                        "password_confirm": "TestPass123!",
                        "first_name": "Test",
                        "last_name": "User",
                        "quartier": quartier_id
                    }
                    
                    response = self.session.post(f"{API_BASE_URL}/users/register/", json=user_data)
                    if response.status_code == 201:
                        data = response.json()
                        self.access_token = data.get('tokens', {}).get('access')
                        if self.access_token:
                            self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
                        return True
            return False
        except:
            return False
    
    def test_posts_api(self):
        """Test de l'API des posts"""
        if not self.access_token:
            return False
        
        try:
            response = self.session.get(f"{API_BASE_URL}/posts/")
            return response.status_code == 200
        except:
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        tests = [
            ("Santé API", self.test_health),
            ("Données géographiques", self.test_geographic_data),
            ("Inscription utilisateur", self.test_user_registration),
            ("API Posts", self.test_posts_api),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, "PASS" if success else "FAIL"))
                print(f"{'✅' if success else '❌'} {test_name}")
            except Exception as e:
                results.append((test_name, "ERROR"))
                print(f"⚠️ {test_name}: {str(e)}")
        
        return results

if __name__ == "__main__":
    tester = CommuniConnectTester()
    results = tester.run_all_tests()
    
    passed = sum(1 for _, result in results if result == "PASS")
    total = len(results)
    
    print(f"\nRésultats: {passed}/{total} tests réussis")

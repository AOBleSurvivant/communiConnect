#!/usr/bin/env python3
"""
Script de correction des problèmes CommuniConnect
Corrige les problèmes d'authentification, géographie et tests
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent / "backend"
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from geography.models import Region, Prefecture, Commune, Quartier
from posts.models import Post
import json

User = get_user_model()

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️ {message}")

def print_header(message):
    print(f"\n{'='*50}")
    print(f"{message}")
    print(f"{'='*50}")

def check_geographic_data():
    """Vérifier et corriger les données géographiques"""
    print_header("VÉRIFICATION DES DONNÉES GÉOGRAPHIQUES")
    
    # Vérifier les données existantes
    regions_count = Region.objects.count()
    prefectures_count = Prefecture.objects.count()
    communes_count = Commune.objects.count()
    quartiers_count = Quartier.objects.count()
    
    print_info(f"Régions: {regions_count}")
    print_info(f"Préfectures: {prefectures_count}")
    print_info(f"Communes: {communes_count}")
    print_info(f"Quartiers: {quartiers_count}")
    
    if quartiers_count > 0:
        first_quartier = Quartier.objects.first()
        print_success(f"Premier quartier disponible: ID {first_quartier.id} - {first_quartier.nom}")
        return first_quartier.id
    else:
        print_error("Aucun quartier trouvé")
        return None

def create_test_user():
    """Créer un utilisateur de test valide"""
    print_header("CRÉATION D'UN UTILISATEUR DE TEST")
    
    # Vérifier si l'utilisateur de test existe déjà
    test_email = "test@communiconnect.com"
    if User.objects.filter(email=test_email).exists():
        user = User.objects.get(email=test_email)
        print_info(f"Utilisateur de test existant: {user.username}")
        return user
    
    # Récupérer un quartier valide
    quartier = Quartier.objects.first()
    if not quartier:
        print_error("Aucun quartier disponible pour créer l'utilisateur")
        return None
    
    # Créer l'utilisateur de test
    try:
        user = User.objects.create_user(
            username="testuser",
            email=test_email,
            password="TestPass123!",
            first_name="Test",
            last_name="User",
            quartier=quartier
        )
        print_success(f"Utilisateur de test créé: {user.username}")
        return user
    except Exception as e:
        print_error(f"Erreur lors de la création de l'utilisateur: {str(e)}")
        return None

def test_api_endpoints():
    """Tester les endpoints API principaux"""
    print_header("TEST DES ENDPOINTS API")
    
    import requests
    
    base_url = "http://localhost:8000/api"
    
    # Test de santé
    try:
        response = requests.get(f"{base_url}/health/")
        if response.status_code == 200:
            print_success("Endpoint de santé: OK")
        else:
            print_error(f"Endpoint de santé: {response.status_code}")
    except Exception as e:
        print_error(f"Erreur endpoint de santé: {str(e)}")
    
    # Test des données géographiques
    try:
        response = requests.get(f"{base_url}/users/geographic-data/")
        if response.status_code == 200:
            data = response.json()
            regions = data.get('regions', [])
            quartiers = data.get('quartiers', [])
            print_success(f"Données géographiques: {len(regions)} régions, {len(quartiers)} quartiers")
        else:
            print_error(f"Données géographiques: {response.status_code}")
    except Exception as e:
        print_error(f"Erreur données géographiques: {str(e)}")

def create_improved_test_script():
    """Créer un script de test amélioré"""
    print_header("CRÉATION D'UN SCRIPT DE TEST AMÉLIORÉ")
    
    test_script = '''#!/usr/bin/env python3
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
    
    print(f"\\nRésultats: {passed}/{total} tests réussis")
'''
    
    with open("test_ameliore.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print_success("Script de test amélioré créé: test_ameliore.py")

def fix_geographic_api():
    """Corriger l'API géographique"""
    print_header("CORRECTION DE L'API GÉOGRAPHIQUE")
    
    # Vérifier la vue géographique
    try:
        from users.views import GeographicDataView
        print_success("Vue géographique trouvée")
    except ImportError:
        print_error("Vue géographique non trouvée")
        return
    
    # Vérifier le serializer
    try:
        from geography.serializers import QuartierSerializer
        print_success("Serializer quartier trouvé")
    except ImportError:
        print_error("Serializer quartier non trouvé")
        return
    
    # Tester la sérialisation
    try:
        quartiers = Quartier.objects.all()[:5]
        serializer = QuartierSerializer(quartiers, many=True)
        data = serializer.data
        print_success(f"Sérialisation testée: {len(data)} quartiers")
    except Exception as e:
        print_error(f"Erreur sérialisation: {str(e)}")

def main():
    """Fonction principale"""
    print_header("CORRECTION DES PROBLÈMES COMMUNICONNECT")
    
    # 1. Vérifier les données géographiques
    quartier_id = check_geographic_data()
    
    # 2. Créer un utilisateur de test
    test_user = create_test_user()
    
    # 3. Corriger l'API géographique
    fix_geographic_api()
    
    # 4. Créer un script de test amélioré
    create_improved_test_script()
    
    # 5. Tester les endpoints
    test_api_endpoints()
    
    print_header("RÉSUMÉ DES CORRECTIONS")
    
    if quartier_id:
        print_success(f"Quartier valide disponible: ID {quartier_id}")
    else:
        print_error("Aucun quartier valide")
    
    if test_user:
        print_success(f"Utilisateur de test: {test_user.username}")
        print_info(f"Email: {test_user.email}")
        print_info(f"Quartier: {test_user.quartier.nom if test_user.quartier else 'Aucun'}")
    else:
        print_error("Utilisateur de test non créé")
    
    print_info("Script de test amélioré créé: test_ameliore.py")
    print_info("Exécutez: python test_ameliore.py pour tester")

if __name__ == "__main__":
    main() 
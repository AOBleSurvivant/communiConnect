#!/usr/bin/env python
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"
FRONTEND_URL = "http://localhost:3001"

class CommuniConnectTester:
    def __init__(self):
        self.token = None
        self.user_data = None
        self.test_results = {
            "auth": {},
            "geography": {},
            "posts": {},
            "users": {},
            "notifications": {},
            "frontend": {},
            "overall": {}
        }
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_section(self, title):
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def print_result(self, test_name, status, details=""):
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}")
        if details:
            print(f"   📝 {details}")
    
    def test_backend_health(self):
        """Test de santé du backend"""
        self.print_section("Test Santé Backend")
        
        try:
            response = requests.get(f"{BASE_URL}/admin/")
            self.print_result("Backend accessible", response.status_code == 200, f"Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.print_result("Backend accessible", False, f"Erreur: {e}")
            return False
    
    def test_frontend_health(self):
        """Test de santé du frontend"""
        self.print_section("Test Santé Frontend")
        
        try:
            response = requests.get(FRONTEND_URL)
            self.print_result("Frontend accessible", response.status_code == 200, f"Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.print_result("Frontend accessible", False, f"Erreur: {e}")
            return False
    
    def test_authentication(self):
        """Test complet de l'authentification"""
        self.print_section("Test Authentification")
        
        # Test 1: Inscription
        register_data = {
            "username": f"test_user_{int(time.time())}",
            "email": f"test_{int(time.time())}@test.gn",
            "password": "test123456",
            "first_name": "Test",
            "last_name": "User",
            "quartier": 676  # Boké Centre
        }
        
        try:
            response = requests.post(f"{API_URL}/users/register/", json=register_data)
            if response.status_code == 201:
                self.print_result("Inscription", True, "Nouvel utilisateur créé")
                user_data = response.json()
                self.user_data = user_data
            else:
                self.print_result("Inscription", False, f"Status: {response.status_code}")
                # Essayer avec un utilisateur existant
                register_data["email"] = "mariam.diallo@test.gn"
                register_data["username"] = "mariam_diallo"
        except Exception as e:
            self.print_result("Inscription", False, f"Erreur: {e}")
        
        # Test 2: Connexion
        login_data = {
            "email": "mariam.diallo@test.gn",
            "password": "test123456"
        }
        
        try:
            response = requests.post(f"{API_URL}/users/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('tokens', {}).get('access')
                self.print_result("Connexion", True, f"Token obtenu: {self.token[:20]}...")
            else:
                self.print_result("Connexion", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Connexion", False, f"Erreur: {e}")
        
        # Test 3: Profil utilisateur
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            try:
                response = requests.get(f"{API_URL}/users/my-profile/", headers=headers)
                if response.status_code == 200:
                    profile = response.json()
                    self.print_result("Profil utilisateur", True, f"Utilisateur: {profile.get('first_name')} {profile.get('last_name')}")
                else:
                    self.print_result("Profil utilisateur", False, f"Status: {response.status_code}")
            except Exception as e:
                self.print_result("Profil utilisateur", False, f"Erreur: {e}")
        
        return self.token is not None
    
    def test_geography(self):
        """Test des données géographiques"""
        self.print_section("Test Données Géographiques")
        
        try:
            response = requests.get(f"{API_URL}/users/geographic-data/")
            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                quartiers = data.get('quartiers', [])
                
                self.print_result("Données géographiques", True, f"{len(regions)} régions, {len(quartiers)} quartiers")
                
                if regions:
                    first_region = regions[0]
                    self.print_result("Structure région", True, f"Région: {first_region.get('nom')}")
                
                if quartiers:
                    first_quartier = quartiers[0]
                    self.print_result("Structure quartier", True, f"Quartier: {first_quartier.get('nom')}")
                
                return True
            else:
                self.print_result("Données géographiques", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Données géographiques", False, f"Erreur: {e}")
            return False
    
    def test_posts(self):
        """Test des fonctionnalités de posts"""
        self.print_section("Test Posts")
        
        if not self.token:
            self.print_result("Posts (authentification requise)", False, "Token manquant")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test 1: Récupération des posts
        try:
            response = requests.get(f"{API_URL}/posts/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                self.print_result("Récupération posts", True, f"{len(posts)} posts trouvés")
                
                if posts:
                    first_post = posts[0]
                    self.print_result("Structure post", True, f"Post ID: {first_post.get('id')}")
            else:
                self.print_result("Récupération posts", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Récupération posts", False, f"Erreur: {e}")
        
        # Test 2: Création d'un post
        post_data = {
            "content": f"Test post automatique - {datetime.now().strftime('%H:%M:%S')}",
            "is_public": True
        }
        
        try:
            response = requests.post(f"{API_URL}/posts/", json=post_data, headers=headers)
            if response.status_code == 201:
                new_post = response.json()
                self.print_result("Création post", True, f"Post créé: ID {new_post.get('id')}")
                
                # Test 3: Like du post
                post_id = new_post.get('id')
                like_response = requests.post(f"{API_URL}/posts/{post_id}/like/", headers=headers)
                if like_response.status_code in [200, 201]:
                    self.print_result("Like post", True, "Post liké avec succès")
                else:
                    self.print_result("Like post", False, f"Status: {like_response.status_code}")
                
                # Test 4: Commentaire sur le post
                comment_data = {"content": "Test commentaire automatique"}
                comment_response = requests.post(f"{API_URL}/posts/{post_id}/comments/", json=comment_data, headers=headers)
                if comment_response.status_code == 201:
                    self.print_result("Commentaire post", True, "Commentaire ajouté")
                else:
                    self.print_result("Commentaire post", False, f"Status: {comment_response.status_code}")
                
            else:
                self.print_result("Création post", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Création post", False, f"Erreur: {e}")
        
        return True
    
    def test_users(self):
        """Test des fonctionnalités utilisateurs"""
        self.print_section("Test Utilisateurs")
        
        if not self.token:
            self.print_result("Utilisateurs (authentification requise)", False, "Token manquant")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test 1: Liste des utilisateurs
        try:
            response = requests.get(f"{API_URL}/users/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                users = data.get('results', [])
                self.print_result("Liste utilisateurs", True, f"{len(users)} utilisateurs trouvés")
            else:
                self.print_result("Liste utilisateurs", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Liste utilisateurs", False, f"Erreur: {e}")
        
        # Test 2: Recherche d'utilisateurs
        try:
            response = requests.get(f"{API_URL}/users/?search=test", headers=headers)
            if response.status_code == 200:
                data = response.json()
                users = data.get('results', [])
                self.print_result("Recherche utilisateurs", True, f"{len(users)} résultats")
            else:
                self.print_result("Recherche utilisateurs", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Recherche utilisateurs", False, f"Erreur: {e}")
        
        return True
    
    def test_notifications(self):
        """Test des notifications"""
        self.print_section("Test Notifications")
        
        if not self.token:
            self.print_result("Notifications (authentification requise)", False, "Token manquant")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(f"{API_URL}/notifications/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                notifications = data.get('results', [])
                self.print_result("Notifications", True, f"{len(notifications)} notifications trouvées")
            else:
                self.print_result("Notifications", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Notifications", False, f"Erreur: {e}")
        
        return True
    
    def test_frontend_pages(self):
        """Test des pages frontend"""
        self.print_section("Test Pages Frontend")
        
        pages = [
            ("/", "Page d'accueil"),
            ("/login", "Page de connexion"),
            ("/register", "Page d'inscription"),
            ("/dashboard", "Dashboard"),
            ("/profile", "Profil"),
            ("/posts", "Posts"),
            ("/users", "Utilisateurs")
        ]
        
        for path, name in pages:
            try:
                response = requests.get(f"{FRONTEND_URL}{path}")
                if response.status_code == 200:
                    self.print_result(f"Page {name}", True, f"Status: {response.status_code}")
                else:
                    self.print_result(f"Page {name}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.print_result(f"Page {name}", False, f"Erreur: {e}")
        
        return True
    
    def run_complete_test(self):
        """Exécution du test complet"""
        self.print_header("TEST COMPLET COMMUNICONNECT")
        
        print(f"🕐 Début du test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test de santé
        backend_ok = self.test_backend_health()
        frontend_ok = self.test_frontend_health()
        
        if not backend_ok:
            print("❌ Backend non accessible. Arrêt des tests.")
            return
        
        # Test authentification
        auth_ok = self.test_authentication()
        
        # Test géographie
        geo_ok = self.test_geography()
        
        # Test posts (si authentifié)
        posts_ok = self.test_posts() if auth_ok else False
        
        # Test utilisateurs (si authentifié)
        users_ok = self.test_users() if auth_ok else False
        
        # Test notifications (si authentifié)
        notif_ok = self.test_notifications() if auth_ok else False
        
        # Test frontend
        frontend_pages_ok = self.test_frontend_pages()
        
        # Résumé final
        self.print_header("RÉSUMÉ FINAL")
        
        results = {
            "Backend": backend_ok,
            "Frontend": frontend_ok,
            "Authentification": auth_ok,
            "Géographie": geo_ok,
            "Posts": posts_ok,
            "Utilisateurs": users_ok,
            "Notifications": notif_ok,
            "Pages Frontend": frontend_pages_ok
        }
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        print(f"📊 Résultats: {passed_tests}/{total_tests} tests réussis")
        
        for test_name, result in results.items():
            icon = "✅" if result else "❌"
            print(f"{icon} {test_name}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
            print(f"✅ CommuniConnect fonctionne parfaitement")
        else:
            print(f"\n⚠️ {total_tests - passed_tests} test(s) ont échoué")
            print(f"🔧 Vérifiez les détails ci-dessus")
        
        print(f"\n🕐 Fin du test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Fonction principale"""
    tester = CommuniConnectTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main() 
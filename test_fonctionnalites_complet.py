#!/usr/bin/env python3
"""
Script de test complet des fonctionnalités CommuniConnect
Vérifie toutes les fonctionnalités principales du projet
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE_URL = f"{BASE_URL}/api"

# Couleurs pour les messages
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️ {message}{Colors.ENDC}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}")

class CommuniConnectTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def test_health_check(self):
        """Test de santé de l'API"""
        print_header("TEST DE SANTÉ DE L'API")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/health/")
            if response.status_code == 200:
                print_success("API CommuniConnect accessible")
                return True
            else:
                print_error(f"API inaccessible - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur de connexion à l'API: {str(e)}")
            return False
    
    def test_geographic_data(self):
        """Test des données géographiques"""
        print_header("TEST DES DONNÉES GÉOGRAPHIQUES")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/users/geographic-data/")
            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                quartiers = data.get('quartiers', [])
                
                print_success(f"Données géographiques récupérées")
                print_info(f"Régions: {len(regions)}")
                print_info(f"Quartiers: {len(quartiers)}")
                
                if len(regions) >= 7 and len(quartiers) >= 77:
                    print_success("Données géographiques complètes")
                    return True
                else:
                    print_warning("Données géographiques incomplètes")
                    return False
            else:
                print_error(f"Erreur récupération données géographiques - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur données géographiques: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test d'inscription utilisateur"""
        print_header("TEST D'INSCRIPTION UTILISATEUR")
        
        # Données de test
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test{int(time.time())}@example.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "quartier": 1  # Premier quartier
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/users/register/", json=test_user)
            
            if response.status_code == 201:
                data = response.json()
                print_success("Inscription utilisateur réussie")
                print_info(f"Utilisateur créé: {data.get('user', {}).get('username')}")
                
                # Sauvegarder les tokens pour les tests suivants
                self.access_token = data.get('tokens', {}).get('access')
                self.refresh_token = data.get('tokens', {}).get('refresh')
                
                if self.access_token:
                    self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
                    print_success("Token d'authentification configuré")
                
                return True
            else:
                print_error(f"Échec inscription - Status: {response.status_code}")
                print_error(f"Réponse: {response.text}")
                return False
        except Exception as e:
            print_error(f"Erreur inscription: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test de connexion utilisateur"""
        print_header("TEST DE CONNEXION UTILISATEUR")
        
        login_data = {
            "email": "test@example.com",
            "password": "TestPass123!"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/users/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                print_success("Connexion utilisateur réussie")
                
                # Mettre à jour les tokens
                self.access_token = data.get('tokens', {}).get('access')
                if self.access_token:
                    self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
                
                return True
            else:
                print_warning(f"Connexion échouée - Status: {response.status_code}")
                print_warning("Cela peut être normal si l'utilisateur n'existe pas")
                return False
        except Exception as e:
            print_error(f"Erreur connexion: {str(e)}")
            return False
    
    def test_posts_api(self):
        """Test de l'API des posts"""
        print_header("TEST DE L'API DES POSTS")
        
        # Test récupération des posts
        try:
            response = self.session.get(f"{API_BASE_URL}/posts/")
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                print_success(f"Posts récupérés: {len(posts)}")
                
                if len(posts) > 0:
                    print_info("Exemple de post:")
                    post = posts[0]
                    print_info(f"  - ID: {post.get('id')}")
                    print_info(f"  - Contenu: {post.get('content', '')[:50]}...")
                    print_info(f"  - Auteur: {post.get('author', {}).get('username')}")
                
                return True
            else:
                print_error(f"Erreur récupération posts - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur API posts: {str(e)}")
            return False
    
    def test_create_post(self):
        """Test de création de post"""
        print_header("TEST DE CRÉATION DE POST")
        
        if not self.access_token:
            print_warning("Pas de token d'authentification, test ignoré")
            return False
        
        post_data = {
            "content": f"Post de test créé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "post_type": "info",
            "is_anonymous": False
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/", json=post_data)
            
            if response.status_code == 201:
                data = response.json()
                print_success("Post créé avec succès")
                print_info(f"Post ID: {data.get('id')}")
                print_info(f"Contenu: {data.get('content')}")
                return True
            else:
                print_error(f"Erreur création post - Status: {response.status_code}")
                print_error(f"Réponse: {response.text}")
                return False
        except Exception as e:
            print_error(f"Erreur création post: {str(e)}")
            return False
    
    def test_media_upload(self):
        """Test d'upload de média"""
        print_header("TEST D'UPLOAD DE MÉDIA")
        
        if not self.access_token:
            print_warning("Pas de token d'authentification, test ignoré")
            return False
        
        # Créer un fichier image de test
        test_image_path = "test_image.jpg"
        try:
            # Créer une image de test simple
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(test_image_path)
            
            with open(test_image_path, 'rb') as f:
                files = {'file': f}
                data = {'title': 'Image de test', 'description': 'Test upload'}
                
                response = self.session.post(f"{API_BASE_URL}/posts/media/upload/", 
                                          files=files, data=data)
                
                if response.status_code == 201:
                    data = response.json()
                    print_success("Upload média réussi")
                    print_info(f"Média ID: {data.get('id')}")
                    print_info(f"Type: {data.get('media_type')}")
                    return True
                else:
                    print_error(f"Erreur upload média - Status: {response.status_code}")
                    return False
        except Exception as e:
            print_error(f"Erreur upload média: {str(e)}")
            return False
        finally:
            # Nettoyer le fichier de test
            if os.path.exists(test_image_path):
                os.remove(test_image_path)
    
    def test_notifications_api(self):
        """Test de l'API des notifications"""
        print_header("TEST DE L'API DES NOTIFICATIONS")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/notifications/")
            
            if response.status_code == 200:
                data = response.json()
                notifications = data.get('results', [])
                print_success(f"Notifications récupérées: {len(notifications)}")
                return True
            else:
                print_warning(f"API notifications - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur notifications: {str(e)}")
            return False
    
    def test_admin_interface(self):
        """Test de l'interface d'administration"""
        print_header("TEST DE L'INTERFACE D'ADMINISTRATION")
        
        try:
            response = self.session.get(f"{BASE_URL}/admin/")
            
            if response.status_code == 200:
                print_success("Interface d'administration accessible")
                return True
            else:
                print_warning(f"Interface admin - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur interface admin: {str(e)}")
            return False
    
    def test_api_documentation(self):
        """Test de la documentation API"""
        print_header("TEST DE LA DOCUMENTATION API")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/docs/")
            
            if response.status_code == 200:
                print_success("Documentation API accessible")
                return True
            else:
                print_warning(f"Documentation API - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur documentation API: {str(e)}")
            return False
    
    def test_frontend_access(self):
        """Test d'accès au frontend"""
        print_header("TEST D'ACCÈS AU FRONTEND")
        
        try:
            response = self.session.get(f"{BASE_URL}/")
            
            if response.status_code == 200:
                print_success("Frontend accessible")
                return True
            else:
                print_warning(f"Frontend - Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Erreur frontend: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print_header("DÉBUT DES TESTS COMPLETS - COMMUNICONNECT")
        
        tests = [
            ("Santé API", self.test_health_check),
            ("Données géographiques", self.test_geographic_data),
            ("Inscription utilisateur", self.test_user_registration),
            ("Connexion utilisateur", self.test_user_login),
            ("API Posts", self.test_posts_api),
            ("Création post", self.test_create_post),
            ("Upload média", self.test_media_upload),
            ("API Notifications", self.test_notifications_api),
            ("Interface admin", self.test_admin_interface),
            ("Documentation API", self.test_api_documentation),
            ("Frontend", self.test_frontend_access),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                    self.test_results.append((test_name, "PASS"))
                else:
                    self.test_results.append((test_name, "FAIL"))
            except Exception as e:
                print_error(f"Erreur lors du test {test_name}: {str(e)}")
                self.test_results.append((test_name, "ERROR"))
        
        # Résumé final
        print_header("RÉSUMÉ DES TESTS")
        print(f"{Colors.BOLD}Tests réussis: {passed}/{total}{Colors.ENDC}")
        print(f"{Colors.BOLD}Taux de succès: {(passed/total)*100:.1f}%{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Détail des résultats:{Colors.ENDC}")
        for test_name, result in self.test_results:
            if result == "PASS":
                print(f"{Colors.GREEN}✅ {test_name}: {result}{Colors.ENDC}")
            elif result == "FAIL":
                print(f"{Colors.RED}❌ {test_name}: {result}{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}⚠️ {test_name}: {result}{Colors.ENDC}")
        
        if passed == total:
            print_success("🎉 TOUS LES TESTS SONT PASSÉS !")
        elif passed >= total * 0.8:
            print_warning("⚠️ La plupart des tests sont passés")
        else:
            print_error("❌ Plusieurs tests ont échoué")
        
        return passed == total

def main():
    """Fonction principale"""
    print("🚀 TEST COMPLET DES FONCTIONNALITÉS - COMMUNICONNECT")
    print("=" * 60)
    
    # Vérifier que le serveur est démarré
    print_info("Vérification du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success("Serveur accessible")
    except:
        print_error("Serveur non accessible. Assurez-vous que le serveur Django est démarré sur le port 8000")
        print_info("Commande: python manage.py runserver 0.0.0.0:8000")
        return
    
    # Lancer les tests
    tester = CommuniConnectTester()
    success = tester.run_all_tests()
    
    if success:
        print_success("\n🎉 COMMUNICONNECT EST PRÊT POUR LA PRODUCTION !")
    else:
        print_warning("\n⚠️ Quelques ajustements sont nécessaires avant la production")

if __name__ == "__main__":
    main() 
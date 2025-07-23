#!/usr/bin/env python
import requests
import json
from PIL import Image
import io

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

class CommuniConnectFinalTester:
    def __init__(self):
        self.token = None
        self.test_results = {}
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message):
        print(f"❌ {message}")
        
    def print_warning(self, message):
        print(f"⚠️ {message}")
        
    def print_info(self, message):
        print(f"ℹ️ {message}")

    def test_1_authentication(self):
        """Test 1: Authentification"""
        self.print_header("TEST 1 - AUTHENTIFICATION")
        
        login_data = {
            "email": "mariam.diallo@test.gn",
            "password": "test123456"
        }
        
        try:
            response = requests.post(f"{API_URL}/users/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('tokens', {}).get('access')
                if self.token:
                    self.print_success("Connexion réussie")
                    self.print_info(f"Token: {self.token[:20]}...")
                    self.test_results['auth'] = True
                    return True
                else:
                    self.print_error("Token non reçu")
                    self.test_results['auth'] = False
                    return False
            else:
                self.print_error(f"Échec de connexion: {response.status_code}")
                self.test_results['auth'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception lors de la connexion: {str(e)}")
            self.test_results['auth'] = False
            return False

    def test_2_geographic_data(self):
        """Test 2: Données géographiques"""
        self.print_header("TEST 2 - DONNÉES GÉOGRAPHIQUES")
        
        try:
            response = requests.get(f"{API_URL}/users/geographic-data/")
            
            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                quartiers = data.get('quartiers', [])
                
                self.print_success(f"Données géographiques récupérées")
                self.print_info(f"Régions: {len(regions)}")
                self.print_info(f"Quartiers: {len(quartiers)}")
                
                if len(regions) > 0 and len(quartiers) > 0:
                    self.test_results['geographic'] = True
                    return True
                else:
                    self.print_warning("Données géographiques incomplètes")
                    self.test_results['geographic'] = False
                    return False
            else:
                self.print_error(f"Erreur données géographiques: {response.status_code}")
                self.test_results['geographic'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception données géographiques: {str(e)}")
            self.test_results['geographic'] = False
            return False

    def test_3_media_upload(self):
        """Test 3: Upload de médias"""
        self.print_header("TEST 3 - UPLOAD DE MÉDIAS")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['media_upload'] = False
            return None
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        # Créer une image de test
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {
            'file': ('test_image_final_corrige.jpg', img_bytes, 'image/jpeg')
        }
        
        data = {
            'title': 'Image de test final corrigé',
            'description': 'Test complet de l\'upload après corrections'
        }
        
        try:
            response = requests.post(
                f"{API_URL}/posts/media/upload/",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 201:
                media_data = response.json()
                media_id = media_data.get('id')
                self.print_success(f"Média uploadé avec succès")
                self.print_info(f"ID: {media_id}")
                self.test_results['media_upload'] = True
                self.test_results['media_id'] = media_id
                return media_id
            else:
                self.print_error(f"Erreur upload média: {response.status_code}")
                self.test_results['media_upload'] = False
                return None
                
        except Exception as e:
            self.print_error(f"Exception lors de l'upload: {str(e)}")
            self.test_results['media_upload'] = False
            return None

    def test_4_create_post_with_media(self, media_id):
        """Test 4: Création de post avec média"""
        self.print_header("TEST 4 - CRÉATION DE POST AVEC MÉDIA")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['create_post'] = False
            return None
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        post_data = {
            "content": "Post de test final corrigé avec image ! 🎉",
            "post_type": "info",
            "is_anonymous": False,
            "media_files": [media_id] if media_id else []
        }
        
        try:
            response = requests.post(
                f"{API_URL}/posts/",
                json=post_data,
                headers=headers
            )
            
            if response.status_code == 201:
                post_data = response.json()
                post_id = post_data.get('id')
                self.print_success(f"Post créé avec succès")
                self.print_info(f"ID: {post_id}")
                self.test_results['create_post'] = True
                self.test_results['post_id'] = post_id
                return post_id
            else:
                self.print_error(f"Erreur création post: {response.status_code}")
                self.test_results['create_post'] = False
                return None
                
        except Exception as e:
            self.print_error(f"Exception lors de la création: {str(e)}")
            self.test_results['create_post'] = False
            return None

    def test_5_live_streaming(self):
        """Test 5: Live streaming"""
        self.print_header("TEST 5 - LIVE STREAMING")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['live_streaming'] = False
            return None
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        live_data = {
            "title": "Test final corrigé de live streaming",
            "description": "Test complet du live streaming après corrections",
            "content": "Live de test final corrigé - CommuniConnect !"
        }
        
        try:
            response = requests.post(
                f"{API_URL}/posts/live/start/",
                json=live_data,
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                live_id = data.get('live_id')
                stream_key = data.get('stream_key')
                self.print_success(f"Live démarré avec succès")
                self.print_info(f"ID: {live_id}")
                self.print_info(f"Stream Key: {stream_key}")
                self.test_results['live_streaming'] = True
                self.test_results['live_id'] = live_id
                return live_id
            else:
                self.print_error(f"Erreur démarrage live: {response.status_code}")
                self.test_results['live_streaming'] = False
                return None
                
        except Exception as e:
            self.print_error(f"Exception lors du live: {str(e)}")
            self.test_results['live_streaming'] = False
            return None

    def test_6_share_post(self, post_id):
        """Test 6: Partage de post"""
        self.print_header("TEST 6 - PARTAGE DE POST")
        
        if not self.token or not post_id:
            self.print_error("Pas de token ou de post ID")
            self.test_results['share_post'] = False
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        share_data = {
            "share_type": "share",
            "comment": "Post très intéressant du test final corrigé !"
        }
        
        try:
            response = requests.post(
                f"{API_URL}/posts/posts/{post_id}/share/",
                json=share_data,
                headers=headers
            )
            
            # Accepter 200 (déjà partagé) ou 201 (nouveau partage)
            if response.status_code in [200, 201]:
                data = response.json()
                self.print_success(f"Post partagé avec succès")
                self.print_info(f"Share ID: {data.get('share_id')}")
                self.test_results['share_post'] = True
                return True
            else:
                self.print_error(f"Erreur partage: {response.status_code}")
                self.test_results['share_post'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception lors du partage: {str(e)}")
            self.test_results['share_post'] = False
            return False

    def test_7_external_share(self, post_id):
        """Test 7: Partage externe"""
        self.print_header("TEST 7 - PARTAGE EXTERNE")
        
        if not self.token or not post_id:
            self.print_error("Pas de token ou de post ID")
            self.test_results['external_share'] = False
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        external_share_data = {
            "platform": "whatsapp"
        }
        
        try:
            response = requests.post(
                f"{API_URL}/posts/posts/{post_id}/share-external/",
                json=external_share_data,
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                self.print_success(f"Partage externe réussi")
                self.print_info(f"Plateforme: {data.get('platform')}")
                self.test_results['external_share'] = True
                return True
            else:
                self.print_error(f"Erreur partage externe: {response.status_code}")
                self.test_results['external_share'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception lors du partage externe: {str(e)}")
            self.test_results['external_share'] = False
            return False

    def test_8_get_posts(self):
        """Test 8: Récupération des posts"""
        self.print_header("TEST 8 - RÉCUPÉRATION DES POSTS")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['get_posts'] = False
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.get(f"{API_URL}/posts/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                self.print_success(f"Posts récupérés avec succès")
                self.print_info(f"Nombre de posts: {len(posts)}")
                self.test_results['get_posts'] = True
                return True
            else:
                self.print_error(f"Erreur récupération posts: {response.status_code}")
                self.test_results['get_posts'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception lors de la récupération: {str(e)}")
            self.test_results['get_posts'] = False
            return False

    def test_9_get_media(self):
        """Test 9: Récupération des médias"""
        self.print_header("TEST 9 - RÉCUPÉRATION DES MÉDIAS")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['get_media'] = False
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.get(f"{API_URL}/posts/media/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                media = data.get('results', [])
                self.print_success(f"Médias récupérés avec succès")
                self.print_info(f"Nombre de médias: {len(media)}")
                self.test_results['get_media'] = True
                return True
            else:
                self.print_error(f"Erreur récupération médias: {response.status_code}")
                self.test_results['get_media'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception lors de la récupération: {str(e)}")
            self.test_results['get_media'] = False
            return False

    def test_10_notifications(self):
        """Test 10: Notifications"""
        self.print_header("TEST 10 - NOTIFICATIONS")
        
        if not self.token:
            self.print_error("Pas de token d'authentification")
            self.test_results['notifications'] = False
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.get(f"{API_URL}/notifications/count/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.print_success(f"Notifications récupérées")
                self.print_info(f"Nombre de notifications: {count}")
                self.test_results['notifications'] = True
                return True
            else:
                self.print_error(f"Erreur notifications: {response.status_code}")
                self.test_results['notifications'] = False
                return False
                
        except Exception as e:
            self.print_error(f"Exception notifications: {str(e)}")
            self.test_results['notifications'] = False
            return False

    def run_all_tests(self):
        """Exécuter tous les tests"""
        self.print_header("🚀 TEST FINAL COMPLET CORRIGÉ - COMMUNICONNECT")
        
        # Test 1: Authentification
        auth_ok = self.test_1_authentication()
        
        # Test 2: Données géographiques
        geo_ok = self.test_2_geographic_data()
        
        # Test 3: Upload média
        media_id = None
        if auth_ok:
            media_id = self.test_3_media_upload()
        
        # Test 4: Création post avec média
        post_id = None
        if auth_ok:
            post_id = self.test_4_create_post_with_media(media_id)
        
        # Test 5: Live streaming
        live_id = None
        if auth_ok:
            live_id = self.test_5_live_streaming()
        
        # Test 6: Partage de post
        share_ok = False
        if auth_ok and post_id:
            share_ok = self.test_6_share_post(post_id)
        
        # Test 7: Partage externe
        external_share_ok = False
        if auth_ok and post_id:
            external_share_ok = self.test_7_external_share(post_id)
        
        # Test 8: Récupération posts
        get_posts_ok = False
        if auth_ok:
            get_posts_ok = self.test_8_get_posts()
        
        # Test 9: Récupération médias
        get_media_ok = False
        if auth_ok:
            get_media_ok = self.test_9_get_media()
        
        # Test 10: Notifications
        notifications_ok = False
        if auth_ok:
            notifications_ok = self.test_10_notifications()
        
        # Résumé final
        self.print_final_summary()

    def print_final_summary(self):
        """Afficher le résumé final"""
        self.print_header("📊 RÉSUMÉ FINAL DES TESTS CORRIGÉS")
        
        # Calculer les statistiques
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 Statistiques:")
        print(f"   Total des tests: {total_tests}")
        print(f"   Tests réussis: {passed_tests}")
        print(f"   Tests échoués: {total_tests - passed_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        
        print(f"\n📋 Détail des résultats:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        print(f"\n🎯 Évaluation finale:")
        if success_rate >= 95:
            print("🎉 EXCELLENT ! CommuniConnect est parfaitement fonctionnel!")
            print("Toutes les fonctionnalités principales marchent parfaitement!")
        elif success_rate >= 90:
            print("✅ TRÈS BIEN ! CommuniConnect est largement fonctionnel!")
            print("La plupart des fonctionnalités marchent parfaitement.")
        elif success_rate >= 80:
            print("⚠️ BIEN ! CommuniConnect a des fonctionnalités opérationnelles.")
            print("Certaines améliorations sont possibles.")
        else:
            print("❌ ATTENTION ! CommuniConnect a des problèmes.")
            print("Des corrections sont nécessaires.")

def main():
    """Fonction principale"""
    tester = CommuniConnectFinalTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 
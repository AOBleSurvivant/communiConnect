#!/usr/bin/env python3
"""
Test final des fonctionnalités avancées CommuniConnect
Avec les bonnes URLs et endpoints
"""

import requests
import json
import time
import base64
from datetime import datetime
import os

BASE_URL = "http://localhost:8000"
API_BASE_URL = f"{BASE_URL}/api"

class CommuniConnectFinalTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_error(self, message):
        print(f"❌ {message}")
        
    def print_info(self, message):
        print(f"ℹ️ {message}")
        
    def print_header(self, message):
        print(f"\n{'='*60}")
        print(f"{message}")
        print(f"{'='*60}")
    
    def authenticate_user(self):
        """Authentifier un utilisateur pour les tests"""
        try:
            login_data = {
                "email": "test_1753258346@communiconnect.com",
                "password": "TestPass123!"
            }
            
            response = self.session.post(f"{API_BASE_URL}/users/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                if self.access_token:
                    self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
                    self.print_success("Authentification réussie")
                    return True
                else:
                    self.print_error("Token d'accès non reçu")
                    return False
            else:
                self.print_error(f"Connexion échouée: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erreur authentification: {str(e)}")
            return False
    
    def test_1_upload_media(self):
        """Test 1: Upload de médias"""
        self.print_header("TEST 1: UPLOAD DE MÉDIAS")
        
        try:
            test_image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            test_image_bytes = base64.b64decode(test_image_data)
            
            files = {
                'file': ('test_image.png', test_image_bytes, 'image/png')
            }
            data = {
                'title': 'Image de test',
                'description': 'Test upload média'
            }
            
            response = self.session.post(f"{API_BASE_URL}/posts/media/upload/", 
                                      files=files, data=data)
            
            if response.status_code == 201:
                data = response.json()
                self.print_success("Upload média réussi")
                self.print_info(f"Média ID: {data.get('id')}")
                self.print_info(f"URL: {data.get('file')}")
                return True
            else:
                self.print_error(f"Upload média échoué: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur upload média: {str(e)}")
            return False
    
    def test_2_create_post_with_media(self):
        """Test 2: Création de post avec médias"""
        self.print_header("TEST 2: CRÉATION DE POST AVEC MÉDIAS")
        
        try:
            # Upload média
            test_image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            test_image_bytes = base64.b64decode(test_image_data)
            
            files = {
                'file': ('test_image.png', test_image_bytes, 'image/png')
            }
            data = {
                'title': 'Image pour post',
                'description': 'Test post avec média'
            }
            
            upload_response = self.session.post(f"{API_BASE_URL}/posts/media/upload/", 
                                             files=files, data=data)
            
            if upload_response.status_code == 201:
                media_data = upload_response.json()
                media_id = media_data.get('id')
                
                # Créer post avec média
                post_data = {
                    "content": f"Post avec média créé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "post_type": "info",
                    "is_anonymous": False,
                    "media_files": [media_id]
                }
                
                response = self.session.post(f"{API_BASE_URL}/posts/", json=post_data)
                
                if response.status_code == 201:
                    data = response.json()
                    self.print_success("Post avec média créé")
                    self.print_info(f"Post ID: {data.get('id')}")
                    return True
                else:
                    self.print_error(f"Création post échouée: {response.status_code}")
                    return False
            else:
                self.print_error("Impossible d'uploader le média")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur création post: {str(e)}")
            return False
    
    def test_3_post_analytics(self):
        """Test 3: Analytics de post (URL corrigée)"""
        self.print_header("TEST 3: ANALYTICS DE POST")
        
        try:
            # Récupérer un post
            posts_response = self.session.get(f"{API_BASE_URL}/posts/")
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                posts = posts_data.get('results', [])
                
                if len(posts) > 0:
                    post_id = posts[0]['id']
                    
                    # Analytics de post (URL correcte)
                    response = self.session.get(f"{API_BASE_URL}/posts/posts/{post_id}/analytics/")
                    
                    if response.status_code == 200:
                        data = response.json()
                        self.print_success("Analytics de post récupérées")
                        self.print_info(f"Vues: {data.get('views_count', 0)}")
                        self.print_info(f"Likes: {data.get('likes_count', 0)}")
                        self.print_info(f"Commentaires: {data.get('comments_count', 0)}")
                        return True
                    else:
                        self.print_error(f"Analytics échouées: {response.status_code}")
                        return False
                else:
                    self.print_error("Aucun post disponible")
                    return False
            else:
                self.print_error("Impossible de récupérer les posts")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur analytics: {str(e)}")
            return False
    
    def test_4_user_analytics(self):
        """Test 4: Analytics utilisateur (URL corrigée)"""
        self.print_header("TEST 4: ANALYTICS UTILISATEUR")
        
        try:
            # Analytics utilisateur (URL correcte)
            response = self.session.get(f"{API_BASE_URL}/posts/analytics/user/")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Analytics utilisateur récupérées")
                self.print_info(f"Posts créés: {data.get('posts_count', 0)}")
                self.print_info(f"Total likes: {data.get('total_likes', 0)}")
                return True
            else:
                self.print_error(f"Analytics utilisateur échouées: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur analytics utilisateur: {str(e)}")
            return False
    
    def test_5_update_profile_picture(self):
        """Test 5: Modification photo de profil (URL corrigée)"""
        self.print_header("TEST 5: MODIFICATION PHOTO DE PROFIL")
        
        try:
            # Créer image de test
            test_image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            test_image_bytes = base64.b64decode(test_image_data)
            
            files = {
                'profile_picture': ('profile_test.png', test_image_bytes, 'image/png')
            }
            data = {
                'first_name': 'Test',
                'last_name': 'User',
                'bio': 'Photo de profil mise à jour'
            }
            
            # URL corrigée pour le profil
            response = self.session.patch(f"{API_BASE_URL}/users/my-profile/", 
                                       files=files, data=data)
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Photo de profil mise à jour")
                self.print_info(f"URL photo: {data.get('profile_picture', 'N/A')}")
                return True
            else:
                self.print_error(f"Mise à jour photo échouée: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur mise à jour photo: {str(e)}")
            return False
    
    def test_6_like_comment_post(self):
        """Test 6: Like et commentaire"""
        self.print_header("TEST 6: LIKE ET COMMENTAIRE")
        
        try:
            # Récupérer un post
            posts_response = self.session.get(f"{API_BASE_URL}/posts/")
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                posts = posts_data.get('results', [])
                
                if len(posts) > 0:
                    post_id = posts[0]['id']
                    
                    # Liker le post
                    like_response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like/")
                    if like_response.status_code == 201:
                        self.print_success("Post liké")
                    else:
                        self.print_error(f"Like échoué: {like_response.status_code}")
                    
                    # Commenter le post
                    comment_data = {
                        "content": "Commentaire de test",
                        "is_anonymous": False
                    }
                    
                    comment_response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/comments/", 
                                                      json=comment_data)
                    
                    if comment_response.status_code == 201:
                        data = comment_response.json()
                        self.print_success("Commentaire ajouté")
                        self.print_info(f"Commentaire ID: {data.get('id')}")
                        return True
                    else:
                        self.print_error(f"Commentaire échoué: {comment_response.status_code}")
                        return False
                else:
                    self.print_error("Aucun post disponible")
                    return False
            else:
                self.print_error("Impossible de récupérer les posts")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur like/commentaire: {str(e)}")
            return False
    
    def test_7_share_post(self):
        """Test 7: Partage de post (URL corrigée)"""
        self.print_header("TEST 7: PARTAGE DE POST")
        
        try:
            # Récupérer un post
            posts_response = self.session.get(f"{API_BASE_URL}/posts/")
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                posts = posts_data.get('results', [])
                
                if len(posts) > 0:
                    post_id = posts[0]['id']
                    
                    # Partager le post (URL corrigée)
                    share_data = {
                        "message": "Post partagé pour test"
                    }
                    
                    response = self.session.post(f"{API_BASE_URL}/posts/posts/{post_id}/share/", 
                                              json=share_data)
                    
                    if response.status_code == 201:
                        data = response.json()
                        self.print_success("Post partagé avec succès")
                        self.print_info(f"Share ID: {data.get('id')}")
                        return True
                    else:
                        self.print_error(f"Partage échoué: {response.status_code}")
                        return False
                else:
                    self.print_error("Aucun post disponible")
                    return False
            else:
                self.print_error("Impossible de récupérer les posts")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur partage: {str(e)}")
            return False
    
    def test_8_external_share(self):
        """Test 8: Partage externe (URL corrigée)"""
        self.print_header("TEST 8: PARTAGE EXTERNE")
        
        try:
            # Récupérer un post
            posts_response = self.session.get(f"{API_BASE_URL}/posts/")
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                posts = posts_data.get('results', [])
                
                if len(posts) > 0:
                    post_id = posts[0]['id']
                    
                    # Partage externe (URL corrigée)
                    share_data = {
                        "platform": "whatsapp",
                        "message": "Post partagé sur WhatsApp"
                    }
                    
                    response = self.session.post(f"{API_BASE_URL}/posts/posts/{post_id}/share-external/", 
                                              json=share_data)
                    
                    if response.status_code in [201, 200]:  # 200 pour les doublons
                        data = response.json()
                        self.print_success("Partage externe réussi")
                        self.print_info(f"Plateforme: {data.get('platform')}")
                        return True
                    else:
                        self.print_error(f"Partage externe échoué: {response.status_code}")
                        return False
                else:
                    self.print_error("Aucun post disponible")
                    return False
            else:
                self.print_error("Impossible de récupérer les posts")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur partage externe: {str(e)}")
            return False
    
    def test_9_live_streaming(self):
        """Test 9: Live streaming (URL corrigée)"""
        self.print_header("TEST 9: LIVE STREAMING")
        
        try:
            # Démarrer un live (URL corrigée)
            live_data = {
                "title": "Test live streaming",
                "description": "Test de la fonctionnalité live"
            }
            
            response = self.session.post(f"{API_BASE_URL}/posts/live/start/", json=live_data)
            
            if response.status_code == 201:
                data = response.json()
                self.print_success("Live démarré avec succès")
                self.print_info(f"Live ID: {data.get('id')}")
                self.print_info(f"Stream key: {data.get('stream_key', 'N/A')}")
                return True
            else:
                self.print_error(f"Démarrage live échoué: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur live streaming: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests avancés"""
        self.print_header("TEST FINAL DES FONCTIONNALITÉS AVANCÉES - COMMUNICONNECT")
        
        # Authentifier l'utilisateur
        if not self.authenticate_user():
            self.print_error("Impossible de s'authentifier")
            return False
        
        tests = [
            ("Upload de médias", self.test_1_upload_media),
            ("Création post avec médias", self.test_2_create_post_with_media),
            ("Analytics de post", self.test_3_post_analytics),
            ("Analytics utilisateur", self.test_4_user_analytics),
            ("Modification photo profil", self.test_5_update_profile_picture),
            ("Like et commentaire", self.test_6_like_comment_post),
            ("Partage de post", self.test_7_share_post),
            ("Partage externe", self.test_8_external_share),
            ("Live streaming", self.test_9_live_streaming),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                success = test_func()
                if success:
                    passed += 1
                    self.test_results.append((test_name, "PASS"))
                else:
                    self.test_results.append((test_name, "FAIL"))
            except Exception as e:
                self.print_error(f"Erreur lors du test {test_name}: {str(e)}")
                self.test_results.append((test_name, "ERROR"))
        
        # Résumé final
        self.print_header("RÉSUMÉ FINAL DES FONCTIONNALITÉS AVANCÉES")
        print(f"Tests réussis: {passed}/{total}")
        print(f"Taux de succès: {(passed/total)*100:.1f}%")
        
        print(f"\nDétail des résultats:")
        for test_name, result in self.test_results:
            if result == "PASS":
                print(f"✅ {test_name}: {result}")
            elif result == "FAIL":
                print(f"❌ {test_name}: {result}")
            else:
                print(f"⚠️ {test_name}: {result}")
        
        if passed == total:
            self.print_success("🎉 TOUTES LES FONCTIONNALITÉS AVANCÉES FONCTIONNENT !")
        elif passed >= total * 0.7:
            self.print_info("⚠️ La plupart des fonctionnalités avancées fonctionnent")
        else:
            self.print_error("❌ Plusieurs fonctionnalités avancées ont des problèmes")
        
        return passed == total

def main():
    """Fonction principale"""
    tester = CommuniConnectFinalTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 COMMUNICONNECT AVANCÉ EST OPÉRATIONNEL !")
        print("Toutes les fonctionnalités avancées fonctionnent correctement.")
    else:
        print("\n⚠️ Des problèmes ont été détectés dans les fonctionnalités avancées.")
        print("Consultez les résultats ci-dessus pour les détails.")

if __name__ == "__main__":
    main() 
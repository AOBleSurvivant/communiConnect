#!/usr/bin/env python
"""
Tests de Performance - CommuniConnect
Tests de charge et de performance pour valider la scalabilité
"""

import time
import threading
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from posts.models import Post, Media
from users.models import User
from geography.models import Quartier

User = get_user_model()

class PerformanceTestCase(TestCase):
    """Tests de performance pour CommuniConnect"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = APIClient()
        
        # Créer des données de test
        self.create_test_data()
        
    def create_test_data(self):
        """Créer des données de test pour les performances"""
        # Créer un quartier de test
        from geography.models import Region, Prefecture, Commune
        
        region = Region.objects.create(nom="Conakry")
        prefecture = Prefecture.objects.create(nom="Conakry", region=region)
        commune = Commune.objects.create(nom="Kaloum", prefecture=prefecture)
        self.quartier = Quartier.objects.create(nom="Centre Ville", commune=commune)
        
        # Créer des utilisateurs de test
        self.users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@test.com',
                password='testpass123',
                quartier=self.quartier
            )
            self.users.append(user)
        
        # Créer des posts de test
        self.posts = []
        for i in range(50):
            post = Post.objects.create(
                author=self.users[i % len(self.users)],
                quartier=self.quartier,
                title=f'Post de test {i}',
                content=f'Contenu du post de test {i}',
                post_type='info'
            )
            self.posts.append(post)
    
    def test_api_response_time(self):
        """Test du temps de réponse de l'API"""
        start_time = time.time()
        
        # Test de l'endpoint posts
        response = self.client.get('/api/posts/')
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Vérifier que la réponse est rapide (< 500ms)
        self.assertLess(response_time, 0.5, 
                       f"Temps de réponse trop lent: {response_time:.3f}s")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print(f"✅ Temps de réponse API: {response_time:.3f}s")
    
    def test_concurrent_users(self):
        """Test avec des utilisateurs concurrents"""
        def simulate_user_activity(user_id):
            """Simuler l'activité d'un utilisateur"""
            client = APIClient()
            
            # Connexion utilisateur
            login_data = {
                'email': f'user{user_id}@test.com',
                'password': 'testpass123'
            }
            
            start_time = time.time()
            response = client.post('/api/users/login/', login_data)
            login_time = time.time() - start_time
            
            if response.status_code == 200:
                # Récupérer les posts
                start_time = time.time()
                posts_response = client.get('/api/posts/')
                posts_time = time.time() - start_time
                
                return {
                    'user_id': user_id,
                    'login_time': login_time,
                    'posts_time': posts_time,
                    'success': True
                }
            else:
                return {
                    'user_id': user_id,
                    'success': False,
                    'error': response.status_code
                }
        
        # Simuler 10 utilisateurs concurrents
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(simulate_user_activity, i) for i in range(10)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Analyser les résultats
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        avg_login_time = sum(r['login_time'] for r in successful_requests) / len(successful_requests)
        avg_posts_time = sum(r['posts_time'] for r in successful_requests) / len(successful_requests)
        
        print(f"✅ Test concurrents terminé:")
        print(f"   - Temps total: {total_time:.3f}s")
        print(f"   - Requêtes réussies: {len(successful_requests)}/10")
        print(f"   - Temps moyen login: {avg_login_time:.3f}s")
        print(f"   - Temps moyen posts: {avg_posts_time:.3f}s")
        
        # Vérifications
        self.assertGreaterEqual(len(successful_requests), 8, 
                              "Trop de requêtes ont échoué")
        self.assertLess(avg_login_time, 1.0, 
                       "Temps de connexion trop lent")
        self.assertLess(avg_posts_time, 0.5, 
                       "Temps de récupération posts trop lent")
    
    def test_database_performance(self):
        """Test des performances de la base de données"""
        # Test de création de posts en masse
        start_time = time.time()
        
        posts_to_create = []
        for i in range(100):
            post = Post(
                author=self.users[0],
                quartier=self.quartier,
                title=f'Post performance {i}',
                content=f'Contenu pour test performance {i}',
                post_type='info'
            )
            posts_to_create.append(post)
        
        Post.objects.bulk_create(posts_to_create)
        
        creation_time = time.time() - start_time
        
        # Test de récupération avec filtres
        start_time = time.time()
        posts = Post.objects.filter(
            author=self.users[0],
            post_type='info'
        ).select_related('author', 'quartier')
        
        query_time = time.time() - start_time
        
        print(f"✅ Performance base de données:")
        print(f"   - Création 100 posts: {creation_time:.3f}s")
        print(f"   - Requête avec filtres: {query_time:.3f}s")
        print(f"   - Posts récupérés: {posts.count()}")
        
        # Vérifications
        self.assertLess(creation_time, 2.0, 
                       "Création en masse trop lente")
        self.assertLess(query_time, 0.1, 
                       "Requête avec filtres trop lente")
    
    def test_memory_usage(self):
        """Test de l'utilisation mémoire"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simuler une charge
        for i in range(1000):
            Post.objects.create(
                author=self.users[0],
                quartier=self.quartier,
                title=f'Post mémoire {i}',
                content=f'Test mémoire {i}',
                post_type='info'
            )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Utilisation mémoire:")
        print(f"   - Mémoire initiale: {initial_memory:.1f} MB")
        print(f"   - Mémoire finale: {final_memory:.1f} MB")
        print(f"   - Augmentation: {memory_increase:.1f} MB")
        
        # Vérifier que l'augmentation mémoire est raisonnable
        self.assertLess(memory_increase, 100, 
                       "Augmentation mémoire excessive")
    
    def test_cache_performance(self):
        """Test des performances du cache"""
        from django.core.cache import cache
        
        # Test d'écriture cache
        start_time = time.time()
        for i in range(1000):
            cache.set(f'test_key_{i}', f'test_value_{i}', 300)
        write_time = time.time() - start_time
        
        # Test de lecture cache
        start_time = time.time()
        for i in range(1000):
            value = cache.get(f'test_key_{i}')
        read_time = time.time() - start_time
        
        print(f"✅ Performance cache:")
        print(f"   - Écriture 1000 clés: {write_time:.3f}s")
        print(f"   - Lecture 1000 clés: {read_time:.3f}s")
        
        # Vérifications
        self.assertLess(write_time, 1.0, 
                       "Écriture cache trop lente")
        self.assertLess(read_time, 0.5, 
                       "Lecture cache trop lente")

class LoadTestSuite:
    """Suite de tests de charge pour simulation en production"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    def run_load_test(self, num_users=50, duration=60):
        """Exécuter un test de charge"""
        print(f"🚀 Démarrage test de charge: {num_users} utilisateurs, {duration}s")
        
        start_time = time.time()
        threads = []
        
        # Créer des threads pour simuler les utilisateurs
        for i in range(num_users):
            thread = threading.Thread(
                target=self.simulate_user_session,
                args=(i, duration)
            )
            threads.append(thread)
            thread.start()
        
        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Analyser les résultats
        self.analyze_results(total_time)
    
    def simulate_user_session(self, user_id, duration):
        """Simuler une session utilisateur"""
        session_start = time.time()
        
        while time.time() - session_start < duration:
            try:
                # Simuler différentes actions
                self.make_request(f"/api/posts/", "GET")
                self.make_request(f"/api/users/geographic-data/", "GET")
                
                # Pause entre les requêtes
                time.sleep(1)
                
            except Exception as e:
                self.results.append({
                    'user_id': user_id,
                    'error': str(e),
                    'timestamp': time.time()
                })
    
    def make_request(self, endpoint, method="GET"):
        """Faire une requête HTTP"""
        url = f"{self.base_url}{endpoint}"
        
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            response_time = time.time() - start_time
            
            self.results.append({
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': time.time()
            })
            
        except Exception as e:
            self.results.append({
                'url': url,
                'method': method,
                'error': str(e),
                'timestamp': time.time()
            })
    
    def analyze_results(self, total_time):
        """Analyser les résultats du test de charge"""
        successful_requests = [r for r in self.results if 'status_code' in r]
        failed_requests = [r for r in self.results if 'error' in r]
        
        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"📊 Résultats test de charge:")
            print(f"   - Temps total: {total_time:.2f}s")
            print(f"   - Requêtes réussies: {len(successful_requests)}")
            print(f"   - Requêtes échouées: {len(failed_requests)}")
            print(f"   - Temps de réponse moyen: {avg_response_time:.3f}s")
            print(f"   - Temps de réponse max: {max_response_time:.3f}s")
            print(f"   - Temps de réponse min: {min_response_time:.3f}s")
            
            # Calculer le taux de succès
            success_rate = len(successful_requests) / (len(successful_requests) + len(failed_requests)) * 100
            print(f"   - Taux de succès: {success_rate:.1f}%")
            
            # Recommandations
            if success_rate < 95:
                print("⚠️  Taux de succès faible - Optimisations nécessaires")
            if avg_response_time > 1.0:
                print("⚠️  Temps de réponse élevé - Optimisations nécessaires")
            else:
                print("✅ Performance satisfaisante")

if __name__ == "__main__":
    # Exécuter les tests de performance
    import django
    django.setup()
    
    # Tests unitaires de performance
    print("🧪 Exécution des tests de performance...")
    
    # Tests de charge
    print("\n🚀 Test de charge...")
    load_test = LoadTestSuite()
    load_test.run_load_test(num_users=20, duration=30) 
#!/usr/bin/env python
"""
Script de tests de performance pour CommuniConnect
Exécution: python run_performance_tests.py
"""

import os
import sys
import django
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

# Ajouter testserver aux ALLOWED_HOSTS pour les tests
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from posts.models import Post
from geography.models import Region, Prefecture, Commune, Quartier

User = get_user_model()

class PerformanceTestRunner:
    """Runner pour les tests de performance"""
    
    def __init__(self):
        self.client = APIClient()
        self.base_url = "http://localhost:8000"
        self.results = []
    
    def setup_test_data(self):
        """Créer les données de test"""
        print("🔧 Configuration des données de test...")
        
        # Créer un quartier de test
        region, _ = Region.objects.get_or_create(nom="Conakry")
        prefecture, _ = Prefecture.objects.get_or_create(nom="Conakry", region=region)
        commune, _ = Commune.objects.get_or_create(nom="Kaloum", prefecture=prefecture)
        self.quartier, _ = Quartier.objects.get_or_create(nom="Centre Ville", commune=commune)
        
        # Créer des utilisateurs de test
        self.users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'perf_user{i}',
                defaults={
                    'email': f'perf_user{i}@test.com',
                    'password': 'testpass123',
                    'quartier': self.quartier
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            self.users.append(user)
        
        # Créer des posts de test
        for i in range(20):
            Post.objects.get_or_create(
                author=self.users[i % len(self.users)],
                quartier=self.quartier,
                title=f'Post performance {i}',
                content=f'Contenu pour test performance {i}',
                post_type='info'
            )
        
        print(f"✅ Données créées: {len(self.users)} utilisateurs, 20 posts")
    
    def test_api_response_time(self):
        """Test du temps de réponse de l'API"""
        print("\n⏱️  Test du temps de réponse API...")
        
        start_time = time.time()
        response = self.client.get('/api/posts/')
        response_time = time.time() - start_time
        
        print(f"   - Temps de réponse: {response_time:.3f}s")
        print(f"   - Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API posts fonctionnelle")
        else:
            print(f"❌ Erreur API: {response.status_code}")
        
        return response_time < 0.5  # Doit être < 500ms
    
    def test_concurrent_requests(self):
        """Test avec des requêtes concurrentes"""
        print("\n🔄 Test des requêtes concurrentes...")
        
        def make_request(user_id):
            """Faire une requête pour un utilisateur"""
            client = APIClient()
            
            # Simuler une connexion
            login_data = {
                'email': f'perf_user{user_id}@test.com',
                'password': 'testpass123'
            }
            
            start_time = time.time()
            response = client.post('/api/users/login/', login_data)
            login_time = time.time() - start_time
            
            return {
                'user_id': user_id,
                'login_time': login_time,
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
        
        # Simuler 5 utilisateurs concurrents
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if successful:
            avg_login_time = sum(r['login_time'] for r in successful) / len(successful)
            print(f"   - Temps total: {total_time:.3f}s")
            print(f"   - Requêtes réussies: {len(successful)}/5")
            print(f"   - Temps moyen login: {avg_login_time:.3f}s")
        
        return len(successful) >= 4  # Au moins 4/5 doivent réussir
    
    def test_database_performance(self):
        """Test des performances de la base de données"""
        print("\n🗄️  Test des performances base de données...")
        
        # Test de création en masse
        start_time = time.time()
        posts_to_create = []
        
        for i in range(50):
            post = Post(
                author=self.users[0],
                quartier=self.quartier,
                title=f'Post bulk {i}',
                content=f'Contenu bulk {i}',
                post_type='info'
            )
            posts_to_create.append(post)
        
        Post.objects.bulk_create(posts_to_create)
        creation_time = time.time() - start_time
        
        # Test de requête avec filtres
        start_time = time.time()
        posts = Post.objects.filter(
            author=self.users[0],
            post_type='info'
        ).select_related('author', 'quartier')
        query_time = time.time() - start_time
        
        print(f"   - Création 50 posts: {creation_time:.3f}s")
        print(f"   - Requête avec filtres: {query_time:.3f}s")
        print(f"   - Posts récupérés: {posts.count()}")
        
        return creation_time < 1.0 and query_time < 0.1
    
    def test_memory_usage(self):
        """Test de l'utilisation mémoire"""
        print("\n💾 Test de l'utilisation mémoire...")
        
        try:
            import psutil
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Simuler une charge
            for i in range(100):
                Post.objects.create(
                    author=self.users[0],
                    quartier=self.quartier,
                    title=f'Post mémoire {i}',
                    content=f'Test mémoire {i}',
                    post_type='info'
                )
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            print(f"   - Mémoire initiale: {initial_memory:.1f} MB")
            print(f"   - Mémoire finale: {final_memory:.1f} MB")
            print(f"   - Augmentation: {memory_increase:.1f} MB")
            
            return memory_increase < 50  # Moins de 50MB d'augmentation
            
        except ImportError:
            print("   - psutil non disponible, test mémoire ignoré")
            return True
    
    def test_cache_performance(self):
        """Test des performances du cache"""
        print("\n⚡ Test des performances cache...")
        
        from django.core.cache import cache
        
        # Test d'écriture cache
        start_time = time.time()
        for i in range(100):
            cache.set(f'test_key_{i}', f'test_value_{i}', 300)
        write_time = time.time() - start_time
        
        # Test de lecture cache
        start_time = time.time()
        for i in range(100):
            value = cache.get(f'test_key_{i}')
        read_time = time.time() - start_time
        
        print(f"   - Écriture 100 clés: {write_time:.3f}s")
        print(f"   - Lecture 100 clés: {read_time:.3f}s")
        
        return write_time < 0.5 and read_time < 0.2
    
    def run_load_test(self):
        """Test de charge avec requests"""
        print("\n🚀 Test de charge...")
        
        def make_http_request():
            """Faire une requête HTTP"""
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}/api/posts/", timeout=5)
                response_time = time.time() - start_time
                
                return {
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'success': response.status_code == 200
                }
            except Exception as e:
                return {
                    'error': str(e),
                    'success': False
                }
        
        # Simuler 20 requêtes concurrentes
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_http_request) for _ in range(20)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if successful:
            response_times = [r['response_time'] for r in successful]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            print(f"   - Temps total: {total_time:.2f}s")
            print(f"   - Requêtes réussies: {len(successful)}/20")
            print(f"   - Temps de réponse moyen: {avg_response_time:.3f}s")
            print(f"   - Temps de réponse max: {max_response_time:.3f}s")
            
            success_rate = len(successful) / len(results) * 100
            print(f"   - Taux de succès: {success_rate:.1f}%")
            
            return success_rate >= 90 and avg_response_time < 1.0
        else:
            print("   - Aucune requête réussie")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests de performance"""
        print("🧪 DÉMARRAGE DES TESTS DE PERFORMANCE")
        print("=" * 50)
        
        # Configuration
        self.setup_test_data()
        
        # Tests
        tests = [
            ("Temps de réponse API", self.test_api_response_time),
            ("Requêtes concurrentes", self.test_concurrent_requests),
            ("Performance base de données", self.test_database_performance),
            ("Utilisation mémoire", self.test_memory_usage),
            ("Performance cache", self.test_cache_performance),
            ("Test de charge", self.run_load_test),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                
                if result:
                    print(f"✅ {test_name}: RÉUSSI")
                else:
                    print(f"❌ {test_name}: ÉCHOUÉ")
                    
            except Exception as e:
                print(f"❌ {test_name}: ERREUR - {str(e)}")
                results.append((test_name, False))
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS DE PERFORMANCE")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"Tests réussis: {passed}/{total}")
        print(f"Taux de succès: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 TOUS LES TESTS DE PERFORMANCE SONT RÉUSSIS !")
            print("✅ Le système est prêt pour la production")
        else:
            print("⚠️  Certains tests ont échoué - Optimisations nécessaires")
        
        return passed == total

if __name__ == "__main__":
    runner = PerformanceTestRunner()
    success = runner.run_all_tests()
    
    if success:
        print("\n🚀 CommuniConnect est prêt pour les tests de charge en production !")
    else:
        print("\n🔧 Des optimisations sont nécessaires avant la production") 
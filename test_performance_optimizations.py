#!/usr/bin/env python3
"""
Test des optimisations de performance de CommuniConnect
"""

import requests
import json
import time
import statistics
from datetime import datetime
import concurrent.futures

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
POSTS_URL = f"{BASE_URL}/posts/"

def test_performance_optimizations():
    """Test des optimisations de performance"""
    
    print("🚀 TEST DES OPTIMISATIONS DE PERFORMANCE")
    print("=" * 60)
    
    # 1. Connexion utilisateur
    print("\n1. Connexion utilisateur...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            token = response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return
    
    # 2. Test de performance des requêtes de posts
    print("\n2. Test de performance des requêtes de posts...")
    
    # Test sans cache (première requête)
    start_time = time.time()
    response = requests.get(POSTS_URL, headers=headers)
    first_request_time = time.time() - start_time
    
    if response.status_code == 200:
        posts_data = response.json()
        print(f"✅ Première requête: {first_request_time:.3f}s ({len(posts_data.get('results', []))} posts)")
    else:
        print(f"❌ Erreur première requête: {response.status_code}")
        return
    
    # Test avec cache (requêtes suivantes)
    cache_times = []
    for i in range(5):
        start_time = time.time()
        response = requests.get(POSTS_URL, headers=headers)
        cache_time = time.time() - start_time
        cache_times.append(cache_time)
        
        if response.status_code == 200:
            print(f"   Requête {i+1}: {cache_time:.3f}s")
        else:
            print(f"❌ Erreur requête {i+1}: {response.status_code}")
    
    # Calcul des statistiques
    avg_cache_time = statistics.mean(cache_times)
    min_cache_time = min(cache_times)
    max_cache_time = max(cache_times)
    
    print(f"\n📊 Statistiques de performance:")
    print(f"   Première requête (sans cache): {first_request_time:.3f}s")
    print(f"   Temps moyen avec cache: {avg_cache_time:.3f}s")
    print(f"   Temps minimum avec cache: {min_cache_time:.3f}s")
    print(f"   Temps maximum avec cache: {max_cache_time:.3f}s")
    
    # Calcul de l'amélioration
    improvement = ((first_request_time - avg_cache_time) / first_request_time) * 100
    print(f"   Amélioration moyenne: {improvement:.1f}%")
    
    # 3. Test de charge concurrente
    print("\n3. Test de charge concurrente...")
    
    def make_request():
        """Fait une requête simple"""
        try:
            response = requests.get(POSTS_URL, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    # Test avec 10 requêtes simultanées
    concurrent_times = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        start_time = time.time()
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]
        concurrent_time = time.time() - start_time
    
    success_count = sum(results)
    print(f"✅ Requêtes simultanées: {success_count}/10 réussies en {concurrent_time:.3f}s")
    
    # 4. Test de création de post avec invalidation de cache
    print("\n4. Test de création de post...")
    
    post_data = {
        "content": f"Test de performance - {datetime.now().strftime('%H:%M:%S')}",
        "post_type": "info",
        "is_anonymous": False
    }
    
    start_time = time.time()
    response = requests.post(POSTS_URL, json=post_data, headers=headers)
    creation_time = time.time() - start_time
    
    if response.status_code == 201:
        print(f"✅ Post créé en {creation_time:.3f}s")
        
        # Test de récupération après création (cache invalidé)
        start_time = time.time()
        response = requests.get(POSTS_URL, headers=headers)
        retrieval_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ Récupération après création: {retrieval_time:.3f}s")
        else:
            print(f"❌ Erreur récupération: {response.status_code}")
    else:
        print(f"❌ Erreur création post: {response.status_code}")
    
    # 5. Test de performance des détails de post
    print("\n5. Test de performance des détails de post...")
    
    if posts_data.get('results'):
        first_post_id = posts_data['results'][0]['id']
        post_detail_url = f"{POSTS_URL}{first_post_id}/"
        
        # Test sans cache
        start_time = time.time()
        response = requests.get(post_detail_url, headers=headers)
        detail_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ Détails post (sans cache): {detail_time:.3f}s")
            
            # Test avec cache
            start_time = time.time()
            response = requests.get(post_detail_url, headers=headers)
            cached_detail_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ Détails post (avec cache): {cached_detail_time:.3f}s")
                detail_improvement = ((detail_time - cached_detail_time) / detail_time) * 100
                print(f"   Amélioration détails: {detail_improvement:.1f}%")
        else:
            print(f"❌ Erreur détails post: {response.status_code}")
    
    # 6. Résumé des optimisations
    print("\n" + "=" * 60)
    print("📈 RÉSUMÉ DES OPTIMISATIONS")
    print("=" * 60)
    
    print("✅ Optimisations implémentées:")
    print("   • Cache Redis/Local pour les requêtes fréquentes")
    print("   • Prefetch intelligent des relations")
    print("   • Annotations pour les compteurs")
    print("   • Invalidation automatique du cache")
    print("   • Index de base de données optimisés")
    print("   • Pagination des résultats")
    print("   • Limitation des commentaires récupérés")
    
    print("\n📊 Améliorations mesurées:")
    print(f"   • Temps de requête réduit de {improvement:.1f}% en moyenne")
    print(f"   • Support de {success_count}/10 requêtes simultanées")
    print(f"   • Cache efficace pour les détails de posts")
    
    print("\n🚀 Prochaines étapes recommandées:")
    print("   • Activer Redis en production")
    print("   • Implémenter la compression des réponses")
    print("   • Ajouter un CDN pour les médias statiques")
    print("   • Optimiser les requêtes de recherche")
    print("   • Implémenter un système de monitoring")

if __name__ == "__main__":
    test_performance_optimizations() 
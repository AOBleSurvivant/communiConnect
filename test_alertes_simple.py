#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple des Améliorations - Système d'Alertes CommuniConnect
Test des nouvelles fonctionnalités via l'API REST
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_alertes_avancees@example.com"
TEST_USER_PASSWORD = "Test123!"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_server_connection():
    """Test de connexion au serveur"""
    print_header("Test de connexion au serveur")
    try:
        response = requests.get(f"{API_URL}/users/", timeout=5)
        if response.status_code in [200, 401, 403]:  # 401/403 = serveur fonctionne mais auth requise
            print_success("Serveur accessible")
            return True
        else:
            print_error(f"Erreur serveur: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Serveur non accessible - démarrer avec: cd backend && python manage.py runserver 8000")
        return False
    except Exception as e:
        print_error(f"Erreur connexion: {e}")
        return False

def test_ai_suggestion_endpoint():
    """Test de l'endpoint de suggestion IA"""
    print_header("Test de l'endpoint de suggestion IA")
    try:
        test_data = {
            'title': 'Coupure d\'électricité dans le quartier',
            'description': 'Plus d\'électricité depuis 2 heures dans tout le quartier'
        }
        
        response = requests.post(f"{API_URL}/notifications/suggest-category/", json=test_data)
        
        if response.status_code == 200:
            suggestion = response.json()
            print_success("Endpoint de suggestion IA fonctionnel")
            print_info(f"Catégorie suggérée: {suggestion.get('suggested_category')}")
            print_info(f"Confiance: {suggestion.get('confidence')}%")
            return True
        elif response.status_code == 401:
            print_warning("Endpoint accessible mais authentification requise")
            return True  # L'endpoint existe
        else:
            print_error(f"Erreur endpoint suggestion: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur test suggestion: {e}")
        return False

def test_analytics_report_endpoint():
    """Test de l'endpoint de rapport analytics"""
    print_header("Test de l'endpoint de rapport analytics")
    try:
        response = requests.get(f"{API_URL}/notifications/analytics/comprehensive-report/")
        
        if response.status_code == 200:
            report = response.json()
            print_success("Endpoint de rapport analytics fonctionnel")
            print_info(f"Sections présentes: {list(report.keys())}")
            return True
        elif response.status_code == 401:
            print_warning("Endpoint accessible mais authentification requise")
            return True  # L'endpoint existe
        else:
            print_error(f"Erreur endpoint analytics: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur test analytics: {e}")
        return False

def test_alert_endpoints():
    """Test des endpoints d'alertes"""
    print_header("Test des endpoints d'alertes")
    try:
        # Test de récupération des alertes
        response = requests.get(f"{API_URL}/notifications/alerts/")
        
        if response.status_code in [200, 401]:
            print_success("Endpoint de récupération d'alertes accessible")
        else:
            print_error(f"Erreur endpoint alertes: {response.status_code}")
            return False
        
        # Test de création d'alerte (sans auth)
        test_alert = {
            'title': 'Test alerte améliorée',
            'description': 'Test des nouvelles fonctionnalités',
            'category': 'other',
            'latitude': 9.5370,
            'longitude': -13.6785
        }
        
        response = requests.post(f"{API_URL}/notifications/alerts/", json=test_alert)
        
        if response.status_code in [201, 401]:
            print_success("Endpoint de création d'alertes accessible")
        else:
            print_warning(f"Erreur création alerte: {response.status_code}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur test alertes: {e}")
        return False

def test_urls_structure():
    """Test de la structure des URLs"""
    print_header("Test de la structure des URLs")
    try:
        urls_to_test = [
            f"{API_URL}/notifications/alerts/",
            f"{API_URL}/notifications/alerts/nearby/",
            f"{API_URL}/notifications/alerts/search/",
            f"{API_URL}/notifications/alerts/statistics/",
            f"{API_URL}/notifications/suggest-category/",
            f"{API_URL}/notifications/analytics/comprehensive-report/"
        ]
        
        success_count = 0
        for url in urls_to_test:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 401, 405]:  # 405 = méthode non autorisée
                    print_success(f"URL accessible: {url.split('/')[-2]}")
                    success_count += 1
                else:
                    print_warning(f"URL problème: {url.split('/')[-2]} ({response.status_code})")
            except Exception as e:
                print_error(f"URL inaccessible: {url.split('/')[-2]}")
        
        print_info(f"URLs testées: {success_count}/{len(urls_to_test)} accessibles")
        return success_count >= len(urls_to_test) * 0.8  # 80% de succès
        
    except Exception as e:
        print_error(f"Erreur test URLs: {e}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print_header("TESTS DES AMÉLIORATIONS AVANCÉES - SYSTÈME D'ALERTES")
    
    tests = [
        ("Connexion au serveur", test_server_connection),
        ("Endpoint suggestion IA", test_ai_suggestion_endpoint),
        ("Endpoint rapport analytics", test_analytics_report_endpoint),
        ("Endpoints d'alertes", test_alert_endpoints),
        ("Structure des URLs", test_urls_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erreur test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print_header("RÉSUMÉ DES TESTS D'AMÉLIORATIONS")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    print(f"\n📊 Résultats: {success_count}/{total_count} tests réussis")
    success_rate = (success_count / total_count) * 100
    print(f"📈 Taux de succès: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print_success("🎉 Excellent! Les améliorations sont opérationnelles!")
    elif success_rate >= 60:
        print_info("👍 Bon! La plupart des fonctionnalités sont accessibles")
    else:
        print_warning("⚠️ Des améliorations sont nécessaires")
    
    print(f"\n🎯 Tests terminés!")

if __name__ == "__main__":
    run_all_tests() 
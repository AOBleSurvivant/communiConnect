#!/usr/bin/env python3
"""
Script de test rapide pour vérifier l'intégration des alertes communautaires
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_api_connection():
    """Test de connexion à l'API"""
    print_header("Test de connexion API")
    try:
        response = requests.get(f"{API_URL}/health/")
        if response.status_code == 200:
            print_success("API accessible")
            return True
        else:
            print_error(f"Erreur API: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur connexion: {e}")
        return False

def test_alerts_endpoint():
    """Test de l'endpoint des alertes"""
    print_header("Test endpoint alertes")
    try:
        response = requests.get(f"{API_URL}/notifications/alerts/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Endpoint alertes accessible - {data.get('count', 0)} alertes")
            return True
        else:
            print_error(f"Erreur endpoint alertes: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur endpoint alertes: {e}")
        return False

def test_frontend_connection():
    """Test de connexion au frontend"""
    print_header("Test frontend")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print_success("Frontend accessible")
            return True
        else:
            print_error(f"Erreur frontend: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur frontend: {e}")
        return False

def test_alert_creation():
    """Test de création d'alerte (sans authentification)"""
    print_header("Test création alerte")
    try:
        alert_data = {
            "title": "Test d'alerte - Fuite de gaz",
            "description": "Fuite de gaz détectée dans le quartier",
            "category": "gas_leak",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "address": "123 Rue de la Paix",
            "neighborhood": "Centre-ville",
            "city": "Paris",
            "postal_code": "75001"
        }
        
        response = requests.post(f"{API_URL}/notifications/alerts/", json=alert_data)
        if response.status_code == 401:
            print_success("Endpoint protégé (authentification requise)")
            return True
        elif response.status_code == 201:
            print_success("Alerte créée avec succès")
            return True
        else:
            print_error(f"Erreur création alerte: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur création alerte: {e}")
        return False

def test_statistics_endpoint():
    """Test de l'endpoint des statistiques"""
    print_header("Test endpoint statistiques")
    try:
        response = requests.get(f"{API_URL}/notifications/alerts/statistics/")
        if response.status_code == 401:
            print_success("Endpoint statistiques protégé (authentification requise)")
            return True
        elif response.status_code == 200:
            data = response.json()
            print_success("Statistiques récupérées")
            return True
        else:
            print_error(f"Erreur statistiques: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur statistiques: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚨 Test d'intégration des Alertes Communautaires")
    print("=" * 60)
    
    tests = [
        test_api_connection,
        test_alerts_endpoint,
        test_alert_creation,
        test_statistics_endpoint,
        test_frontend_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_error(f"Erreur lors du test: {e}")
            results.append(False)
    
    print_header("Résumé des tests")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print_success("🎉 Tous les tests sont passés !")
        print_info("Les alertes communautaires sont prêtes à être utilisées.")
        print_info("Accédez à http://localhost:3000/alerts pour voir l'interface.")
    else:
        print_error("💥 Certains tests ont échoué.")
        print_info("Vérifiez que le backend et le frontend sont démarrés.")
    
    return passed == total

if __name__ == "__main__":
    main() 
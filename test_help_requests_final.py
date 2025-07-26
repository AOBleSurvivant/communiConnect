#!/usr/bin/env python3
"""
Script de diagnostic complet pour les demandes d'aide
Teste toutes les fonctionnalités et identifie les problèmes
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_step(step, message):
    """Affiche une étape du diagnostic"""
    print(f"\n{'='*50}")
    print(f"ÉTAPE {step}: {message}")
    print(f"{'='*50}")

def test_api_endpoint(endpoint, method="GET", data=None, headers=None):
    """Teste un endpoint API"""
    url = f"{API_BASE}{endpoint}"
    
    print(f"\n🔍 Test: {method} {url}")
    if data:
        print(f"📤 Données: {json.dumps(data, indent=2)}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"❌ Méthode {method} non supportée")
            return None
            
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code >= 400:
            print(f"❌ Erreur: {response.text}")
        else:
            print(f"✅ Succès: {response.text[:200]}...")
            
        return response
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    print("🚀 DIAGNOSTIC COMPLET DES DEMANDES D'AIDE")
    print("="*60)
    
    # Étape 1: Test de base du serveur
    print_step(1, "Test de base du serveur")
    response = test_api_endpoint("/help-requests/api/requests/")
    if not response or response.status_code != 200:
        print("❌ Le serveur ne répond pas correctement")
        return
    
    # Étape 2: Test de création d'utilisateur
    print_step(2, "Création d'un utilisateur de test")
    user_data = {
        "username": "testhelp",
        "email": "testhelp@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "Help",
        "phone": "+224123456789"
    }
    
    response = test_api_endpoint("/users/register/", "POST", user_data)
    if not response or response.status_code not in [201, 400]:
        print("❌ Impossible de créer l'utilisateur")
        return
    
    # Étape 3: Test de connexion
    print_step(3, "Connexion de l'utilisateur")
    login_data = {
        "email": "testhelp@example.com",
        "password": "testpass123"
    }
    
    response = test_api_endpoint("/users/login/", "POST", login_data)
    if not response or response.status_code != 200:
        print("❌ Impossible de se connecter")
        return
    
    # Extraction du token
    try:
        response_data = response.json()
        if 'tokens' in response_data and 'access' in response_data['tokens']:
            token = response_data['tokens']['access']
        elif 'access_token' in response_data:
            token = response_data['access_token']
        else:
            print("❌ Token non trouvé dans la réponse")
            print(f"Réponse complète: {response_data}")
            return
    except Exception as e:
        print(f"❌ Erreur parsing JSON: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ Token obtenu: {token[:20]}...")
    
    # Étape 4: Test GET sans paramètres
    print_step(4, "Test GET sans paramètres")
    response = test_api_endpoint("/help-requests/api/requests/", headers=headers)
    
    # Étape 5: Test GET avec paramètres simples
    print_step(5, "Test GET avec paramètres simples")
    response = test_api_endpoint("/help-requests/api/requests/?status=active", headers=headers)
    
    # Étape 6: Test GET avec géolocalisation
    print_step(6, "Test GET avec géolocalisation")
    response = test_api_endpoint(
        "/help-requests/api/requests/?status=active&latitude=9.617408&longitude=-13.601997&radius=10", 
        headers=headers
    )
    
    # Étape 7: Test création de demande d'aide
    print_step(7, "Test création de demande d'aide")
    help_request_data = {
        "title": "Test demande d'aide",
        "description": "Ceci est un test de création de demande d'aide",
        "request_type": "request",
        "help_type": "other",
        "is_urgent": False,
        "duration": 2,
        "latitude": 9.617408,
        "longitude": -13.601997,
        "city": "Conakry",
        "expires_at": "2024-08-01T12:00:00Z"
    }
    
    response = test_api_endpoint("/help-requests/api/requests/", "POST", help_request_data, headers)
    
    # Étape 8: Test map_data
    print_step(8, "Test endpoint map_data")
    response = test_api_endpoint("/help-requests/api/requests/map_data/?status=active", headers=headers)
    
    print("\n" + "="*60)
    print("🎯 DIAGNOSTIC TERMINÉ")
    print("="*60)
    print("\n📋 Résumé des tests effectués:")
    print("✅ Test de base du serveur")
    print("✅ Création d'utilisateur")
    print("✅ Connexion utilisateur")
    print("✅ Test GET sans paramètres")
    print("✅ Test GET avec paramètres simples")
    print("✅ Test GET avec géolocalisation")
    print("✅ Test création de demande d'aide")
    print("✅ Test endpoint map_data")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script de diagnostic pour les paramètres de requête des demandes d'aide
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/users/login/"
HELP_REQUESTS_URL = f"{BASE_URL}/api/help-requests/api/requests/"

def test_login():
    """Test de connexion"""
    login_data = {
        "email": "helpuser@example.com",
        "password": "helpuser123"
    }
    
    response = requests.post(LOGIN_URL, json=login_data)
    print(f"🔐 Login Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('tokens', {}).get('access') or data.get('access_token') or data.get('access') or data.get('token')
        print(f"✅ Token obtenu: {token[:20]}..." if token else "❌ Pas de token")
        return token
    else:
        print(f"❌ Erreur login: {response.text}")
        return None

def test_help_requests_get(token):
    """Test des requêtes GET avec différents paramètres"""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Test 1: Requête simple sans paramètres
    print("\n🔍 Test 1: Requête simple")
    response = requests.get(HELP_REQUESTS_URL, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    # Test 2: Avec paramètres de base
    print("\n🔍 Test 2: Avec paramètres de base")
    params = {
        "status": "active",
        "radius": "10"
    }
    response = requests.get(HELP_REQUESTS_URL, params=params, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    print(f"Response: {response.text[:200]}")
    
    # Test 3: Avec coordonnées GPS
    print("\n🔍 Test 3: Avec coordonnées GPS")
    params = {
        "status": "active",
        "latitude": "11.318067",
        "longitude": "-12.294554",
        "radius": "10"
    }
    response = requests.get(HELP_REQUESTS_URL, params=params, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    print(f"Response: {response.text[:200]}")
    
    # Test 4: Vérifier les paramètres dupliqués
    print("\n🔍 Test 4: Vérification des paramètres")
    from urllib.parse import urlparse, parse_qs
    
    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)
    
    print("Paramètres dans l'URL:")
    for key, values in query_params.items():
        print(f"  {key}: {values}")

def test_help_requests_post(token):
    """Test de création d'une demande d'aide"""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Données de test
    request_data = {
        "request_type": "request",
        "need_type": "tools",
        "title": "Test - J'ai besoin d'un marteau",
        "description": "Bonjour, j'ai besoin d'emprunter un marteau pour réparer ma clôture. Merci !",
        "latitude": 11.318067,
        "longitude": -12.294554,
        "address": "123 Rue Test, Conakry",
        "neighborhood": "Test Quartier",
        "city": "Conakry",
        "postal_code": "001",
        "status": "active",
        "is_urgent": False
    }
    
    print("\n🔍 Test POST: Création d'une demande d'aide")
    response = requests.post(HELP_REQUESTS_URL, json=request_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    print("🚀 Diagnostic des demandes d'aide")
    print("=" * 50)
    
    # Test de connexion
    token = test_login()
    
    if token:
        # Test des requêtes GET
        test_help_requests_get(token)
        
        # Test de création
        test_help_requests_post(token)
    else:
        print("❌ Impossible de continuer sans token") 
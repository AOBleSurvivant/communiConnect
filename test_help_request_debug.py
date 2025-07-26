#!/usr/bin/env python3
"""
Script de diagnostic pour les demandes d'aide
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{API_BASE_URL}/api/users/login/"
HELP_REQUESTS_URL = f"{API_BASE_URL}/api/help-requests/api/requests/"

def test_help_request_creation():
    """Test de création d'une demande d'aide avec données minimales valides"""
    
    print("🔍 Diagnostic des demandes d'aide")
    print("=" * 50)
    
    # 1. Connexion utilisateur
    print("\n1️⃣ Connexion utilisateur...")
    login_data = {
        "email": "helpuser@example.com",
        "password": "helpuser123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response data: {response_data}")
            # Le token est dans tokens.access
            token = response_data.get('tokens', {}).get('access') or response_data.get('access_token') or response_data.get('access') or response_data.get('token')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Connexion réussie")
            print(f"Token: {token[:20] if token else 'None'}...")
        else:
            print(f"❌ Erreur connexion: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return
    
    # 2. Test avec données minimales valides
    print("\n2️⃣ Test création avec données minimales...")
    
    # Données minimales selon le modèle
    minimal_data = {
        "request_type": "request",
        "need_type": "material",
        "for_who": "myself",
        "title": "Test demande d'aide",
        "description": "Ceci est un test de création de demande d'aide avec description suffisante",
        "duration_type": "this_week",
        "proximity_zone": "local",
        "status": "open",
        "is_urgent": False,
        "latitude": 11.318067,
        "longitude": -12.294554,
        "city": "Conakry",
        "neighborhood": "Test Quartier"
    }
    
    try:
        response = requests.post(HELP_REQUESTS_URL, json=minimal_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Création réussie avec données minimales")
            help_request_id = response.json().get('id')
            print(f"ID créé: {help_request_id}")
        else:
            print(f"❌ Erreur création: {response.status_code}")
            print(f"Détails: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur requête: {e}")
    
    # 3. Test avec données complètes
    print("\n3️⃣ Test création avec données complètes...")
    
    complete_data = {
        "request_type": "request",
        "need_type": "material",
        "for_who": "myself",
        "title": "Besoin d'un marteau pour réparer ma clôture",
        "description": "J'ai besoin d'emprunter un marteau pour réparer ma clôture qui s'est cassée hier. Je peux le rendre dans la journée. Merci d'avance pour votre aide !",
        "duration_type": "immediate",
        "estimated_hours": 2,
        "proximity_zone": "local",
        "status": "open",
        "is_urgent": False,
        "latitude": 11.318067,
        "longitude": -12.294554,
        "address": "123 Rue Test, Conakry",
        "neighborhood": "Quartier Test",
        "city": "Conakry",
        "postal_code": "001",
        "contact_preference": "message",
        "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    try:
        response = requests.post(HELP_REQUESTS_URL, json=complete_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Création réussie avec données complètes")
        else:
            print(f"❌ Erreur création complète: {response.status_code}")
            print(f"Détails: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur requête complète: {e}")
    
    # 4. Vérification des demandes créées
    print("\n4️⃣ Vérification des demandes existantes...")
    
    try:
        response = requests.get(HELP_REQUESTS_URL, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            results = data.get('results', [])
            print(f"Nombre de demandes: {count}")
            
            if results:
                print("Dernières demandes:")
                for i, request in enumerate(results[:3]):
                    print(f"  {i+1}. {request.get('title')} - {request.get('status')}")
            else:
                print("Aucune demande trouvée")
        else:
            print(f"❌ Erreur récupération: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")

if __name__ == "__main__":
    test_help_request_creation() 
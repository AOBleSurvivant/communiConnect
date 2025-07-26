#!/usr/bin/env python3
"""
Test script pour vérifier l'API des demandes d'aide
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
HELP_REQUESTS_URL = f"{BASE_URL}/help-requests/api/requests/"

# Données de test
test_data = {
    "request_type": "request",
    "need_type": "material",
    "for_who": "myself",
    "title": "Test - Demande d'aide",
    "description": "Ceci est un test de création de demande d'aide",
    "duration_type": "this_week",
    "estimated_hours": "2",
    "proximity_zone": "local",
    "is_urgent": False,
    "contact_preference": "message",
    "latitude": 9.5370,
    "longitude": -13.6785,
    "address": "Conakry, Guinée",
    "neighborhood": "Centre-ville",
    "city": "Conakry",
    "postal_code": "001",
    "expires_at": "2025-08-08T17:08:50.892Z"
}

def test_api_endpoint():
    """Test de l'endpoint API"""
    print("🧪 Test de l'API des demandes d'aide")
    print(f"🔗 URL: {HELP_REQUESTS_URL}")
    print(f"📋 Données: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test GET (récupération des demandes)
        print("\n📥 Test GET (récupération des demandes)...")
        response = requests.get(HELP_REQUESTS_URL)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET réussi - {len(data.get('results', []))} demandes trouvées")
        else:
            print(f"❌ GET échoué - {response.text}")
        
        # Test POST (création d'une demande)
        print("\n📤 Test POST (création d'une demande)...")
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(HELP_REQUESTS_URL, json=test_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ POST réussi - Demande créée avec ID: {data.get('id')}")
        else:
            print(f"❌ POST échoué")
            print(f"Response: {response.text}")
            
            # Essayer de parser la réponse JSON pour plus de détails
            try:
                error_data = response.json()
                print(f"Erreur détaillée: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Réponse brute: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion - Le serveur Django n'est pas démarré")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def test_form_data():
    """Test avec FormData (simulation d'upload de fichier)"""
    print("\n📷 Test avec FormData...")
    
    try:
        # Créer un fichier de test
        test_file_content = b"Test file content"
        
        files = {
            'photo': ('test.jpg', test_file_content, 'image/jpeg')
        }
        
        # Convertir les données en FormData
        form_data = {}
        for key, value in test_data.items():
            if isinstance(value, bool):
                form_data[key] = str(value)
            else:
                form_data[key] = value
        
        response = requests.post(HELP_REQUESTS_URL, data=form_data, files=files)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ POST avec FormData réussi")
        else:
            print(f"❌ POST avec FormData échoué: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur FormData: {e}")

if __name__ == "__main__":
    test_api_endpoint()
    test_form_data()
    print("\n✅ Test terminé") 
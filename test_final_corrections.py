#!/usr/bin/env python3
"""
Test final après corrections - Vérification complète
"""

import requests
import json

def test_final_corrections():
    """Test final après toutes les corrections"""
    
    print("🎯 TEST FINAL - VÉRIFICATION DES CORRECTIONS")
    print("=" * 60)
    
    # Configuration
    BASE_URL = "http://localhost:8000"
    API_BASE = f"{BASE_URL}/api"
    
    # Test 1: Connexion utilisateur
    print("\n🔐 1. Test de connexion...")
    login_data = {
        "email": "testhelp@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{API_BASE}/users/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Erreur connexion: {response.status_code}")
        return False
    
    token = response.json().get('tokens', {}).get('access')
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Connexion réussie")
    
    # Test 2: GET sans paramètres (doit fonctionner)
    print("\n📋 2. Test GET sans paramètres...")
    response = requests.get(f"{API_BASE}/help-requests/api/requests/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        print(f"✅ GET sans paramètres: {count} demandes trouvées")
    else:
        print(f"❌ Erreur GET: {response.status_code} - {response.text}")
        return False
    
    # Test 3: GET avec status=open (doit fonctionner)
    print("\n🔍 3. Test GET avec status=open...")
    response = requests.get(f"{API_BASE}/help-requests/api/requests/?status=open", headers=headers)
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        print(f"✅ GET avec status=open: {count} demandes trouvées")
    else:
        print(f"❌ Erreur GET status=open: {response.status_code} - {response.text}")
        return False
    
    # Test 4: GET avec géolocalisation (doit fonctionner)
    print("\n📍 4. Test GET avec géolocalisation...")
    response = requests.get(
        f"{API_BASE}/help-requests/api/requests/?status=open&latitude=9.617408&longitude=-13.601997&radius=10", 
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        print(f"✅ GET avec géolocalisation: {count} demandes trouvées")
    else:
        print(f"❌ Erreur GET géolocalisation: {response.status_code} - {response.text}")
        return False
    
    # Test 5: Création de demande d'aide (doit fonctionner)
    print("\n📝 5. Test création de demande d'aide...")
    help_request_data = {
        "title": "Test final - Demande d'aide",
        "description": "Ceci est un test final après corrections",
        "request_type": "request",
        "need_type": "material",
        "for_who": "myself",
        "duration_type": "this_week",
        "is_urgent": False,
        "latitude": 9.617408,
        "longitude": -13.601997,
        "city": "Conakry",
        "contact_preference": "message"
    }
    
    response = requests.post(f"{API_BASE}/help-requests/api/requests/", json=help_request_data, headers=headers)
    if response.status_code == 201:
        created_request = response.json()
        request_id = created_request.get('id')
        print(f"✅ Demande d'aide créée (ID: {request_id})")
    else:
        print(f"❌ Erreur création: {response.status_code} - {response.text}")
        return False
    
    # Test 6: Map data (doit fonctionner)
    print("\n🗺️ 6. Test map_data...")
    response = requests.get(f"{API_BASE}/help-requests/api/requests/map_data/?status=open", headers=headers)
    if response.status_code == 200:
        map_data = response.json()
        print(f"✅ Map data: {len(map_data)} points")
    else:
        print(f"❌ Erreur map_data: {response.status_code} - {response.text}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 TOUS LES TESTS SONT PASSÉS !")
    print("✅ Les corrections ont résolu les problèmes")
    print("✅ L'API fonctionne correctement")
    print("✅ Le frontend peut maintenant communiquer avec le backend")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_final_corrections() 
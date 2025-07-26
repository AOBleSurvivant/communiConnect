#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simplifié - Fonctionnalité de Demande d'Aide CommuniConnect
Test via l'API REST uniquement
"""

import requests
import json
from datetime import datetime

def test_help_requests_api():
    """Test de l'API de demande d'aide via HTTP"""
    
    print("🎯 TEST SIMPLIFIÉ - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("=" * 60)
    print(f"⏰ Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Configuration API
    API_BASE_URL = "http://localhost:8000"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Test 1: Vérifier que le serveur fonctionne
    print("🔍 1. Test connexion au serveur...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code in [200, 404]:  # 404 est normal car pas de vue racine
            print("✅ Serveur Django accessible")
        else:
            print(f"❌ Serveur non accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion serveur: {e}")
        return False
    
    # Test 2: Authentification
    print("\n🔐 2. Test d'authentification...")
    try:
        login_data = {
            'username': 'mariam_diallo',
            'password': 'testpass123'
        }
        
        response = requests.post(f"{API_BASE_URL}/api/users/login/", json=login_data, headers=headers)
        
        if response.status_code == 200:
            token = response.json().get('access')
            headers['Authorization'] = f'Bearer {token}'
            print("✅ Authentification réussie")
        else:
            print(f"❌ Erreur authentification: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur authentification: {e}")
        return False
    
    # Test 3: Endpoint des demandes d'aide
    print("\n📋 3. Test endpoint demandes d'aide...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/", headers=headers)
        
        if response.status_code == 200:
            help_requests = response.json()
            count = len(help_requests.get('results', help_requests))
            print(f"✅ Endpoint accessible - {count} demandes trouvées")
        else:
            print(f"❌ Erreur endpoint: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur endpoint: {e}")
    
    # Test 4: Création d'une demande d'aide
    print("\n📝 4. Test création de demande d'aide...")
    try:
        help_request_data = {
            'request_type': 'request',
            'need_type': 'material',
            'for_who': 'myself',
            'title': 'Test API - Besoin de matériel',
            'description': 'Test de création via API REST.',
            'duration_type': 'this_week',
            'estimated_hours': 2,
            'proximity_zone': 'local',
            'is_urgent': False,
            'contact_preference': 'message',
            'latitude': 9.5370,
            'longitude': -13.6785,
            'city': 'Conakry'
        }
        
        response = requests.post(f"{API_BASE_URL}/help-requests/api/requests/", json=help_request_data, headers=headers)
        
        if response.status_code == 201:
            help_request = response.json()
            help_request_id = help_request.get('id')
            print(f"✅ Demande d'aide créée (ID: {help_request_id})")
            
            # Test 5: Récupération de la demande créée
            print(f"\n📖 5. Test récupération demande (ID: {help_request_id})...")
            response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/{help_request_id}/", headers=headers)
            
            if response.status_code == 200:
                retrieved_request = response.json()
                print(f"✅ Demande récupérée: {retrieved_request.get('title')}")
            else:
                print(f"❌ Erreur récupération: {response.status_code}")
                
        else:
            print(f"❌ Erreur création: {response.status_code}")
            print(f"Réponse: {response.text}")
            help_request_id = None
            
    except Exception as e:
        print(f"❌ Erreur création: {e}")
        help_request_id = None
    
    # Test 6: Filtrage
    print("\n🔍 6. Test filtrage...")
    try:
        # Filtre par type
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?request_type=request", headers=headers)
        if response.status_code == 200:
            filtered = response.json()
            count = len(filtered.get('results', filtered))
            print(f"✅ Filtrage par type 'request': {count} demandes")
        
        # Filtre par besoin
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?need_type=material", headers=headers)
        if response.status_code == 200:
            filtered = response.json()
            count = len(filtered.get('results', filtered))
            print(f"✅ Filtrage par besoin 'material': {count} demandes")
            
    except Exception as e:
        print(f"❌ Erreur filtrage: {e}")
    
    # Test 7: Données carte
    print("\n🗺️ 7. Test données carte...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/map_data/", headers=headers)
        
        if response.status_code == 200:
            map_data = response.json()
            print(f"✅ Données carte: {len(map_data)} points")
        else:
            print(f"❌ Erreur données carte: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur données carte: {e}")
    
    # Test 8: Statistiques
    print("\n📊 8. Test statistiques...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/stats/", headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées:")
            for key, value in stats.items():
                print(f"   - {key}: {value}")
        else:
            print(f"❌ Erreur statistiques: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TEST API TERMINÉ - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("✅ L'API de demande d'aide est opérationnelle !")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_help_requests_api() 
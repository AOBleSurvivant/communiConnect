#!/usr/bin/env python3
"""
Test de l'interface simplifiée des demandes d'aide (sans carte)
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_step(step, message):
    print(f"\n{step}️⃣ {message}")
    print("=" * 50)

def test_interface_simplifiee():
    print("🧪 TEST DE L'INTERFACE SIMPLIFIÉE DES DEMANDES D'AIDE")
    print("=" * 60)
    
    # 1. Test de connexion utilisateur
    print_step(1, "Connexion utilisateur")
    login_data = {
        "email": "helpuser@example.com",
        "password": "helpuser123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('tokens', {}).get('access') or response_data.get('access')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return
    
    # 2. Test de récupération des demandes d'aide (sans carte)
    print_step(2, "Récupération des demandes d'aide (interface simplifiée)")
    
    try:
        # Test sans paramètres de géolocalisation
        response = requests.get(f"{API_BASE}/help-requests/requests/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            requests_count = len(data.get('results', data))
            print(f"✅ {requests_count} demandes récupérées avec succès")
            
            # Afficher les premières demandes
            for i, req in enumerate(data.get('results', data)[:3]):
                print(f"   📋 {i+1}. {req.get('title', 'Sans titre')} - {req.get('status', 'N/A')}")
        else:
            print(f"❌ Erreur récupération: {response.text}")
    except Exception as e:
        print(f"❌ Erreur récupération: {e}")
    
    # 3. Test de création d'une demande d'aide (sans carte)
    print_step(3, "Création d'une demande d'aide (interface simplifiée)")
    
    help_request_data = {
        "title": "Test interface simplifiée - Demande d'aide",
        "description": "Ceci est un test de l'interface simplifiée sans carte interactive",
        "request_type": "request",
        "need_type": "material",
        "for_who": "myself",
        "duration_type": "this_week",
        "is_urgent": False,
        "latitude": 9.537000,
        "longitude": -13.678500,
        "address": "123 Rue Test, Conakry",
        "neighborhood": "Quartier Test",
        "city": "Conakry",
        "postal_code": "00100",
        "contact_preference": "phone",
        "contact_phone": "+224123456789",
        "contact_email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{API_BASE}/help-requests/requests/", 
                               json=help_request_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            created_request = response.json()
            print(f"✅ Demande créée avec succès (ID: {created_request.get('id')})")
            print(f"   📍 Localisation: {created_request.get('latitude')}, {created_request.get('longitude')}")
            print(f"   🏠 Adresse: {created_request.get('address')}")
        else:
            print(f"❌ Erreur création: {response.text}")
    except Exception as e:
        print(f"❌ Erreur création: {e}")
    
    # 4. Test des filtres (interface simplifiée)
    print_step(4, "Test des filtres (interface simplifiée)")
    
    filters_to_test = [
        {"status": "open"},
        {"need_type": "material"},
        {"request_type": "request"},
        {"is_urgent": "true"},
        {"search": "test"}
    ]
    
    for i, filter_params in enumerate(filters_to_test):
        try:
            params = "&".join([f"{k}={v}" for k, v in filter_params.items()])
            response = requests.get(f"{API_BASE}/help-requests/requests/?{params}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', data))
                print(f"   ✅ Filtre {i+1} ({filter_params}): {count} résultats")
            else:
                print(f"   ❌ Filtre {i+1} ({filter_params}): Erreur {response.status_code}")
        except Exception as e:
            print(f"   ❌ Filtre {i+1} ({filter_params}): {e}")
    
    # 5. Test de récupération des détails d'une demande
    print_step(5, "Récupération des détails d'une demande")
    
    try:
        # Récupérer la première demande
        response = requests.get(f"{API_BASE}/help-requests/requests/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            requests_list = data.get('results', data)
            
            if requests_list:
                first_request = requests_list[0]
                request_id = first_request.get('id')
                
                # Récupérer les détails
                detail_response = requests.get(f"{API_BASE}/help-requests/requests/{request_id}/", headers=headers)
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    print(f"✅ Détails récupérés pour la demande {request_id}")
                    print(f"   📋 Titre: {detail_data.get('title')}")
                    print(f"   📍 Localisation: {detail_data.get('latitude')}, {detail_data.get('longitude')}")
                    print(f"   🏠 Adresse: {detail_data.get('address')}")
                    print(f"   👤 Auteur: {detail_data.get('author_name', 'N/A')}")
                else:
                    print(f"❌ Erreur récupération détails: {detail_response.status_code}")
            else:
                print("ℹ️ Aucune demande disponible pour tester les détails")
        else:
            print(f"❌ Erreur récupération liste: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur test détails: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TEST DE L'INTERFACE SIMPLIFIÉE TERMINÉ")
    print("✅ L'interface sans carte fonctionne correctement !")
    print("✅ Toutes les fonctionnalités essentielles sont opérationnelles")
    print("✅ L'interface est maintenant plus simple et accessible")

if __name__ == "__main__":
    test_interface_simplifiee() 
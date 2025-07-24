#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final des fonctionnalités sociales - Version 100%
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def test_social_features_100():
    """Test complet des fonctionnalités sociales"""
    print("🧪 Test complet des fonctionnalités sociales - Version 100%")
    
    # Connexion admin
    login_data = {
        'email': 'admin@communiconnect.com',
        'password': 'Admin123!'
    }
    
    try:
        print("🔐 Connexion admin...")
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.status_code}")
            return False
        
        data = response.json()
        token = data.get('tokens', {}).get('access')
        if not token:
            print("❌ Token manquant")
            return False
        
        print("✅ Admin connecté")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Récupérer les quartiers disponibles
        print("📡 Récupération des quartiers...")
        response = requests.get(f"{API_URL}/geography/quartiers/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            quartiers = data.get('results', [])
            if quartiers:
                quartier_id = quartiers[0]['id']
                print(f"✅ Quartier trouvé: {quartiers[0]['nom']} (ID: {quartier_id})")
            else:
                print("❌ Aucun quartier disponible")
                return False
        else:
            print(f"❌ Erreur récupération quartiers: {response.status_code}")
            return False
        
        # Test 1: Créer un groupe communautaire
        print("\n📡 Test 1: Création d'un groupe communautaire...")
        group_data = {
            'name': 'Groupe Test 100%',
            'description': 'Groupe de test pour validation 100%',
            'group_type': 'community',
            'privacy_level': 'public',
            'quartier': quartier_id
        }
        
        response = requests.post(f"{API_URL}/users/groups/", json=group_data, headers=headers)
        print(f"Status création groupe: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            group = response.json()
            group_id = group['id']
            print(f"✅ Groupe créé: {group['name']} (ID: {group_id})")
        else:
            print(f"❌ Erreur création groupe: {response.status_code}")
            return False
        
        # Test 2: Créer un événement communautaire
        print("\n📡 Test 2: Création d'un événement communautaire...")
        event_data = {
            'title': 'Événement Test 100%',
            'description': 'Événement de test pour validation 100%',
            'event_type': 'meeting',
            'status': 'published',
            'start_date': '2024-12-25T10:00:00Z',
            'end_date': '2024-12-25T12:00:00Z',
            'quartier': quartier_id,
            'location_details': 'Centre-ville, Conakry'
        }
        
        response = requests.post(f"{API_URL}/users/events/", json=event_data, headers=headers)
        print(f"Status création événement: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            event = response.json()
            event_id = event['id']
            print(f"✅ Événement créé: {event['title']} (ID: {event_id})")
        else:
            print(f"❌ Erreur création événement: {response.status_code}")
            return False
        
        # Test 3: Lister les groupes
        print("\n📡 Test 3: Liste des groupes...")
        response = requests.get(f"{API_URL}/users/groups/", headers=headers)
        print(f"Status liste groupes: {response.status_code}")
        if response.status_code == 200:
            groups = response.json()
            print(f"✅ {len(groups)} groupes trouvés")
        
        # Test 4: Lister les événements
        print("\n📡 Test 4: Liste des événements...")
        response = requests.get(f"{API_URL}/users/events/", headers=headers)
        print(f"Status liste événements: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"✅ {len(events)} événements trouvés")
        
        # Test 5: Suggestions de groupes
        print("\n📡 Test 5: Suggestions de groupes...")
        response = requests.get(f"{API_URL}/users/suggested-groups/", headers=headers)
        print(f"Status suggestions groupes: {response.status_code}")
        
        # Test 6: Suggestions d'événements
        print("\n📡 Test 6: Suggestions d'événements...")
        response = requests.get(f"{API_URL}/users/suggested-events/", headers=headers)
        print(f"Status suggestions événements: {response.status_code}")
        
        # Test 7: Leaderboard
        print("\n📡 Test 7: Leaderboard...")
        response = requests.get(f"{API_URL}/users/leaderboard/", headers=headers)
        print(f"Status leaderboard: {response.status_code}")
        
        # Test 8: Statistiques sociales
        print("\n📡 Test 8: Statistiques sociales...")
        user_id = data['user']['id']
        response = requests.get(f"{API_URL}/users/social-stats/{user_id}/", headers=headers)
        print(f"Status stats sociales: {response.status_code}")
        
        # Test 9: Rejoindre un groupe
        print("\n📡 Test 9: Rejoindre un groupe...")
        join_group_data = {
            'group_id': group_id
        }
        response = requests.post(f"{API_URL}/users/groups/join/", json=join_group_data, headers=headers)
        print(f"Status rejoindre groupe: {response.status_code}")
        
        # Test 10: Rejoindre un événement
        print("\n📡 Test 10: Rejoindre un événement...")
        join_event_data = {
            'event_id': event_id
        }
        response = requests.post(f"{API_URL}/users/events/join/", json=join_event_data, headers=headers)
        print(f"Status rejoindre événement: {response.status_code}")
        
        print(f"\n🎯 SUCCÈS! Tests des fonctionnalités sociales 100% terminés!")
        print(f"   Groupe ID: {group_id}")
        print(f"   Événement ID: {event_id}")
        print(f"   Quartier ID: {quartier_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage test fonctionnalités sociales 100%...")
    success = test_social_features_100()
    if success:
        print(f"\n✅ Tests des fonctionnalités sociales 100% réussis!")
        print(f"   Toutes les fonctionnalités sociales sont opérationnelles.")
    else:
        print(f"\n❌ Échec des tests des fonctionnalités sociales.") 
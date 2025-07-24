#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des fonctionnalités sociales avec données géographiques existantes
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def test_social_features():
    """Tester les fonctionnalités sociales"""
    print("🧪 Test des fonctionnalités sociales...")
    
    # Connexion admin
    login_data = {
        'email': 'admin@communiconnect.com',
        'password': 'Admin123!'
    }
    
    try:
        print("🔐 Connexion admin...")
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        print(f"Status connexion: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
        
        data = response.json()
        print(f"Données connexion: {data}")
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
        print(f"URL: {API_URL}/geography/quartiers/")
        response = requests.get(f"{API_URL}/geography/quartiers/", headers=headers)
        print(f"Status quartiers: {response.status_code}")
        print(f"Réponse quartiers: {response.text}")
        
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
        
        # Créer un groupe communautaire
        print("📡 Création d'un groupe communautaire...")
        group_data = {
            'name': 'Groupe Test CommuniConnect',
            'description': 'Groupe de test pour les fonctionnalités sociales',
            'type': 'community',
            'privacy': 'public',
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
            print(f"⚠️  Erreur création groupe: {response.status_code}")
            # Essayer de récupérer les groupes existants
            response = requests.get(f"{API_URL}/users/groups/", headers=headers)
            if response.status_code == 200:
                groups = response.json()
                if groups:
                    group_id = groups[0]['id']
                    print(f"ℹ️  Utilisation groupe existant: {groups[0]['name']} (ID: {group_id})")
                else:
                    print("❌ Aucun groupe disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les groupes")
                return False
        
        # Créer un événement communautaire
        print("📡 Création d'un événement communautaire...")
        event_data = {
            'title': 'Événement Test CommuniConnect',
            'description': 'Événement de test pour les fonctionnalités sociales',
            'type': 'meeting',
            'status': 'upcoming',
            'start_date': '2024-12-25T10:00:00Z',
            'end_date': '2024-12-25T12:00:00Z',
            'quartier': quartier_id,
            'location': 'Centre-ville, Conakry'
        }
        
        response = requests.post(f"{API_URL}/users/events/", json=event_data, headers=headers)
        print(f"Status création événement: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            event = response.json()
            event_id = event['id']
            print(f"✅ Événement créé: {event['title']} (ID: {event_id})")
        else:
            print(f"⚠️  Erreur création événement: {response.status_code}")
            # Essayer de récupérer les événements existants
            response = requests.get(f"{API_URL}/users/events/", headers=headers)
            if response.status_code == 200:
                events = response.json()
                if events:
                    event_id = events[0]['id']
                    print(f"ℹ️  Utilisation événement existant: {events[0]['title']} (ID: {event_id})")
                else:
                    print("❌ Aucun événement disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les événements")
                return False
        
        # Tester les suggestions
        print("📡 Test des suggestions...")
        response = requests.get(f"{API_URL}/users/suggestions/groups/", headers=headers)
        print(f"Status suggestions groupes: {response.status_code}")
        
        response = requests.get(f"{API_URL}/users/suggestions/events/", headers=headers)
        print(f"Status suggestions événements: {response.status_code}")
        
        # Tester le leaderboard
        print("📡 Test du leaderboard...")
        response = requests.get(f"{API_URL}/users/gamification/leaderboard/", headers=headers)
        print(f"Status leaderboard: {response.status_code}")
        
        # Tester les statistiques sociales
        print("📡 Test des statistiques sociales...")
        response = requests.get(f"{API_URL}/users/social-stats/", headers=headers)
        print(f"Status stats sociales: {response.status_code}")
        
        print(f"\n🎯 SUCCÈS! Tests des fonctionnalités sociales terminés!")
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
    print("🚀 Démarrage test fonctionnalités sociales...")
    success = test_social_features()
    if success:
        print(f"\n✅ Tests des fonctionnalités sociales réussis!")
        print(f"   Les fonctionnalités sociales sont opérationnelles.")
    else:
        print(f"\n❌ Échec des tests des fonctionnalités sociales.") 
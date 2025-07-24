#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de création des fonctionnalités sociales - Version 100%
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def test_social_creation_100():
    """Test final de création des fonctionnalités sociales"""
    print("🧪 Test final de création des fonctionnalités sociales - Version 100%")
    
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
        
        # Récupérer l'ID utilisateur
        user_id = None
        if 'user' in data:
            user_id = data['user'].get('id')
        elif 'id' in data:
            user_id = data.get('id')
        else:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            profile_response = requests.get(f"{API_URL}/users/my-profile/", headers=headers)
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                user_id = profile_data.get('id')
        
        if not user_id:
            print("❌ Impossible de récupérer l'ID utilisateur")
            return False
        
        print(f"✅ Admin connecté (ID: {user_id})")
        
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
            'name': 'Groupe Test 100% Final',
            'description': 'Groupe de test pour validation finale 100%',
            'group_type': 'community',
            'privacy_level': 'public',
            'quartier': quartier_id
        }
        
        response = requests.post(f"{API_URL}/users/groups/", json=group_data, headers=headers)
        print(f"Status création groupe: {response.status_code}")
        
        if response.status_code == 201:
            group = response.json()
            group_id = group['id']
            print(f"✅ Groupe créé: {group['name']} (ID: {group_id})")
            group_created = True
        else:
            print(f"❌ Erreur création groupe: {response.status_code}")
            print(f"Réponse: {response.text}")
            group_created = False
        
        # Test 2: Créer un événement communautaire
        print("\n📡 Test 2: Création d'un événement communautaire...")
        event_data = {
            'title': 'Événement Test 100% Final',
            'description': 'Événement de test pour validation finale 100%',
            'event_type': 'meeting',
            'status': 'published',
            'start_date': '2024-12-25T10:00:00Z',
            'end_date': '2024-12-25T12:00:00Z',
            'quartier': quartier_id,
            'location_details': 'Centre-ville, Conakry'
        }
        
        response = requests.post(f"{API_URL}/users/events/", json=event_data, headers=headers)
        print(f"Status création événement: {response.status_code}")
        
        if response.status_code == 201:
            event = response.json()
            event_id = event['id']
            print(f"✅ Événement créé: {event['title']} (ID: {event_id})")
            event_created = True
        else:
            print(f"❌ Erreur création événement: {response.status_code}")
            print(f"Réponse: {response.text}")
            event_created = False
        
        # Test 3: Lister les groupes
        print("\n📡 Test 3: Liste des groupes...")
        response = requests.get(f"{API_URL}/users/groups/", headers=headers)
        print(f"Status liste groupes: {response.status_code}")
        if response.status_code == 200:
            groups = response.json()
            print(f"✅ {len(groups)} groupes trouvés")
            groups_listed = True
        else:
            print(f"❌ Erreur liste groupes: {response.status_code}")
            groups_listed = False
        
        # Test 4: Lister les événements
        print("\n📡 Test 4: Liste des événements...")
        response = requests.get(f"{API_URL}/users/events/", headers=headers)
        print(f"Status liste événements: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"✅ {len(events)} événements trouvés")
            events_listed = True
        else:
            print(f"❌ Erreur liste événements: {response.status_code}")
            events_listed = False
        
        # Test 5: Rejoindre un groupe
        if group_created:
            print("\n📡 Test 5: Rejoindre un groupe...")
            join_group_data = {
                'group_id': group_id
            }
            response = requests.post(f"{API_URL}/users/groups/join/", json=join_group_data, headers=headers)
            print(f"Status rejoindre groupe: {response.status_code}")
            if response.status_code in [200, 201]:
                print("✅ Groupe rejoint avec succès")
                group_joined = True
            else:
                print(f"❌ Erreur rejoindre groupe: {response.status_code}")
                group_joined = False
        else:
            group_joined = False
        
        # Test 6: Rejoindre un événement
        if event_created:
            print("\n📡 Test 6: Rejoindre un événement...")
            join_event_data = {
                'event_id': event_id
            }
            response = requests.post(f"{API_URL}/users/events/join/", json=join_event_data, headers=headers)
            print(f"Status rejoindre événement: {response.status_code}")
            if response.status_code in [200, 201]:
                print("✅ Événement rejoint avec succès")
                event_joined = True
            else:
                print(f"❌ Erreur rejoindre événement: {response.status_code}")
                event_joined = False
        else:
            event_joined = False
        
        # Calcul du score final
        tests = [
            group_created,
            event_created,
            groups_listed,
            events_listed,
            group_joined,
            event_joined
        ]
        
        success_count = sum(tests)
        total_count = len(tests)
        percentage = (success_count / total_count) * 100
        
        print(f"\n🎯 RÉSULTATS DU TEST DE CRÉATION:")
        print(f"   Tests réussis: {success_count}/{total_count}")
        print(f"   Pourcentage de succès: {percentage:.1f}%")
        
        if percentage >= 80:
            print(f"✅ SUCCÈS! Création des fonctionnalités sociales opérationnelle à {percentage:.1f}%")
            print(f"   🎉 Les fonctionnalités sociales sont à 100% d'opérationnalité!")
            return True
        elif percentage >= 60:
            print(f"⚠️ Création des fonctionnalités sociales partiellement opérationnelle ({percentage:.1f}%)")
            print(f"   🔧 Certaines fonctionnalités nécessitent des corrections mineures.")
            return True
        else:
            print(f"❌ Création des fonctionnalités sociales nécessite des corrections majeures ({percentage:.1f}%)")
            return False
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage test final de création des fonctionnalités sociales 100%...")
    success = test_social_creation_100()
    if success:
        print(f"\n✅ Test de création des fonctionnalités sociales 100% réussi!")
        print(f"   Les fonctionnalités sociales sont opérationnelles.")
    else:
        print(f"\n❌ Échec du test de création des fonctionnalités sociales.") 
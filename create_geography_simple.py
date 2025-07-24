#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour créer des données géographiques de base
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def create_simple_geography():
    """Créer des données géographiques simples"""
    print("🗺️  Création de données géographiques simples...")
    
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
            print(f"Réponse: {response.text}")
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
        
        # Créer une région
        print("📡 Création région...")
        region_data = {'nom': 'Conakry', 'code': 'CNK'}
        print(f"Données région: {region_data}")
        response = requests.post(f"{API_URL}/geography/regions/", json=region_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            region = response.json()
            region_id = region['id']
            print(f"✅ Région créée: {region['nom']} (ID: {region_id})")
        else:
            print(f"⚠️  Région existante: {response.status_code}")
            # Récupérer la région existante
            response = requests.get(f"{API_URL}/geography/regions/", headers=headers)
            if response.status_code == 200:
                regions = response.json()
                if regions:
                    region_id = regions[0]['id']
                    print(f"ℹ️  Utilisation région existante: {regions[0]['nom']} (ID: {region_id})")
                else:
                    print("❌ Aucune région disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les régions")
                return False
        
        # Créer une préfecture
        print("📡 Création préfecture...")
        prefecture_data = {'nom': 'Conakry', 'code': 'CNK', 'region': region_id}
        print(f"Données préfecture: {prefecture_data}")
        response = requests.post(f"{API_URL}/geography/prefectures/", json=prefecture_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            prefecture = response.json()
            prefecture_id = prefecture['id']
            print(f"✅ Préfecture créée: {prefecture['nom']} (ID: {prefecture_id})")
        else:
            print(f"⚠️  Préfecture existante: {response.status_code}")
            # Récupérer la préfecture existante
            response = requests.get(f"{API_URL}/geography/prefectures/", headers=headers)
            if response.status_code == 200:
                prefectures = response.json()
                if prefectures:
                    prefecture_id = prefectures[0]['id']
                    print(f"ℹ️  Utilisation préfecture existante: {prefectures[0]['nom']} (ID: {prefecture_id})")
                else:
                    print("❌ Aucune préfecture disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les préfectures")
                return False
        
        # Créer une commune
        print("📡 Création commune...")
        commune_data = {'nom': 'Kaloum', 'code': 'KLM', 'prefecture': prefecture_id}
        print(f"Données commune: {commune_data}")
        response = requests.post(f"{API_URL}/geography/communes/", json=commune_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            commune = response.json()
            commune_id = commune['id']
            print(f"✅ Commune créée: {commune['nom']} (ID: {commune_id})")
        else:
            print(f"⚠️  Commune existante: {response.status_code}")
            # Récupérer la commune existante
            response = requests.get(f"{API_URL}/geography/communes/", headers=headers)
            if response.status_code == 200:
                communes = response.json()
                if communes:
                    commune_id = communes[0]['id']
                    print(f"ℹ️  Utilisation commune existante: {communes[0]['nom']} (ID: {commune_id})")
                else:
                    print("❌ Aucune commune disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les communes")
                return False
        
        # Créer un quartier
        print("📡 Création quartier...")
        quartier_data = {'nom': 'Centre-ville', 'code': 'CTR', 'commune': commune_id}
        print(f"Données quartier: {quartier_data}")
        response = requests.post(f"{API_URL}/geography/quartiers/", json=quartier_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            quartier = response.json()
            quartier_id = quartier['id']
            print(f"✅ Quartier créé: {quartier['nom']} (ID: {quartier_id})")
        else:
            print(f"⚠️  Quartier existant: {response.status_code}")
            # Récupérer le quartier existant
            response = requests.get(f"{API_URL}/geography/quartiers/", headers=headers)
            if response.status_code == 200:
                quartiers = response.json()
                if quartiers:
                    quartier_id = quartiers[0]['id']
                    print(f"ℹ️  Utilisation quartier existant: {quartiers[0]['nom']} (ID: {quartier_id})")
                else:
                    print("❌ Aucun quartier disponible")
                    return False
            else:
                print("❌ Impossible de récupérer les quartiers")
                return False
        
        print(f"\n🎯 SUCCÈS! Quartier disponible: ID {quartier_id}")
        return quartier_id
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage création données géographiques...")
    quartier_id = create_simple_geography()
    if quartier_id:
        print(f"\n✅ Données géographiques créées avec succès!")
        print(f"   Quartier ID: {quartier_id}")
        print(f"   Vous pouvez maintenant tester les fonctionnalités sociales.")
    else:
        print(f"\n❌ Échec de la création des données géographiques.") 
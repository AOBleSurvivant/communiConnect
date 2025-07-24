#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création de données géographiques via l'API REST
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def create_geography_via_api():
    """Créer des données géographiques via l'API"""
    print("🗺️  Création des données géographiques via l'API...")
    
    # Créer une région
    region_data = {
        'name': 'Conakry',
        'code': 'CNK'
    }
    
    try:
        response = requests.post(f"{API_URL}/geography/regions/", json=region_data)
        if response.status_code == 201:
            region = response.json()
            print(f"✅ Région créée: {region['name']} (ID: {region['id']})")
            region_id = region['id']
        else:
            print(f"⚠️  Région existe déjà ou erreur: {response.status_code}")
            # Essayer de récupérer la région existante
            response = requests.get(f"{API_URL}/geography/regions/")
            if response.status_code == 200:
                regions = response.json()
                if regions:
                    region_id = regions[0]['id']
                    print(f"✅ Région trouvée: ID {region_id}")
                else:
                    print("❌ Aucune région disponible")
                    return None
            else:
                print("❌ Impossible de récupérer les régions")
                return None
    except Exception as e:
        print(f"❌ Erreur création région: {e}")
        return None
    
    # Créer une préfecture
    prefecture_data = {
        'name': 'Conakry',
        'code': 'CNK',
        'region': region_id
    }
    
    try:
        response = requests.post(f"{API_URL}/geography/prefectures/", json=prefecture_data)
        if response.status_code == 201:
            prefecture = response.json()
            print(f"✅ Préfecture créée: {prefecture['name']} (ID: {prefecture['id']})")
            prefecture_id = prefecture['id']
        else:
            print(f"⚠️  Préfecture existe déjà ou erreur: {response.status_code}")
            # Essayer de récupérer la préfecture existante
            response = requests.get(f"{API_URL}/geography/prefectures/")
            if response.status_code == 200:
                prefectures = response.json()
                if prefectures:
                    prefecture_id = prefectures[0]['id']
                    print(f"✅ Préfecture trouvée: ID {prefecture_id}")
                else:
                    print("❌ Aucune préfecture disponible")
                    return None
            else:
                print("❌ Impossible de récupérer les préfectures")
                return None
    except Exception as e:
        print(f"❌ Erreur création préfecture: {e}")
        return None
    
    # Créer une commune
    commune_data = {
        'name': 'Kaloum',
        'code': 'KLM',
        'prefecture': prefecture_id
    }
    
    try:
        response = requests.post(f"{API_URL}/geography/communes/", json=commune_data)
        if response.status_code == 201:
            commune = response.json()
            print(f"✅ Commune créée: {commune['name']} (ID: {commune['id']})")
            commune_id = commune['id']
        else:
            print(f"⚠️  Commune existe déjà ou erreur: {response.status_code}")
            # Essayer de récupérer la commune existante
            response = requests.get(f"{API_URL}/geography/communes/")
            if response.status_code == 200:
                communes = response.json()
                if communes:
                    commune_id = communes[0]['id']
                    print(f"✅ Commune trouvée: ID {commune_id}")
                else:
                    print("❌ Aucune commune disponible")
                    return None
            else:
                print("❌ Impossible de récupérer les communes")
                return None
    except Exception as e:
        print(f"❌ Erreur création commune: {e}")
        return None
    
    # Créer un quartier
    quartier_data = {
        'name': 'Centre-ville',
        'code': 'CTR',
        'commune': commune_id,
        'latitude': 9.5370,
        'longitude': -13.6785
    }
    
    try:
        response = requests.post(f"{API_URL}/geography/quartiers/", json=quartier_data)
        if response.status_code == 201:
            quartier = response.json()
            print(f"✅ Quartier créé: {quartier['name']} (ID: {quartier['id']})")
            return quartier['id']
        else:
            print(f"⚠️  Quartier existe déjà ou erreur: {response.status_code}")
            # Essayer de récupérer le quartier existant
            response = requests.get(f"{API_URL}/geography/quartiers/")
            if response.status_code == 200:
                quartiers = response.json()
                if quartiers:
                    quartier_id = quartiers[0]['id']
                    print(f"✅ Quartier trouvé: ID {quartier_id}")
                    return quartier_id
                else:
                    print("❌ Aucun quartier disponible")
                    return None
            else:
                print("❌ Impossible de récupérer les quartiers")
                return None
    except Exception as e:
        print(f"❌ Erreur création quartier: {e}")
        return None

if __name__ == "__main__":
    quartier_id = create_geography_via_api()
    if quartier_id:
        print(f"\n🎯 Quartier ID pour les tests: {quartier_id}")
    else:
        print("\n❌ Impossible de créer les données géographiques") 
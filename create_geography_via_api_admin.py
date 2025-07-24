#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création de données géographiques via l'API avec authentification admin
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def get_admin_token():
    """Obtenir le token admin"""
    print("🔐 Connexion admin...")
    
    login_data = {
        'email': 'admin@communiconnect.com',
        'password': 'Admin123!'
    }
    
    try:
        print(f"📡 Envoi requête POST vers {API_URL}/users/login/")
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        print(f"📊 Réponse reçue: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Données reçues: {data}")
            tokens = data.get('tokens', {})
            token = tokens.get('access')
            if token:
                print("✅ Admin connecté")
                return token
            else:
                print("❌ Token manquant")
                print(f"Tokens disponibles: {tokens}")
                return None
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def create_geography_data(token):
    """Créer les données géographiques"""
    print("🗺️  Création des données géographiques...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Créer une région
    region_data = {
        'nom': 'Conakry',
        'code': 'CNK'
    }
    
    try:
        print(f"📡 Création région: {region_data}")
        response = requests.post(f"{API_URL}/geography/regions/", json=region_data, headers=headers)
        print(f"📊 Réponse création région: {response.status_code}")
        
        if response.status_code == 201:
            region = response.json()
            print(f"✅ Région créée: {region['nom']} (ID: {region['id']})")
            region_id = region['id']
        else:
            print(f"⚠️  Région existante ou erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            # Essayer de récupérer la région existante
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
    except Exception as e:
        print(f"❌ Erreur création région: {e}")
        return False
    
    # Créer une préfecture
    prefecture_data = {
        'nom': 'Conakry',
        'code': 'CNK',
        'region': region_id
    }
    
    try:
        print(f"📡 Création préfecture: {prefecture_data}")
        response = requests.post(f"{API_URL}/geography/prefectures/", json=prefecture_data, headers=headers)
        print(f"📊 Réponse création préfecture: {response.status_code}")
        
        if response.status_code == 201:
            prefecture = response.json()
            print(f"✅ Préfecture créée: {prefecture['nom']} (ID: {prefecture['id']})")
            prefecture_id = prefecture['id']
        else:
            print(f"⚠️  Préfecture existante ou erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
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
    except Exception as e:
        print(f"❌ Erreur création préfecture: {e}")
        return False
    
    # Créer des communes
    communes_data = [
        {'nom': 'Kaloum', 'code': 'KLM'},
        {'nom': 'Dixinn', 'code': 'DXN'},
        {'nom': 'Ratoma', 'code': 'RTM'},
        {'nom': 'Matam', 'code': 'MTM'},
        {'nom': 'Matoto', 'code': 'MTO'},
    ]
    
    commune_ids = {}
    for commune_data in communes_data:
        commune_data['prefecture'] = prefecture_id
        
        try:
            print(f"📡 Création commune: {commune_data}")
            response = requests.post(f"{API_URL}/geography/communes/", json=commune_data, headers=headers)
            print(f"📊 Réponse création commune: {response.status_code}")
            
            if response.status_code == 201:
                commune = response.json()
                print(f"✅ Commune créée: {commune['nom']} (ID: {commune['id']})")
                commune_ids[commune['nom']] = commune['id']
            else:
                print(f"⚠️  Commune existante: {commune_data['nom']}")
                print(f"Réponse: {response.text}")
                # Récupérer l'ID de la commune existante
                response = requests.get(f"{API_URL}/geography/communes/", headers=headers)
                if response.status_code == 200:
                    communes = response.json()
                    for commune in communes:
                        if commune['nom'] == commune_data['nom']:
                            commune_ids[commune['nom']] = commune['id']
                            break
        except Exception as e:
            print(f"❌ Erreur création commune {commune_data['nom']}: {e}")
    
    # Créer des quartiers
    quartiers_data = [
        {'nom': 'Centre-ville', 'code': 'CTR', 'commune': 'Kaloum'},
        {'nom': 'Almamya', 'code': 'ALM', 'commune': 'Kaloum'},
        {'nom': 'Sandervalia', 'code': 'SND', 'commune': 'Kaloum'},
        {'nom': 'Dixinn', 'code': 'DXN', 'commune': 'Dixinn'},
        {'nom': 'Ratoma', 'code': 'RTM', 'commune': 'Ratoma'},
        {'nom': 'Matam', 'code': 'MTM', 'commune': 'Matam'},
        {'nom': 'Matoto', 'code': 'MTO', 'commune': 'Matoto'},
    ]
    
    quartier_ids = []
    for quartier_data in quartiers_data:
        commune_name = quartier_data.pop('commune')
        if commune_name in commune_ids:
            quartier_data['commune'] = commune_ids[commune_name]
            
            try:
                print(f"📡 Création quartier: {quartier_data}")
                response = requests.post(f"{API_URL}/geography/quartiers/", json=quartier_data, headers=headers)
                print(f"📊 Réponse création quartier: {response.status_code}")
                
                if response.status_code == 201:
                    quartier = response.json()
                    print(f"✅ Quartier créé: {quartier['nom']} (ID: {quartier['id']})")
                    quartier_ids.append(quartier['id'])
                else:
                    print(f"⚠️  Quartier existant: {quartier_data['nom']}")
                    print(f"Réponse: {response.text}")
                    # Récupérer l'ID du quartier existant
                    response = requests.get(f"{API_URL}/geography/quartiers/", headers=headers)
                    if response.status_code == 200:
                        quartiers = response.json()
                        for quartier in quartiers:
                            if quartier['nom'] == quartier_data['nom']:
                                quartier_ids.append(quartier['id'])
                                break
            except Exception as e:
                print(f"❌ Erreur création quartier {quartier_data['nom']}: {e}")
        else:
            print(f"❌ Commune {commune_name} non trouvée")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   Quartiers créés/récupérés: {len(quartier_ids)}")
    
    if quartier_ids:
        print(f"\n📍 QUARTIERS DISPONIBLES:")
        for quartier_id in quartier_ids:
            print(f"   - ID: {quartier_id}")
    
    return len(quartier_ids) > 0

if __name__ == "__main__":
    print("🚀 Démarrage du script de création des données géographiques...")
    print("📡 Test de connexion au serveur...")
    try:
        response = requests.get("http://localhost:8000/api/users/register/")
        print(f"✅ Serveur accessible (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Serveur inaccessible: {e}")
        exit(1)
    
    token = get_admin_token()
    if token:
        success = create_geography_data(token)
        if success:
            print(f"\n🎯 Données géographiques créées avec succès!")
            print(f"   Vous pouvez maintenant tester les fonctionnalités sociales.")
        else:
            print(f"\n❌ Échec de la création des données géographiques.")
    else:
        print(f"\n❌ Impossible d'obtenir le token admin.") 
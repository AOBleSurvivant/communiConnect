#!/usr/bin/env python3
"""
Test complet du processus d'inscription et de connexion pour un nouvel utilisateur
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
REGISTER_URL = f"{BASE_URL}/users/register/"
LOGIN_URL = f"{BASE_URL}/users/login/"
PROFILE_URL = f"{BASE_URL}/users/my-profile/"

def test_complete_user_flow():
    """Test complet du processus utilisateur"""
    
    print("👤 TEST COMPLET DU PROCESSUS UTILISATEUR")
    print("=" * 60)
    
    # Générer un email unique
    timestamp = int(time.time())
    test_email = f"testuser{timestamp}@example.com"
    test_username = f"testuser{timestamp}"
    
    print(f"📧 Email de test: {test_email}")
    print(f"👤 Username de test: {test_username}")
    
    # 1. Récupérer les données géographiques
    print("\n1. Récupération des données géographiques...")
    try:
        response = requests.get(f"{BASE_URL}/users/geographic-data/")
        if response.status_code == 200:
            geo_data = response.json()
            quartiers = geo_data.get('regions', [])[0].get('prefectures', [])[0].get('communes', [])[0].get('quartiers', [])
            if quartiers:
                quartier_id = quartiers[0]['id']
                print(f"✅ Quartier trouvé: {quartiers[0]['nom']} (ID: {quartier_id})")
            else:
                print("❌ Aucun quartier trouvé")
                return
        else:
            print(f"❌ Erreur données géographiques: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur récupération données géographiques: {e}")
        return
    
    # 2. Inscription du nouvel utilisateur
    print("\n2. Inscription du nouvel utilisateur...")
    user_data = {
        "username": test_username,
        "email": test_email,
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Nouveau",
        "last_name": "Utilisateur",
        "phone_number": "+224123456789",
        "quartier": quartier_id,
        "bio": "Nouvel utilisateur de test"
    }
    
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"Status inscription: {response.status_code}")
        
        if response.status_code == 201:
            user_info = response.json()
            print("✅ Inscription réussie")
            print(f"ID: {user_info.get('user', {}).get('id')}")
            print(f"Email: {user_info.get('user', {}).get('email')}")
        else:
            print(f"❌ Échec d'inscription: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur d'inscription: {e}")
        return
    
    # 3. Connexion du nouvel utilisateur
    print("\n3. Connexion du nouvel utilisateur...")
    login_data = {
        "email": test_email,
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('tokens', {}).get('access')
            if token:
                print("✅ Connexion réussie")
                print(f"Token: {token[:20]}...")
                
                # Sauvegarder le token
                with open('new_user_token.txt', 'w') as f:
                    f.write(token)
                print("✅ Token sauvegardé dans new_user_token.txt")
                
                # 4. Test de l'API profile avec le nouveau token
                print("\n4. Test de l'API profile avec le nouveau token...")
                headers = {'Authorization': f'Bearer {token}'}
                
                response = requests.get(PROFILE_URL, headers=headers)
                print(f"Status profile: {response.status_code}")
                
                if response.status_code == 200:
                    profile = response.json()
                    print("✅ Profil récupéré avec succès")
                    print(f"Nom: {profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}")
                    print(f"Email: {profile.get('email', 'N/A')}")
                    print(f"ID: {profile.get('id', 'N/A')}")
                else:
                    print(f"❌ Échec de récupération profile: {response.text}")
                
                # 5. Test de modification du profil
                print("\n5. Test de modification du profil...")
                update_data = {
                    "first_name": "Modifié",
                    "last_name": "Utilisateur",
                    "bio": "Profil modifié avec succès"
                }
                
                response = requests.patch(PROFILE_URL, json=update_data, headers=headers)
                print(f"Status modification: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Profil modifié avec succès")
                    print(f"Message: {result.get('message', 'N/A')}")
                else:
                    print(f"❌ Échec de modification: {response.text}")
                
            else:
                print("❌ Token non trouvé dans la réponse")
        else:
            print(f"❌ Échec de connexion: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   - Email utilisé: {test_email}")
    print(f"   - Username utilisé: {test_username}")
    print(f"   - Token sauvegardé: new_user_token.txt")
    print(f"   - Test complet: {'✅ Réussi' if response.status_code == 200 else '❌ Échoué'}")

if __name__ == "__main__":
    test_complete_user_flow() 
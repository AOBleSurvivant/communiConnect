#!/usr/bin/env python3
"""
Création d'un utilisateur de test pour les tests
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
REGISTER_URL = f"{BASE_URL}/users/register/"
LOGIN_URL = f"{BASE_URL}/users/login/"

def create_test_user():
    """Créer un utilisateur de test"""
    
    print("👤 CRÉATION D'UN UTILISATEUR DE TEST")
    print("=" * 50)
    
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
    
    # 2. Créer l'utilisateur de test
    print("\n2. Création de l'utilisateur de test...")
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "Utilisateur",
        "phone_number": "+224123456789",
        "quartier": quartier_id,
        "bio": "Utilisateur de test pour les développements"
    }
    
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"Status inscription: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Utilisateur créé avec succès")
            user_info = response.json()
            print(f"ID: {user_info.get('user', {}).get('id')}")
            print(f"Email: {user_info.get('user', {}).get('email')}")
        else:
            print(f"❌ Échec de création: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return
    
    # 3. Tester la connexion
    print("\n3. Test de connexion...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Réponse complète: {data}")
            token = data.get('access')
            if token:
                print("✅ Connexion réussie")
                print(f"Token: {token[:20]}...")
                
                # Sauvegarder le token pour les tests
                with open('test_token.txt', 'w') as f:
                    f.write(token)
                print("✅ Token sauvegardé dans test_token.txt")
            else:
                print("❌ Token non trouvé dans la réponse")
                print(f"Réponse: {data}")
        else:
            print(f"❌ Échec de connexion: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"Réponse: {response.text if 'response' in locals() else 'Pas de réponse'}")

if __name__ == "__main__":
    create_test_user() 
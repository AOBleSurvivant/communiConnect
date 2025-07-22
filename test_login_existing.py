#!/usr/bin/env python3
"""
Test de connexion avec l'utilisateur existant
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
PROFILE_URL = f"{BASE_URL}/users/my-profile/"

def test_login_existing():
    """Test de connexion avec l'utilisateur existant"""
    
    print("🔐 TEST DE CONNEXION UTILISATEUR EXISTANT")
    print("=" * 50)
    
    # Test de connexion
    print("\n1. Test de connexion...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status connexion: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('tokens', {}).get('access')
            if token:
                print("✅ Connexion réussie")
                print(f"Token: {token[:20]}...")
                
                # Sauvegarder le token
                with open('test_token.txt', 'w') as f:
                    f.write(token)
                print("✅ Token sauvegardé")
                
                # Tester l'API profile
                print("\n2. Test de l'API profile...")
                headers = {'Authorization': f'Bearer {token}'}
                
                response = requests.get(PROFILE_URL, headers=headers)
                print(f"Status profile: {response.status_code}")
                
                if response.status_code == 200:
                    profile = response.json()
                    print("✅ Profil récupéré avec succès")
                    print(f"Nom: {profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}")
                    print(f"Email: {profile.get('email', 'N/A')}")
                else:
                    print(f"❌ Échec de récupération profile: {response.text}")
            else:
                print("❌ Token non trouvé dans la réponse")
                print(f"Structure de la réponse: {list(data.keys())}")
        else:
            print(f"❌ Échec de connexion")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_login_existing() 
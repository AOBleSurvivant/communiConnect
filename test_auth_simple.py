#!/usr/bin/env python3
"""
Test simple d'authentification et d'API profile
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
PROFILE_URL = f"{BASE_URL}/users/my-profile/"

def test_auth_and_profile():
    """Test d'authentification et d'API profile"""
    
    print("🔐 TEST D'AUTHENTIFICATION ET PROFILE")
    print("=" * 50)
    
    # 1. Test de connexion
    print("\n1. Test de connexion...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Connexion réussie")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Échec de connexion: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Test de récupération du profil
    print("\n2. Test de récupération du profil...")
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        print(f"Status profil: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profil récupéré avec succès")
            print(f"Nom: {profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}")
            print(f"Email: {profile.get('email', 'N/A')}")
        else:
            print(f"❌ Échec de récupération: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de récupération: {e}")
    
    # 3. Test de modification du profil
    print("\n3. Test de modification du profil...")
    update_data = {
        "first_name": "Test",
        "last_name": "Utilisateur",
        "bio": "Test de modification de profil"
    }
    
    try:
        response = requests.patch(PROFILE_URL, json=update_data, headers=headers)
        print(f"Status modification: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profil modifié avec succès")
            print(f"Message: {result.get('message', 'N/A')}")
        else:
            print(f"❌ Échec de modification: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de modification: {e}")

if __name__ == "__main__":
    test_auth_and_profile() 
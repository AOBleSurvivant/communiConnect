#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test pour les demandes d'aide
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{API_BASE_URL}/api/users/register/"
LOGIN_URL = f"{API_BASE_URL}/api/users/login/"

def create_test_user():
    """Créer un utilisateur de test pour les demandes d'aide"""
    
    print("🔧 Création d'un utilisateur de test pour les demandes d'aide")
    print("=" * 60)
    
    # Données utilisateur de test
    user_data = {
        "username": "helpuser",
        "email": "helpuser@example.com",
        "password": "helpuser123",
        "password_confirm": "helpuser123",
        "first_name": "Test",
        "last_name": "Help",
        "phone": "+224123456789"
    }
    
    # 1. Créer l'utilisateur
    print("\n1️⃣ Création de l'utilisateur...")
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Utilisateur créé avec succès")
            print(f"Username: {user_data['username']}")
            print(f"Email: {user_data['email']}")
        else:
            print(f"❌ Erreur création: {response.text}")
            # Vérifier si l'utilisateur existe déjà
            if "already exists" in response.text.lower():
                print("ℹ️ L'utilisateur existe déjà, on continue...")
            else:
                return
    except Exception as e:
        print(f"❌ Erreur création: {e}")
        return
    
    # 2. Connexion de l'utilisateur
    print("\n2️⃣ Connexion de l'utilisateur...")
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response data: {response_data}")
            token = response_data.get('access') or response_data.get('token')
            print("✅ Connexion réussie")
            print(f"Token: {token[:20] if token else 'None'}...")
            
            # Sauvegarder les informations
            with open('help_user_credentials.txt', 'w') as f:
                f.write(f"Username: {user_data['username']}\n")
                f.write(f"Email: {user_data['email']}\n")
                f.write(f"Password: {user_data['password']}\n")
                f.write(f"Token: {token}\n")
            
            print("💾 Informations sauvegardées dans help_user_credentials.txt")
            
        else:
            print(f"❌ Erreur connexion: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")

if __name__ == "__main__":
    create_test_user() 
#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

def get_auth_token():
    print("🔑 Obtention du token d'authentification...")
    
    # URL de l'API de connexion
    login_url = "http://127.0.0.1:8000/api/users/login/"
    
    # Données de connexion
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        # Faire la requête de connexion
        response = requests.post(login_url, json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            
            print("✅ Connexion réussie !")
            print(f"🔑 Access Token: {access_token[:50]}...")
            print(f"🔄 Refresh Token: {refresh_token[:50]}...")
            
            # Sauvegarder le token dans un fichier pour le frontend
            token_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "username": "testuser",
                    "email": "test@example.com"
                }
            }
            
            with open("token_data.json", "w") as f:
                json.dump(token_data, f, indent=2)
            
            print("💾 Token sauvegardé dans token_data.json")
            print("\n📋 Instructions pour le frontend:")
            print("1. Ouvrez la console du navigateur")
            print("2. Collez cette commande:")
            print(f"localStorage.setItem('access_token', '{access_token}')")
            print("3. Rechargez la page")
            
            return access_token
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    get_auth_token() 
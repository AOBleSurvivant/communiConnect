#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création d'un superutilisateur pour CommuniConnect
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def create_admin_user():
    """Créer un superutilisateur"""
    print("👑 Création d'un superutilisateur...")
    
    admin_data = {
        'email': 'admin@communiconnect.com',
        'password': 'Admin123!',
        'password_confirm': 'Admin123!',
        'first_name': 'Admin',
        'last_name': 'CommuniConnect',
        'username': 'admin',
        'is_staff': True,
        'is_superuser': True
    }
    
    try:
        response = requests.post(f"{API_URL}/users/register/", json=admin_data)
        if response.status_code == 201:
            print("✅ Superutilisateur créé avec succès")
            return True
        else:
            print(f"⚠️  Erreur création admin: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def login_admin():
    """Connexion de l'admin"""
    print("🔐 Connexion de l'admin...")
    
    login_data = {
        'email': 'admin@communiconnect.com',
        'password': 'Admin123!'
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            tokens = data.get('tokens', {})
            token = tokens.get('access')
            if token:
                print("✅ Admin connecté avec succès")
                return token
            else:
                print("❌ Token manquant")
                return None
        else:
            print(f"❌ Erreur connexion admin: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    if create_admin_user():
        token = login_admin()
        if token:
            print(f"\n🎯 Admin créé et connecté!")
            print(f"   Email: admin@communiconnect.com")
            print(f"   Mot de passe: Admin123!")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"\n❌ Impossible de connecter l'admin")
    else:
        print(f"\n❌ Impossible de créer l'admin") 
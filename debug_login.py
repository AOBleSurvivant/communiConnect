#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug de l'API de connexion
"""

import requests
import json

API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_social_nouveau@example.com"
TEST_USER_PASSWORD = "Test123!"

def debug_login():
    """Debug de la connexion"""
    print("🔍 Debug de l'API de connexion")
    
    login_data = {
        'email': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Data keys: {list(data.keys())}")
            if 'token' in data:
                print(f"Token trouvé: {data['token'][:20]}...")
            else:
                print("Token non trouvé dans la réponse")
        else:
            print("Erreur de connexion")
            
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    debug_login() 
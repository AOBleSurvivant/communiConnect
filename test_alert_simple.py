#!/usr/bin/env python3
"""
Test simple pour diagnostiquer le problème de création d'alertes
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000/api"

def test_alert_creation():
    print("🔍 Diagnostic du problème de création d'alertes")
    print("=" * 50)
    
    # 1. Test de connexion à l'API
    print("1. Test de connexion à l'API...")
    try:
        response = requests.get(f"{API_URL}/health/")
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print(f"❌ API non accessible: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur connexion API: {e}")
        return
    
    # 2. Test de création d'utilisateur...
    print("\n2. Test de création d'utilisateur...")
    import time
    timestamp = int(time.time())
    user_data = {
        "username": f"testuser_alert_{timestamp}",
        "email": f"testalert_{timestamp}@communiconnect.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "Test",
        "last_name": "Alert"
    }
    
    try:
        response = requests.post(f"{API_URL}/users/register/", json=user_data)
        print(f"Status création utilisateur: {response.status_code}")
        print(f"Réponse création utilisateur: {response.text}")
        if response.status_code == 201:
            print("✅ Utilisateur créé")
            # Récupérer le token directement de la création
            data = response.json()
            token = data.get('tokens', {}).get('access')
            if token:
                print(f"✅ Token obtenu: {token[:20]}...")
            else:
                print("❌ Token non reçu")
                return
        elif response.status_code == 400:
            print("ℹ️ Utilisateur existe déjà")
            # Essayer de se connecter avec l'utilisateur existant
            login_data = {
                "email": f"testalert_{timestamp}@communiconnect.com",
                "password": "TestPass123!"
            }
            
            try:
                login_response = requests.post(f"{API_URL}/users/login/", json=login_data)
                if login_response.status_code == 200:
                    login_data = login_response.json()
                    token = login_data.get("tokens", {}).get("access")
                    if token:
                        print("✅ Connexion réussie")
                        print(f"Token: {token[:20]}...")
                    else:
                        print("❌ Token non reçu")
                        return
                else:
                    print(f"❌ Erreur connexion: {login_response.status_code}")
                    print(f"Réponse: {login_response.text}")
                    return
            except Exception as e:
                print(f"❌ Erreur connexion: {e}")
                return
        else:
            print(f"❌ Erreur création utilisateur: {response.status_code}")
            print(f"Réponse: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return
    
    # 4. Test de création d'alerte
    print("\n4. Test de création d'alerte...")
    alert_data = {
        "title": "Test d'alerte - Fuite de gaz",
        "description": "Fuite de gaz détectée dans le quartier. Odeur forte dans la rue principale.",
        "category": "gas_leak",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "address": "123 Rue de la Paix",
        "neighborhood": "Centre-ville",
        "city": "Paris",
        "postal_code": "75001"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{API_URL}/notifications/alerts/", json=alert_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 201:
            print("✅ Alerte créée avec succès!")
            alert = response.json()
            print(f"ID de l'alerte: {alert.get('alert_id')}")
        else:
            print(f"❌ Erreur création alerte: {response.status_code}")
            print(f"Réponse complète: {response.text}")
    except Exception as e:
        print(f"❌ Erreur création alerte: {e}")
    
    # 5. Test de récupération des alertes
    print("\n5. Test de récupération des alertes...")
    try:
        response = requests.get(f"{API_URL}/notifications/alerts/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get("results", data)
            print(f"✅ {len(alerts)} alertes récupérées")
        else:
            print(f"❌ Erreur récupération alertes: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur récupération alertes: {e}")

if __name__ == "__main__":
    test_alert_creation() 
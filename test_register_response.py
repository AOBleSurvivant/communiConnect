#!/usr/bin/env python3
"""
Test de la structure de la réponse d'inscription
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
REGISTER_URL = f"{BASE_URL}/users/register/"

def test_register_response():
    """Test de la structure de la réponse d'inscription"""
    
    print("📝 TEST DE LA RÉPONSE D'INSCRIPTION")
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
    
    # 2. Inscription avec structure détaillée
    print("\n2. Test d'inscription avec analyse de la réponse...")
    timestamp = int(time.time())
    user_data = {
        "username": f"testuser{timestamp}",
        "email": f"testuser{timestamp}@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "Response",
        "phone_number": "+224123456789",
        "quartier": quartier_id,
        "bio": "Test de structure de réponse"
    }
    
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"Status inscription: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Inscription réussie")
            print("\n📊 STRUCTURE DE LA RÉPONSE:")
            print("=" * 40)
            
            # Analyser la structure
            print(f"Type de réponse: {type(data)}")
            print(f"Clés disponibles: {list(data.keys())}")
            
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"\n🔑 {key}:")
                    print(f"   Type: {type(value)}")
                    print(f"   Clés: {list(value.keys())}")
                    if key == 'user':
                        print(f"   ID: {value.get('id')}")
                        print(f"   Email: {value.get('email')}")
                        print(f"   Username: {value.get('username')}")
                    elif key == 'tokens':
                        print(f"   Access token présent: {'access' in value}")
                        print(f"   Refresh token présent: {'refresh' in value}")
                else:
                    print(f"\n🔑 {key}: {value}")
            
            # Vérifier si la structure correspond au frontend
            print(f"\n🎯 VÉRIFICATION FRONTEND:")
            print(f"   - 'tokens' présent: {'tokens' in data}")
            print(f"   - 'user' présent: {'user' in data}")
            print(f"   - 'message' présent: {'message' in data}")
            
            if 'tokens' in data and 'user' in data:
                print("   ✅ Structure compatible avec le frontend")
            else:
                print("   ❌ Structure incompatible avec le frontend")
                print("   📝 Correction nécessaire dans AuthContext.js")
                
        else:
            print(f"❌ Échec d'inscription: {response.text}")
    except Exception as e:
        print(f"❌ Erreur d'inscription: {e}")

if __name__ == "__main__":
    test_register_response() 
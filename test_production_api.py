#!/usr/bin/env python3
"""
Script pour tester l'API de production et vérifier les données géographiques
"""

import requests
import json

# Configuration
PRODUCTION_API_URL = "https://communiconnect-backend.onrender.com/api"
LOCAL_API_URL = "http://localhost:8000/api"

def test_api_endpoint(url, endpoint, name):
    """Test un endpoint API"""
    print(f"\n🔍 Test {name}:")
    print(f"URL: {url}{endpoint}")
    
    try:
        response = requests.get(f"{url}{endpoint}", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Succès! Données reçues")
                print(f"Type de données: {type(data)}")
                
                # Vérifier si c'est une liste ou un objet
                if isinstance(data, dict):
                    regions = data.get('regions', [])
                    print(f"📊 {len(regions)} régions trouvées")
                    
                    if regions:
                        print("📊 Première région:")
                        first_region = regions[0]
                        print(f"   Nom: {first_region.get('nom')}")
                        print(f"   Préfectures: {len(first_region.get('prefectures', []))}")
                        
                        if first_region.get('prefectures'):
                            first_prefecture = first_region['prefectures'][0]
                            print(f"   Première préfecture: {first_prefecture.get('nom')}")
                            print(f"   Communes: {len(first_prefecture.get('communes', []))}")
                            
                            if first_prefecture.get('communes'):
                                first_commune = first_prefecture['communes'][0]
                                print(f"   Première commune: {first_commune.get('nom')}")
                                print(f"   Quartiers: {len(first_commune.get('quartiers', []))}")
                                
                                if first_commune.get('quartiers'):
                                    first_quartier = first_commune['quartiers'][0]
                                    print(f"   Premier quartier: {first_quartier.get('nom')}")
                    else:
                        print("❌ Aucune région trouvée")
                        
                elif isinstance(data, list):
                    print(f"📊 Données reçues comme liste: {len(data)} éléments")
                    print(f"Premier élément: {data[0] if data else 'Aucun'}")
                else:
                    print(f"📊 Type de données inattendu: {type(data)}")
                    print(f"Contenu: {data}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON: {e}")
                print(f"Contenu brut: {response.text[:200]}...")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def test_user_registration(url, name):
    """Test l'inscription d'un utilisateur"""
    print(f"\n👤 Test inscription utilisateur ({name}):")
    
    test_user_data = {
        "username": "test_user_geo",
        "first_name": "Test",
        "last_name": "User",
        "email": "test.geo@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "quartier": 1  # Premier quartier
    }
    
    try:
        response = requests.post(f"{url}/users/register/", json=test_user_data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Inscription réussie!")
            data = response.json()
            print(f"Utilisateur créé: {data.get('user', {}).get('username')}")
        else:
            print(f"❌ Erreur d'inscription: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def test_health_check(url, name):
    """Test de santé de l'API"""
    print(f"\n🏥 Test de santé ({name}):")
    
    try:
        response = requests.get(f"{url}/", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test de l'API CommuniConnect")
    print("=" * 50)
    
    # Test de santé
    test_health_check(PRODUCTION_API_URL, "Production")
    
    # Test API locale (si disponible)
    try:
        test_api_endpoint(LOCAL_API_URL, "/users/geographic-data/", "API Locale")
    except:
        print("\n🔍 Test API Locale: Serveur local non disponible")
    
    # Test API de production
    test_api_endpoint(PRODUCTION_API_URL, "/users/geographic-data/", "API Production")
    
    # Test inscription production
    test_user_registration(PRODUCTION_API_URL, "Production")
    
    print("\n" + "=" * 50)
    print("📋 Résumé des tests:")
    print("1. Vérifiez que l'API de production répond")
    print("2. Vérifiez que l'API retourne des données géographiques")
    print("3. Si aucune donnée, chargez-les sur Render")
    print("4. Testez l'inscription d'utilisateurs")

if __name__ == "__main__":
    main() 
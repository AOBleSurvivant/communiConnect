import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/api/users/register/"

# Données de test
test_user_data = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "+224123456789",
    "quartier": 54  # ID du quartier
}

def test_registration():
    print("🔍 Test d'inscription...")
    print(f"URL: {REGISTER_URL}")
    print(f"Données: {json.dumps(test_user_data, indent=2)}")
    
    try:
        response = requests.post(REGISTER_URL, json=test_user_data)
        
        print(f"\n📊 Réponse:")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 400:
            print(f"❌ Erreur 400 - Détails:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Contenu brut: {response.text}")
        elif response.status_code == 201:
            print("✅ Inscription réussie!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"⚠️ Status inattendu: {response.status_code}")
            print(f"Contenu: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def test_health():
    print("\n🏥 Test de santé du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erreur health check: {e}")

if __name__ == "__main__":
    test_health()
    test_registration() 
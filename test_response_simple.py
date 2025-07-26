import requests
import json

# URL de l'API
url = "http://127.0.0.1:8000/api/help-requests/api/requests/faa7c105-216d-4d4f-ba42-e36da2731d92/respond/"

# Données de test
data = {
    "response_type": "offer_help",
    "message": "Je peux vous aider avec cela",
    "contact_phone": "",
    "contact_email": ""
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"  # Remplace par un vrai token
}

print("🔍 Test API Response")
print(f"📤 URL: {url}")
print(f"📋 Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"📊 Status: {response.status_code}")
    print(f"📋 Response: {response.text}")
except Exception as e:
    print(f"❌ Erreur: {e}") 
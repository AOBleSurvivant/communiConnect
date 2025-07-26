import requests
import json

# URL de l'API
url = "http://127.0.0.1:8000/api/help-requests/api/requests/"

# Données de test
data = {
    "title": "Test demande d'aide",
    "description": "Ceci est un test de création de demande d'aide",
    "need_type": "presence",
    "request_type": "offer",
    "for_who": "myself",
    "duration_type": "this_week",
    "proximity_zone": "local",
    "is_urgent": True,
    "contact_preference": "phone",
    "phone": "623516708",
    "latitude": 11.318067,
    "longitude": -12.294554,
    "address": "Wanindara, Conakry, Guinée",
    "neighborhood": "Pounthioun",
    "city": "Conakry",
    "postal_code": "625"
}

# Headers
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 400:
        print(f"Erreur de validation: {json.dumps(response.json(), indent=2)}")
    elif response.status_code == 201:
        print("✅ Demande créée avec succès!")
    else:
        print(f"Erreur inattendue: {response.status_code}")
        
except Exception as e:
    print(f"Erreur de connexion: {e}") 
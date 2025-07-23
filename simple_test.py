import requests
import json

print("Test de l'API CommuniConnect")

# Test de connexion
login_data = {
    "email": "mariam.diallo@test.gn",
    "password": "test123456"
}

print("Tentative de connexion...")
response = requests.post("http://127.0.0.1:8000/api/users/login/", json=login_data)
print(f"Status: {response.status_code}")
print(f"Réponse: {response.text}")

if response.status_code == 200:
    data = response.json()
    token = data.get('tokens', {}).get('access')
    print(f"Token obtenu: {token[:50]}...")
    
    # Test de l'API posts
    headers = {"Authorization": f"Bearer {token}"}
    posts_response = requests.get("http://127.0.0.1:8000/api/posts/", headers=headers)
    print(f"Posts API Status: {posts_response.status_code}")
    print(f"Posts API Réponse: {posts_response.text[:200]}...")
else:
    print("Échec de connexion") 
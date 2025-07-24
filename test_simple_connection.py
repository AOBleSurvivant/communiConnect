#!/usr/bin/env python3
"""
Script de test simple pour vérifier la connexion à l'API
"""

try:
    import requests
    print("✅ Module requests importé avec succès")
except ImportError as e:
    print(f"❌ Erreur import requests: {e}")
    exit(1)

# Test de connexion simple
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

print(f"🔗 Test de connexion à {API_URL}/health/")

try:
    response = requests.get(f"{API_URL}/health/")
    print(f"📡 Statut de la réponse: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Connexion réussie!")
        print(f"📋 Réponse: {data}")
    else:
        print(f"❌ Erreur de connexion: {response.status_code}")
        print(f"📋 Réponse: {response.text}")
        
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")

print("\n🎯 Test terminé!") 
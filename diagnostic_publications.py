#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_login():
    """Test de connexion utilisateur"""
    print("🔐 Test de connexion...")
    
    login_data = {
        "email": "mariam.diallo@test.gn",
        "password": "test123456"
    }
    
    response = requests.post(f"{API_URL}/users/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('tokens', {}).get('access')
        print(f"✅ Connexion réussie pour mariam_diallo")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        return None

def test_posts_retrieval(token):
    """Test de récupération des publications"""
    print(f"\n📝 TEST RÉCUPÉRATION PUBLICATIONS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test 1: Récupération de toutes les publications
    print("\n1️⃣ Test récupération toutes les publications...")
    response = requests.get(f"{API_URL}/posts/", headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📊 Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Récupération réussie")
        print(f"📊 Structure de la réponse: {type(data)}")
        
        if isinstance(data, dict):
            print(f"📊 Clés disponibles: {list(data.keys())}")
            if 'results' in data:
                posts = data['results']
                print(f"📊 Nombre de publications: {len(posts)}")
                if posts:
                    print(f"📊 Premier post: {posts[0].get('id')} - {posts[0].get('content', '')[:50]}...")
            elif 'data' in data:
                posts = data['data']
                print(f"📊 Nombre de publications: {len(posts)}")
                if posts:
                    print(f"📊 Premier post: {posts[0].get('id')} - {posts[0].get('content', '')[:50]}...")
            else:
                print(f"📊 Données directes: {len(data) if isinstance(data, list) else 'N/A'}")
        elif isinstance(data, list):
            print(f"📊 Nombre de publications: {len(data)}")
            if data:
                print(f"📊 Premier post: {data[0].get('id')} - {data[0].get('content', '')[:50]}...")
        
        return data
    else:
        print(f"❌ Erreur récupération: {response.status_code}")
        print(f"📊 Réponse: {response.text}")
        return None

def test_posts_with_filters(token):
    """Test de récupération avec filtres"""
    print(f"\n🔍 TEST RÉCUPÉRATION AVEC FILTRES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test avec différents filtres
    filters = [
        {'type': 'info'},
        {'type': 'event'},
        {'type': 'help'},
        {'type': 'announcement'},
        {'search': 'test'}
    ]
    
    for i, filter_params in enumerate(filters, 1):
        print(f"\n{i}️⃣ Test avec filtre: {filter_params}")
        response = requests.get(f"{API_URL}/posts/", headers=headers, params=filter_params)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                posts = data['results']
                print(f"✅ {len(posts)} publications trouvées")
            elif isinstance(data, list):
                print(f"✅ {len(data)} publications trouvées")
            else:
                print(f"✅ Réponse reçue (structure: {type(data)})")
        else:
            print(f"❌ Erreur: {response.status_code}")

def test_notifications_retrieval(token):
    """Test de récupération des notifications"""
    print(f"\n🔔 TEST RÉCUPÉRATION NOTIFICATIONS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test notifications
    print("\n1️⃣ Test récupération notifications...")
    response = requests.get(f"{API_URL}/notifications/", headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Récupération notifications réussie")
        print(f"📊 Structure: {type(data)}")
        
        if isinstance(data, dict):
            print(f"📊 Clés: {list(data.keys())}")
            if 'results' in data:
                notifications = data['results']
                print(f"📊 Nombre de notifications: {len(notifications)}")
            else:
                print(f"📊 Données: {len(data) if isinstance(data, list) else 'N/A'}")
        elif isinstance(data, list):
            print(f"📊 Nombre de notifications: {len(data)}")
    else:
        print(f"❌ Erreur notifications: {response.status_code}")
        print(f"📊 Réponse: {response.text}")

def test_notifications_count(token):
    """Test du compteur de notifications"""
    print(f"\n📊 TEST COMPTEUR NOTIFICATIONS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{API_URL}/notifications/count/", headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Compteur récupéré")
        print(f"📊 Données: {data}")
    else:
        print(f"❌ Erreur compteur: {response.status_code}")
        print(f"📊 Réponse: {response.text}")

def main():
    """Diagnostic complet des publications et notifications"""
    print("🔍 DIAGNOSTIC PUBLICATIONS ET NOTIFICATIONS")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Test des publications
    posts_data = test_posts_retrieval(token)
    
    # Test avec filtres
    test_posts_with_filters(token)
    
    # Test des notifications
    test_notifications_retrieval(token)
    
    # Test du compteur
    test_notifications_count(token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    if posts_data:
        print("✅ Publications: Données récupérées")
    else:
        print("❌ Publications: Problème de récupération")
    
    print("✅ Notifications: Testé")
    print("✅ Compteur: Testé")
    print("💡 Vérifiez les détails ci-dessus pour identifier les problèmes")

if __name__ == "__main__":
    main() 
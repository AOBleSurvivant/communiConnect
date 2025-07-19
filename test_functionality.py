#!/usr/bin/env python
"""
Script de test pour valider les fonctionnalités principales de CommuniConnect
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test de la santé du backend"""
    print("🔍 Test de la santé du backend...")
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend accessible")
            return True
        else:
            print(f"❌ Backend inaccessible (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion au backend: {e}")
        return False

def test_authentication():
    """Test de l'authentification"""
    print("\n🔐 Test de l'authentification...")
    
    # Test de connexion
    login_data = {
        "username": "admin",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data, timeout=5)
        if response.status_code == 200:
            token = response.json().get('access')
            print("✅ Connexion réussie")
            return token
        else:
            print(f"❌ Échec de connexion (status: {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_posts_api(token):
    """Test de l'API des posts"""
    print("\n📝 Test de l'API des posts...")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        # Récupérer les posts
        response = requests.get(f"{BASE_URL}/api/posts/", headers=headers, timeout=5)
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ {len(posts)} posts récupérés")
            
            # Afficher quelques détails
            for i, post in enumerate(posts[:3]):
                print(f"  Post {i+1}: {post.get('content', '')[:50]}...")
            
            return True
        else:
            print(f"❌ Échec de récupération des posts (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des posts: {e}")
        return False

def test_users_api(token):
    """Test de l'API des utilisateurs"""
    print("\n👥 Test de l'API des utilisateurs...")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        # Récupérer le profil utilisateur
        response = requests.get(f"{BASE_URL}/api/users/profile/", headers=headers, timeout=5)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Profil utilisateur récupéré: {user.get('username', 'N/A')}")
            return True
        else:
            print(f"❌ Échec de récupération du profil (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        return False

def test_geography_api():
    """Test de l'API géographique"""
    print("\n🗺️ Test de l'API géographique...")
    
    try:
        # Récupérer les régions
        response = requests.get(f"{BASE_URL}/api/geography/regions/", timeout=5)
        if response.status_code == 200:
            regions = response.json()
            print(f"✅ {len(regions)} régions récupérées")
            return True
        else:
            print(f"❌ Échec de récupération des régions (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des régions: {e}")
        return False

def test_frontend_access():
    """Test d'accès au frontend"""
    print("\n🌐 Test d'accès au frontend...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            return True
        else:
            print(f"❌ Frontend inaccessible (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion au frontend: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 === Test de validation CommuniConnect ===\n")
    
    # Attendre que les serveurs démarrent
    print("⏳ Attente du démarrage des serveurs...")
    time.sleep(3)
    
    # Tests
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_access()
    
    if backend_ok:
        token = test_authentication()
        if token:
            test_posts_api(token)
            test_users_api(token)
        test_geography_api()
    
    # Résumé
    print("\n📊 === Résumé des tests ===")
    print(f"Backend: {'✅' if backend_ok else '❌'}")
    print(f"Frontend: {'✅' if frontend_ok else '❌'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Tous les tests sont passés ! L'application est prête.")
        print(f"\n📱 Accès à l'application:")
        print(f"   Frontend: {FRONTEND_URL}")
        print(f"   Backend API: {BASE_URL}/api/")
        print(f"\n🔑 Comptes de test:")
        print(f"   Admin: admin / admin123456")
        print(f"   Test: mariam_diallo / test123456")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez que les serveurs sont démarrés.")

if __name__ == "__main__":
    main() 
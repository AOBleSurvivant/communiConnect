#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test CommuniConnect
"""

import os
import sys
import django
from pathlib import Path
import time

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent / "backend"
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from geography.models import Quartier

User = get_user_model()

def create_test_user():
    """Créer un utilisateur de test avec des données valides"""
    
    # Générer un nom d'utilisateur unique
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"test_{timestamp}@communiconnect.com"
    
    # Récupérer un quartier valide
    quartier = Quartier.objects.first()
    if not quartier:
        print("❌ Aucun quartier disponible")
        return None
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        print(f"⚠️ Utilisateur {username} existe déjà")
        return User.objects.get(username=username)
    
    # Créer l'utilisateur
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password="TestPass123!",
            first_name="Test",
            last_name="User",
            quartier=quartier
        )
        
        print(f"✅ Utilisateur de test créé:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Quartier: {quartier.nom}")
        print(f"   ID: {user.id}")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        return None

def test_api_with_user(user):
    """Tester l'API avec l'utilisateur créé"""
    import requests
    
    base_url = "http://localhost:8000/api"
    
    # Test de connexion
    login_data = {
        "email": user.email,
        "password": "TestPass123!"
    }
    
    try:
        response = requests.post(f"{base_url}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('tokens', {}).get('access')
            
            if access_token:
                print("✅ Connexion réussie")
                
                # Tester l'API des posts avec le token
                headers = {'Authorization': f'Bearer {access_token}'}
                posts_response = requests.get(f"{base_url}/posts/", headers=headers)
                
                if posts_response.status_code == 200:
                    print("✅ API posts accessible")
                    return True
                else:
                    print(f"❌ API posts: {posts_response.status_code}")
            else:
                print("❌ Token d'accès non reçu")
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test API: {str(e)}")
    
    return False

def main():
    """Fonction principale"""
    print("🚀 CRÉATION D'UN UTILISATEUR DE TEST")
    print("=" * 50)
    
    # Créer l'utilisateur
    user = create_test_user()
    
    if user:
        print("\n🧪 TEST DE L'API")
        print("=" * 30)
        
        # Tester l'API
        success = test_api_with_user(user)
        
        if success:
            print("\n🎉 TOUT FONCTIONNE !")
            print("L'utilisateur de test est prêt pour les tests")
        else:
            print("\n⚠️ Problèmes détectés dans l'API")
    else:
        print("\n❌ Impossible de créer l'utilisateur de test")

if __name__ == "__main__":
    main() 
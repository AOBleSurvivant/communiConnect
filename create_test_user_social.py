#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création d'un utilisateur de test pour les fonctionnalités sociales
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_social_avance@example.com"
TEST_USER_PASSWORD = "Test123!"

def create_test_user():
    """Créer un utilisateur de test"""
    print("🚀 Création d'un utilisateur de test pour les fonctionnalités sociales...")
    
    user_data = {
        "username": "test_social_avance",
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "first_name": "Test",
        "last_name": "Social",
        "quartier": 1  # Premier quartier disponible
    }
    
    try:
        response = requests.post(f"{API_URL}/users/register/", json=user_data)
        
        if response.status_code == 201:
            print("✅ Utilisateur créé avec succès")
            data = response.json()
            print(f"📧 Email: {data.get('user', {}).get('email')}")
            print(f"🆔 ID: {data.get('user', {}).get('id')}")
            return True
        elif response.status_code == 400:
            print("⚠️  Utilisateur existe déjà")
            # Essayer de se connecter
            return login_test_user()
        else:
            print(f"❌ Erreur création utilisateur: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def login_test_user():
    """Se connecter avec l'utilisateur de test"""
    print("🔐 Tentative de connexion...")
    
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie")
            print(f"🆔 ID utilisateur: {data.get('user', {}).get('id')}")
            print(f"🔑 Token: {data.get('access', '')[:20]}...")
            return True
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return False

def test_basic_endpoints():
    """Tester les endpoints de base"""
    print("\n🧪 Test des endpoints de base...")
    
    # Test de connexion
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            user_id = data.get('user', {}).get('id')
            
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test des groupes
            print("📋 Test des groupes...")
            response = requests.get(f"{API_URL}/users/groups/", headers=headers)
            print(f"Groupes: {response.status_code}")
            
            # Test des événements
            print("📅 Test des événements...")
            response = requests.get(f"{API_URL}/users/events/", headers=headers)
            print(f"Événements: {response.status_code}")
            
            # Test des suggestions
            print("💡 Test des suggestions...")
            response = requests.get(f"{API_URL}/users/suggested-groups/", headers=headers)
            print(f"Suggestions groupes: {response.status_code}")
            
            response = requests.get(f"{API_URL}/users/suggested-events/", headers=headers)
            print(f"Suggestions événements: {response.status_code}")
            
            response = requests.get(f"{API_URL}/users/suggested-connections/", headers=headers)
            print(f"Suggestions connexions: {response.status_code}")
            
            # Test du score social
            print("🏆 Test du score social...")
            response = requests.get(f"{API_URL}/users/social-score/{user_id}/", headers=headers)
            print(f"Score social: {response.status_code}")
            
            # Test des réalisations
            print("🎖️ Test des réalisations...")
            response = requests.get(f"{API_URL}/users/achievements/{user_id}/", headers=headers)
            print(f"Réalisations: {response.status_code}")
            
            # Test du classement
            print("📊 Test du classement...")
            response = requests.get(f"{API_URL}/users/leaderboard/", headers=headers)
            print(f"Classement: {response.status_code}")
            
            # Test des statistiques sociales
            print("📈 Test des statistiques sociales...")
            response = requests.get(f"{API_URL}/users/social-stats/{user_id}/", headers=headers)
            print(f"Statistiques: {response.status_code}")
            
        else:
            print("❌ Impossible de se connecter pour tester les endpoints")
            
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

def main():
    """Fonction principale"""
    print("="*60)
    print("🚀 CRÉATION UTILISATEUR DE TEST - FONCTIONNALITÉS SOCIALES")
    print("="*60)
    
    # Créer l'utilisateur
    if create_test_user():
        print("\n✅ Utilisateur de test prêt !")
        
        # Tester les endpoints
        test_basic_endpoints()
        
        print("\n🎉 Tests terminés !")
        print("Vous pouvez maintenant utiliser l'utilisateur de test pour les fonctionnalités sociales.")
    else:
        print("\n❌ Impossible de créer l'utilisateur de test")

if __name__ == "__main__":
    main() 
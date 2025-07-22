#!/usr/bin/env python3
"""
Script pour charger les données géographiques directement via l'API de production
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "https://communiconnect-backend.onrender.com/api"

def test_api_health():
    """Test la santé de l'API"""
    print("🏥 Test de santé de l'API...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/users/geographic-data/", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"📊 Données actuelles: {len(data)} éléments")
                return len(data) > 0
            else:
                print("❌ Format de données inattendu")
                return False
        else:
            print(f"❌ API non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def create_test_user():
    """Crée un utilisateur de test pour vérifier l'inscription"""
    print("\n👤 Test de création d'utilisateur...")
    
    test_user_data = {
        "username": "test_geo_user",
        "first_name": "Test",
        "last_name": "Geographic",
        "email": "test.geo@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "quartier": 1  # Premier quartier disponible
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/register/", json=test_user_data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Utilisateur créé avec succès!")
            return True
        else:
            print(f"❌ Erreur d'inscription: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def check_render_deployment_status():
    """Vérifie le statut du déploiement Render"""
    print("\n🔍 Vérification du statut de déploiement...")
    
    # Test des endpoints principaux
    endpoints = [
        "/users/geographic-data/",
        "/users/register/",
        "/users/login/",
        "/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
            print(f"  {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"  {endpoint}: Erreur - {e}")

def wait_for_deployment():
    """Attend que le déploiement soit terminé"""
    print("\n⏳ Attente du déploiement Render...")
    
    max_attempts = 20
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Tentative {attempt}/{max_attempts}...")
        
        if test_api_health():
            print("✅ Déploiement réussi ! Les données sont chargées.")
            return True
        
        print("⏳ Déploiement en cours, attente de 30 secondes...")
        time.sleep(30)
    
    print("❌ Déploiement échoué ou timeout")
    return False

def main():
    """Fonction principale"""
    print("🚀 Vérification du déploiement CommuniConnect")
    print("=" * 50)
    
    # Vérifier le statut actuel
    print("1️⃣ Vérification de l'état actuel...")
    if test_api_health():
        print("✅ Les données sont déjà chargées sur Render")
        print("\n2️⃣ Test de création d'utilisateur...")
        if create_test_user():
            print("\n🎉 Tout fonctionne ! Vous pouvez maintenant créer des comptes.")
            return
        else:
            print("\n❌ Problème avec l'inscription d'utilisateurs")
            return
    
    # Vérifier le statut du déploiement
    print("\n2️⃣ Vérification du statut de déploiement...")
    check_render_deployment_status()
    
    # Attendre le déploiement
    print("\n3️⃣ Attente du déploiement...")
    if wait_for_deployment():
        print("\n4️⃣ Test de création d'utilisateur...")
        if create_test_user():
            print("\n🎉 Déploiement réussi !")
            print("📋 Prochaines étapes:")
            print("1. Testez l'inscription d'utilisateurs")
            print("2. Vérifiez que les données géographiques sont disponibles")
            print("3. Lancez les tests utilisateurs")
        else:
            print("\n❌ Problème avec l'inscription d'utilisateurs")
    else:
        print("\n❌ Déploiement échoué")
        print("📋 Actions recommandées:")
        print("1. Vérifiez le dashboard Render")
        print("2. Consultez les logs de déploiement")
        print("3. Relancez le déploiement manuellement")

if __name__ == "__main__":
    main() 
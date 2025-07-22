#!/usr/bin/env python3
"""
Script simple pour tester l'inscription d'utilisateur
"""

import requests
import json

def test_production_api():
    """Test l'API de production"""
    print("🔍 Test de l'API de production...")
    
    api_url = "https://communiconnect-backend.onrender.com/api"
    
    # Test des données géographiques
    try:
        response = requests.get(f"{api_url}/users/geographic-data/", timeout=10)
        print(f"Geographic data status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"📊 Données géographiques: {len(data)} éléments")
                return len(data) > 0
            else:
                print("❌ Format de données inattendu")
                return False
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_registration():
    """Test l'inscription d'utilisateur"""
    print("\n👤 Test d'inscription...")
    
    api_url = "https://communiconnect-backend.onrender.com/api"
    
    test_user_data = {
        "username": "test_user_final",
        "first_name": "Test",
        "last_name": "Final",
        "email": "test.final@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "quartier": 1  # Premier quartier
    }
    
    try:
        response = requests.post(f"{api_url}/users/register/", json=test_user_data, timeout=10)
        print(f"Registration status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Inscription réussie!")
            data = response.json()
            print(f"Utilisateur créé: {data.get('user', {}).get('username')}")
            return True
        else:
            print(f"❌ Erreur d'inscription: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test d'inscription CommuniConnect")
    print("=" * 50)
    
    # Test de l'API de production
    print("1️⃣ Test de l'API de production...")
    if test_production_api():
        print("✅ Données géographiques disponibles sur Render")
        
        # Test d'inscription
        print("\n2️⃣ Test d'inscription...")
        if test_registration():
            print("\n🎉 Succès ! Vous pouvez créer des comptes.")
            print("📋 L'application est prête pour les tests utilisateurs.")
        else:
            print("\n❌ Problème avec l'inscription")
            print("📋 Actions recommandées:")
            print("1. Vérifiez les logs Render")
            print("2. Testez avec un autre utilisateur")
            print("3. Vérifiez la configuration de l'API")
    else:
        print("❌ Données géographiques non disponibles sur Render")
        print("📋 Actions recommandées:")
        print("1. Vérifiez le dashboard Render")
        print("2. Consultez les logs de déploiement")
        print("3. Relancez le déploiement manuellement")

if __name__ == "__main__":
    main() 
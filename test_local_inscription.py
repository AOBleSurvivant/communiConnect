#!/usr/bin/env python3
"""
Test d'inscription utilisateur avec données géographiques locales
"""

import requests
import json
import time

def test_local_registration():
    print("🚀 Test d'inscription CommuniConnect - Environnement Local")
    print("=" * 60)
    
    # Test 1: Vérifier les données géographiques
    print("🔍 Test 1: Vérification des données géographiques...")
    try:
        response = requests.get("http://localhost:8000/api/users/geographic-data/")
        if response.status_code == 200:
            data = response.json()
            regions = data.get('regions', [])
            print(f"✅ Données géographiques disponibles: {len(regions)} régions")
            
            # Afficher quelques exemples
            if regions:
                region = regions[0]
                prefectures = region.get('prefectures', [])
                if prefectures:
                    prefecture = prefectures[0]
                    communes = prefecture.get('communes', [])
                    if communes:
                        commune = communes[0]
                        quartiers = commune.get('quartiers', [])
                        if quartiers:
                            quartier = quartiers[0]
                            print(f"📍 Exemple: {region['nom']} > {prefecture['nom']} > {commune['nom']} > {quartier['nom']}")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Test d'inscription
    print("\n🔍 Test 2: Test d'inscription utilisateur...")
    
    # Récupérer un quartier pour l'inscription
    try:
        response = requests.get("http://localhost:8000/api/users/geographic-data/")
        data = response.json()
        regions = data.get('regions', [])
        
        if not regions:
            print("❌ Aucune région disponible")
            return False
            
        # Prendre le premier quartier disponible
        quartier_id = None
        for region in regions:
            for prefecture in region.get('prefectures', []):
                for commune in prefecture.get('communes', []):
                    for quartier in commune.get('quartiers', []):
                        quartier_id = quartier['id']
                        quartier_nom = quartier['nom']
                        break
                    if quartier_id:
                        break
                if quartier_id:
                    break
            if quartier_id:
                break
        
        if not quartier_id:
            print("❌ Aucun quartier disponible")
            return False
            
        print(f"📍 Utilisation du quartier: {quartier_nom} (ID: {quartier_id})")
        
        # Données de test avec tous les champs requis
        timestamp = int(time.time())
        user_data = {
            "username": f"testuser{timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "Test123!",
            "password_confirm": "Test123!",
            "first_name": "Test",
            "last_name": "Utilisateur",
            "quartier": quartier_id
        }
        
        print(f"📝 Tentative d'inscription pour: {user_data['email']}")
        
        # Test d'inscription
        response = requests.post(
            "http://localhost:8000/api/users/register/",
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print("✅ Inscription réussie!")
            user_info = response.json()
            print(f"👤 Utilisateur créé: {user_info.get('user', {}).get('email', 'N/A')}")
            return True
        else:
            print(f"❌ Erreur d'inscription: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'inscription: {e}")
        return False

if __name__ == "__main__":
    success = test_local_registration()
    
    if success:
        print("\n🎉 Tous les tests sont passés!")
        print("✅ L'environnement local est prêt pour les tests utilisateurs")
        print("\n📋 Prochaines étapes:")
        print("1. Ouvrez http://localhost:3004 dans votre navigateur")
        print("2. Testez l'inscription avec les données géographiques")
        print("3. Testez la connexion et les autres fonctionnalités")
    else:
        print("\n❌ Certains tests ont échoué")
        print("🔧 Vérifiez que les serveurs sont démarrés:")
        print("   - Backend: cd backend && python manage.py runserver 8000")
        print("   - Frontend: cd frontend && npm start") 
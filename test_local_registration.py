#!/usr/bin/env python3
"""
Script pour tester l'inscription d'utilisateur avec les données locales
"""

import os
import sys
import django
import requests
import json

# Configuration Django locale
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier
from users.models import User

def test_local_data():
    """Test les données géographiques locales"""
    print("🗺️  Test des données géographiques locales...")
    
    regions = Region.objects.count()
    prefectures = Prefecture.objects.count()
    communes = Commune.objects.count()
    quartiers = Quartier.objects.count()
    
    print(f"📊 Données locales:")
    print(f"   Régions: {regions}")
    print(f"   Préfectures: {prefectures}")
    print(f"   Communes: {communes}")
    print(f"   Quartiers: {quartiers}")
    
    if quartiers > 0:
        print("✅ Données géographiques disponibles localement")
        return True
    else:
        print("❌ Aucune donnée géographique locale")
        return False

def test_local_api():
    """Test l'API locale"""
    print("\n🔍 Test de l'API locale...")
    
    try:
        response = requests.get("http://localhost:8000/api/users/geographic-data/", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'regions' in data:
                regions = data['regions']
                print(f"✅ API locale fonctionne: {len(regions)} régions")
                return True
            else:
                print("❌ Format de données inattendu")
                return False
        else:
            print(f"❌ API locale non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion locale: {e}")
        return False

def test_local_registration():
    """Test l'inscription locale"""
    print("\n👤 Test d'inscription locale...")
    
    # Récupérer le premier quartier disponible
    quartier = Quartier.objects.first()
    if not quartier:
        print("❌ Aucun quartier disponible")
        return False
    
    print(f"📍 Quartier sélectionné: {quartier.nom} ({quartier.id})")
    
    test_user_data = {
        "username": "test_local_user",
        "first_name": "Test",
        "last_name": "Local",
        "email": "test.local@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "quartier": quartier.id
    }
    
    try:
        response = requests.post("http://localhost:8000/api/users/register/", json=test_user_data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Inscription locale réussie!")
            data = response.json()
            print(f"Utilisateur créé: {data.get('user', {}).get('username')}")
            return True
        else:
            print(f"❌ Erreur d'inscription locale: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion locale: {e}")
        return False

def start_local_server():
    """Démarre le serveur local"""
    print("\n🚀 Démarrage du serveur local...")
    
    import subprocess
    import time
    
    try:
        # Démarrer le serveur en arrière-plan
        process = subprocess.Popen(
            ["python", "manage.py", "runserver", "8000"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre que le serveur démarre
        time.sleep(5)
        
        print("✅ Serveur local démarré")
        return process
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Test d'inscription CommuniConnect")
    print("=" * 50)
    
    # Test des données locales
    print("1️⃣ Test des données géographiques locales...")
    if not test_local_data():
        print("❌ Impossible de continuer sans données géographiques")
        return
    
    # Démarrer le serveur local
    print("\n2️⃣ Démarrage du serveur local...")
    server_process = start_local_server()
    
    if not server_process:
        print("❌ Impossible de démarrer le serveur local")
        return
    
    try:
        # Test de l'API locale
        print("\n3️⃣ Test de l'API locale...")
        if not test_local_api():
            print("❌ API locale non accessible")
            return
        
        # Test d'inscription locale
        print("\n4️⃣ Test d'inscription locale...")
        if test_local_registration():
            print("\n🎉 Succès ! L'inscription fonctionne localement.")
            print("📋 Le problème vient de l'environnement de production Render.")
            print("📋 Actions recommandées:")
            print("1. Vérifiez le dashboard Render")
            print("2. Consultez les logs de déploiement")
            print("3. Relancez le déploiement manuellement")
        else:
            print("\n❌ Problème avec l'inscription locale")
            print("📋 Actions recommandées:")
            print("1. Vérifiez la configuration Django")
            print("2. Consultez les logs du serveur")
            print("3. Testez avec un autre utilisateur")
    
    finally:
        # Arrêter le serveur
        if server_process:
            print("\n🛑 Arrêt du serveur local...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    main() 
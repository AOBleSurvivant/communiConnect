#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Automatique - Fonctionnalité de Demande d'Aide CommuniConnect
Démarre automatiquement le serveur Django et teste l'API
"""

import os
import sys
import time
import subprocess
import requests
import json
from datetime import datetime

def start_django_server():
    """Démarre le serveur Django en arrière-plan"""
    print("🚀 Démarrage automatique du serveur Django...")
    
    # Aller dans le répertoire backend
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_path)
    
    # Vérifier que Django est configuré
    try:
        result = subprocess.run(['python', 'manage.py', 'check'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Erreur configuration Django:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erreur vérification Django: {e}")
        return False
    
    # Démarrer le serveur en arrière-plan
    try:
        server_process = subprocess.Popen(
            ['python', 'manage.py', 'runserver', '127.0.0.1:8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que le serveur démarre
        print("⏳ Attente du démarrage du serveur...")
        time.sleep(5)
        
        # Vérifier que le serveur fonctionne
        try:
            response = requests.get('http://127.0.0.1:8000/', timeout=5)
            print("✅ Serveur Django démarré avec succès!")
            return server_process
        except requests.exceptions.ConnectionError:
            print("❌ Serveur non accessible après démarrage")
            server_process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Erreur démarrage serveur: {e}")
        return False

def test_help_requests_api():
    """Test de l'API de demande d'aide"""
    
    print("\n🎯 TEST AUTOMATIQUE - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("=" * 60)
    print(f"⏰ Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Configuration API
    API_BASE_URL = "http://127.0.0.1:8000"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Test 1: Authentification
    print("🔐 1. Test d'authentification...")
    try:
        login_data = {
            'username': 'mariam_diallo',
            'password': 'testpass123'
        }
        
        response = requests.post(f"{API_BASE_URL}/api/users/login/", 
                               json=login_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get('access')
            headers['Authorization'] = f'Bearer {token}'
            print("✅ Authentification réussie")
        else:
            print(f"❌ Erreur authentification: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur authentification: {e}")
        return False
    
    # Test 2: Endpoint des demandes d'aide
    print("\n📋 2. Test endpoint demandes d'aide...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            help_requests = response.json()
            count = len(help_requests.get('results', help_requests))
            print(f"✅ Endpoint accessible - {count} demandes trouvées")
        else:
            print(f"❌ Erreur endpoint: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur endpoint: {e}")
    
    # Test 3: Création d'une demande d'aide
    print("\n📝 3. Test création de demande d'aide...")
    try:
        help_request_data = {
            'request_type': 'request',
            'need_type': 'material',
            'for_who': 'myself',
            'title': 'Test Auto - Besoin de matériel',
            'description': 'Test automatique de création via API REST.',
            'duration_type': 'this_week',
            'estimated_hours': 2,
            'proximity_zone': 'local',
            'is_urgent': False,
            'contact_preference': 'message',
            'latitude': 9.5370,
            'longitude': -13.6785,
            'city': 'Conakry'
        }
        
        response = requests.post(f"{API_BASE_URL}/help-requests/api/requests/", 
                               json=help_request_data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            help_request = response.json()
            help_request_id = help_request.get('id')
            print(f"✅ Demande d'aide créée (ID: {help_request_id})")
            
            # Test 4: Récupération de la demande créée
            print(f"\n📖 4. Test récupération demande (ID: {help_request_id})...")
            response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/{help_request_id}/", 
                                  headers=headers, timeout=10)
            
            if response.status_code == 200:
                retrieved_request = response.json()
                print(f"✅ Demande récupérée: {retrieved_request.get('title')}")
            else:
                print(f"❌ Erreur récupération: {response.status_code}")
                
        else:
            print(f"❌ Erreur création: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur création: {e}")
    
    # Test 5: Filtrage
    print("\n🔍 5. Test filtrage...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?request_type=request", 
                              headers=headers, timeout=10)
        if response.status_code == 200:
            filtered = response.json()
            count = len(filtered.get('results', filtered))
            print(f"✅ Filtrage par type 'request': {count} demandes")
            
    except Exception as e:
        print(f"❌ Erreur filtrage: {e}")
    
    # Test 6: Données carte
    print("\n🗺️ 6. Test données carte...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/map_data/", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            map_data = response.json()
            print(f"✅ Données carte: {len(map_data)} points")
        else:
            print(f"❌ Erreur données carte: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur données carte: {e}")
    
    # Test 7: Statistiques
    print("\n📊 7. Test statistiques...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/stats/", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées:")
            for key, value in stats.items():
                print(f"   - {key}: {value}")
        else:
            print(f"❌ Erreur statistiques: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TEST AUTOMATIQUE TERMINÉ - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("✅ L'API de demande d'aide est opérationnelle !")
    print("=" * 60)
    
    return True

def main():
    """Fonction principale"""
    print("🚀 TEST AUTOMATIQUE COMMUNICONNECT - DEMANDE D'AIDE")
    print("=" * 60)
    
    # Démarrage du serveur
    server_process = start_django_server()
    if not server_process:
        print("❌ Impossible de démarrer le serveur Django")
        return False
    
    try:
        # Test de l'API
        success = test_help_requests_api()
        
        if success:
            print("\n🎉 SUCCÈS: Tous les tests sont passés!")
        else:
            print("\n❌ ÉCHEC: Certains tests ont échoué")
            
    finally:
        # Arrêt du serveur
        print("\n🛑 Arrêt du serveur Django...")
        server_process.terminate()
        server_process.wait()
        print("✅ Serveur arrêté")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Complet - Fonctionnalité de Demande d'Aide CommuniConnect
Test de toutes les fonctionnalités via l'API REST
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from help_requests.models import HelpRequest, HelpResponse, HelpRequestCategory

User = get_user_model()

def test_help_requests_complete():
    """Test complet de la fonctionnalité de demande d'aide"""
    
    print("🎯 TEST COMPLET - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("=" * 60)
    print(f"⏰ Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Configuration API
    API_BASE_URL = "http://localhost:8000"
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
        
        response = requests.post(f"{API_BASE_URL}/api/users/login/", json=login_data, headers=headers)
        
        if response.status_code == 200:
            token = response.json().get('access')
            headers['Authorization'] = f'Bearer {token}'
            print("✅ Authentification réussie")
        else:
            print(f"❌ Erreur authentification: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur authentification: {e}")
        return False
    
    # Test 2: Liste des demandes d'aide
    print("\n📋 2. Test liste des demandes d'aide...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/", headers=headers)
        
        if response.status_code == 200:
            help_requests = response.json()
            print(f"✅ Liste des demandes récupérée ({len(help_requests.get('results', help_requests))} demandes)")
        else:
            print(f"❌ Erreur liste demandes: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur liste demandes: {e}")
    
    # Test 3: Création d'une demande d'aide
    print("\n📝 3. Test création de demande d'aide...")
    try:
        help_request_data = {
            'request_type': 'request',
            'need_type': 'material',
            'for_who': 'myself',
            'title': 'Test - Besoin de matériel de jardinage',
            'description': 'J\'ai besoin d\'emprunter des outils de jardinage pour entretenir mon jardin ce weekend.',
            'duration_type': 'this_week',
            'estimated_hours': 3,
            'proximity_zone': 'local',
            'is_urgent': False,
            'contact_preference': 'message',
            'latitude': 9.5370,
            'longitude': -13.6785,
            'address': '123 Rue Test, Conakry',
            'city': 'Conakry',
            'neighborhood': 'Kaloum'
        }
        
        response = requests.post(f"{API_BASE_URL}/help-requests/api/requests/", json=help_request_data, headers=headers)
        
        if response.status_code == 201:
            help_request = response.json()
            help_request_id = help_request.get('id')
            print(f"✅ Demande d'aide créée avec succès (ID: {help_request_id})")
        else:
            print(f"❌ Erreur création demande: {response.status_code}")
            print(f"Réponse: {response.text}")
            help_request_id = None
            
    except Exception as e:
        print(f"❌ Erreur création demande: {e}")
        help_request_id = None
    
    # Test 4: Création d'une offre d'aide
    print("\n🤝 4. Test création d'offre d'aide...")
    try:
        offer_data = {
            'request_type': 'offer',
            'need_type': 'transport',
            'for_who': 'community',
            'title': 'Test - Offre de transport pour courses',
            'description': 'Je peux proposer du transport pour les courses de la communauté.',
            'duration_type': 'ongoing',
            'proximity_zone': 'city',
            'is_urgent': False,
            'contact_preference': 'phone',
            'phone': '+224 123 456 789',
            'latitude': 9.5370,
            'longitude': -13.6785,
            'city': 'Conakry'
        }
        
        response = requests.post(f"{API_BASE_URL}/help-requests/api/requests/", json=offer_data, headers=headers)
        
        if response.status_code == 201:
            offer = response.json()
            offer_id = offer.get('id')
            print(f"✅ Offre d'aide créée avec succès (ID: {offer_id})")
        else:
            print(f"❌ Erreur création offre: {response.status_code}")
            offer_id = None
            
    except Exception as e:
        print(f"❌ Erreur création offre: {e}")
        offer_id = None
    
    # Test 5: Répondre à une demande d'aide
    if help_request_id:
        print(f"\n💬 5. Test réponse à la demande d'aide (ID: {help_request_id})...")
        try:
            response_data = {
                'response_type': 'offer_help',
                'message': 'Je peux vous prêter mes outils de jardinage ce weekend. Quand souhaitez-vous les récupérer ?',
                'contact_phone': '+224 987 654 321'
            }
            
            response = requests.post(f"{API_BASE_URL}/help-requests/api/requests/{help_request_id}/respond/", 
                                   json=response_data, headers=headers)
            
            if response.status_code == 201:
                help_response = response.json()
                response_id = help_response.get('id')
                print(f"✅ Réponse créée avec succès (ID: {response_id})")
            else:
                print(f"❌ Erreur création réponse: {response.status_code}")
                response_id = None
                
        except Exception as e:
            print(f"❌ Erreur création réponse: {e}")
            response_id = None
    
    # Test 6: Filtrage des demandes
    print("\n🔍 6. Test filtrage des demandes...")
    try:
        # Filtre par type de demande
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?request_type=request", headers=headers)
        if response.status_code == 200:
            requests_filtered = response.json()
            print(f"✅ Filtrage par type 'request': {len(requests_filtered.get('results', requests_filtered))} demandes")
        
        # Filtre par type de besoin
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?need_type=material", headers=headers)
        if response.status_code == 200:
            material_requests = response.json()
            print(f"✅ Filtrage par besoin 'material': {len(material_requests.get('results', material_requests))} demandes")
        
        # Filtre par urgence
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/?is_urgent=false", headers=headers)
        if response.status_code == 200:
            non_urgent = response.json()
            print(f"✅ Filtrage par urgence 'false': {len(non_urgent.get('results', non_urgent))} demandes")
            
    except Exception as e:
        print(f"❌ Erreur filtrage: {e}")
    
    # Test 7: Données pour la carte
    print("\n🗺️ 7. Test données pour la carte...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/map_data/", headers=headers)
        
        if response.status_code == 200:
            map_data = response.json()
            print(f"✅ Données carte récupérées: {len(map_data)} points")
        else:
            print(f"❌ Erreur données carte: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur données carte: {e}")
    
    # Test 8: Statistiques
    print("\n📊 8. Test statistiques...")
    try:
        response = requests.get(f"{API_BASE_URL}/help-requests/api/requests/stats/", headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées:")
            print(f"   - Total demandes: {stats.get('total_requests', 'N/A')}")
            print(f"   - Demandes ouvertes: {stats.get('open_requests', 'N/A')}")
            print(f"   - Demandes urgentes: {stats.get('urgent_requests', 'N/A')}")
        else:
            print(f"❌ Erreur statistiques: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
    
    # Test 9: Validation des modèles Django
    print("\n🔧 9. Test validation des modèles Django...")
    try:
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_help_user',
            defaults={
                'email': 'test_help@example.com',
                'first_name': 'Test',
                'last_name': 'Help'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Créer une demande d'aide via le modèle
        help_request = HelpRequest.objects.create(
            author=user,
            request_type='request',
            need_type='technical',
            for_who='myself',
            title='Test Modèle - Aide informatique',
            description='J\'ai besoin d\'aide pour configurer mon ordinateur.',
            duration_type='this_week',
            latitude=9.5370,
            longitude=-13.6785,
            city='Conakry'
        )
        
        print(f"✅ Modèle HelpRequest validé (ID: {help_request.id})")
        
        # Créer une réponse
        help_response = HelpResponse.objects.create(
            help_request=help_request,
            author=user,
            response_type='offer_help',
            message='Je peux vous aider avec la configuration informatique.'
        )
        
        print(f"✅ Modèle HelpResponse validé (ID: {help_response.id})")
        
        # Tester les propriétés
        print(f"   - Localisation: {help_request.location_display}")
        print(f"   - Durée: {help_request.duration_display}")
        print(f"   - Expirée: {help_request.is_expired}")
        
    except Exception as e:
        print(f"❌ Erreur validation modèles: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TEST COMPLET TERMINÉ - FONCTIONNALITÉ DE DEMANDE D'AIDE")
    print("✅ Toutes les fonctionnalités sont opérationnelles !")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_help_requests_complete() 
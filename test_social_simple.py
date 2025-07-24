#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple des Fonctionnalités Sociales - CommuniConnect
Test rapide des nouvelles fonctionnalités
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "test_social_nouveau@example.com"
TEST_USER_PASSWORD = "Test123!"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def test_server_connection():
    """Test de connexion au serveur"""
    print_header("Test de Connexion au Serveur")
    
    try:
        response = requests.get(f"{API_URL}/users/register/")
        if response.status_code in [200, 405]:
            print_success("Serveur accessible")
            return True
        else:
            print_error(f"Erreur serveur: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Impossible de se connecter au serveur: {e}")
        return False

def create_test_user():
    """Créer un utilisateur de test"""
    print_header("Création Utilisateur de Test")
    
    user_data = {
        'email': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD,
        'password_confirm': TEST_USER_PASSWORD,
        'first_name': 'Test',
        'last_name': 'Social',
        'username': 'test_social_nouveau'
    }
    
    try:
        response = requests.post(f"{API_URL}/users/register/", json=user_data)
        if response.status_code == 201:
            print_success("Utilisateur créé avec succès")
            return True
        else:
            print_error(f"Erreur création: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def login_user():
    """Connexion utilisateur"""
    print_header("Connexion Utilisateur")
    
    login_data = {
        'email': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{API_URL}/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            # Le token est dans tokens.access
            tokens = data.get('tokens', {})
            token = tokens.get('access')
            if token:
                print_success("Connexion réussie")
                return token
            else:
                print_error("Token manquant dans la réponse")
                print(f"Structure de la réponse: {list(data.keys())}")
                return None
        else:
            print_error(f"Erreur connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
    except Exception as e:
        print_error(f"Erreur: {e}")
        return None

def test_groups_api(token):
    """Test des API de groupes"""
    print_header("Test API Groupes")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test création de groupe
    group_data = {
        'name': 'Groupe Test Social',
        'description': 'Groupe de test pour les fonctionnalités sociales',
        'group_type': 'community',
        'privacy': 'public'
    }
    
    try:
        response = requests.post(f"{API_URL}/users/groups/", json=group_data, headers=headers)
        if response.status_code == 201:
            print_success("Groupe créé avec succès")
            group_id = response.json().get('id')
            return group_id
        else:
            print_error(f"Erreur création groupe: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
    except Exception as e:
        print_error(f"Erreur: {e}")
        return None

def test_events_api(token):
    """Test des API d'événements"""
    print_header("Test API Événements")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test création d'événement
    event_data = {
        'title': 'Événement Test Social',
        'description': 'Événement de test pour les fonctionnalités sociales',
        'event_type': 'meeting',
        'date': '2024-12-25T18:00:00Z',
        'location': 'Conakry, Guinée'
    }
    
    try:
        response = requests.post(f"{API_URL}/users/events/", json=event_data, headers=headers)
        if response.status_code == 201:
            print_success("Événement créé avec succès")
            return True
        else:
            print_error(f"Erreur création événement: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def test_suggestions_api(token):
    """Test des API de suggestions"""
    print_header("Test API Suggestions")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test suggestions de groupes
    try:
        response = requests.get(f"{API_URL}/users/suggested-groups/", headers=headers)
        if response.status_code == 200:
            print_success("Suggestions de groupes récupérées")
            return True
        else:
            print_error(f"Erreur suggestions groupes: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def run_complete_test():
    """Test complet"""
    print_header("TEST COMPLET DES FONCTIONNALITÉS SOCIALES")
    
    # Test connexion serveur
    if not test_server_connection():
        return
    
    # Créer utilisateur
    if not create_test_user():
        print_warning("Tentative de connexion avec utilisateur existant")
    
    # Connexion
    token = login_user()
    if not token:
        return
    
    # Test groupes
    group_id = test_groups_api(token)
    
    # Test événements
    test_events_api(token)
    
    # Test suggestions
    test_suggestions_api(token)
    
    print_header("TEST TERMINÉ")
    print_success("Tests des fonctionnalités sociales terminés")

if __name__ == "__main__":
    run_complete_test() 
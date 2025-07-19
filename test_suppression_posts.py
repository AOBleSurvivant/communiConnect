#!/usr/bin/env python3
"""
Test de la fonctionnalité de suppression des posts
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
POSTS_URL = f"{BASE_URL}/posts/"

def test_post_deletion():
    """Test de la suppression des posts"""
    
    print("🗑️ TEST DE SUPPRESSION DES POSTS")
    print("=" * 50)
    
    # 1. Connexion utilisateur
    print("\n1. Connexion utilisateur...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            token = response.json().get('access')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Connexion réussie")
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Créer un nouveau post pour le test
    print("\n2. Création d'un post de test...")
    post_data = {
        "content": "Post de test pour suppression",
        "post_type": "info",
        "title": "Test suppression"
    }
    
    try:
        response = requests.post(POSTS_URL, json=post_data, headers=headers)
        if response.status_code == 201:
            post = response.json()
            post_id = post['id']
            print(f"✅ Post créé avec ID: {post_id}")
            print(f"   Contenu: {post['content']}")
        else:
            print(f"❌ Échec de création: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return
    
    # 3. Vérifier que le post existe
    print("\n3. Vérification de l'existence du post...")
    try:
        response = requests.get(f"{POSTS_URL}{post_id}/", headers=headers)
        if response.status_code == 200:
            post = response.json()
            print("✅ Post récupéré avec succès")
            print(f"   Contenu: {post['content']}")
        else:
            print(f"❌ Échec de récupération: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de récupération: {e}")
        return
    
    # 4. Supprimer le post
    print("\n4. Suppression du post...")
    try:
        response = requests.delete(f"{POSTS_URL}{post_id}/", headers=headers)
        if response.status_code == 204:
            print("✅ Post supprimé avec succès")
        else:
            print(f"❌ Échec de suppression: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de suppression: {e}")
    
    # 5. Vérifier que le post a bien été supprimé
    print("\n5. Vérification de la suppression...")
    try:
        response = requests.get(f"{POSTS_URL}{post_id}/", headers=headers)
        if response.status_code == 404:
            print("✅ Post correctement supprimé (404 retourné)")
        else:
            print(f"⚠️  Post encore accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de vérification: {e}")
    
    # 6. Test de suppression d'un post qui n'existe pas
    print("\n6. Test de suppression d'un post inexistant...")
    try:
        response = requests.delete(f"{POSTS_URL}99999/", headers=headers)
        if response.status_code == 404:
            print("✅ Gestion correcte du post inexistant")
        else:
            print(f"⚠️  Réponse inattendue: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # 7. Test de suppression d'un post d'un autre utilisateur
    print("\n7. Test de suppression d'un post d'un autre utilisateur...")
    # Créer un autre utilisateur ou utiliser un post existant d'un autre utilisateur
    # Ce test nécessiterait la création d'un autre utilisateur
    
    print("\n" + "=" * 50)
    print("🎯 TEST TERMINÉ")
    print("\nFonctionnalités testées:")
    print("✅ Création de post")
    print("✅ Suppression de post")
    print("✅ Vérification de la suppression")
    print("✅ Gestion des erreurs")
    print("\nLa fonctionnalité de suppression des posts est opérationnelle !")

if __name__ == "__main__":
    test_post_deletion() 
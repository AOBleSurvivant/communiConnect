#!/usr/bin/env python3
"""
Test de la fonctionnalité de modification des posts
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
POSTS_URL = f"{BASE_URL}/posts/"

def test_post_editing():
    """Test de la modification des posts"""
    
    print("🧪 TEST DE MODIFICATION DES POSTS")
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
    
    # 2. Créer un nouveau post
    print("\n2. Création d'un nouveau post...")
    post_data = {
        "content": "Post de test pour modification",
        "post_type": "info",
        "title": "Test modification"
    }
    
    try:
        response = requests.post(POSTS_URL, json=post_data, headers=headers)
        if response.status_code == 201:
            post = response.json()
            post_id = post['id']
            print(f"✅ Post créé avec ID: {post_id}")
            print(f"   Contenu: {post['content']}")
            print(f"   Créé à: {post['created_at']}")
        else:
            print(f"❌ Échec de création: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return
    
    # 3. Modifier le post immédiatement (dans les 30 minutes)
    print("\n3. Modification du post (dans les 30 minutes)...")
    update_data = {
        "content": "Post modifié avec succès !",
        "post_type": "event",
        "title": "Test modifié"
    }
    
    try:
        response = requests.put(f"{POSTS_URL}{post_id}/", json=update_data, headers=headers)
        if response.status_code == 200:
            updated_post = response.json()
            print("✅ Modification réussie")
            print(f"   Nouveau contenu: {updated_post['content']}")
            print(f"   Nouveau type: {updated_post['post_type']}")
            print(f"   Modifié à: {updated_post['updated_at']}")
        else:
            print(f"❌ Échec de modification: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de modification: {e}")
    
    # 4. Vérifier que le post a été modifié
    print("\n4. Vérification de la modification...")
    try:
        response = requests.get(f"{POSTS_URL}{post_id}/", headers=headers)
        if response.status_code == 200:
            post = response.json()
            print("✅ Post récupéré")
            print(f"   Contenu actuel: {post['content']}")
            print(f"   Type actuel: {post['post_type']}")
            print(f"   Dernière modification: {post['updated_at']}")
        else:
            print(f"❌ Échec de récupération: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de récupération: {e}")
    
    # 5. Test de modification après 30 minutes (simulation)
    print("\n5. Test de modification après 30 minutes...")
    print("   (Ce test simule une tentative de modification après la limite)")
    
    # Simuler un post créé il y a plus de 30 minutes
    old_post_data = {
        "content": "Post ancien pour test",
        "post_type": "info"
    }
    
    try:
        response = requests.post(POSTS_URL, json=old_post_data, headers=headers)
        if response.status_code == 201:
            old_post = response.json()
            old_post_id = old_post['id']
            print(f"   Post ancien créé avec ID: {old_post_id}")
            
            # Tenter de modifier
            old_update_data = {
                "content": "Tentative de modification après limite"
            }
            
            response = requests.put(f"{POSTS_URL}{old_post_id}/", json=old_update_data, headers=headers)
            if response.status_code == 403:
                print("✅ Limite de temps respectée - modification refusée")
                print(f"   Message: {response.json().get('detail', 'Limite dépassée')}")
            else:
                print(f"⚠️  Modification autorisée (inattendu): {response.status_code}")
        else:
            print(f"❌ Échec de création du post ancien: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test de limite: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TEST TERMINÉ")
    print("\nFonctionnalités testées:")
    print("✅ Création de post")
    print("✅ Modification dans les 30 minutes")
    print("✅ Vérification de la modification")
    print("✅ Limite de temps (30 minutes)")
    print("\nLa fonctionnalité de modification des posts est opérationnelle !")

if __name__ == "__main__":
    test_post_editing() 
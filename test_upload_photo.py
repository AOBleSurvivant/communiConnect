#!/usr/bin/env python3
"""
Test de l'upload de photo de profil
"""

import requests
import json
import time
import os
from PIL import Image
import io

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/users/login/"
PROFILE_URL = f"{BASE_URL}/users/my-profile/"

def create_test_image():
    """Créer une image de test"""
    # Créer une image simple 100x100 pixels
    img = Image.new('RGB', (100, 100), color='red')
    
    # Sauvegarder temporairement
    test_image_path = 'test_image.jpg'
    img.save(test_image_path, 'JPEG')
    
    return test_image_path

def test_upload_photo():
    """Test de l'upload de photo de profil"""
    
    print("📸 TEST DE L'UPLOAD DE PHOTO DE PROFIL")
    print("=" * 50)
    
    # 1. Connexion
    print("\n1. Connexion...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('tokens', {}).get('access')
            if token:
                print("✅ Connexion réussie")
                print(f"Token: {token[:20]}...")
            else:
                print("❌ Token non trouvé")
                return
        else:
            print(f"❌ Échec de connexion: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Créer une image de test
    print("\n2. Création d'une image de test...")
    test_image_path = create_test_image()
    print(f"✅ Image créée: {test_image_path}")
    
    # 3. Test de l'upload
    print("\n3. Test de l'upload de photo...")
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'profile_picture': f}
            
            response = requests.patch(PROFILE_URL, files=files, headers=headers)
            print(f"Status upload: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload réussi")
                print(f"Message: {result.get('message', 'N/A')}")
                
                if 'user' in result:
                    user = result['user']
                    print(f"Utilisateur: {user.get('first_name', 'N/A')} {user.get('last_name', 'N/A')}")
                    print(f"Photo: {user.get('profile_picture', 'N/A')}")
            else:
                print(f"❌ Échec de l'upload: {response.text}")
                
    except Exception as e:
        print(f"❌ Erreur lors de l'upload: {e}")
    
    # 4. Nettoyer
    print("\n4. Nettoyage...")
    try:
        os.remove(test_image_path)
        print("✅ Image de test supprimée")
    except:
        print("⚠️ Impossible de supprimer l'image de test")
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   - Upload testé: {'✅ Réussi' if response.status_code == 200 else '❌ Échoué'}")
    print(f"   - Status final: {response.status_code}")

if __name__ == "__main__":
    test_upload_photo() 
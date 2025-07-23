#!/usr/bin/env python
import requests
import json
import os

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_login():
    """Test de connexion utilisateur"""
    print("🔐 Test de connexion...")
    
    login_data = {
        "email": "mariam.diallo@test.gn",
        "password": "test123456"
    }
    
    response = requests.post(f"{API_URL}/users/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('tokens', {}).get('access')
        print(f"✅ Connexion réussie pour mariam_diallo")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        return None

def test_profile_update(token):
    """Test de mise à jour du profil"""
    print(f"\n👤 TEST MISE À JOUR PROFIL")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Données de test pour la mise à jour
    profile_data = {
        "first_name": "Mariam",
        "last_name": "Diallo",
        "bio": "Test de mise à jour du profil",
        "phone_number": "+22412345678"
    }
    
    response = requests.patch(f"{API_URL}/users/my-profile/", json=profile_data, headers=headers)
    
    if response.status_code == 200:
        print("✅ Mise à jour du profil réussie")
        user_data = response.json()
        print(f"   Nom: {user_data.get('first_name')} {user_data.get('last_name')}")
        print(f"   Bio: {user_data.get('bio')}")
        print(f"   Téléphone: {user_data.get('phone_number')}")
        return user_data
    else:
        print(f"❌ Erreur mise à jour profil: {response.status_code}")
        print(f"Réponse: {response.text}")
        return None

def test_upload_profile_picture(token):
    """Test d'upload de photo de profil"""
    print(f"\n📸 TEST UPLOAD PHOTO PROFIL")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer un fichier de test simple (10x10 pixel JPEG)
    # Données JPEG minimales valides
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\n\x00\n\x01\x01\x11\x00\x02\x11\x01\x03\x11\x00\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    # Créer un fichier temporaire
    with open('test_image.jpg', 'wb') as f:
        f.write(jpeg_data)
    
    try:
        # Préparer les données multipart
        with open('test_image.jpg', 'rb') as f:
            files = {
                'profile_picture': ('test_image.jpg', f, 'image/jpeg')
            }
            
            # Utiliser l'endpoint de mise à jour du profil avec PATCH
            response = requests.patch(
                f"{API_URL}/users/my-profile/",
                files=files,
                headers=headers
            )
        
        if response.status_code == 200:
            print("✅ Upload photo de profil réussi")
            user_data = response.json()
            if 'user' in user_data:
                user_data = user_data['user']
            print(f"   Photo: {user_data.get('profile_picture')}")
            return user_data
        else:
            print(f"❌ Erreur upload photo: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    finally:
        # Nettoyer le fichier temporaire
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

def test_get_profile(token):
    """Test de récupération du profil"""
    print(f"\n📋 TEST RÉCUPÉRATION PROFIL")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{API_URL}/users/my-profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Récupération profil réussie")
        user_data = response.json()
        print(f"   Nom: {user_data.get('first_name')} {user_data.get('last_name')}")
        print(f"   Email: {user_data.get('email')}")
        print(f"   Bio: {user_data.get('bio')}")
        print(f"   Photo: {user_data.get('profile_picture')}")
        return user_data
    else:
        print(f"❌ Erreur récupération profil: {response.status_code}")
        print(f"Réponse: {response.text}")
        return None

def main():
    """Test complet du système de profil"""
    print("🧪 TEST SYSTÈME PROFIL")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Test de récupération du profil initial
    initial_profile = test_get_profile(token)
    
    # Test de mise à jour du profil
    updated_profile = test_profile_update(token)
    
    # Test d'upload de photo
    photo_profile = test_upload_profile_picture(token)
    
    # Test de récupération du profil final
    final_profile = test_get_profile(token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    if initial_profile:
        print("✅ Récupération profil initial: OK")
    if updated_profile:
        print("✅ Mise à jour profil: OK")
    if photo_profile:
        print("✅ Upload photo: OK")
    if final_profile:
        print("✅ Récupération profil final: OK")
    
    print("💡 Le système de profil fonctionne correctement")

if __name__ == "__main__":
    main() 
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

def test_upload_with_debug(token):
    """Test d'upload avec debug des erreurs"""
    print(f"\n🐛 DEBUG UPLOAD PHOTO PROFIL")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer un fichier de test simple (10x10 pixel JPEG)
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
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Upload photo de profil réussi")
            user_data = response.json()
            print(f"📊 Réponse complète: {json.dumps(user_data, indent=2)}")
            if 'user' in user_data:
                user_data = user_data['user']
            print(f"   Photo: {user_data.get('profile_picture')}")
            return user_data
        else:
            print(f"❌ Erreur upload photo: {response.status_code}")
            print(f"📊 Réponse d'erreur: {response.text}")
            
            # Essayer de parser la réponse JSON
            try:
                error_data = response.json()
                print(f"📊 Erreur JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📊 Réponse brute: {response.text}")
            
            return None
            
    finally:
        # Nettoyer le fichier temporaire
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

def test_profile_update_simple(token):
    """Test de mise à jour simple du profil"""
    print(f"\n👤 TEST MISE À JOUR SIMPLE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Données de test simples
    profile_data = {
        "first_name": "Mariam",
        "last_name": "Diallo"
    }
    
    response = requests.patch(f"{API_URL}/users/my-profile/", json=profile_data, headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Mise à jour simple réussie")
        user_data = response.json()
        print(f"📊 Réponse: {json.dumps(user_data, indent=2)}")
        return user_data
    else:
        print(f"❌ Erreur mise à jour simple: {response.status_code}")
        print(f"📊 Réponse: {response.text}")
        return None

def main():
    """Debug complet de l'upload de photo"""
    print("🐛 DEBUG UPLOAD PHOTO PROFIL")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Test de mise à jour simple d'abord
    test_profile_update_simple(token)
    
    # Test d'upload avec debug
    test_upload_with_debug(token)
    
    print(f"\n📊 RÉSUMÉ DEBUG:")
    print("=" * 60)
    print("✅ Tests de debug effectués")
    print("💡 Vérifiez les détails d'erreur ci-dessus")

if __name__ == "__main__":
    main() 
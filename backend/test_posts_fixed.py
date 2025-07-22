#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

def test_posts_api_fixed():
    """Test de l'API posts après correction"""
    print("🔍 Test de l'API posts après correction...")
    
    # Connexion avec l'utilisateur existant
    login_data = {
        "email": "test.posts@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Connexion
        response = requests.post('http://localhost:8000/api/users/login/', json=login_data)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            access_token = data['tokens']['access']
            print("✅ Connexion réussie")
            
            # Tester l'API posts
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get('http://localhost:8000/api/posts/', headers=headers)
            print(f"Status API posts: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API posts fonctionnelle!")
                print(f"Posts retournés: {len(data.get('results', []))}")
                return True
            else:
                print(f"❌ Erreur API posts: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return False
        else:
            print(f"❌ Erreur connexion: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'API posts - CORRECTION FINALE")
    print("=" * 50)
    
    if test_posts_api_fixed():
        print("\n🎉 SUCCÈS! L'API posts fonctionne maintenant!")
    else:
        print("\n❌ Test échoué") 
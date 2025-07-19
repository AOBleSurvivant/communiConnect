#!/usr/bin/env python
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Media
from users.models import User

def test_media_upload_response():
    """Test pour voir la réponse de l'upload de média"""
    
    # Récupérer un média existant pour voir sa structure
    media = Media.objects.filter(approval_status='approved').first()
    
    if media:
        print("=== STRUCTURE D'UN MÉDIA ===")
        print(f"ID: {media.id}")
        print(f"Titre: {media.title}")
        print(f"Type: {media.media_type}")
        print(f"Statut: {media.approval_status}")
        print(f"Approprié: {media.is_appropriate}")
        print(f"URL: {media.file_url}")
        print(f"Créé: {media.created_at}")
        
        # Simuler la réponse de l'API
        response_data = {
            'id': media.id,
            'title': media.title,
            'media_type': media.media_type,
            'approval_status': media.approval_status,
            'is_appropriate': media.is_appropriate,
            'file_url': media.file_url,
            'created_at': media.created_at.isoformat()
        }
        
        print("\n=== RÉPONSE API SIMULÉE ===")
        print(json.dumps(response_data, indent=2))
        
        # Vérifier si l'ID est bien présent
        print(f"\nID extrait: {response_data.get('id')}")
        print(f"Type de l'ID: {type(response_data.get('id'))}")
        
    else:
        print("Aucun média approuvé trouvé")

if __name__ == "__main__":
    test_media_upload_response() 
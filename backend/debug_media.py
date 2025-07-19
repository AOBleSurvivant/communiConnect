#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Media

def debug_media_status():
    """Affiche le statut de tous les médias"""
    print("=== STATUT DES MÉDIAS ===")
    medias = Media.objects.all().order_by('-created_at')
    
    for media in medias:
        print(f"ID: {media.id}")
        print(f"  Titre: {media.title}")
        print(f"  Type: {media.media_type}")
        print(f"  Statut: {media.approval_status}")
        print(f"  Approprié: {media.is_appropriate}")
        print(f"  Score: {media.moderation_score}")
        print(f"  Créé: {media.created_at}")
        print(f"  URL: {media.file_url}")
        print("---")

if __name__ == "__main__":
    debug_media_status() 
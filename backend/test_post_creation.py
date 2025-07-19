#!/usr/bin/env python
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post, Media
from users.models import User

def test_post_creation_with_media():
    """Test de création d'un post avec des médias"""
    
    # Récupérer un utilisateur et des médias existants
    user = User.objects.first()
    medias = Media.objects.filter(approval_status='approved')[:3]
    
    if not user:
        print("Aucun utilisateur trouvé")
        return
    
    if not medias:
        print("Aucun média approuvé trouvé")
        return
    
    print(f"Utilisateur: {user.username}")
    print(f"Médias disponibles: {[m.id for m in medias]}")
    
    # Créer un post avec des médias
    post_data = {
        'content': 'Test post avec médias',
        'post_type': 'info',
        'media_files': [m.id for m in medias]
    }
    
    print(f"Données du post: {post_data}")
    
    # Créer le post
    post = Post.objects.create(
        author=user,
        quartier=user.quartier,
        content=post_data['content'],
        post_type=post_data['post_type']
    )
    
    # Associer les médias
    post.media_files.set(medias)
    
    print(f"Post créé: {post.id}")
    print(f"Médias associés: {post.media_files.count()}")
    
    for media in post.media_files.all():
        print(f"  - Média {media.id}: {media.title}")

if __name__ == "__main__":
    test_post_creation_with_media() 
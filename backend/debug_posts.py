#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post, Media

def debug_posts_and_media():
    """Affiche les posts et leurs médias associés"""
    print("=== POSTS ET MÉDIAS ===")
    posts = Post.objects.all().order_by('-created_at')
    
    for post in posts:
        print(f"Post ID: {post.id}")
        print(f"  Auteur: {post.author.username}")
        print(f"  Contenu: {post.content[:50]}...")
        print(f"  Type: {post.post_type}")
        print(f"  Créé: {post.created_at}")
        print(f"  Médias associés: {post.media_files.count()}")
        
        for media in post.media_files.all():
            print(f"    - Média ID: {media.id}, Titre: {media.title}, Statut: {media.approval_status}")
        
        print("---")

if __name__ == "__main__":
    debug_posts_and_media() 
#!/usr/bin/env python3
"""
Test script pour vérifier l'upload des vidéos live
"""

import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post, Media
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

def test_video_upload():
    """Test principal"""
    print("🎬 TEST UPLOAD VIDÉO LIVE")
    print("=" * 40)
    
    # Vérifier les posts live récents
    recent_live_posts = Post.objects.filter(
        is_live_post=False,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')[:10]
    
    print(f"📊 Posts live récents (24h): {recent_live_posts.count()}")
    
    for post in recent_live_posts:
        print(f"\n📊 Post {post.id}:")
        print(f"   Contenu: {post.content[:50]}...")
        print(f"   Type: {post.post_type}")
        print(f"   Live: {post.is_live_post}")
        print(f"   Médias: {post.media_files.count()}")
        
        media_files = post.media_files.all()
        for media in media_files:
            print(f"   📹 Média {media.id}:")
            print(f"      Type: {media.media_type}")
            print(f"      Titre: {media.title}")
            print(f"      Live recording: {media.is_live_recording}")
            print(f"      Fichier: {media.file.name if media.file else 'N/A'}")
            print(f"      URL: {media.cdn_url[:50] if media.cdn_url else 'N/A'}...")
            print(f"      Taille: {media.file_size} bytes")
    
    # Vérifier les vidéos avec fichiers
    videos_with_files = Media.objects.filter(
        Q(media_type='video') & 
        Q(is_live_recording=True) & 
        Q(file__isnull=False)
    )
    
    print(f"\n🎥 Vidéos avec fichiers uploadés: {videos_with_files.count()}")
    
    for video in videos_with_files:
        print(f"   📹 Vidéo {video.id}: {video.title}")
        print(f"      Fichier: {video.file.name}")
        print(f"      Taille: {video.file_size} bytes")
        print(f"      Post: {video.live_post.id if video.live_post else 'N/A'}")

if __name__ == "__main__":
    test_video_upload() 
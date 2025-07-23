#!/usr/bin/env python3
"""
Test script pour vérifier la sauvegarde des vidéos et l'apparition dans le feed
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

def test_video_saving():
    """Test principal"""
    print("🎬 TEST DE SAUVEGARDE VIDÉO")
    print("=" * 40)
    
    # Vérifier les posts avec vidéos
    posts_with_videos = Post.objects.filter(media_files__isnull=False).distinct()
    print(f"📹 Posts avec médias: {posts_with_videos.count()}")
    
    # Vérifier les vidéos live
    live_videos = Media.objects.filter(
        Q(media_type='video') & Q(is_live_recording=True)
    )
    print(f"🎥 Vidéos live enregistrées: {live_videos.count()}")
    
    # Analyser chaque post avec vidéo
    for post in posts_with_videos:
        print(f"\n📊 Post {post.id}:")
        print(f"   Contenu: {post.content[:50]}...")
        print(f"   Type: {post.post_type}")
        print(f"   Live: {post.is_live_post}")
        print(f"   Médias: {post.media_files.count()}")
        
        for media in post.media_files.all():
            print(f"   📹 Média {media.id}:")
            print(f"      Type: {media.media_type}")
            print(f"      Titre: {media.title}")
            print(f"      Live recording: {media.is_live_recording}")
            print(f"      URL: {media.cdn_url[:50] if media.cdn_url else 'N/A'}...")
    
    # Vérifier les posts live récents
    recent_live_posts = Post.objects.filter(
        is_live_post=False,
        created_at__gte=django.utils.timezone.now() - django.utils.timezone.timedelta(hours=24)
    ).order_by('-created_at')[:5]
    
    print(f"\n🕐 Posts récents (24h): {recent_live_posts.count()}")
    for post in recent_live_posts:
        print(f"   - ID {post.id}: {post.content[:30]}... (Live: {post.is_live_post})")

if __name__ == "__main__":
    test_video_saving() 
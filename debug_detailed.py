#!/usr/bin/env python3
"""
Script de debug détaillé pour identifier les problèmes exacts
"""

import requests
import json
import traceback

BASE_URL = "http://localhost:8000"
API_BASE_URL = f"{BASE_URL}/api"

def authenticate():
    """Authentifier l'utilisateur"""
    login_data = {
        "email": "test_1753258346@communiconnect.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{API_BASE_URL}/users/login/", json=login_data)
    if response.status_code == 200:
        data = response.json()
        return data.get('tokens', {}).get('access')
    return None

def test_analytics_post_detailed(token):
    """Test détaillé analytics de post"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Récupérer un post
    posts_response = requests.get(f"{API_BASE_URL}/posts/", headers=headers)
    if posts_response.status_code == 200:
        posts_data = posts_response.json()
        posts = posts_data.get('results', [])
        
        if len(posts) > 0:
            post_id = posts[0]['id']
            print(f"Testing analytics for post ID: {post_id}")
            
            # Test analytics
            response = requests.get(f"{API_BASE_URL}/posts/posts/{post_id}/analytics/", headers=headers)
            
            print(f"Analytics response status: {response.status_code}")
            print(f"Analytics response headers: {dict(response.headers)}")
            print(f"Analytics response: {response.text[:500]}...")
            
            return response.status_code == 200
    return False

def test_share_post_detailed(token):
    """Test détaillé partage de post"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Récupérer un post
    posts_response = requests.get(f"{API_BASE_URL}/posts/", headers=headers)
    if posts_response.status_code == 200:
        posts_data = posts_response.json()
        posts = posts_data.get('results', [])
        
        if len(posts) > 0:
            post_id = posts[0]['id']
            print(f"Testing share for post ID: {post_id}")
            
            # Test partage
            share_data = {
                "message": "Post partagé pour test"
            }
            
            response = requests.post(f"{API_BASE_URL}/posts/posts/{post_id}/share/", 
                                  json=share_data, headers=headers)
            
            print(f"Share response status: {response.status_code}")
            print(f"Share response headers: {dict(response.headers)}")
            print(f"Share response: {response.text[:500]}...")
            
            return response.status_code == 201
    return False

def test_external_share_detailed(token):
    """Test détaillé partage externe"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Récupérer un post
    posts_response = requests.get(f"{API_BASE_URL}/posts/", headers=headers)
    if posts_response.status_code == 200:
        posts_data = posts_response.json()
        posts = posts_data.get('results', [])
        
        if len(posts) > 0:
            post_id = posts[0]['id']
            print(f"Testing external share for post ID: {post_id}")
            
            # Test partage externe
            share_data = {
                "platform": "whatsapp",
                "message": "Post partagé sur WhatsApp"
            }
            
            response = requests.post(f"{API_BASE_URL}/posts/posts/{post_id}/share-external/", 
                                  json=share_data, headers=headers)
            
            print(f"External share response status: {response.status_code}")
            print(f"External share response headers: {dict(response.headers)}")
            print(f"External share response: {response.text[:500]}...")
            
            return response.status_code == 201
    return False

def test_live_streaming_detailed(token):
    """Test détaillé live streaming"""
    headers = {'Authorization': f'Bearer {token}'}
    
    live_data = {
        "title": "Test live streaming",
        "description": "Test de la fonctionnalité live"
    }
    
    response = requests.post(f"{API_BASE_URL}/posts/live/start/", 
                           json=live_data, headers=headers)
    
    print(f"Live streaming response status: {response.status_code}")
    print(f"Live streaming response headers: {dict(response.headers)}")
    print(f"Live streaming response: {response.text[:500]}...")
    
    return response.status_code == 201

def main():
    """Fonction principale"""
    print("🔍 DEBUG DÉTAILLÉ DES ERREURS 500")
    print("=" * 60)
    
    # Authentifier
    token = authenticate()
    if not token:
        print("❌ Impossible de s'authentifier")
        return
    
    print("✅ Authentification réussie")
    
    # Test analytics de post
    print("\n🧪 TEST ANALYTICS DE POST (DÉTAILLÉ)")
    print("-" * 50)
    test_analytics_post_detailed(token)
    
    # Test partage de post
    print("\n🧪 TEST PARTAGE DE POST (DÉTAILLÉ)")
    print("-" * 50)
    test_share_post_detailed(token)
    
    # Test partage externe
    print("\n🧪 TEST PARTAGE EXTERNE (DÉTAILLÉ)")
    print("-" * 50)
    test_external_share_detailed(token)
    
    # Test live streaming
    print("\n🧪 TEST LIVE STREAMING (DÉTAILLÉ)")
    print("-" * 50)
    test_live_streaming_detailed(token)

if __name__ == "__main__":
    main() 
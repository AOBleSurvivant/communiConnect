#!/usr/bin/env python
import requests
import json

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

def verifier_analytics_post(token, post_id):
    """Vérifier les analytics d'un post"""
    print(f"\n📊 VÉRIFICATION ANALYTICS POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/posts/{post_id}/analytics/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analytics récupérées avec succès")
            print(f"📊 Données analytics:")
            print(f"   Post ID: {data.get('post', {}).get('id')}")
            print(f"   Total vues: {data.get('total_views', 0)}")
            print(f"   Vues uniques: {data.get('unique_views', 0)}")
            print(f"   Total likes: {data.get('total_likes', 0)}")
            print(f"   Total commentaires: {data.get('total_comments', 0)}")
            print(f"   Total partages: {data.get('total_shares', 0)}")
            print(f"   Total partages externes: {data.get('total_external_shares', 0)}")
            print(f"   Score viral: {data.get('viral_score', 0)}")
            print(f"   Taux d'engagement: {data.get('engagement_rate', 0)}")
            print(f"   Multiplicateur de portée: {data.get('reach_multiplier', 0)}")
            
            # Détails des partages externes
            external_shares = data.get('external_shares_breakdown', {})
            if external_shares:
                print(f"   📤 Partages externes:")
                for platform, count in external_shares.items():
                    print(f"      - {platform}: {count}")
            
            return data
        else:
            print(f"❌ Erreur récupération analytics: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_analytics_utilisateur(token):
    """Vérifier les analytics de l'utilisateur"""
    print(f"\n👤 VÉRIFICATION ANALYTICS UTILISATEUR")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/analytics/user/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analytics utilisateur récupérées avec succès")
            print(f"📊 Données analytics utilisateur:")
            print(f"   Total posts: {data.get('total_posts', 0)}")
            print(f"   Total vues: {data.get('total_views', 0)}")
            print(f"   Total likes: {data.get('total_likes', 0)}")
            print(f"   Total commentaires: {data.get('total_comments', 0)}")
            print(f"   Total partages: {data.get('total_shares', 0)}")
            print(f"   Total partages externes: {data.get('total_external_shares', 0)}")
            print(f"   Score viral moyen: {data.get('average_viral_score', 0)}")
            print(f"   Taux d'engagement moyen: {data.get('average_engagement_rate', 0)}")
            
            # Posts les plus performants
            top_posts = data.get('top_performing_posts', [])
            if top_posts:
                print(f"   🏆 Posts les plus performants:")
                for i, post in enumerate(top_posts[:3]):
                    print(f"      {i+1}. Post ID: {post.get('post', {}).get('id')}")
                    print(f"         Score viral: {post.get('viral_score', 0)}")
                    print(f"         Taux d'engagement: {post.get('engagement_rate', 0)}")
            
            return data
        else:
            print(f"❌ Erreur récupération analytics utilisateur: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_analytics_communaute(token):
    """Vérifier les analytics de la communauté"""
    print(f"\n🏘️ VÉRIFICATION ANALYTICS COMMUNAUTÉ")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/analytics/community/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analytics communauté récupérées avec succès")
            print(f"📊 Données analytics communauté:")
            print(f"   Total posts: {data.get('total_posts', 0)}")
            print(f"   Total vues: {data.get('total_views', 0)}")
            print(f"   Total likes: {data.get('total_likes', 0)}")
            print(f"   Total commentaires: {data.get('total_comments', 0)}")
            print(f"   Total partages: {data.get('total_shares', 0)}")
            print(f"   Total partages externes: {data.get('total_external_shares', 0)}")
            print(f"   Score viral moyen: {data.get('average_viral_score', 0)}")
            print(f"   Taux d'engagement moyen: {data.get('average_engagement_rate', 0)}")
            print(f"   Posts viraux: {data.get('viral_posts_count', 0)}")
            print(f"   Posts populaires: {data.get('popular_posts_count', 0)}")
            
            # Répartition par plateforme
            platform_breakdown = data.get('platform_breakdown', {})
            if platform_breakdown:
                print(f"   📱 Répartition par plateforme:")
                for platform, count in platform_breakdown.items():
                    print(f"      - {platform}: {count}")
            
            # Posts les plus performants
            top_posts = data.get('top_performing_posts', [])
            if top_posts:
                print(f"   🏆 Posts les plus performants:")
                for i, post in enumerate(top_posts[:3]):
                    print(f"      {i+1}. Post ID: {post.get('post', {}).get('id')}")
                    print(f"         Score viral: {post.get('viral_score', 0)}")
                    print(f"         Taux d'engagement: {post.get('engagement_rate', 0)}")
            
            return data
        else:
            print(f"❌ Erreur récupération analytics communauté: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_endpoints_analytics():
    """Vérifier les endpoints d'analytics"""
    print("\n🔗 VÉRIFICATION ENDPOINTS ANALYTICS")
    print("=" * 60)
    
    endpoints = [
        f"{API_URL}/posts/posts/1/analytics/",
        f"{API_URL}/posts/analytics/user/",
        f"{API_URL}/posts/analytics/community/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)}")

def main():
    """Diagnostic complet du système d'analytics"""
    print("📊 DIAGNOSTIC SYSTÈME ANALYTICS")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier les endpoints
    verifier_endpoints_analytics()
    
    # Vérifier les analytics d'un post spécifique
    post_id = 410  # Post existant
    analytics_post = verifier_analytics_post(token, post_id)
    
    # Vérifier les analytics utilisateur
    analytics_user = verifier_analytics_utilisateur(token)
    
    # Vérifier les analytics communauté
    analytics_community = verifier_analytics_communaute(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ Endpoints analytics vérifiés")
    print(f"✅ Analytics post testées")
    print(f"✅ Analytics utilisateur testées")
    print(f"✅ Analytics communauté testées")
    print(f"💡 Si les analytics ne fonctionnent pas:")
    print(f"   1. Vérifiez les endpoints API")
    print(f"   2. Vérifiez la base de données")
    print(f"   3. Vérifiez les permissions")
    print(f"   4. Vérifiez le frontend")

if __name__ == "__main__":
    main() 
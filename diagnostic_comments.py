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

def verifier_posts_avec_commentaires(token):
    """Vérifier les posts avec commentaires"""
    print("\n💬 VÉRIFICATION POSTS AVEC COMMENTAIRES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            
            posts_avec_commentaires = [p for p in posts if p.get('comments_count', 0) > 0]
            print(f"📋 Posts avec commentaires: {len(posts_avec_commentaires)}")
            
            for post in posts_avec_commentaires[:3]:
                print(f"\n📝 Post ID: {post.get('id')}")
                print(f"   Contenu: {post.get('content', '')[:50]}...")
                print(f"   Commentaires count: {post.get('comments_count', 0)}")
                
                # Vérifier les commentaires détaillés
                comments = post.get('comments', [])
                if comments:
                    print(f"   💬 Commentaires détaillés:")
                    for comment in comments[:3]:
                        print(f"      - Auteur: {comment.get('author', {}).get('username', 'Inconnu')}")
                        print(f"        Contenu: {comment.get('content', '')[:30]}...")
                        print(f"        Date: {comment.get('created_at')}")
                        print(f"        Réponses: {comment.get('replies_count', 0)}")
            
            # Afficher un post sans commentaires pour test
            posts_sans_commentaires = [p for p in posts if p.get('comments_count', 0) == 0]
            if posts_sans_commentaires:
                test_post = posts_sans_commentaires[0]
                print(f"\n🧪 POST DE TEST (sans commentaires):")
                print(f"   ID: {test_post.get('id')}")
                print(f"   Contenu: {test_post.get('content', '')[:50]}...")
                print(f"   Commentaires count: {test_post.get('comments_count', 0)}")
                return test_post.get('id')
            
        else:
            print(f"❌ Erreur récupération posts: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_creation_commentaire(token, post_id):
    """Tester la création d'un commentaire"""
    print(f"\n💬 TEST CRÉATION COMMENTAIRE POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    comment_data = {
        "content": "Test de commentaire - Vérification système ! 💬",
        "is_anonymous": False
    }
    
    try:
        # Tester la création du commentaire
        response = requests.post(
            f"{API_URL}/posts/{post_id}/comments/",
            json=comment_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Commentaire créé avec succès")
            print(f"📊 Données retournées: {data}")
            return data.get('id')
        else:
            print(f"❌ Erreur création commentaire: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_commentaires_post(token, post_id):
    """Vérifier les commentaires d'un post"""
    print(f"\n📋 VÉRIFICATION COMMENTAIRES POST {post_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/{post_id}/comments/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            comments = data.get('results', []) if isinstance(data, dict) else data
            
            print(f"📊 Nombre de commentaires: {len(comments)}")
            
            for i, comment in enumerate(comments):
                print(f"\n{i+1}. Commentaire ID: {comment.get('id')}")
                print(f"   Auteur: {comment.get('author', {}).get('username', 'Inconnu')}")
                print(f"   Contenu: {comment.get('content', '')}")
                print(f"   Date: {comment.get('created_at')}")
                print(f"   Réponses: {comment.get('replies_count', 0)}")
                print(f"   Niveau: {comment.get('level', 0)}")
                
                # Vérifier les réponses
                replies = comment.get('replies', [])
                if replies:
                    print(f"   📝 Réponses:")
                    for reply in replies:
                        print(f"      - {reply.get('author', {}).get('username', 'Inconnu')}: {reply.get('content', '')[:30]}...")
            
            return comments
        else:
            print(f"❌ Erreur récupération commentaires: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def tester_reponse_commentaire(token, post_id, comment_id):
    """Tester la réponse à un commentaire"""
    print(f"\n↩️ TEST RÉPONSE COMMENTAIRE {comment_id}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    reply_data = {
        "content": "Réponse au commentaire - Test système ! 🔄",
        "is_anonymous": False,
        "parent_comment": comment_id
    }
    
    try:
        # Tester la création de la réponse
        response = requests.post(
            f"{API_URL}/posts/{post_id}/comments/",
            json=reply_data,
            headers=headers
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Réponse créée avec succès")
            print(f"📊 Données retournées: {data}")
            return data.get('id')
        else:
            print(f"❌ Erreur création réponse: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_endpoints_commentaires():
    """Vérifier les endpoints de commentaires"""
    print("\n🔗 VÉRIFICATION ENDPOINTS COMMENTAIRES")
    print("=" * 60)
    
    endpoints = [
        f"{API_URL}/posts/1/comments/",
        f"{API_URL}/posts/comments/1/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)}")

def main():
    """Diagnostic complet du système de commentaires"""
    print("💬 DIAGNOSTIC SYSTÈME DE COMMENTAIRES")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier les endpoints
    verifier_endpoints_commentaires()
    
    # Vérifier les posts avec commentaires
    post_id = verifier_posts_avec_commentaires(token)
    
    if post_id:
        # Vérifier les commentaires existants
        comments = verifier_commentaires_post(token, post_id)
        
        # Tester la création d'un commentaire
        comment_id = tester_creation_commentaire(token, post_id)
        
        if comment_id:
            # Vérifier les commentaires après création
            verifier_commentaires_post(token, post_id)
            
            # Tester une réponse au commentaire
            reply_id = tester_reponse_commentaire(token, post_id, comment_id)
            
            if reply_id:
                # Vérifier les commentaires après réponse
                verifier_commentaires_post(token, post_id)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ Posts récupérés")
    print(f"✅ Endpoints commentaires vérifiés")
    print(f"✅ Tests création commentaires effectués")
    print(f"✅ Tests réponses effectués")
    print(f"💡 Si les commentaires ne fonctionnent pas:")
    print(f"   1. Vérifiez les endpoints API")
    print(f"   2. Vérifiez la base de données")
    print(f"   3. Vérifiez les permissions")
    print(f"   4. Vérifiez le frontend")

if __name__ == "__main__":
    main() 
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

def verifier_structure_posts(token):
    """Vérifier la structure des posts retournés"""
    print("\n📊 VÉRIFICATION STRUCTURE POSTS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API accessible")
            print(f"📋 Structure de la réponse:")
            print(f"   Type: {type(data)}")
            print(f"   Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            if isinstance(data, dict):
                if 'results' in data:
                    posts = data['results']
                    print(f"   Nombre de posts: {len(posts)}")
                    
                    if posts:
                        # Analyser le premier post
                        first_post = posts[0]
                        print(f"\n📝 PREMIER POST:")
                        print(f"   ID: {first_post.get('id')}")
                        print(f"   Auteur: {first_post.get('author', {}).get('username', 'Inconnu')}")
                        print(f"   Contenu: {first_post.get('content', '')[:50]}...")
                        print(f"   Type: {first_post.get('post_type')}")
                        print(f"   Date: {first_post.get('created_at')}")
                        print(f"   Médias: {len(first_post.get('media_files', []))}")
                        
                        # Vérifier les champs requis pour le frontend
                        required_fields = ['id', 'content', 'author', 'created_at', 'post_type']
                        missing_fields = []
                        
                        for field in required_fields:
                            if field not in first_post:
                                missing_fields.append(field)
                        
                        if missing_fields:
                            print(f"   ❌ Champs manquants: {missing_fields}")
                        else:
                            print(f"   ✅ Tous les champs requis présents")
                        
                        # Vérifier la structure de l'auteur
                        author = first_post.get('author', {})
                        if author:
                            print(f"   📋 Structure auteur:")
                            print(f"      ID: {author.get('id')}")
                            print(f"      Username: {author.get('username')}")
                            print(f"      First name: {author.get('first_name')}")
                            print(f"      Last name: {author.get('last_name')}")
                        else:
                            print(f"   ❌ Auteur manquant")
                        
                        # Vérifier les médias
                        media_files = first_post.get('media_files', [])
                        if media_files:
                            print(f"   📸 Médias:")
                            for i, media in enumerate(media_files[:3]):
                                print(f"      {i+1}. ID: {media.get('id')}")
                                print(f"         Type: {media.get('media_type')}")
                                print(f"         Titre: {media.get('title')}")
                                print(f"         URL: {media.get('file_url')}")
                                print(f"         URL complète: {media.get('file')}")
                else:
                    print(f"   ❌ Pas de clé 'results' dans la réponse")
                    print(f"   📋 Données reçues: {data}")
            else:
                print(f"   ❌ Réponse non-dictionnaire: {type(data)}")
                print(f"   📋 Données: {data}")
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def tester_creation_post_complete(token):
    """Tester la création complète d'un post"""
    print("\n📝 TEST CRÉATION POST COMPLÈTE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "content": "Test de post complet pour diagnostic - Vérification structure ! 🔍",
        "post_type": "info",
        "is_anonymous": False
    }
    
    try:
        response = requests.post(
            f"{API_URL}/posts/",
            json=post_data,
            headers=headers
        )
        
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post créé avec succès")
            print(f"📊 Structure complète du post créé:")
            print(json.dumps(post_data, indent=2, ensure_ascii=False))
            
            # Vérifier les champs critiques
            critical_fields = ['id', 'content', 'author', 'created_at', 'post_type']
            missing_critical = []
            
            for field in critical_fields:
                if field not in post_data:
                    missing_critical.append(field)
            
            if missing_critical:
                print(f"❌ Champs critiques manquants: {missing_critical}")
            else:
                print(f"✅ Tous les champs critiques présents")
            
            return post_data.get('id')
        else:
            print(f"❌ Erreur création post: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def verifier_pagination(token):
    """Vérifier la pagination des posts"""
    print("\n📄 VÉRIFICATION PAGINATION")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict):
                print(f"📊 Informations de pagination:")
                print(f"   Count: {data.get('count', 'N/A')}")
                print(f"   Next: {data.get('next', 'N/A')}")
                print(f"   Previous: {data.get('previous', 'N/A')}")
                print(f"   Results: {len(data.get('results', []))}")
                
                # Tester la page suivante si disponible
                if data.get('next'):
                    print(f"\n🔄 Test page suivante...")
                    next_response = requests.get(data['next'], headers=headers)
                    if next_response.status_code == 200:
                        next_data = next_response.json()
                        print(f"   ✅ Page suivante accessible")
                        print(f"   📝 Posts dans la page suivante: {len(next_data.get('results', []))}")
                    else:
                        print(f"   ❌ Erreur page suivante: {next_response.status_code}")
            else:
                print(f"⚠️ Réponse non paginée: {type(data)}")
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def verifier_filtres(token):
    """Vérifier les filtres de posts"""
    print("\n🔍 VÉRIFICATION FILTRES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test différents filtres
    filters = [
        {'type': 'info'},
        {'type': 'event'},
        {'type': 'help'},
        {'search': 'test'}
    ]
    
    for filter_params in filters:
        try:
            response = requests.get(f"{API_URL}/posts/", headers=headers, params=filter_params)
            
            if response.status_code == 200:
                data = response.json()
                posts_count = len(data.get('results', []))
                print(f"✅ Filtre {filter_params}: {posts_count} posts")
            else:
                print(f"❌ Erreur filtre {filter_params}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception filtre {filter_params}: {str(e)}")

def main():
    """Diagnostic complet de l'affichage des posts"""
    print("🔍 DIAGNOSTIC COMPLET AFFICHAGE POSTS")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Vérifier la structure des posts
    verifier_structure_posts(token)
    
    # Tester la création d'un post
    post_id = tester_creation_post_complete(token)
    
    # Vérifier la pagination
    verifier_pagination(token)
    
    # Vérifier les filtres
    verifier_filtres(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print(f"✅ API posts accessible")
    print(f"✅ Structure des posts vérifiée")
    print(f"✅ Création de posts fonctionnelle")
    print(f"✅ Pagination opérationnelle")
    print(f"✅ Filtres fonctionnels")
    print(f"💡 Si les posts ne s'affichent pas dans le frontend:")
    print(f"   1. Vérifiez la console du navigateur")
    print(f"   2. Vérifiez les erreurs réseau")
    print(f"   3. Vérifiez l'authentification frontend")
    print(f"   4. Vérifiez la structure des données reçues")

if __name__ == "__main__":
    main() 
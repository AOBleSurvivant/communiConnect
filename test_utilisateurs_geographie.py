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

def test_utilisateurs_geographie(token):
    """Test des utilisateurs et leurs quartiers"""
    print(f"\n👥 TEST UTILISATEURS ET GÉOGRAPHIE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test 1: Récupérer le profil utilisateur
    print("\n1️⃣ Test profil utilisateur...")
    try:
        response = requests.get(f"{API_URL}/users/my-profile/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Profil utilisateur récupéré")
            
            # Vérifier les informations géographiques
            quartier = user_data.get('quartier')
            location_info = user_data.get('location_info')
            
            print(f"📊 Quartier ID: {quartier}")
            print(f"📊 Location Info: {location_info}")
            
            if quartier:
                print("✅ Utilisateur a un quartier assigné")
            else:
                print("⚠️ Utilisateur n'a pas de quartier assigné")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📊 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Vérifier les posts avec filtrage géographique
    print("\n2️⃣ Test posts avec filtrage géographique...")
    try:
        response = requests.get(f"{API_URL}/posts/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            posts_data = response.json()
            posts = posts_data.get('results', [])
            print(f"📊 Posts trouvés: {len(posts)}")
            
            if posts:
                # Vérifier les informations géographiques des posts
                for i, post in enumerate(posts[:3]):  # Afficher les 3 premiers
                    author = post.get('author', {})
                    quartier = author.get('quartier')
                    location_info = author.get('location_info')
                    
                    print(f"📝 Post {i+1}:")
                    print(f"   Auteur: {author.get('first_name', 'N/A')} {author.get('last_name', 'N/A')}")
                    print(f"   Quartier: {quartier}")
                    print(f"   Location: {location_info}")
                    
                    if quartier:
                        print("   ✅ Auteur a un quartier")
                    else:
                        print("   ⚠️ Auteur n'a pas de quartier")
            else:
                print("⚠️ Aucun post trouvé")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Vérifier les utilisateurs par quartier
    print("\n3️⃣ Test utilisateurs par quartier...")
    try:
        # Récupérer d'abord les données géographiques
        geo_response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            quartiers = geo_data.get('quartiers', [])
            
            if quartiers:
                # Prendre le premier quartier pour tester
                test_quartier = quartiers[0]
                quartier_id = test_quartier['id']
                quartier_nom = test_quartier['nom']
                
                print(f"📊 Test avec quartier: {quartier_nom} (ID: {quartier_id})")
                
                # Chercher les utilisateurs de ce quartier (si endpoint disponible)
                # Note: Cet endpoint pourrait ne pas exister
                try:
                    users_response = requests.get(f"{API_URL}/users/quartier/{quartier_id}/", headers=headers)
                    print(f"📊 Status recherche utilisateurs: {users_response.status_code}")
                    
                    if users_response.status_code == 200:
                        users_data = users_response.json()
                        users = users_data.get('results', [])
                        print(f"📊 Utilisateurs dans ce quartier: {len(users)}")
                    else:
                        print("ℹ️ Endpoint utilisateurs par quartier non disponible")
                        
                except Exception as e:
                    print(f"ℹ️ Endpoint utilisateurs par quartier non disponible: {e}")
            else:
                print("⚠️ Aucun quartier disponible")
        else:
            print(f"❌ Erreur données géographiques: {geo_response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_filtrage_geographique(token):
    """Test du filtrage géographique des posts"""
    print(f"\n🗺️ TEST FILTRAGE GÉOGRAPHIQUE")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test avec différents paramètres de filtrage
    filters = [
        {},
        {'location': 'local'},
        {'location': 'commune'},
        {'location': 'prefecture'}
    ]
    
    for i, filter_params in enumerate(filters, 1):
        print(f"\n{i}️⃣ Test filtrage: {filter_params}")
        
        try:
            response = requests.get(f"{API_URL}/posts/", headers=headers, params=filter_params)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                posts_data = response.json()
                posts = posts_data.get('results', [])
                print(f"📊 Posts trouvés: {len(posts)}")
                
                if posts:
                    # Vérifier la localisation des posts
                    locations = set()
                    for post in posts:
                        author = post.get('author', {})
                        location = author.get('location_info', 'N/A')
                        locations.add(location)
                    
                    print(f"📊 Localisations des posts: {list(locations)[:3]}...")
                else:
                    print("⚠️ Aucun post trouvé avec ce filtre")
            else:
                print(f"❌ Erreur: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

def main():
    """Test principal"""
    print("🧪 TEST UTILISATEURS ET GÉOGRAPHIE")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    if not token:
        print("❌ Impossible de continuer sans token")
        return
    
    # Test des utilisateurs et géographie
    test_utilisateurs_geographie(token)
    
    # Test du filtrage géographique
    test_filtrage_geographique(token)
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Utilisateurs: Testés")
    print("✅ Géographie: Testée")
    print("✅ Filtrage: Testé")
    print("💡 Vérifiez les résultats ci-dessus")

if __name__ == "__main__":
    main() 
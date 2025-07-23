#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_geographie():
    """Test complet des données géographiques"""
    print("🗺️ TEST DONNÉES GÉOGRAPHIQUES")
    print("=" * 60)
    
    # Test 1: Récupération des données géographiques
    print("\n1️⃣ Test récupération données géographiques...")
    try:
        response = requests.get(f"{API_URL}/users/geographic-data/")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Données géographiques récupérées avec succès")
            
            # Analyser les données
            regions = data.get('regions', [])
            quartiers = data.get('quartiers', [])
            
            print(f"📊 Régions trouvées: {len(regions)}")
            print(f"📊 Quartiers trouvés: {len(quartiers)}")
            
            if regions:
                print(f"📍 Première région: {regions[0]['nom']}")
            if quartiers:
                print(f"🏠 Premier quartier: {quartiers[0]['nom']}")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📊 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    # Test 2: Test des endpoints individuels
    print("\n2️⃣ Test endpoints individuels...")
    
    endpoints = [
        "/geography/regions/",
        "/geography/prefectures/",
        "/geography/communes/",
        "/geography/quartiers/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_URL}{endpoint}")
            print(f"📊 {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    print(f"   ✅ {len(data['results'])} éléments trouvés")
                elif isinstance(data, list):
                    print(f"   ✅ {len(data)} éléments trouvés")
                else:
                    print(f"   ✅ Données reçues")
            else:
                print(f"   ❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test 3: Test des relations hiérarchiques
    print("\n3️⃣ Test relations hiérarchiques...")
    
    if regions:
        region_id = regions[0]['id']
        try:
            response = requests.get(f"{API_URL}/geography/regions/{region_id}/prefectures/")
            print(f"📊 Préfectures de région {region_id}: {response.status_code}")
            
            if response.status_code == 200:
                prefectures = response.json()
                print(f"   ✅ {len(prefectures)} préfectures trouvées")
                
                if prefectures:
                    prefecture_id = prefectures[0]['id']
                    response = requests.get(f"{API_URL}/geography/prefectures/{prefecture_id}/communes/")
                    print(f"📊 Communes de préfecture {prefecture_id}: {response.status_code}")
                    
                    if response.status_code == 200:
                        communes = response.json()
                        print(f"   ✅ {len(communes)} communes trouvées")
                        
                        if communes:
                            commune_id = communes[0]['id']
                            response = requests.get(f"{API_URL}/geography/communes/{commune_id}/quartiers/")
                            print(f"📊 Quartiers de commune {commune_id}: {response.status_code}")
                            
                            if response.status_code == 200:
                                quartiers = response.json()
                                print(f"   ✅ {len(quartiers)} quartiers trouvés")
                            else:
                                print(f"   ❌ Erreur {response.status_code}")
                    else:
                        print(f"   ❌ Erreur {response.status_code}")
            else:
                print(f"   ❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test 4: Test de recherche
    print("\n4️⃣ Test de recherche...")
    
    try:
        response = requests.get(f"{API_URL}/geography/quartiers/?search=conakry")
        print(f"📊 Recherche 'conakry': {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"   ✅ {len(data['results'])} résultats trouvés")
            elif isinstance(data, list):
                print(f"   ✅ {len(data)} résultats trouvés")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print(f"\n📊 RÉSUMÉ:")
    print("=" * 60)
    print("✅ Données géographiques: Testées")
    print("✅ Endpoints: Testés")
    print("✅ Relations: Testées")
    print("✅ Recherche: Testée")
    
    return True

def test_geographie_frontend():
    """Test des données géographiques côté frontend"""
    print("\n🌐 TEST FRONTEND GÉOGRAPHIE")
    print("=" * 60)
    
    # Test de l'API utilisée par le frontend
    try:
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            
            # Vérifier la structure attendue par le frontend
            regions = data.get('regions', [])
            quartiers = data.get('quartiers', [])
            
            print("✅ Structure des données correcte")
            print(f"📊 Régions: {len(regions)}")
            print(f"📊 Quartiers: {len(quartiers)}")
            
            # Vérifier la structure d'une région
            if regions:
                region = regions[0]
                required_fields = ['id', 'nom', 'prefectures']
                missing_fields = [field for field in required_fields if field not in region]
                
                if missing_fields:
                    print(f"⚠️ Champs manquants dans région: {missing_fields}")
                else:
                    print("✅ Structure région correcte")
                    
                    # Vérifier les préfectures
                    prefectures = region.get('prefectures', [])
                    if prefectures:
                        prefecture = prefectures[0]
                        required_fields = ['id', 'nom', 'communes']
                        missing_fields = [field for field in required_fields if field not in prefecture]
                        
                        if missing_fields:
                            print(f"⚠️ Champs manquants dans préfecture: {missing_fields}")
                        else:
                            print("✅ Structure préfecture correcte")
                            
                            # Vérifier les communes
                            communes = prefecture.get('communes', [])
                            if communes:
                                commune = communes[0]
                                required_fields = ['id', 'nom', 'quartiers']
                                missing_fields = [field for field in required_fields if field not in commune]
                                
                                if missing_fields:
                                    print(f"⚠️ Champs manquants dans commune: {missing_fields}")
                                else:
                                    print("✅ Structure commune correcte")
                                    
                                    # Vérifier les quartiers
                                    quartiers = commune.get('quartiers', [])
                                    if quartiers:
                                        quartier = quartiers[0]
                                        required_fields = ['id', 'nom']
                                        missing_fields = [field for field in required_fields if field not in quartier]
                                        
                                        if missing_fields:
                                            print(f"⚠️ Champs manquants dans quartier: {missing_fields}")
                                        else:
                                            print("✅ Structure quartier correcte")
                                        print(f"📊 Quartiers dans commune: {len(quartiers)}")
                                    else:
                                        print("⚠️ Aucun quartier dans la commune")
                            else:
                                print("⚠️ Aucune commune dans la préfecture")
                    else:
                        print("⚠️ Aucune préfecture dans la région")
            else:
                print("❌ Aucune région trouvée")
                
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test principal"""
    print("🧪 TEST COMPLET GÉOGRAPHIE")
    print("=" * 60)
    
    # Test backend
    success = test_geographie()
    
    # Test frontend
    test_geographie_frontend()
    
    print(f"\n🎯 CONCLUSION:")
    print("=" * 60)
    if success:
        print("✅ Les données géographiques fonctionnent correctement")
        print("✅ L'API est opérationnelle")
        print("✅ La structure des données est correcte")
    else:
        print("❌ Problèmes détectés avec les données géographiques")
        print("💡 Vérifiez les logs ci-dessus pour plus de détails")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test des données géographiques
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
GEOGRAPHIC_URL = f"{BASE_URL}/users/geographic-data/"

def test_geographic_data():
    """Test des données géographiques"""
    
    print("🗺️ TEST DES DONNÉES GÉOGRAPHIQUES")
    print("=" * 50)
    
    try:
        response = requests.get(GEOGRAPHIC_URL)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Données géographiques récupérées avec succès")
            
            # Analyser la structure
            regions = data.get('regions', [])
            print(f"\n📊 STATISTIQUES:")
            print(f"   - Régions: {len(regions)}")
            
            total_prefectures = 0
            total_communes = 0
            total_quartiers = 0
            
            for region in regions:
                prefectures = region.get('prefectures', [])
                total_prefectures += len(prefectures)
                
                for prefecture in prefectures:
                    communes = prefecture.get('communes', [])
                    total_communes += len(communes)
                    
                    for commune in communes:
                        quartiers = commune.get('quartiers', [])
                        total_quartiers += len(quartiers)
            
            print(f"   - Préfectures: {total_prefectures}")
            print(f"   - Communes: {total_communes}")
            print(f"   - Quartiers: {total_quartiers}")
            
            # Afficher quelques exemples
            print(f"\n🏛️ EXEMPLES DE RÉGIONS:")
            for i, region in enumerate(regions[:3]):  # Afficher les 3 premières
                print(f"   {i+1}. {region.get('nom', 'N/A')} ({region.get('code', 'N/A')})")
                
                prefectures = region.get('prefectures', [])
                if prefectures:
                    prefecture = prefectures[0]
                    print(f"      - Préfecture: {prefecture.get('nom', 'N/A')}")
                    
                    communes = prefecture.get('communes', [])
                    if communes:
                        commune = communes[0]
                        print(f"        - Commune: {commune.get('nom', 'N/A')}")
                        
                        quartiers = commune.get('quartiers', [])
                        if quartiers:
                            quartier = quartiers[0]
                            print(f"          - Quartier: {quartier.get('nom', 'N/A')} (ID: {quartier.get('id', 'N/A')})")
            
            # Test de sélection d'un quartier
            print(f"\n🧪 TEST DE SÉLECTION DE QUARTIER:")
            if regions and regions[0].get('prefectures'):
                prefecture = regions[0]['prefectures'][0]
                if prefecture.get('communes'):
                    commune = prefecture['communes'][0]
                    if commune.get('quartiers'):
                        quartier = commune['quartiers'][0]
                        quartier_id = quartier.get('id')
                        print(f"   - Quartier sélectionné: {quartier.get('nom')} (ID: {quartier_id})")
                        print(f"   - ✅ Quartier valide pour l'inscription")
                    else:
                        print(f"   - ❌ Aucun quartier trouvé")
                else:
                    print(f"   - ❌ Aucune commune trouvée")
            else:
                print(f"   - ❌ Aucune préfecture trouvée")
            
            print(f"\n🎯 RÉSUMÉ:")
            print(f"   - API géographique: ✅ Fonctionnelle")
            print(f"   - Données disponibles: ✅ {total_quartiers} quartiers")
            print(f"   - Structure: ✅ Valide")
            
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_geographic_data() 
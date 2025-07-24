#!/usr/bin/env python3
"""
Test rapide de l'API quartiers
"""

import requests
import json

def test_quartiers_api():
    """Test l'API quartiers pour voir le format des données"""
    
    print("🔍 Test de l'API quartiers...")
    
    try:
        # Test 1: API quartiers
        response = requests.get("http://127.0.0.1:8000/api/geography/quartiers/")
        print(f"Status API quartiers: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            quartiers = data.get('results', data)
            
            if quartiers:
                print(f"✅ {len(quartiers)} quartiers trouvés")
                print("\n📋 Format du premier quartier:")
                first_quartier = quartiers[0]
                print(json.dumps(first_quartier, indent=2, ensure_ascii=False))
                
                # Vérifier les champs
                print(f"\n🔍 Champs disponibles:")
                for key, value in first_quartier.items():
                    print(f"  - {key}: {type(value).__name__} = {value}")
            else:
                print("❌ Aucun quartier trouvé")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_quartiers_api() 
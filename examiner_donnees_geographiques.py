#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def examiner_donnees_geographiques():
    """Examiner la structure exacte des données géographiques"""
    print("🔍 EXAMEN DES DONNÉES GÉOGRAPHIQUES")
    print("=" * 60)
    
    try:
        # Récupérer les données géographiques
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            
            print("📋 STRUCTURE COMPLÈTE DES DONNÉES:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            print("\n🔍 ANALYSE DES CLÉS:")
            print("-" * 40)
            for key, value in data.items():
                if isinstance(value, list):
                    print(f"  📍 {key}: {len(value)} éléments")
                    if value and len(value) > 0:
                        print(f"     Premier élément: {value[0]}")
                else:
                    print(f"  📍 {key}: {type(value)}")
            
            # Analyser les quartiers en détail
            quartiers = data.get('quartiers', [])
            if quartiers:
                print(f"\n🏠 ANALYSE DES QUARTIERS:")
                print("-" * 40)
                print(f"  Nombre total: {len(quartiers)}")
                
                # Examiner le premier quartier
                premier_quartier = quartiers[0]
                print(f"  Premier quartier: {premier_quartier}")
                
                # Analyser les clés du premier quartier
                if isinstance(premier_quartier, dict):
                    print(f"  Clés du premier quartier:")
                    for key, value in premier_quartier.items():
                        print(f"    - {key}: {type(value)} = {value}")
            
            return True
            
        else:
            print(f"❌ Erreur récupération données: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def afficher_donnees_simple():
    """Afficher les données de manière simple"""
    print("\n🗺️ AFFICHAGE SIMPLE DES DONNÉES")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            
            # Afficher les régions
            regions = data.get('regions', [])
            print(f"\n🏛️ RÉGIONS ({len(regions)}):")
            for region in regions:
                print(f"  📍 {region['nom']} (ID: {region['id']})")
            
            # Afficher les quartiers
            quartiers = data.get('quartiers', [])
            print(f"\n🏠 QUARTIERS ({len(quartiers)}):")
            for quartier in quartiers:
                if isinstance(quartier, dict):
                    nom = quartier.get('nom', 'Inconnu')
                    quartier_id = quartier.get('id', 'N/A')
                    print(f"  📍 {nom} (ID: {quartier_id})")
                    
                    # Afficher les détails si disponibles
                    if quartier.get('commune'):
                        commune = quartier['commune']
                        if isinstance(commune, dict):
                            print(f"     Commune: {commune.get('nom', 'N/A')}")
                        else:
                            print(f"     Commune: {commune}")
                    
                    if quartier.get('region'):
                        region = quartier['region']
                        if isinstance(region, dict):
                            print(f"     Région: {region.get('nom', 'N/A')}")
                        else:
                            print(f"     Région: {region}")
                else:
                    print(f"  📍 {quartier}")
            
            return True
            
        else:
            print(f"❌ Erreur récupération données: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔍 EXAMEN DES DONNÉES GÉOGRAPHIQUES")
    print("=" * 60)
    
    # Examiner la structure
    success1 = examiner_donnees_geographiques()
    
    # Afficher les données simples
    success2 = afficher_donnees_simple()
    
    if success1 and success2:
        print("\n✅ Données géographiques examinées avec succès!")
    else:
        print("\n❌ Erreur lors de l'examen des données")

if __name__ == "__main__":
    main() 
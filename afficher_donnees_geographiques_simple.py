#!/usr/bin/env python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def afficher_donnees_geographiques():
    """Afficher toutes les données géographiques"""
    print("🗺️ DONNÉES GÉOGRAPHIQUES - COMMUNICONNECT")
    print("=" * 60)
    
    try:
        # Récupérer les données géographiques
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            
            # Afficher les régions
            regions = data.get('regions', [])
            print(f"\n🏛️ RÉGIONS ({len(regions)}):")
            print("-" * 40)
            for region in regions:
                print(f"  📍 {region['nom']} (ID: {region['id']})")
                if region.get('code'):
                    print(f"     Code: {region['code']}")
            
            # Afficher les quartiers
            quartiers = data.get('quartiers', [])
            print(f"\n🏠 QUARTIERS ({len(quartiers)}):")
            print("-" * 40)
            
            # Grouper les quartiers par région
            quartiers_par_region = {}
            for quartier in quartiers:
                region_nom = quartier.get('region', {}).get('nom', 'Inconnue')
                if region_nom not in quartiers_par_region:
                    quartiers_par_region[region_nom] = []
                quartiers_par_region[region_nom].append(quartier)
            
            for region_nom, quartiers_region in quartiers_par_region.items():
                print(f"\n  🏛️ RÉGION: {region_nom}")
                for quartier in quartiers_region:
                    print(f"    🏠 {quartier['nom']} (ID: {quartier['id']})")
                    if quartier.get('commune'):
                        print(f"       Commune: {quartier['commune']['nom']}")
                    if quartier.get('code'):
                        print(f"       Code: {quartier['code']}")
                    if quartier.get('population_estimee'):
                        print(f"       Population: {quartier['population_estimee']} habitants")
                    if quartier.get('superficie_km2'):
                        print(f"       Superficie: {quartier['superficie_km2']} km²")
            
            # Statistiques
            print(f"\n📊 STATISTIQUES:")
            print("-" * 40)
            print(f"  🏛️ Régions: {len(regions)}")
            print(f"  🏠 Quartiers: {len(quartiers)}")
            
            # Exemples de quartiers
            if quartiers:
                print(f"\n📋 EXEMPLES DE QUARTIERS:")
                print("-" * 40)
                for i, quartier in enumerate(quartiers[:10], 1):
                    print(f"  {i}. {quartier['nom']}")
                    if quartier.get('commune'):
                        print(f"     Commune: {quartier['commune']['nom']}")
                    if quartier.get('region'):
                        print(f"     Région: {quartier['region']['nom']}")
                    print()
            
            return True
            
        else:
            print(f"❌ Erreur récupération données: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def afficher_structure_simple():
    """Afficher la structure géographique de manière simple"""
    print("\n🗺️ STRUCTURE GÉOGRAPHIQUE SIMPLIFIÉE")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            regions = data.get('regions', [])
            quartiers = data.get('quartiers', [])
            
            for region in regions:
                print(f"\n🏛️ RÉGION: {region['nom']}")
                print(f"   📍 Code: {region.get('code', 'N/A')}")
                
                # Trouver les quartiers de cette région
                quartiers_region = [q for q in quartiers 
                                  if q.get('region', {}).get('id') == region['id']]
                
                if quartiers_region:
                    print(f"   🏠 Quartiers ({len(quartiers_region)}):")
                    for quartier in quartiers_region:
                        print(f"      📍 {quartier['nom']}")
                        if quartier.get('commune'):
                            print(f"         Commune: {quartier['commune']['nom']}")
                        if quartier.get('population_estimee'):
                            print(f"         Population: {quartier['population_estimee']}")
                else:
                    print(f"   ⚠️ Aucun quartier trouvé")
            
            return True
            
        else:
            print(f"❌ Erreur récupération structure: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🗺️ AFFICHAGE DES DONNÉES GÉOGRAPHIQUES")
    print("=" * 60)
    
    # Afficher les données géographiques
    success1 = afficher_donnees_geographiques()
    
    # Afficher la structure simple
    success2 = afficher_structure_simple()
    
    if success1 and success2:
        print("\n✅ Données géographiques affichées avec succès!")
    else:
        print("\n❌ Erreur lors de l'affichage des données")

if __name__ == "__main__":
    main() 
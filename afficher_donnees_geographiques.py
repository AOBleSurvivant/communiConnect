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
            
            # Afficher les préfectures
            prefectures = data.get('prefectures', [])
            print(f"\n🏛️ PRÉFECTURES ({len(prefectures)}):")
            print("-" * 40)
            for prefecture in prefectures:
                print(f"  📍 {prefecture['nom']} (ID: {prefecture['id']})")
                print(f"     Région: {prefecture['region']['nom']}")
                if prefecture.get('code'):
                    print(f"     Code: {prefecture['code']}")
            
            # Afficher les communes
            communes = data.get('communes', [])
            print(f"\n🏘️ COMMUNES ({len(communes)}):")
            print("-" * 40)
            for commune in communes:
                print(f"  📍 {commune['nom']} (ID: {commune['id']})")
                print(f"     Préfecture: {commune['prefecture']['nom']}")
                print(f"     Type: {commune['type']}")
                if commune.get('code'):
                    print(f"     Code: {commune['code']}")
            
            # Afficher les quartiers
            quartiers = data.get('quartiers', [])
            print(f"\n🏠 QUARTIERS ({len(quartiers)}):")
            print("-" * 40)
            for quartier in quartiers:
                print(f"  📍 {quartier['nom']} (ID: {quartier['id']})")
                print(f"     Commune: {quartier['commune']['nom']}")
                print(f"     Préfecture: {quartier['commune']['prefecture']['nom']}")
                if quartier.get('code'):
                    print(f"     Code: {quartier['code']}")
                if quartier.get('population_estimee'):
                    print(f"     Population: {quartier['population_estimee']} habitants")
                if quartier.get('superficie_km2'):
                    print(f"     Superficie: {quartier['superficie_km2']} km²")
            
            # Statistiques
            print(f"\n📊 STATISTIQUES:")
            print("-" * 40)
            print(f"  🏛️ Régions: {len(regions)}")
            print(f"  🏛️ Préfectures: {len(prefectures)}")
            print(f"  🏘️ Communes: {len(communes)}")
            print(f"  🏠 Quartiers: {len(quartiers)}")
            
            # Exemples de données
            if quartiers:
                print(f"\n📋 EXEMPLES DE QUARTIERS:")
                print("-" * 40)
                for i, quartier in enumerate(quartiers[:5], 1):
                    print(f"  {i}. {quartier['nom']}")
                    print(f"     Commune: {quartier['commune']['nom']}")
                    print(f"     Préfecture: {quartier['commune']['prefecture']['nom']}")
                    print(f"     Région: {quartier['commune']['prefecture']['region']['nom']}")
                    print()
            
            return True
            
        else:
            print(f"❌ Erreur récupération données: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def afficher_structure_geographique():
    """Afficher la structure géographique hiérarchique"""
    print("\n🗺️ STRUCTURE GÉOGRAPHIQUE HIÉRARCHIQUE")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/users/geographic-data/")
        
        if response.status_code == 200:
            data = response.json()
            regions = data.get('regions', [])
            
            for region in regions:
                print(f"\n🏛️ RÉGION: {region['nom']}")
                print(f"   📍 Code: {region.get('code', 'N/A')}")
                
                # Trouver les préfectures de cette région
                prefectures = [p for p in data.get('prefectures', []) 
                             if p['region']['id'] == region['id']]
                
                for prefecture in prefectures:
                    print(f"   🏛️ Préfecture: {prefecture['nom']}")
                    print(f"      📍 Code: {prefecture.get('code', 'N/A')}")
                    
                    # Trouver les communes de cette préfecture
                    communes = [c for c in data.get('communes', []) 
                              if c['prefecture']['id'] == prefecture['id']]
                    
                    for commune in communes:
                        print(f"      🏘️ Commune: {commune['nom']} ({commune['type']})")
                        print(f"         📍 Code: {commune.get('code', 'N/A')}")
                        
                        # Trouver les quartiers de cette commune
                        quartiers = [q for q in data.get('quartiers', []) 
                                   if q['commune']['id'] == commune['id']]
                        
                        for quartier in quartiers:
                            print(f"         🏠 Quartier: {quartier['nom']}")
                            if quartier.get('population_estimee'):
                                print(f"            👥 Population: {quartier['population_estimee']}")
                            if quartier.get('superficie_km2'):
                                print(f"            📏 Superficie: {quartier['superficie_km2']} km²")
            
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
    
    # Afficher la structure hiérarchique
    success2 = afficher_structure_geographique()
    
    if success1 and success2:
        print("\n✅ Données géographiques affichées avec succès!")
    else:
        print("\n❌ Erreur lors de l'affichage des données")

if __name__ == "__main__":
    main() 
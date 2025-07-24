#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création de données géographiques de base pour CommuniConnect
Script pour ajouter des quartiers de test
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def create_basic_geography():
    """Créer des données géographiques de base"""
    print("🗺️  Création des données géographiques de base...")
    
    try:
        from geography.models import Region, Prefecture, Commune, Quartier
        
        # Créer une région
        region, created = Region.objects.get_or_create(
            name="Conakry",
            defaults={'code': 'CNK'}
        )
        if created:
            print(f"✅ Région créée: {region.name}")
        else:
            print(f"ℹ️  Région existante: {region.name}")
        
        # Créer une préfecture
        prefecture, created = Prefecture.objects.get_or_create(
            name="Conakry",
            region=region,
            defaults={'code': 'CNK'}
        )
        if created:
            print(f"✅ Préfecture créée: {prefecture.name}")
        else:
            print(f"ℹ️  Préfecture existante: {prefecture.name}")
        
        # Créer plusieurs communes
        communes_data = [
            {'name': 'Kaloum', 'code': 'KLM'},
            {'name': 'Dixinn', 'code': 'DXN'},
            {'name': 'Ratoma', 'code': 'RTM'},
            {'name': 'Matam', 'code': 'MTM'},
            {'name': 'Matoto', 'code': 'MTO'},
        ]
        
        for commune_data in communes_data:
            commune, created = Commune.objects.get_or_create(
                name=commune_data['name'],
                prefecture=prefecture,
                defaults={'code': commune_data['code']}
            )
            if created:
                print(f"✅ Commune créée: {commune.name}")
            else:
                print(f"ℹ️  Commune existante: {commune.name}")
        
        # Créer plusieurs quartiers
        quartiers_data = [
            {'name': 'Centre-ville', 'code': 'CTR', 'commune': 'Kaloum', 'lat': 9.5370, 'lng': -13.6785},
            {'name': 'Almamya', 'code': 'ALM', 'commune': 'Kaloum', 'lat': 9.5400, 'lng': -13.6800},
            {'name': 'Sandervalia', 'code': 'SND', 'commune': 'Kaloum', 'lat': 9.5350, 'lng': -13.6750},
            {'name': 'Dixinn', 'code': 'DXN', 'commune': 'Dixinn', 'lat': 9.5500, 'lng': -13.7000},
            {'name': 'Ratoma', 'code': 'RTM', 'commune': 'Ratoma', 'lat': 9.5600, 'lng': -13.7200},
            {'name': 'Matam', 'code': 'MTM', 'commune': 'Matam', 'lat': 9.5700, 'lng': -13.7400},
            {'name': 'Matoto', 'code': 'MTO', 'commune': 'Matoto', 'lat': 9.5800, 'lng': -13.7600},
        ]
        
        for quartier_data in quartiers_data:
            commune = Commune.objects.get(name=quartier_data['commune'])
            quartier, created = Quartier.objects.get_or_create(
                name=quartier_data['name'],
                commune=commune,
                defaults={
                    'code': quartier_data['code'],
                    'latitude': quartier_data['lat'],
                    'longitude': quartier_data['lng']
                }
            )
            if created:
                print(f"✅ Quartier créé: {quartier.name} (ID: {quartier.id})")
            else:
                print(f"ℹ️  Quartier existant: {quartier.name} (ID: {quartier.id})")
        
        # Afficher le résumé
        print(f"\n📊 RÉSUMÉ DES DONNÉES GÉOGRAPHIQUES:")
        print(f"   Régions: {Region.objects.count()}")
        print(f"   Préfectures: {Prefecture.objects.count()}")
        print(f"   Communes: {Commune.objects.count()}")
        print(f"   Quartiers: {Quartier.objects.count()}")
        
        # Lister les quartiers disponibles
        print(f"\n📍 QUARTIERS DISPONIBLES:")
        for quartier in Quartier.objects.all():
            print(f"   - {quartier.name} (ID: {quartier.id}) - {quartier.commune.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données géographiques: {e}")
        return False

if __name__ == "__main__":
    success = create_basic_geography()
    if success:
        print(f"\n🎯 Données géographiques créées avec succès!")
        print(f"   Vous pouvez maintenant tester les fonctionnalités sociales.")
    else:
        print(f"\n❌ Échec de la création des données géographiques.") 
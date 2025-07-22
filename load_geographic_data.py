#!/usr/bin/env python3
"""
Script pour charger les données géographiques de la Guinée
sur l'environnement de production Render
"""

import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier

def load_geographic_data():
    """Charge les données géographiques de la Guinée"""
    
    print("🗺️  Chargement des données géographiques de la Guinée...")
    
    # Données des régions de Guinée
    regions_data = [
        {
            'nom': 'Conakry',
            'code': 'CON',
            'prefectures': [
                {
                    'nom': 'Conakry',
                    'code': 'CON',
                    'communes': [
                        {
                            'nom': 'Dixinn',
                            'type': 'commune urbaine',
                            'code': 'DIX',
                            'quartiers': [
                                {'nom': 'Cité des Nations', 'code': 'CDN'},
                                {'nom': 'Cité des Professeurs', 'code': 'CDP'},
                                {'nom': 'Cité Ministérielle', 'code': 'CMI'},
                                {'nom': 'Cité Universitaire', 'code': 'CUN'},
                                {'nom': 'Dixinn Centre', 'code': 'DIC'},
                                {'nom': 'Donka', 'code': 'DON'},
                                {'nom': 'Hamdallaye', 'code': 'HAM'},
                                {'nom': 'Kipé', 'code': 'KIP'},
                                {'nom': 'Lansébounyi', 'code': 'LAN'},
                                {'nom': 'Ratoma', 'code': 'RAT'},
                            ]
                        },
                        {
                            'nom': 'Kaloum',
                            'type': 'commune urbaine',
                            'code': 'KAL',
                            'quartiers': [
                                {'nom': 'Almamya', 'code': 'ALM'},
                                {'nom': 'Bambéto', 'code': 'BAM'},
                                {'nom': 'Boulbinet', 'code': 'BOU'},
                                {'nom': 'Camayenne', 'code': 'CAM'},
                                {'nom': 'Coronthie', 'code': 'COR'},
                                {'nom': 'Dagougnan', 'code': 'DAG'},
                                {'nom': 'Démoudoula', 'code': 'DEM'},
                                {'nom': 'Enta', 'code': 'ENT'},
                                {'nom': 'Kaporo', 'code': 'KAP'},
                                {'nom': 'Koloma', 'code': 'KOL'},
                                {'nom': 'Madina', 'code': 'MAD'},
                                {'nom': 'Sandervalia', 'code': 'SAN'},
                                {'nom': 'Taouyah', 'code': 'TAO'},
                            ]
                        },
                        {
                            'nom': 'Matam',
                            'type': 'commune urbaine',
                            'code': 'MAT',
                            'quartiers': [
                                {'nom': 'Bambéto', 'code': 'BAM'},
                                {'nom': 'Boulbinet', 'code': 'BOU'},
                                {'nom': 'Cosa', 'code': 'COS'},
                                {'nom': 'Dagougnan', 'code': 'DAG'},
                                {'nom': 'Démoudoula', 'code': 'DEM'},
                                {'nom': 'Enta', 'code': 'ENT'},
                                {'nom': 'Kaporo', 'code': 'KAP'},
                                {'nom': 'Koloma', 'code': 'KOL'},
                                {'nom': 'Madina', 'code': 'MAD'},
                                {'nom': 'Sandervalia', 'code': 'SAN'},
                                {'nom': 'Taouyah', 'code': 'TAO'},
                            ]
                        },
                        {
                            'nom': 'Matoto',
                            'type': 'commune urbaine',
                            'code': 'MAT',
                            'quartiers': [
                                {'nom': 'Cosa', 'code': 'COS'},
                                {'nom': 'Dagougnan', 'code': 'DAG'},
                                {'nom': 'Démoudoula', 'code': 'DEM'},
                                {'nom': 'Enta', 'code': 'ENT'},
                                {'nom': 'Kaporo', 'code': 'KAP'},
                                {'nom': 'Koloma', 'code': 'KOL'},
                                {'nom': 'Madina', 'code': 'MAD'},
                                {'nom': 'Sandervalia', 'code': 'SAN'},
                                {'nom': 'Taouyah', 'code': 'TAO'},
                            ]
                        },
                        {
                            'nom': 'Ratoma',
                            'type': 'commune urbaine',
                            'code': 'RAT',
                            'quartiers': [
                                {'nom': 'Cité des Nations', 'code': 'CDN'},
                                {'nom': 'Cité des Professeurs', 'code': 'CDP'},
                                {'nom': 'Cité Ministérielle', 'code': 'CMI'},
                                {'nom': 'Cité Universitaire', 'code': 'CUN'},
                                {'nom': 'Dixinn Centre', 'code': 'DIC'},
                                {'nom': 'Donka', 'code': 'DON'},
                                {'nom': 'Hamdallaye', 'code': 'HAM'},
                                {'nom': 'Kipé', 'code': 'KIP'},
                                {'nom': 'Lansébounyi', 'code': 'LAN'},
                                {'nom': 'Ratoma', 'code': 'RAT'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Boké',
            'code': 'BOK',
            'prefectures': [
                {
                    'nom': 'Boké',
                    'code': 'BOK',
                    'communes': [
                        {
                            'nom': 'Boké Centre',
                            'type': 'commune urbaine',
                            'code': 'BOC',
                            'quartiers': [
                                {'nom': 'Boké Centre', 'code': 'BOC'},
                                {'nom': 'Boké Port', 'code': 'BOP'},
                                {'nom': 'Kamsar', 'code': 'KAM'},
                                {'nom': 'Sangarédi', 'code': 'SAN'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Faranah',
            'code': 'FAR',
            'prefectures': [
                {
                    'nom': 'Faranah',
                    'code': 'FAR',
                    'communes': [
                        {
                            'nom': 'Faranah Centre',
                            'type': 'commune urbaine',
                            'code': 'FAC',
                            'quartiers': [
                                {'nom': 'Faranah Centre', 'code': 'FAC'},
                                {'nom': 'Faranah Port', 'code': 'FAP'},
                                {'nom': 'Kissidougou', 'code': 'KIS'},
                                {'nom': 'Gueckedou', 'code': 'GUE'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Kankan',
            'code': 'KAN',
            'prefectures': [
                {
                    'nom': 'Kankan',
                    'code': 'KAN',
                    'communes': [
                        {
                            'nom': 'Kankan Centre',
                            'type': 'commune urbaine',
                            'code': 'KAC',
                            'quartiers': [
                                {'nom': 'Kankan Centre', 'code': 'KAC'},
                                {'nom': 'Kankan Port', 'code': 'KAP'},
                                {'nom': 'Siguiri', 'code': 'SIG'},
                                {'nom': 'Kérouané', 'code': 'KER'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Kindia',
            'code': 'KIN',
            'prefectures': [
                {
                    'nom': 'Kindia',
                    'code': 'KIN',
                    'communes': [
                        {
                            'nom': 'Kindia Centre',
                            'type': 'commune urbaine',
                            'code': 'KIC',
                            'quartiers': [
                                {'nom': 'Kindia Centre', 'code': 'KIC'},
                                {'nom': 'Kindia Port', 'code': 'KIP'},
                                {'nom': 'Télimélé', 'code': 'TEL'},
                                {'nom': 'Coyah', 'code': 'COY'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Labé',
            'code': 'LAB',
            'prefectures': [
                {
                    'nom': 'Labé',
                    'code': 'LAB',
                    'communes': [
                        {
                            'nom': 'Labé Centre',
                            'type': 'commune urbaine',
                            'code': 'LAC',
                            'quartiers': [
                                {'nom': 'Labé Centre', 'code': 'LAC'},
                                {'nom': 'Labé Port', 'code': 'LAP'},
                                {'nom': 'Mamou', 'code': 'MAM'},
                                {'nom': 'Pita', 'code': 'PIT'},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'nom': 'Nzérékoré',
            'code': 'NZE',
            'prefectures': [
                {
                    'nom': 'Nzérékoré',
                    'code': 'NZE',
                    'communes': [
                        {
                            'nom': 'Nzérékoré Centre',
                            'type': 'commune urbaine',
                            'code': 'NZC',
                            'quartiers': [
                                {'nom': 'Nzérékoré Centre', 'code': 'NZC'},
                                {'nom': 'Nzérékoré Port', 'code': 'NZP'},
                                {'nom': 'Yomou', 'code': 'YOM'},
                                {'nom': 'Lola', 'code': 'LOL'},
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    
    # Supprimer les données existantes
    print("🧹 Suppression des données existantes...")
    Quartier.objects.all().delete()
    Commune.objects.all().delete()
    Prefecture.objects.all().delete()
    Region.objects.all().delete()
    
    # Charger les nouvelles données
    regions_created = 0
    prefectures_created = 0
    communes_created = 0
    quartiers_created = 0
    
    for region_data in regions_data:
        region = Region.objects.create(
            nom=region_data['nom'],
            code=region_data['code']
        )
        regions_created += 1
        print(f"✅ Région créée: {region.nom}")
        
        for prefecture_data in region_data['prefectures']:
            prefecture = Prefecture.objects.create(
                nom=prefecture_data['nom'],
                code=prefecture_data['code'],
                region=region
            )
            prefectures_created += 1
            print(f"  ✅ Préfecture créée: {prefecture.nom}")
            
            for commune_data in prefecture_data['communes']:
                commune = Commune.objects.create(
                    nom=commune_data['nom'],
                    type=commune_data['type'],
                    code=commune_data['code'],
                    prefecture=prefecture
                )
                communes_created += 1
                print(f"    ✅ Commune créée: {commune.nom}")
                
                for quartier_data in commune_data['quartiers']:
                    quartier = Quartier.objects.create(
                        nom=quartier_data['nom'],
                        code=quartier_data['code'],
                        commune=commune
                    )
                    quartiers_created += 1
                    print(f"      ✅ Quartier créé: {quartier.nom}")
    
    print(f"\n🎉 Chargement terminé !")
    print(f"📊 Statistiques:")
    print(f"   Régions: {regions_created}")
    print(f"   Préfectures: {prefectures_created}")
    print(f"   Communes: {communes_created}")
    print(f"   Quartiers: {quartiers_created}")
    
    # Vérification finale
    total_regions = Region.objects.count()
    total_prefectures = Prefecture.objects.count()
    total_communes = Commune.objects.count()
    total_quartiers = Quartier.objects.count()
    
    print(f"\n🔍 Vérification finale:")
    print(f"   Régions en base: {total_regions}")
    print(f"   Préfectures en base: {total_prefectures}")
    print(f"   Communes en base: {total_communes}")
    print(f"   Quartiers en base: {total_quartiers}")

if __name__ == '__main__':
    load_geographic_data() 
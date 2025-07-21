from django.core.management.base import BaseCommand
from geography.models import Region, Prefecture, Commune, Quartier
from users.models import User

class Command(BaseCommand):
    help = 'Charge les données géographiques de la Guinée'

    def handle(self, *args, **options):
        self.stdout.write("🗺️  Chargement des données géographiques de la Guinée...")
        
        # Vérifier s'il y a des utilisateurs existants
        user_count = User.objects.count()
        if user_count > 0:
            self.stdout.write(f"⚠️  {user_count} utilisateurs existants détectés")
            self.stdout.write("🔄 Mise à jour des données géographiques sans suppression...")
            
            # Ne pas supprimer les données existantes si des utilisateurs existent
            self.stdout.write("ℹ️  Conservation des données existantes pour éviter les conflits")
        else:
            # Supprimer toutes les données existantes
            self.stdout.write("🧹 Suppression des données existantes...")
            Quartier.objects.all().delete()
            Commune.objects.all().delete()
            Prefecture.objects.all().delete()
            Region.objects.all().delete()
        
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
        
        # Charger les nouvelles données
        regions_created = 0
        prefectures_created = 0
        communes_created = 0
        quartiers_created = 0
        
        for region_data in regions_data:
            # Vérifier si la région existe déjà
            region, created = Region.objects.get_or_create(
                nom=region_data['nom'],
                defaults={'code': region_data['code']}
            )
            if created:
                regions_created += 1
                self.stdout.write(f"✅ Région créée: {region.nom}")
            else:
                self.stdout.write(f"ℹ️  Région existante: {region.nom}")
            
            for prefecture_data in region_data['prefectures']:
                # Vérifier si la préfecture existe déjà
                prefecture, created = Prefecture.objects.get_or_create(
                    nom=prefecture_data['nom'],
                    region=region,
                    defaults={'code': prefecture_data['code']}
                )
                if created:
                    prefectures_created += 1
                    self.stdout.write(f"  ✅ Préfecture créée: {prefecture.nom}")
                else:
                    self.stdout.write(f"  ℹ️  Préfecture existante: {prefecture.nom}")
                
                for commune_data in prefecture_data['communes']:
                    # Vérifier si la commune existe déjà
                    commune, created = Commune.objects.get_or_create(
                        nom=commune_data['nom'],
                        prefecture=prefecture,
                        defaults={
                            'type': commune_data['type'],
                            'code': commune_data['code']
                        }
                    )
                    if created:
                        communes_created += 1
                        self.stdout.write(f"    ✅ Commune créée: {commune.nom}")
                    else:
                        self.stdout.write(f"    ℹ️  Commune existante: {commune.nom}")
                    
                    for quartier_data in commune_data['quartiers']:
                        # Vérifier si le quartier existe déjà
                        quartier, created = Quartier.objects.get_or_create(
                            nom=quartier_data['nom'],
                            commune=commune,
                            defaults={'code': quartier_data['code']}
                        )
                        if created:
                            quartiers_created += 1
                            self.stdout.write(f"      ✅ Quartier créé: {quartier.nom}")
                        else:
                            self.stdout.write(f"      ℹ️  Quartier existant: {quartier.nom}")
        
        self.stdout.write(f"\n🎉 Chargement terminé !")
        self.stdout.write(f"📊 Statistiques:")
        self.stdout.write(f"   Régions créées: {regions_created}")
        self.stdout.write(f"   Préfectures créées: {prefectures_created}")
        self.stdout.write(f"   Communes créées: {communes_created}")
        self.stdout.write(f"   Quartiers créés: {quartiers_created}")
        
        # Vérification finale
        total_regions = Region.objects.count()
        total_prefectures = Prefecture.objects.count()
        total_communes = Commune.objects.count()
        total_quartiers = Quartier.objects.count()
        
        self.stdout.write(f"\n🔍 Vérification finale:")
        self.stdout.write(f"   Régions en base: {total_regions}")
        self.stdout.write(f"   Préfectures en base: {total_prefectures}")
        self.stdout.write(f"   Communes en base: {total_communes}")
        self.stdout.write(f"   Quartiers en base: {total_quartiers}")
        
        self.stdout.write(self.style.SUCCESS('✅ Données géographiques chargées avec succès !')) 
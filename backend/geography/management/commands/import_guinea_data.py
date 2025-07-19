import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from geography.models import Region, Prefecture, Commune, Quartier


class Command(BaseCommand):
    help = 'Importe les données géographiques de la Guinée depuis le fichier JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/guinea_regions.json',
            help='Chemin vers le fichier JSON contenant les données géographiques'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'Fichier non trouvé: {file_path}')
            )
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.stdout.write('Importation des données géographiques de la Guinée...')
            
            with transaction.atomic():
                # Supprimer les données existantes
                Quartier.objects.all().delete()
                Commune.objects.all().delete()
                Prefecture.objects.all().delete()
                Region.objects.all().delete()
                
                self.stdout.write('Anciennes données supprimées.')
                
                # Importer les nouvelles données
                regions_created = 0
                prefectures_created = 0
                communes_created = 0
                quartiers_created = 0
                
                for region_data in data['regions']:
                    region = Region.objects.create(
                        nom=region_data['nom']
                    )
                    regions_created += 1
                    
                    for prefecture_data in region_data['prefectures']:
                        prefecture = Prefecture.objects.create(
                            region=region,
                            nom=prefecture_data['nom']
                        )
                        prefectures_created += 1
                        
                        for commune_data in prefecture_data['communes']:
                            commune = Commune.objects.create(
                                prefecture=prefecture,
                                nom=commune_data['nom'],
                                type=commune_data['type']
                            )
                            communes_created += 1
                            
                            # Créer des quartiers par défaut pour les communes urbaines
                            if commune_data['type'] == 'commune urbaine':
                                # Créer quelques quartiers par défaut
                                quartier_names = [
                                    'Centre', 'Nord', 'Sud', 'Est', 'Ouest',
                                    'Résidentiel', 'Commercial', 'Industriel'
                                ]
                                
                                for i, quartier_name in enumerate(quartier_names):
                                    Quartier.objects.create(
                                        commune=commune,
                                        nom=f"{quartier_name} {commune.nom}",
                                        code=f"{commune.nom[:3].upper()}{i+1:02d}"
                                    )
                                    quartiers_created += 1
                            else:
                                # Pour les communes rurales, créer un quartier principal
                                Quartier.objects.create(
                                    commune=commune,
                                    nom=f"Centre {commune.nom}",
                                    code=f"{commune.nom[:3].upper()}01"
                                )
                                quartiers_created += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Importation terminée avec succès!\n'
                        f'Régions créées: {regions_created}\n'
                        f'Préfectures créées: {prefectures_created}\n'
                        f'Communes créées: {communes_created}\n'
                        f'Quartiers créés: {quartiers_created}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de l\'importation: {str(e)}')
            )
            raise 
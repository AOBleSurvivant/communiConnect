#!/usr/bin/env python3
"""
Script pour déployer et charger les données géographiques sur Render
"""

import os
import subprocess
import requests
import time

def check_render_deployment():
    """Vérifie le statut du déploiement sur Render"""
    print("🔍 Vérification du déploiement Render...")
    
    # URL de l'API de production
    api_url = "https://communiconnect-backend.onrender.com/api"
    
    try:
        # Test de santé
        response = requests.get(f"{api_url}/users/geographic-data/", timeout=10)
        print(f"Status API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"📊 Données géographiques: {len(data)} éléments")
                return len(data) > 0
            else:
                print("❌ Format de données inattendu")
                return False
        else:
            print(f"❌ API non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def create_data_loading_script():
    """Crée un script pour charger les données sur Render"""
    script_content = '''#!/usr/bin/env python3
"""
Script pour charger les données géographiques sur Render
"""

import os
import sys
import django
from django.conf import settings

# Configuration Django pour Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings_render')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier

def load_geographic_data():
    """Charge les données géographiques de la Guinée"""
    
    print("🗺️  Chargement des données géographiques sur Render...")
    
    # Données simplifiées pour le test
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
                                {'nom': 'Dixinn Centre', 'code': 'DIC'},
                                {'nom': 'Donka', 'code': 'DON'},
                                {'nom': 'Hamdallaye', 'code': 'HAM'},
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
                                {'nom': 'Kamsar', 'code': 'KAM'},
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
    
    print(f"\\n🎉 Chargement terminé !")
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
    
    print(f"\\n🔍 Vérification finale:")
    print(f"   Régions en base: {total_regions}")
    print(f"   Préfectures en base: {total_prefectures}")
    print(f"   Communes en base: {total_communes}")
    print(f"   Quartiers en base: {total_quartiers}")

if __name__ == '__main__':
    load_geographic_data()
'''
    
    with open('load_render_data.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script de chargement créé: load_render_data.py")

def deploy_to_render():
    """Déploie l'application sur Render"""
    print("🚀 Déploiement sur Render...")
    
    # Vérifier si git est configuré
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git n'est pas configuré. Configurez Git d'abord.")
            return False
    except FileNotFoundError:
        print("❌ Git n'est pas installé. Installez Git d'abord.")
        return False
    
    # Ajouter les fichiers
    subprocess.run(['git', 'add', '.'])
    
    # Commit
    subprocess.run(['git', 'commit', '-m', 'Chargement des données géographiques'])
    
    # Push vers Render
    print("📤 Push vers Render...")
    subprocess.run(['git', 'push', 'origin', 'main'])
    
    print("✅ Déploiement initié sur Render")
    return True

def wait_for_deployment():
    """Attend que le déploiement soit terminé"""
    print("⏳ Attente du déploiement...")
    
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Tentative {attempt}/{max_attempts}...")
        
        if check_render_deployment():
            print("✅ Déploiement réussi ! Les données sont chargées.")
            return True
        
        time.sleep(30)  # Attendre 30 secondes
    
    print("❌ Déploiement échoué ou timeout")
    return False

def main():
    """Fonction principale"""
    print("🚀 Déploiement CommuniConnect sur Render")
    print("=" * 50)
    
    # Vérifier l'état actuel
    print("1️⃣ Vérification de l'état actuel...")
    if check_render_deployment():
        print("✅ Les données sont déjà chargées sur Render")
        return
    
    # Créer le script de chargement
    print("\\n2️⃣ Création du script de chargement...")
    create_data_loading_script()
    
    # Déployer
    print("\\n3️⃣ Déploiement sur Render...")
    if deploy_to_render():
        print("\\n4️⃣ Attente du déploiement...")
        if wait_for_deployment():
            print("\\n🎉 Déploiement réussi !")
            print("📋 Prochaines étapes:")
            print("1. Testez l'inscription d'utilisateurs")
            print("2. Vérifiez que les données géographiques sont disponibles")
            print("3. Lancez les tests utilisateurs")
        else:
            print("\\n❌ Déploiement échoué")
    else:
        print("\\n❌ Erreur lors du déploiement")

if __name__ == "__main__":
    main() 
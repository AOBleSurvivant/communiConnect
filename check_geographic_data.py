#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier

def check_geographic_data():
    """Vérifie les données géographiques"""
    print("🔍 Vérification des données géographiques...")
    
    # Compter les données
    regions_count = Region.objects.count()
    prefectures_count = Prefecture.objects.count()
    communes_count = Commune.objects.count()
    quartiers_count = Quartier.objects.count()
    
    print(f"📊 Statistiques des données géographiques:")
    print(f"   Régions: {regions_count}")
    print(f"   Préfectures: {prefectures_count}")
    print(f"   Communes: {communes_count}")
    print(f"   Quartiers: {quartiers_count}")
    
    if quartiers_count == 0:
        print("❌ Aucun quartier trouvé! Il faut charger les données.")
        return False
    else:
        print("✅ Données géographiques disponibles!")
        
        # Afficher quelques exemples
        print("\n📍 Exemples de quartiers:")
        quartiers = Quartier.objects.all()[:5]
        for quartier in quartiers:
            print(f"   - {quartier.commune.prefecture.region.nom} > {quartier.commune.prefecture.nom} > {quartier.commune.nom} > {quartier.nom}")
        
        return True

def load_geographic_data():
    """Charge les données géographiques depuis le fichier JSON"""
    print("\n📥 Chargement des données géographiques...")
    
    try:
        from django.core.management import call_command
        call_command('load_geographic_data')
        print("✅ Données géographiques chargées avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Diagnostic des données géographiques CommuniConnect")
    print("=" * 60)
    
    # Vérifier les données existantes
    if not check_geographic_data():
        print("\n🔄 Tentative de chargement des données...")
        if load_geographic_data():
            print("\n✅ Diagnostic terminé - Données disponibles!")
        else:
            print("\n❌ Diagnostic échoué - Problème de chargement")
    else:
        print("\n✅ Diagnostic terminé - Données déjà disponibles!") 
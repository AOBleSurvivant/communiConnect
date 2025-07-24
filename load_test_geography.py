#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chargement des données géographiques de test
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier

def create_test_geography():
    """Créer des données géographiques de test"""
    print("🗺️  Création des données géographiques de test...")
    
    # Créer une région
    region, created = Region.objects.get_or_create(
        name="Conakry",
        defaults={'code': 'CNK'}
    )
    if created:
        print(f"✅ Région créée: {region.name}")
    
    # Créer une préfecture
    prefecture, created = Prefecture.objects.get_or_create(
        name="Conakry",
        region=region,
        defaults={'code': 'CNK'}
    )
    if created:
        print(f"✅ Préfecture créée: {prefecture.name}")
    
    # Créer une commune
    commune, created = Commune.objects.get_or_create(
        name="Kaloum",
        prefecture=prefecture,
        defaults={'code': 'KLM'}
    )
    if created:
        print(f"✅ Commune créée: {commune.name}")
    
    # Créer un quartier
    quartier, created = Quartier.objects.get_or_create(
        name="Centre-ville",
        commune=commune,
        defaults={
            'code': 'CTR',
            'latitude': 9.5370,
            'longitude': -13.6785
        }
    )
    if created:
        print(f"✅ Quartier créé: {quartier.name}")
    
    print(f"✅ Données géographiques créées avec succès!")
    print(f"   Quartier ID: {quartier.id}")
    print(f"   Quartier: {quartier.name}")
    print(f"   Commune: {commune.name}")
    print(f"   Préfecture: {prefecture.name}")
    print(f"   Région: {region.name}")
    
    return quartier.id

if __name__ == "__main__":
    quartier_id = create_test_geography()
    print(f"\n🎯 Quartier ID pour les tests: {quartier_id}") 
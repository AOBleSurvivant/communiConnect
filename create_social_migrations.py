#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer les migrations des modèles sociaux
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_social_migrations():
    """Créer les migrations pour les modèles sociaux"""
    print("🔧 Création des migrations pour les modèles sociaux...")
    
    try:
        # Créer les migrations pour l'app users
        print("📝 Création des migrations users...")
        execute_from_command_line(['manage.py', 'makemigrations', 'users'])
        
        # Appliquer les migrations
        print("📦 Application des migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations créées et appliquées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des migrations: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage création des migrations sociales...")
    success = create_social_migrations()
    if success:
        print("✅ Migrations sociales créées avec succès!")
    else:
        print("❌ Échec de la création des migrations sociales.") 
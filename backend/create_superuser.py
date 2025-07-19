#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from geography.models import Quartier

User = get_user_model()

def create_superuser():
    try:
        # Vérifier si un super utilisateur existe déjà
        if User.objects.filter(is_superuser=True).exists():
            print("Un super utilisateur existe déjà.")
            return
        
        # Récupérer le premier quartier disponible
        quartier = Quartier.objects.first()
        if not quartier:
            print("Aucun quartier trouvé. Veuillez d'abord importer les données géographiques.")
            return
        
        print(f"Quartier sélectionné: {quartier}")
        
        # Créer le super utilisateur
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@communiconnect.gn',
            password='admin123456',
            first_name='Admin',
            last_name='CommuniConnect',
            quartier=quartier
        )
        
        print(f"Super utilisateur créé avec succès:")
        print(f"Username: {superuser.username}")
        print(f"Email: {superuser.email}")
        print(f"Password: admin123456")
        print(f"Quartier: {superuser.quartier}")
        
    except Exception as e:
        print(f"Erreur lors de la création du super utilisateur: {e}")

if __name__ == '__main__':
    create_superuser() 
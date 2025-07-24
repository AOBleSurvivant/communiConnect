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

def create_simple_user():
    print("👤 Création d'un utilisateur simple...")
    
    # Récupérer un quartier existant
    quartier = Quartier.objects.first()
    if not quartier:
        print("❌ Aucun quartier trouvé. Créez d'abord des données géographiques.")
        return None
    
    print(f"✅ Quartier trouvé: {quartier.nom}")
    
    # Créer un utilisateur simple
    try:
        # Supprimer l'utilisateur s'il existe déjà
        User.objects.filter(username="simpleuser").delete()
        
        user = User.objects.create_user(
            username="simpleuser",
            email="simple@test.com",
            password="simple123",
            first_name="Simple",
            last_name="User"
        )
        user.quartier = quartier
        user.save()
        
        print(f"✅ Utilisateur créé: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"🔑 Password: simple123")
        print(f"📍 Quartier: {quartier.nom}")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return None

if __name__ == "__main__":
    create_simple_user() 
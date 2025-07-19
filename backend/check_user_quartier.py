#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from users.models import User

def check_user_quartier():
    """Check if users have quartier assigned"""
    users = User.objects.all()
    
    print("=== Vérification des quartiers des utilisateurs ===")
    for user in users:
        quartier_info = f"Quartier: {user.quartier.nom}" if user.quartier else "Aucun quartier assigné"
        print(f"User: {user.username} - {quartier_info}")
    
    # Check specific user if provided
    if len(sys.argv) > 1:
        username = sys.argv[1]
        try:
            user = User.objects.get(username=username)
            if user.quartier:
                print(f"\n{username} a le quartier: {user.quartier.nom}")
            else:
                print(f"\n{username} n'a pas de quartier assigné")
        except User.DoesNotExist:
            print(f"Utilisateur {username} non trouvé")

if __name__ == "__main__":
    check_user_quartier() 
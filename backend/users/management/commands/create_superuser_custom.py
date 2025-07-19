from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from geography.models import Quartier

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée un superutilisateur avec des valeurs par défaut'

    def handle(self, *args, **options):
        # Vérifier si un superuser existe déjà
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Un superutilisateur existe déjà.')
            )
            return

        # Récupérer le premier quartier disponible
        try:
            quartier = Quartier.objects.first()
            if not quartier:
                self.stdout.write(
                    self.style.ERROR('Aucun quartier trouvé dans la base de données.')
                )
                return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la récupération du quartier: {e}')
            )
            return

        # Créer le superuser
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@communiconnect.com',
                password='Admin123!',
                quartier=quartier
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superutilisateur créé avec succès!\n'
                    f'Username: admin\n'
                    f'Email: admin@communiconnect.com\n'
                    f'Password: Admin123!\n'
                    f'Quartier: {quartier.nom}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la création du superutilisateur: {e}')
            ) 
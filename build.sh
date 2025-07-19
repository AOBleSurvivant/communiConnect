#!/usr/bin/env bash
# Script de build pour Render - CommuniConnect

echo "Build CommuniConnect sur Render..."

# Vérifier la version de Python
python --version

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements_render.txt

# Aller dans le dossier backend
cd backend

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Créer un superuser si nécessaire
echo "Création du superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@communiconnect.com', 'admin123')
    print('Superuser créé: admin/admin123')
else:
    print('Superuser existe déjà')
"

# Démarrer le serveur avec gunicorn
echo "Démarrage du serveur avec gunicorn..."
gunicorn communiconnect.wsgi:application --bind 0.0.0.0:$PORT

echo "Build terminé avec succès!" 
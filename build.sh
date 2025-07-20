#!/bin/bash
# Script de build pour Render - CommuniConnect

echo "🚀 Démarrage du build CommuniConnect sur Render..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Vérifiez la structure du projet."
    exit 1
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements_render.txt

# Aller dans le répertoire backend
cd backend

# Vérifier la configuration Django
echo "🔧 Vérification de la configuration Django..."
python manage.py check --deploy

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superuser si nécessaire (pour le développement)
# echo "👤 Création d'un superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@communiconnect.com

echo "✅ Build terminé avec succès!"
echo "🌐 L'application sera disponible sur: https://communiconnect-backend.onrender.com" 
#!/bin/bash

# Script de déploiement pour CommuniConnect en production
# Usage: ./deploy_production.sh

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement de CommuniConnect en production..."

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="/var/log/communiconnect"
STATIC_DIR="/var/www/communiconnect/static"
MEDIA_DIR="/var/www/communiconnect/media"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier que nous sommes en root ou avec sudo
if [[ $EUID -ne 0 ]]; then
   print_error "Ce script doit être exécuté en tant que root ou avec sudo"
   exit 1
fi

# Créer les répertoires nécessaires
print_status "Création des répertoires de production..."
mkdir -p $LOG_DIR
mkdir -p $STATIC_DIR
mkdir -p $MEDIA_DIR
chown -R www-data:www-data $LOG_DIR
chown -R www-data:www-data $STATIC_DIR
chown -R www-data:www-data $MEDIA_DIR

# Vérifier que l'environnement de production existe
if [ ! -f "$PROJECT_DIR/.env.production" ]; then
    print_error "Le fichier .env.production n'existe pas. Veuillez le créer à partir de env.production.example"
    exit 1
fi

# Copier l'environnement de production
print_status "Configuration de l'environnement..."
cp "$PROJECT_DIR/.env.production" "$PROJECT_DIR/.env"

# Activer l'environnement virtuel
print_status "Activation de l'environnement virtuel..."
source "$VENV_DIR/bin/activate"

# Installer/mettre à jour les dépendances
print_status "Installation des dépendances..."
pip install -r requirements.txt

# Vérifier que PostgreSQL est installé et configuré
print_status "Vérification de PostgreSQL..."
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier que Redis est installé et en cours d'exécution
print_status "Vérification de Redis..."
if ! systemctl is-active --quiet redis; then
    print_warning "Redis n'est pas en cours d'exécution. Démarrage..."
    systemctl start redis
    systemctl enable redis
fi

# Exécuter les migrations
print_status "Exécution des migrations..."
python manage.py migrate --settings=communiconnect.settings_production

# Collecter les fichiers statiques
print_status "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=communiconnect.settings_production

# Créer un superutilisateur si nécessaire
print_status "Création du superutilisateur..."
python manage.py createsuperuser --noinput --settings=communiconnect.settings_production || true

# Vérifier la configuration
print_status "Vérification de la configuration..."
python manage.py check --settings=communiconnect.settings_production

# Tester la connexion à la base de données
print_status "Test de la connexion à la base de données..."
python manage.py dbshell --settings=communiconnect.settings_production <<< "SELECT 1;" || {
    print_error "Impossible de se connecter à la base de données"
    exit 1
}

# Tester la connexion Redis
print_status "Test de la connexion Redis..."
python -c "
import redis
import os
from decouple import config
try:
    r = redis.Redis(
        host=config('REDIS_HOST', default='localhost'),
        port=config('REDIS_PORT', default=6379, cast=int),
        password=config('REDIS_PASSWORD', default=''),
        db=0
    )
    r.ping()
    print('Redis connecté avec succès')
except Exception as e:
    print(f'Erreur Redis: {e}')
    exit(1)
" || {
    print_error "Impossible de se connecter à Redis"
    exit 1
}

# Configurer Gunicorn
print_status "Configuration de Gunicorn..."
cat > /etc/systemd/system/communiconnect.service << EOF
[Unit]
Description=CommuniConnect Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="DJANGO_SETTINGS_MODULE=communiconnect.settings_production"
ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --bind unix:/run/communiconnect.sock communiconnect.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Configurer Nginx
print_status "Configuration de Nginx..."
cat > /etc/nginx/sites-available/communiconnect << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com api.your-domain.com;
    
    # Redirection HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com api.your-domain.com;
    
    # Certificats SSL (à configurer avec Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Configuration SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Headers de sécurité
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Fichiers statiques
    location /static/ {
        alias $STATIC_DIR/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Médias
    location /media/ {
        alias $MEDIA_DIR/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # API Django
    location / {
        proxy_pass http://unix:/run/communiconnect.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_buffering off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
EOF

# Activer le site Nginx
ln -sf /etc/nginx/sites-available/communiconnect /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Tester la configuration Nginx
print_status "Test de la configuration Nginx..."
nginx -t

# Redémarrer les services
print_status "Redémarrage des services..."
systemctl daemon-reload
systemctl enable communiconnect
systemctl restart communiconnect
systemctl restart nginx

# Vérifier le statut des services
print_status "Vérification du statut des services..."
systemctl is-active --quiet communiconnect && print_status "CommuniConnect: ✅ Actif" || print_error "CommuniConnect: ❌ Inactif"
systemctl is-active --quiet nginx && print_status "Nginx: ✅ Actif" || print_error "Nginx: ❌ Inactif"
systemctl is-active --quiet redis && print_status "Redis: ✅ Actif" || print_error "Redis: ❌ Inactif"

# Configuration des logs
print_status "Configuration des logs..."
cat > /etc/logrotate.d/communiconnect << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload communiconnect
    endscript
}
EOF

# Configuration du monitoring
print_status "Configuration du monitoring..."
cat > /etc/systemd/system/communiconnect-monitor.service << EOF
[Unit]
Description=CommuniConnect Monitoring
After=communiconnect.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python $PROJECT_DIR/scripts/monitor.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable communiconnect-monitor
systemctl start communiconnect-monitor

print_status "✅ Déploiement terminé avec succès!"
print_status "🌐 Votre application est accessible sur: https://your-domain.com"
print_status "📊 Documentation API: https://your-domain.com/api/schema/"
print_status "📝 Logs: $LOG_DIR"

echo ""
print_warning "⚠️  N'oubliez pas de:"
echo "   1. Configurer votre domaine dans Nginx"
echo "   2. Obtenir un certificat SSL avec Let's Encrypt"
echo "   3. Configurer les variables d'environnement dans .env.production"
echo "   4. Configurer Cloudinary et Redis avec vos vraies clés"
echo "   5. Tester l'application complètement" 
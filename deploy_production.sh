#!/bin/bash

# Script de déploiement production - CommuniConnect
# Usage: ./deploy_production.sh

set -e  # Arrêter en cas d'erreur

echo "🚀 DÉPLOIEMENT PRODUCTION - COMMUNICONNECT"
echo "=========================================="

# Variables de configuration
PROJECT_DIR="/var/www/communiconnect"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_DIR="/var/log/communiconnect"
ENV_FILE="$PROJECT_DIR/.env"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier si on est root ou sudo
    if [[ $EUID -eq 0 ]]; then
        log_error "Ce script ne doit pas être exécuté en tant que root"
        exit 1
    fi
    
    # Vérifier les outils nécessaires
    command -v python3 >/dev/null 2>&1 || { log_error "Python3 n'est pas installé"; exit 1; }
    command -v pip3 >/dev/null 2>&1 || { log_error "pip3 n'est pas installé"; exit 1; }
    command -v node >/dev/null 2>&1 || { log_error "Node.js n'est pas installé"; exit 1; }
    command -v npm >/dev/null 2>&1 || { log_error "npm n'est pas installé"; exit 1; }
    command -v git >/dev/null 2>&1 || { log_error "git n'est pas installé"; exit 1; }
    
    log_info "Prérequis vérifiés ✓"
}

# Sauvegarde de la version actuelle
backup_current_version() {
    log_info "Sauvegarde de la version actuelle..."
    
    if [ -d "$PROJECT_DIR" ]; then
        BACKUP_DIR="$PROJECT_DIR/backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        cp -r "$PROJECT_DIR" "$BACKUP_DIR"
        log_info "Sauvegarde créée: $BACKUP_DIR"
    else
        log_warn "Aucune version existante à sauvegarder"
    fi
}

# Mise à jour du code source
update_source_code() {
    log_info "Mise à jour du code source..."
    
    if [ -d "$PROJECT_DIR" ]; then
        cd "$PROJECT_DIR"
        git fetch origin
        git reset --hard origin/main
        log_info "Code source mis à jour ✓"
    else
        log_error "Le répertoire du projet n'existe pas: $PROJECT_DIR"
        exit 1
    fi
}

# Installation des dépendances backend
install_backend_dependencies() {
    log_info "Installation des dépendances backend..."
    
    cd "$BACKEND_DIR"
    
    # Créer l'environnement virtuel s'il n'existe pas
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_info "Environnement virtuel créé"
    fi
    
    # Activer l'environnement virtuel
    source venv/bin/activate
    
    # Mettre à jour pip
    pip install --upgrade pip
    
    # Installer les dépendances
    pip install -r requirements.txt
    
    log_info "Dépendances backend installées ✓"
}

# Configuration de la base de données
setup_database() {
    log_info "Configuration de la base de données..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Appliquer les migrations
    python manage.py migrate --settings=communiconnect.settings_production
    
    # Collecter les fichiers statiques
    python manage.py collectstatic --noinput --settings=communiconnect.settings_production
    
    log_info "Base de données configurée ✓"
}

# Installation des dépendances frontend
install_frontend_dependencies() {
    log_info "Installation des dépendances frontend..."
    
    cd "$FRONTEND_DIR"
    
    # Installer les dépendances
    npm ci --production
    
    log_info "Dépendances frontend installées ✓"
}

# Build du frontend
build_frontend() {
    log_info "Build du frontend..."
    
    cd "$FRONTEND_DIR"
    
    # Build de production
    npm run build
    
    # Copier le build vers le répertoire static de Django
    cp -r build/* "$BACKEND_DIR/staticfiles/"
    
    log_info "Frontend buildé ✓"
}

# Configuration des services
setup_services() {
    log_info "Configuration des services..."
    
    # Créer les répertoires nécessaires
    sudo mkdir -p "$LOG_DIR"
    sudo chown -R www-data:www-data "$LOG_DIR"
    
    # Configuration Gunicorn
    sudo tee /etc/systemd/system/communiconnect.service > /dev/null <<EOF
[Unit]
Description=CommuniConnect Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$BACKEND_DIR
Environment=PATH=$BACKEND_DIR/venv/bin
ExecStart=$BACKEND_DIR/venv/bin/gunicorn --workers 3 --bind unix:/tmp/communiconnect.sock communiconnect.wsgi:application --settings=communiconnect.settings_production
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Configuration Nginx
    sudo tee /etc/nginx/sites-available/communiconnect > /dev/null <<EOF
server {
    listen 80;
    server_name communiconnect.com www.communiconnect.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name communiconnect.com www.communiconnect.com;
    
    ssl_certificate /etc/letsencrypt/live/communiconnect.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/communiconnect.com/privkey.pem;
    
    # Configuration SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Headers de sécurité
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Logs
    access_log /var/log/nginx/communiconnect_access.log;
    error_log /var/log/nginx/communiconnect_error.log;
    
    # Fichiers statiques
    location /static/ {
        alias $BACKEND_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Fichiers médias
    location /media/ {
        alias $BACKEND_DIR/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # API Django
    location / {
        proxy_pass http://unix:/tmp/communiconnect.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

    # Activer le site
    sudo ln -sf /etc/nginx/sites-available/communiconnect /etc/nginx/sites-enabled/
    
    # Tester la configuration Nginx
    sudo nginx -t
    
    log_info "Services configurés ✓"
}

# Redémarrage des services
restart_services() {
    log_info "Redémarrage des services..."
    
    # Redémarrer Gunicorn
    sudo systemctl daemon-reload
    sudo systemctl enable communiconnect
    sudo systemctl restart communiconnect
    
    # Redémarrer Nginx
    sudo systemctl restart nginx
    
    # Redémarrer Redis si nécessaire
    sudo systemctl restart redis
    
    log_info "Services redémarrés ✓"
}

# Tests de santé
health_check() {
    log_info "Tests de santé..."
    
    # Attendre que les services démarrent
    sleep 5
    
    # Tester l'API
    if curl -f -s https://communiconnect.com/api/health/ > /dev/null; then
        log_info "API accessible ✓"
    else
        log_error "API inaccessible"
        return 1
    fi
    
    # Tester le site principal
    if curl -f -s https://communiconnect.com/ > /dev/null; then
        log_info "Site principal accessible ✓"
    else
        log_error "Site principal inaccessible"
        return 1
    fi
    
    log_info "Tests de santé réussis ✓"
}

# Nettoyage
cleanup() {
    log_info "Nettoyage..."
    
    # Supprimer les anciennes sauvegardes (garder les 5 plus récentes)
    if [ -d "$PROJECT_DIR" ]; then
        cd "$PROJECT_DIR"
        ls -t backup_* | tail -n +6 | xargs -r rm -rf
    fi
    
    # Nettoyer le cache
    sudo systemctl restart redis
    
    log_info "Nettoyage terminé ✓"
}

# Fonction principale
main() {
    log_info "Début du déploiement..."
    
    check_prerequisites
    backup_current_version
    update_source_code
    install_backend_dependencies
    setup_database
    install_frontend_dependencies
    build_frontend
    setup_services
    restart_services
    health_check
    cleanup
    
    log_info "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !"
    log_info "Site accessible sur: https://communiconnect.com"
    log_info "API accessible sur: https://communiconnect.com/api/"
    log_info "Documentation API: https://communiconnect.com/api/docs/"
}

# Gestion des erreurs
trap 'log_error "Erreur lors du déploiement. Vérifiez les logs."; exit 1' ERR

# Exécution du script
main "$@" 
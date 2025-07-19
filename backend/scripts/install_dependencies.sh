#!/bin/bash

# Script d'installation des dépendances système pour CommuniConnect
# Usage: ./install_dependencies.sh

set -e

echo "🔧 Installation des dépendances système pour CommuniConnect..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Vérifier que nous sommes en root ou avec sudo
if [[ $EUID -ne 0 ]]; then
   print_error "Ce script doit être exécuté en tant que root ou avec sudo"
   exit 1
fi

# Mettre à jour le système
print_header "Mise à jour du système"
print_status "Mise à jour des paquets système..."
apt update && apt upgrade -y

# Installation des paquets de base
print_header "Installation des paquets de base"
print_status "Installation des paquets essentiels..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    curl \
    wget \
    git \
    unzip \
    htop \
    tree \
    vim \
    nano \
    ufw \
    fail2ban \
    logrotate \
    supervisor

# Installation de PostgreSQL
print_header "Installation de PostgreSQL"
print_status "Installation de PostgreSQL..."
apt install -y postgresql postgresql-contrib

# Configuration de PostgreSQL
print_status "Configuration de PostgreSQL..."
sudo -u postgres psql -c "CREATE USER communiconnect_user WITH PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "CREATE DATABASE communiconnect_prod OWNER communiconnect_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE communiconnect_prod TO communiconnect_user;"

# Installation de Redis
print_header "Installation de Redis"
print_status "Installation de Redis..."
apt install -y redis-server

# Configuration de Redis
print_status "Configuration de Redis..."
cat > /etc/redis/redis.conf << EOF
# Configuration Redis pour CommuniConnect
bind 127.0.0.1
port 6379
timeout 0
tcp-keepalive 300
daemonize yes
supervised systemd
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis
maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
EOF

# Redémarrer Redis
systemctl restart redis-server
systemctl enable redis-server

# Installation de Nginx
print_header "Installation de Nginx"
print_status "Installation de Nginx..."
apt install -y nginx

# Configuration de base de Nginx
print_status "Configuration de Nginx..."
cat > /etc/nginx/nginx.conf << EOF
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip
    gzip on;
    gzip_vary on;
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

    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone \$binary_remote_addr zone=login:10m rate=5r/m;

    # Include site configurations
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
EOF

# Installation de Certbot pour SSL
print_header "Installation de Certbot"
print_status "Installation de Certbot pour les certificats SSL..."
apt install -y certbot python3-certbot-nginx

# Installation de Gunicorn
print_status "Installation de Gunicorn..."
pip3 install gunicorn

# Configuration du firewall
print_header "Configuration du firewall"
print_status "Configuration du firewall UFW..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Configuration de Fail2ban
print_header "Configuration de Fail2ban"
print_status "Configuration de Fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https"]
logpath = /var/log/nginx/error.log
maxretry = 3
EOF

systemctl restart fail2ban
systemctl enable fail2ban

# Configuration de la surveillance système
print_header "Configuration de la surveillance"
print_status "Installation des outils de monitoring..."

# Installation de htop et iotop
apt install -y htop iotop

# Configuration de logrotate pour les logs personnalisés
cat > /etc/logrotate.d/communiconnect << EOF
/var/log/communiconnect/*.log {
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

# Création des répertoires nécessaires
print_status "Création des répertoires..."
mkdir -p /var/log/communiconnect
mkdir -p /var/www/communiconnect/static
mkdir -p /var/www/communiconnect/media
chown -R www-data:www-data /var/log/communiconnect
chown -R www-data:www-data /var/www/communiconnect

# Configuration des limites système
print_status "Configuration des limites système..."
cat >> /etc/security/limits.conf << EOF
# Limites pour CommuniConnect
www-data soft nofile 65536
www-data hard nofile 65536
www-data soft nproc 32768
www-data hard nproc 32768
EOF

# Configuration de sysctl pour les performances
print_status "Optimisation des performances système..."
cat >> /etc/sysctl.conf << EOF
# Optimisations pour CommuniConnect
net.core.somaxconn = 65536
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_max_tw_buckets = 2000000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_slow_start_after_idle = 0
EOF

sysctl -p

# Installation des outils de développement Python
print_header "Installation des outils Python"
print_status "Installation des outils de développement Python..."
pip3 install \
    ipython \
    ipdb \
    pytest \
    pytest-django \
    coverage \
    black \
    flake8 \
    isort

# Configuration de l'environnement Python
print_status "Configuration de l'environnement Python..."
cat > /etc/profile.d/communiconnect.sh << EOF
# Configuration CommuniConnect
export PYTHONPATH="/var/www/communiconnect:\$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="communiconnect.settings_production"
EOF

# Installation des outils de monitoring
print_header "Installation des outils de monitoring"
print_status "Installation des outils de monitoring..."

# Installation de netdata (optionnel)
if command -v curl &> /dev/null; then
    print_status "Installation de Netdata pour le monitoring..."
    bash <(curl -Ss https://my-netdata.io/kickstart.sh) --non-interactive
fi

# Configuration des tâches cron
print_status "Configuration des tâches cron..."
cat > /etc/cron.d/communiconnect << EOF
# Tâches cron pour CommuniConnect

# Sauvegarde quotidienne de la base de données
0 2 * * * www-data pg_dump communiconnect_prod > /var/backups/communiconnect_\$(date +\%Y\%m\%d).sql

# Nettoyage des logs anciens
0 3 * * * root find /var/log/communiconnect -name "*.log.*" -mtime +30 -delete

# Vérification de l'espace disque
0 4 * * * root df -h | awk '\$5 > "90%" {system("echo Disque plein: " \$0 | mail -s Alerte disque root@localhost)}'

# Redémarrage hebdomadaire des services
0 5 * * 0 root systemctl restart communiconnect && systemctl restart nginx
EOF

# Création du répertoire de sauvegarde
mkdir -p /var/backups
chown www-data:www-data /var/backups

# Configuration finale
print_header "Configuration finale"
print_status "Redémarrage des services..."
systemctl daemon-reload
systemctl restart nginx
systemctl restart redis-server
systemctl restart fail2ban

# Vérification des services
print_status "Vérification des services..."
systemctl is-active --quiet nginx && print_status "Nginx: ✅ Actif" || print_error "Nginx: ❌ Inactif"
systemctl is-active --quiet redis-server && print_status "Redis: ✅ Actif" || print_error "Redis: ❌ Inactif"
systemctl is-active --quiet postgresql && print_status "PostgreSQL: ✅ Actif" || print_error "PostgreSQL: ❌ Inactif"
systemctl is-active --quiet fail2ban && print_status "Fail2ban: ✅ Actif" || print_error "Fail2ban: ❌ Inactif"

print_header "Installation terminée"
print_status "✅ Toutes les dépendances système ont été installées avec succès!"
print_status "📋 Prochaines étapes:"
echo "   1. Configurer les variables d'environnement dans .env.production"
echo "   2. Exécuter le script de déploiement: ./deploy_production.sh"
echo "   3. Configurer votre domaine dans Nginx"
echo "   4. Obtenir un certificat SSL avec: certbot --nginx -d your-domain.com"
echo "   5. Tester l'application complètement"

print_warning "⚠️  N'oubliez pas de:"
echo "   - Changer les mots de passe par défaut"
echo "   - Configurer les sauvegardes automatiques"
echo "   - Configurer la surveillance et les alertes"
echo "   - Tester la sécurité avec des outils comme nmap" 
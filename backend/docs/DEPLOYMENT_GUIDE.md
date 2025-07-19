# Guide de Déploiement Production - CommuniConnect

Ce guide détaille le processus complet de déploiement de CommuniConnect en production.

## 📋 Prérequis

### Serveur
- Ubuntu 20.04 LTS ou plus récent
- Minimum 2GB RAM
- Minimum 20GB espace disque
- Accès root ou sudo

### Domaine
- Un nom de domaine configuré
- Accès aux enregistrements DNS

## 🚀 Étapes de Déploiement

### 1. Préparation du Serveur

#### 1.1 Connexion au serveur
```bash
ssh root@your-server-ip
```

#### 1.2 Mise à jour du système
```bash
apt update && apt upgrade -y
```

#### 1.3 Installation des dépendances système
```bash
cd /opt
git clone https://github.com/your-repo/communiconnect.git
cd communiconnect/backend
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

### 2. Configuration de l'Environnement

#### 2.1 Création du fichier d'environnement
```bash
cp env.production.example .env.production
nano .env.production
```

#### 2.2 Configuration des variables d'environnement

**Variables obligatoires :**
```bash
# Django
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,api.your-domain.com

# Base de données PostgreSQL
DB_NAME=communiconnect_prod
DB_USER=communiconnect_user
DB_PASSWORD=your-secure-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Cloudinary CDN
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
USE_CLOUDINARY=True

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@communiconnect.com
ADMIN_EMAIL=admin@communiconnect.com

# CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 3. Configuration de la Base de Données

#### 3.1 Vérification de PostgreSQL
```bash
sudo -u postgres psql -c "\l"
```

#### 3.2 Création de la base de données (si pas déjà fait)
```bash
sudo -u postgres psql -c "CREATE USER communiconnect_user WITH PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "CREATE DATABASE communiconnect_prod OWNER communiconnect_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE communiconnect_prod TO communiconnect_user;"
```

### 4. Configuration de Redis

#### 4.1 Vérification de Redis
```bash
redis-cli ping
```

#### 4.2 Configuration de la sécurité Redis
```bash
# Éditer /etc/redis/redis.conf
nano /etc/redis/redis.conf

# Ajouter/modifier :
bind 127.0.0.1
requirepass your-redis-password
maxmemory 256mb
maxmemory-policy allkeys-lru
```

#### 4.3 Redémarrage de Redis
```bash
systemctl restart redis-server
```

### 5. Configuration de Cloudinary

#### 5.1 Création d'un compte Cloudinary
1. Aller sur [cloudinary.com](https://cloudinary.com)
2. Créer un compte gratuit
3. Récupérer les clés d'API

#### 5.2 Configuration dans l'environnement
```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
USE_CLOUDINARY=True
```

### 6. Déploiement de l'Application

#### 6.1 Exécution du script de déploiement
```bash
chmod +x scripts/deploy_production.sh
./scripts/deploy_production.sh
```

#### 6.2 Vérification des services
```bash
systemctl status communiconnect
systemctl status nginx
systemctl status redis-server
```

### 7. Configuration SSL avec Let's Encrypt

#### 7.1 Installation de Certbot (si pas déjà fait)
```bash
apt install certbot python3-certbot-nginx
```

#### 7.2 Obtention du certificat SSL
```bash
certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 7.3 Configuration du renouvellement automatique
```bash
crontab -e
# Ajouter :
0 12 * * * /usr/bin/certbot renew --quiet
```

### 8. Configuration du Monitoring

#### 8.1 Vérification du monitoring
```bash
systemctl status communiconnect-monitor
tail -f /var/log/communiconnect/monitor.log
```

#### 8.2 Configuration des alertes (optionnel)
```bash
# Configurer les notifications par email
nano /etc/aliases
# Ajouter :
root: your-email@domain.com
```

### 9. Tests de Production

#### 9.1 Test de l'API
```bash
# Test de base
curl -I https://your-domain.com/api/

# Test de l'authentification
curl -X POST https://your-domain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

#### 9.2 Test des performances
```bash
# Test de charge simple
ab -n 1000 -c 10 https://your-domain.com/api/
```

#### 9.3 Test de sécurité
```bash
# Vérification des ports ouverts
nmap -sT your-server-ip

# Test SSL
curl -I https://your-domain.com
```

## 🔧 Configuration Avancée

### Configuration de Nginx

#### Optimisation des performances
```nginx
# /etc/nginx/sites-available/communiconnect
server {
    # ... configuration existante ...
    
    # Optimisations supplémentaires
    client_max_body_size 50M;
    client_body_timeout 60s;
    client_header_timeout 60s;
    
    # Cache pour les fichiers statiques
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Rate limiting pour l'API
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://unix:/run/communiconnect.sock;
    }
}
```

### Configuration de Gunicorn

#### Optimisation des workers
```bash
# Éditer /etc/systemd/system/communiconnect.service
ExecStart=/opt/communiconnect/backend/venv/bin/gunicorn \
    --workers 4 \
    --worker-class gevent \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --bind unix:/run/communiconnect.sock \
    communiconnect.wsgi:application
```

### Configuration de Redis

#### Optimisation pour la production
```bash
# /etc/redis/redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
```

## 📊 Monitoring et Maintenance

### Surveillance des Logs
```bash
# Logs Django
tail -f /var/log/communiconnect/django.log

# Logs Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Logs Redis
tail -f /var/log/redis/redis-server.log

# Logs PostgreSQL
tail -f /var/log/postgresql/postgresql-*.log
```

### Sauvegarde Automatique
```bash
# Vérifier les sauvegardes
ls -la /var/backups/

# Restaurer une sauvegarde
sudo -u postgres psql communiconnect_prod < /var/backups/communiconnect_20231201.sql
```

### Mise à Jour de l'Application
```bash
# Arrêter l'application
systemctl stop communiconnect

# Mettre à jour le code
cd /opt/communiconnect
git pull origin main

# Installer les nouvelles dépendances
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate --settings=communiconnect.settings_production

# Collecter les fichiers statiques
python manage.py collectstatic --noinput --settings=communiconnect.settings_production

# Redémarrer l'application
systemctl start communiconnect
```

## 🛡️ Sécurité

### Configuration du Firewall
```bash
# Vérifier le statut
ufw status

# Autoriser seulement les ports nécessaires
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 22/tcp  # Si vous utilisez un autre port SSH
```

### Configuration de Fail2ban
```bash
# Vérifier les bannissements
fail2ban-client status

# Débannir une IP
fail2ban-client set sshd unbanip IP_ADDRESS
```

### Audit de Sécurité
```bash
# Vérifier les processus en cours
ps aux | grep python

# Vérifier les connexions réseau
netstat -tulpn

# Vérifier les permissions
ls -la /var/www/communiconnect/
```

## 🚨 Dépannage

### Problèmes Courants

#### 1. Application ne démarre pas
```bash
# Vérifier les logs
journalctl -u communiconnect -f

# Vérifier la configuration
python manage.py check --settings=communiconnect.settings_production
```

#### 2. Erreurs de base de données
```bash
# Tester la connexion
python manage.py dbshell --settings=communiconnect.settings_production

# Vérifier les migrations
python manage.py showmigrations --settings=communiconnect.settings_production
```

#### 3. Problèmes Redis
```bash
# Tester Redis
redis-cli ping

# Vérifier la mémoire
redis-cli info memory
```

#### 4. Problèmes Nginx
```bash
# Tester la configuration
nginx -t

# Vérifier les logs
tail -f /var/log/nginx/error.log
```

## 📈 Optimisation des Performances

### Optimisation de la Base de Données
```sql
-- Analyser les requêtes lentes
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Nettoyer les statistiques
SELECT pg_stat_statements_reset();
```

### Optimisation du Cache Redis
```bash
# Vérifier l'utilisation mémoire
redis-cli info memory

# Nettoyer le cache si nécessaire
redis-cli FLUSHALL
```

### Monitoring des Performances
```bash
# Utilisation CPU et mémoire
htop

# Utilisation disque
df -h

# Connexions réseau
ss -tulpn
```

## 📞 Support

En cas de problème :
1. Vérifier les logs dans `/var/log/communiconnect/`
2. Consulter la documentation de l'API : `https://your-domain.com/api/schema/`
3. Vérifier le statut des services : `systemctl status communiconnect nginx redis-server`

---

**Note :** Ce guide suppose une installation sur Ubuntu. Adaptez les commandes pour votre distribution Linux si nécessaire. 
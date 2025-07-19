# CommuniConnect - Guide de Production

Ce guide détaille la configuration et le déploiement de CommuniConnect en production.

## 🚀 Déploiement Rapide

### 1. Installation des Dépendances Système

```bash
# Se connecter au serveur
ssh root@your-server-ip

# Cloner le projet
cd /opt
git clone https://github.com/your-repo/communiconnect.git
cd communiconnect/backend

# Installer les dépendances système
./scripts/install_dependencies.sh
```

### 2. Configuration de l'Environnement

```bash
# Copier le fichier d'exemple
cp env.production.example .env.production

# Éditer les variables d'environnement
nano .env.production
```

**Variables obligatoires à configurer :**
- `SECRET_KEY` : Clé secrète Django
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` : Configuration PostgreSQL
- `REDIS_PASSWORD` : Mot de passe Redis
- `CLOUDINARY_*` : Configuration Cloudinary CDN
- `EMAIL_*` : Configuration email
- `ALLOWED_HOSTS` : Domaines autorisés

### 3. Déploiement de l'Application

```bash
# Exécuter le script de déploiement
./scripts/deploy_production.sh
```

### 4. Configuration SSL

```bash
# Obtenir un certificat SSL
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 📋 Vérification de la Configuration

### Vérification Automatique

```bash
# Vérifier la configuration de production
python scripts/check_production.py
```

### Vérification Manuelle

```bash
# Vérifier les services
systemctl status communiconnect nginx redis-server postgresql

# Vérifier les logs
tail -f /var/log/communiconnect/django.log
tail -f /var/log/nginx/error.log

# Tester l'API
curl -I https://your-domain.com/api/
```

## 🔧 Configuration Avancée

### Optimisation des Performances

#### Nginx
```nginx
# /etc/nginx/sites-available/communiconnect
# Ajouter ces optimisations :

# Compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;

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
```

#### Gunicorn
```bash
# Optimiser les workers dans /etc/systemd/system/communiconnect.service
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

#### Redis
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

### Sécurité

#### Firewall
```bash
# Configurer UFW
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

#### Fail2ban
```bash
# Vérifier les bannissements
fail2ban-client status

# Débannir une IP
fail2ban-client set sshd unbanip IP_ADDRESS
```

## 📊 Monitoring

### Surveillance Automatique

Le script de monitoring surveille automatiquement :
- Utilisation CPU, mémoire, disque
- État de Redis et PostgreSQL
- Performance de l'application
- Services externes (Cloudinary)

```bash
# Vérifier le monitoring
systemctl status communiconnect-monitor
tail -f /var/log/communiconnect/monitor.log

# Voir les métriques
cat /var/log/communiconnect/metrics.json
```

### Logs Importants

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

## 🔄 Maintenance

### Sauvegarde

```bash
# Sauvegarde automatique (configurée dans cron)
ls -la /var/backups/

# Sauvegarde manuelle
sudo -u postgres pg_dump communiconnect_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Mise à Jour

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

### Nettoyage

```bash
# Nettoyer les logs anciens
find /var/log/communiconnect -name "*.log.*" -mtime +30 -delete

# Nettoyer les sauvegardes anciennes
find /var/backups -name "*.sql" -mtime +90 -delete

# Nettoyer le cache Redis si nécessaire
redis-cli FLUSHALL
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

### Commandes Utiles

```bash
# Redémarrer tous les services
systemctl restart communiconnect nginx redis-server

# Vérifier l'espace disque
df -h

# Vérifier l'utilisation mémoire
free -h

# Vérifier les processus
ps aux | grep python

# Vérifier les connexions réseau
ss -tulpn
```

## 📈 Optimisation des Performances

### Base de Données

```sql
-- Analyser les requêtes lentes
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Nettoyer les statistiques
SELECT pg_stat_statements_reset();
```

### Cache Redis

```bash
# Vérifier l'utilisation mémoire
redis-cli info memory

# Vérifier les clés
redis-cli keys "*"

# Nettoyer le cache si nécessaire
redis-cli FLUSHALL
```

### Application

```bash
# Vérifier les performances
ab -n 1000 -c 10 https://your-domain.com/api/

# Vérifier les requêtes lentes
tail -f /var/log/communiconnect/django.log | grep "slow"
```

## 🔐 Sécurité

### Audit de Sécurité

```bash
# Vérifier les ports ouverts
nmap -sT your-server-ip

# Vérifier les processus
ps aux | grep python

# Vérifier les permissions
ls -la /var/www/communiconnect/
```

### Mise à Jour de Sécurité

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Redémarrer les services
systemctl restart nginx redis-server postgresql
```

## 📞 Support

En cas de problème :

1. **Vérifier les logs** : `/var/log/communiconnect/`
2. **Consulter la documentation API** : `https://your-domain.com/api/schema/`
3. **Vérifier le statut des services** : `systemctl status communiconnect nginx redis-server`
4. **Exécuter la vérification automatique** : `python scripts/check_production.py`

### Informations Système

```bash
# Informations système
uname -a
lsb_release -a

# Informations réseau
ip addr show
ip route show

# Informations disque
df -h
lsblk
```

---

**Note :** Ce guide suppose une installation sur Ubuntu 20.04+. Adaptez les commandes pour votre distribution Linux si nécessaire. 
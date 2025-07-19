# 🚀 Déploiement CommuniConnect sur Render

## 📋 Prérequis

1. **Compte Render** : Créer un compte sur [render.com](https://render.com)
2. **Repository GitHub** : CommuniConnect doit être sur GitHub
3. **Base de données PostgreSQL** : Incluse gratuitement avec Render

## 🔧 Configuration Render

### 1. Créer un nouveau service Web

1. Aller sur [render.com](https://render.com)
2. Cliquer sur "New +" → "Web Service"
3. Connecter votre repository GitHub
4. Sélectionner le repository CommuniConnect

### 2. Configuration du service

**Nom du service** : `communiconnect-backend`
**Environnement** : `Python 3`
**Plan** : `Free`
**Branch** : `main` (ou votre branche principale)

### 3. Variables d'environnement

Configurer les variables suivantes dans Render :

```bash
# Configuration Django
DJANGO_SETTINGS_MODULE=communiconnect.settings_render
DEBUG=False
SECRET_KEY=<généré automatiquement par Render>

# Base de données (automatique avec Render)
DATABASE_URL=<fourni automatiquement par Render>

# Configuration CORS
ALLOWED_HOSTS=.render.com

# Configuration des médias
MEDIA_URL=/media/
STATIC_URL=/static/
```

### 4. Configuration du build

**Build Command** :
```bash
pip install -r requirements_render.txt
```

**Start Command** :
```bash
cd backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn communiconnect.wsgi:application
```

## 🗄️ Configuration de la base de données

### 1. Créer une base de données PostgreSQL

1. Dans Render, aller à "New +" → "PostgreSQL"
2. Nom : `communiconnect-db`
3. Plan : `Free`
4. Database : `communiconnect`
5. User : `communiconnect_user`

### 2. Connecter la base de données au service

1. Dans votre service web, aller à "Environment"
2. Ajouter la variable `DATABASE_URL`
3. Utiliser la valeur fournie par Render

## 🌐 Configuration du domaine

### URL automatique
Render fournit automatiquement une URL : `https://communiconnect-backend.onrender.com`

### Domaine personnalisé (optionnel)
1. Aller dans les paramètres du service
2. Section "Custom Domains"
3. Ajouter votre domaine

## 📁 Structure des fichiers

```
CommuniConnect/
├── render.yaml              # Configuration Render
├── requirements_render.txt   # Dépendances optimisées
├── build.sh                 # Script de build
├── backend/
│   ├── communiconnect/
│   │   ├── settings.py      # Settings de développement
│   │   └── settings_render.py # Settings pour Render
│   └── manage.py
└── frontend/                # Frontend React
```

## 🔍 Monitoring et logs

### Logs en temps réel
1. Dans votre service Render
2. Onglet "Logs"
3. Voir les logs en temps réel

### Monitoring
- **Uptime** : Automatique avec Render
- **Performance** : Inclus dans le plan gratuit
- **Alertes** : Configurables

## ⚡ Optimisations pour Render gratuit

### Limitations du plan gratuit
- **750h/mois** : Suffisant pour les tests
- **Endormissement** : Après 15min d'inactivité
- **Redémarrage** : 30-60 secondes
- **RAM** : 512MB
- **CPU** : Partagé

### Optimisations appliquées
1. **Cache local** : Utilisation de LocMemCache
2. **Fichiers statiques** : WhiteNoise pour servir les statiques
3. **Base de données** : Connexions optimisées
4. **Logs** : Configuration minimale
5. **Fonctionnalités avancées** : Désactivées pour économiser les ressources

## 🚀 Déploiement automatique

### Branches configurées
- **main** : Déploiement automatique
- **develop** : Tests et développement

### Triggers
- **Push** : Déploiement automatique
- **Pull Request** : Tests automatiques

## 🔧 Dépannage

### Problèmes courants

#### 1. Erreur de migration
```bash
# Solution : Vérifier les migrations
python manage.py showmigrations
python manage.py migrate --plan
```

#### 2. Erreur de fichiers statiques
```bash
# Solution : Recollecter les statiques
python manage.py collectstatic --noinput --clear
```

#### 3. Erreur de base de données
```bash
# Solution : Vérifier la connexion
python manage.py dbshell
```

#### 4. Service qui ne démarre pas
- Vérifier les logs dans Render
- Vérifier les variables d'environnement
- Vérifier la commande de démarrage

### Commandes utiles

```bash
# Vérifier la configuration
python manage.py check --deploy

# Tester la base de données
python manage.py dbshell

# Vérifier les fichiers statiques
python manage.py collectstatic --dry-run

# Tester les URLs
python manage.py check --urls
```

## 📊 Monitoring et métriques

### Métriques disponibles
- **Uptime** : Temps de disponibilité
- **Response Time** : Temps de réponse
- **Error Rate** : Taux d'erreurs
- **Memory Usage** : Utilisation mémoire
- **CPU Usage** : Utilisation CPU

### Alertes configurées
- **Downtime** : Service indisponible
- **High Error Rate** : Taux d'erreurs élevé
- **Memory Usage** : Utilisation mémoire élevée

## 🔐 Sécurité

### Configuration de sécurité
- **HTTPS** : Automatique avec Render
- **HSTS** : Activé
- **CORS** : Configuré pour le frontend
- **CSRF** : Activé
- **XSS Protection** : Activé

### Variables sensibles
- **SECRET_KEY** : Généré automatiquement
- **DATABASE_URL** : Fourni par Render
- **API Keys** : À configurer manuellement

## 📈 Évolutivité

### Passage au plan payant
Quand vous êtes prêt pour un serveur payant :

1. **Upgrade** : Passer au plan Starter ($7/mois)
2. **Performance** : Plus de RAM et CPU
3. **Uptime** : Pas d'endormissement
4. **Support** : Support prioritaire

### Migration vers un autre provider
- **Heroku** : Configuration similaire
- **DigitalOcean** : Plus de contrôle
- **AWS** : Scalabilité maximale

## 🎯 Prochaines étapes

1. **Déployer le backend** sur Render
2. **Configurer le frontend** (Vercel recommandé)
3. **Tester l'application** complète
4. **Configurer le monitoring**
5. **Préparer la migration** vers un serveur payant

## 📞 Support

- **Documentation Render** : [docs.render.com](https://docs.render.com)
- **Communauté** : [Render Community](https://community.render.com)
- **Support** : Via le dashboard Render

---

**CommuniConnect est maintenant prêt pour le déploiement sur Render !** 🚀 
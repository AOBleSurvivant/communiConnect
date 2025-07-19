# CommuniConnect - Plateforme Communautaire

Une plateforme communautaire moderne inspirée de Facebook, permettant aux utilisateurs de partager des publications avec images, vidéos et live streaming.

## 🚀 Fonctionnalités Principales

### 📱 Publication Multimédia
- **Upload d'images** : Support des formats JPEG, PNG, GIF, WebP (max 10MB)
- **Upload de vidéos** : Formats MP4, WebM, QuickTime, AVI (max 50MB, 60s max)
- **Drag & Drop** : Interface intuitive pour sélectionner les fichiers
- **Aperçu instantané** : Prévisualisation des médias avant publication
- **Galerie multimédia** : Affichage élégant des images et vidéos

### 🔴 Live Streaming
- **Streaming en direct** : Utilisation de la webcam et du microphone
- **Chat en temps réel** : Messages instantanés pendant le live
- **Contrôles live** : Mute/unmute, activation/désactivation vidéo
- **Badge "EN DIRECT"** : Indicateur visuel pour les lives actifs

### 🛡️ Modération Automatique
- **Analyse d'images** : Intégration Google Cloud Vision API
- **Détection de contenu inapproprié** : Nudité, violence, contenu choquant
- **Validation vidéo** : Vérification automatique de la durée (60s max)
- **Système d'approbation** : Statuts pending/approved/rejected

### 🎨 Interface Facebook-like
- **Design moderne** : Interface inspirée de Facebook
- **Responsive** : Compatible mobile, tablette, desktop
- **Animations fluides** : Transitions et micro-interactions
- **Galerie plein écran** : Visualisation optimale des médias

## 🛠️ Architecture Technique

### Backend (Django)
```
backend/
├── posts/
│   ├── models.py          # Modèles Post, Media, Comment, Like
│   ├── views.py           # API REST pour les posts et médias
│   ├── serializers.py     # Sérialiseurs Django REST
│   ├── services.py        # Services de modération et traitement
│   └── urls.py           # Routes API
├── users/                 # Gestion des utilisateurs
├── geography/            # Modèles géographiques
└── communiconnect/       # Configuration Django
```

### Frontend (React)
```
frontend/src/
├── components/
│   ├── CreatePost.js      # Interface de création de posts
│   ├── PostCard.js        # Affichage des posts
│   ├── MediaGallery.js    # Galerie multimédia
│   └── LiveStream.js      # Interface de live streaming
├── services/
│   ├── postsAPI.js        # API posts
│   └── mediaAPI.js        # API médias avec upload progress
└── pages/
    └── Dashboard.js       # Page principale
```

## 📋 Prérequis

### Système
- Python 3.8+
- Node.js 16+
- FFmpeg (pour le traitement vidéo)
- Git

### Services Externes (Optionnels)
- Google Cloud Vision API (pour la modération)
- Serveur RTMP (pour le live streaming)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd CommuniConnect
```

### 2. Backend Django
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend React
```bash
cd frontend
npm install
npm start
```

### 4. Configuration (Optionnel)
```bash
# Variables d'environnement pour la modération
export GOOGLE_CLOUD_VISION_API_KEY="your-api-key"

# Configuration RTMP pour le live
export RTMP_SERVER_URL="rtmp://your-server.com/live"
export HLS_SERVER_URL="http://your-server.com/hls"
```

## 📖 Utilisation

### Publication avec Médias
1. Cliquer sur "Nouvelle publication"
2. Rédiger le contenu
3. Glisser-déposer des images/vidéos ou cliquer "Photo/Vidéo"
4. Apercevoir les fichiers sélectionnés
5. Choisir le type de publication et la confidentialité
6. Publier

### Live Streaming
1. Cliquer sur "Lancer un live"
2. Autoriser l'accès caméra/microphone
3. Configurer le titre et la description
4. Démarrer le live
5. Interagir avec le chat en temps réel
6. Arrêter le live

### Modération
- Les images sont automatiquement analysées
- Les vidéos sont validées pour la durée
- Contenu inapproprié rejeté automatiquement
- Système d'approbation manuelle disponible

## 🔧 Configuration Avancée

### Modération avec Google Cloud Vision
```python
# settings.py
GOOGLE_CLOUD_VISION_API_KEY = "your-api-key"
```

### Live Streaming RTMP
```python
# settings.py
RTMP_SERVER_URL = "rtmp://your-server.com/live"
HLS_SERVER_URL = "http://your-server.com/hls"
```

### Compression des Médias
```python
# services.py
MediaCompressionService.compress_image(image_file, max_width=1920, quality=85)
```

## 📊 API Endpoints

### Posts
- `GET /api/posts/` - Lister les posts
- `POST /api/posts/` - Créer un post
- `GET /api/posts/{id}/` - Détails d'un post
- `PUT /api/posts/{id}/` - Modifier un post
- `DELETE /api/posts/{id}/` - Supprimer un post

### Médias
- `POST /api/posts/media/upload/` - Upload de média
- `GET /api/posts/media/` - Lister les médias
- `GET /api/posts/media/{id}/` - Détails d'un média

### Live Streaming
- `POST /api/posts/live/start/` - Démarrer un live
- `PUT /api/posts/live/{id}/stop/` - Arrêter un live

### Interactions
- `POST /api/posts/{id}/like/` - Liker un post
- `DELETE /api/posts/{id}/like/` - Unliker un post
- `GET /api/posts/{id}/comments/` - Commentaires d'un post
- `POST /api/posts/{id}/comments/` - Ajouter un commentaire

## 🎯 Fonctionnalités Clés

### ✅ Implémentées
- [x] Upload d'images et vidéos avec drag & drop
- [x] Aperçu instantané des médias
- [x] Validation automatique des durées vidéo
- [x] Modération automatique des images
- [x] Live streaming avec webcam
- [x] Chat en temps réel
- [x] Interface Facebook-like
- [x] Galerie multimédia responsive
- [x] Système de likes et commentaires
- [x] Gestion des permissions

### 🔄 En Développement
- [ ] Modération vidéo avancée
- [ ] Compression automatique des médias
- [ ] Notifications push
- [ ] Partage de posts
- [ ] Stories/Reels
- [ ] Messagerie privée

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation technique
- Contacter l'équipe de développement

---

**CommuniConnect** - Connecter les communautés locales 🌍 
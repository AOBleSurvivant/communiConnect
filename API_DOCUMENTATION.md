# 📚 Documentation API - CommuniConnect

## 🌐 **Accès à la Documentation Interactive**

### URLs de Documentation
- **Swagger UI** : `http://localhost:8000/api/docs/`
- **ReDoc** : `http://localhost:8000/api/redoc/`
- **Schema OpenAPI** : `http://localhost:8000/api/schema/`

---

## 🔐 **Authentification**

### JWT Token
L'API utilise l'authentification JWT. Incluez le token dans le header :
```http
Authorization: Bearer <your-jwt-token>
```

### Obtenir un Token
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Réponse
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📝 **Endpoints Principaux**

### 1. **Posts** - Gestion des Publications

#### Lister les Posts
```http
GET /api/posts/
Authorization: Bearer <token>
```

**Paramètres de requête :**
- `page` : Numéro de page (défaut: 1)
- `post_type` : Type de post (info, event, help, announcement, discussion)

**Réponse :**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe"
      },
      "content": "Mon premier post !",
      "post_type": "info",
      "media_files": [],
      "likes_count": 5,
      "comments_count": 2,
      "views_count": 25,
      "created_at": "2025-01-18T10:30:00Z"
    }
  ]
}
```

#### Créer un Post
```http
POST /api/posts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Mon nouveau post avec médias !",
  "post_type": "event",
  "is_anonymous": false,
  "media_files": [1, 2, 3]
}
```

#### Détails d'un Post
```http
GET /api/posts/{id}/
Authorization: Bearer <token>
```

#### Modifier un Post
```http
PUT /api/posts/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Contenu modifié",
  "post_type": "info"
}
```

#### Supprimer un Post
```http
DELETE /api/posts/{id}/
Authorization: Bearer <token>
```

### 2. **Médias** - Upload et Gestion

#### Uploader un Média
```http
POST /api/posts/media/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "file": <fichier>,
  "title": "Mon image",
  "description": "Description de l'image"
}
```

**Types de fichiers supportés :**
- **Images** : JPEG, PNG, GIF, WebP (max 10MB)
- **Vidéos** : MP4, WebM, QuickTime, AVI (max 50MB, 60s)

**Réponse :**
```json
{
  "id": 42,
  "file": "http://localhost:8000/media/2025/01/18/image.jpg",
  "cdn_url": "https://res.cloudinary.com/...",
  "title": "Mon image",
  "description": "Description de l'image",
  "media_type": "image",
  "file_size": 1024000,
  "width": 1920,
  "height": 1080,
  "approval_status": "approved",
  "created_at": "2025-01-18T10:30:00Z"
}
```

#### Lister les Médias
```http
GET /api/posts/media/
Authorization: Bearer <token>
```

#### Détails d'un Média
```http
GET /api/posts/media/{id}/
Authorization: Bearer <token>
```

### 3. **Interactions** - Likes et Commentaires

#### Liker un Post
```http
POST /api/posts/{id}/like/
Authorization: Bearer <token>
```

#### Unliker un Post
```http
DELETE /api/posts/{id}/like/
Authorization: Bearer <token>
```

#### Lister les Commentaires
```http
GET /api/posts/{id}/comments/
Authorization: Bearer <token>
```

#### Ajouter un Commentaire
```http
POST /api/posts/{id}/comments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Mon commentaire",
  "is_anonymous": false
}
```

#### Répondre à un Commentaire
```http
POST /api/posts/{id}/comments/{comment_id}/reply/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Ma réponse",
  "is_anonymous": false
}
```

### 4. **Live Streaming** - Diffusion en Direct

#### Démarrer un Live
```http
POST /api/posts/live/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Mon live",
  "description": "Description du live",
  "content": "Contenu du post live"
}
```

**Réponse :**
```json
{
  "live_id": 15,
  "stream_key": "live_abc123def456",
  "post_id": 42,
  "rtmp_url": "rtmp://localhost/live/live_abc123def456",
  "hls_url": "http://localhost:8080/hls/live_abc123def456.m3u8"
}
```

#### Arrêter un Live
```http
PUT /api/posts/live/{live_id}/
Authorization: Bearer <token>
```

### 5. **Utilisateurs** - Gestion des Profils

#### Profil Utilisateur
```http
GET /api/users/profile/
Authorization: Bearer <token>
```

#### Posts d'un Utilisateur
```http
GET /api/users/{id}/posts/
Authorization: Bearer <token>
```

---

## 🚀 **Exemples d'Utilisation**

### Exemple Complet : Créer un Post avec Médias

```bash
# 1. Upload des médias
curl -X POST http://localhost:8000/api/posts/media/upload/ \
  -H "Authorization: Bearer <token>" \
  -F "file=@image.jpg" \
  -F "title=Mon image" \
  -F "description=Description de l'image"

# Réponse
{
  "id": 1,
  "file": "http://localhost:8000/media/...",
  "cdn_url": "https://res.cloudinary.com/...",
  "title": "Mon image",
  "media_type": "image",
  "approval_status": "approved"
}

# 2. Créer le post avec les médias
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Mon post avec image !",
    "post_type": "info",
    "media_files": [1]
  }'

# 3. Liker le post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer <token>"

# 4. Ajouter un commentaire
curl -X POST http://localhost:8000/api/posts/1/comments/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Super post !"
  }'
```

### Exemple : Live Streaming

```bash
# 1. Démarrer un live
curl -X POST http://localhost:8000/api/posts/live/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Live de test",
    "description": "Description du live",
    "content": "Contenu du post live"
  }'

# 2. Utiliser les URLs de streaming
# RTMP: rtmp://localhost/live/live_abc123def456
# HLS: http://localhost:8080/hls/live_abc123def456.m3u8

# 3. Arrêter le live
curl -X PUT http://localhost:8000/api/posts/live/15/ \
  -H "Authorization: Bearer <token>"
```

---

## ⚡ **Optimisations et Performance**

### Cache Redis
- **Requêtes posts** : Cache automatique (10min)
- **Sessions utilisateurs** : Cache Redis
- **Données fréquentes** : Cache automatique

### CDN Cloudinary
- **Images** : Optimisation automatique
- **Vidéos** : Compression et format adaptatif
- **URLs** : Génération dynamique avec transformations

### Compression Médias
- **Images** : Redimensionnement automatique (max 1920px)
- **Vidéos** : Compression H.264/WebM
- **Formats** : WebP pour les images, MP4 pour les vidéos

---

## 🔧 **Configuration**

### Variables d'Environnement
```bash
# Redis Cache
REDIS_URL=redis://127.0.0.1:6379

# Cloudinary CDN
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
USE_CLOUDINARY=True

# Google Cloud Vision (modération)
GOOGLE_CLOUD_VISION_API_KEY=your-vision-api-key
```

### Démarrage du Serveur
```bash
# Backend
cd backend
python manage.py runserver

# Frontend (optionnel)
cd frontend
npm start
```

---

## 📊 **Codes de Statut HTTP**

| Code | Description | Exemple |
|------|-------------|---------|
| `200` | Succès | GET /api/posts/ |
| `201` | Créé | POST /api/posts/ |
| `204` | Pas de contenu | DELETE /api/posts/{id}/ |
| `400` | Requête invalide | Données manquantes |
| `401` | Non authentifié | Token manquant/invalide |
| `403` | Non autorisé | Permissions insuffisantes |
| `404` | Non trouvé | Post inexistant |
| `500` | Erreur serveur | Problème interne |

---

## 🐛 **Gestion d'Erreurs**

### Erreurs Courantes

#### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 400 Bad Request
```json
{
  "content": ["Ce champ est requis."],
  "media_files": ["Vous ne pouvez pas ajouter plus de 5 fichiers."]
}
```

#### 403 Forbidden
```json
{
  "detail": "Vous devez avoir un quartier assigné pour publier."
}
```

### Validation des Médias
```json
{
  "file": ["Seuls les fichiers image et vidéo sont autorisés."],
  "file": ["Le fichier ne peut pas dépasser 50MB."]
}
```

---

## 📈 **Métriques et Monitoring**

### Endpoints de Monitoring
- **Health Check** : `GET /api/health/`
- **Stats** : `GET /api/stats/`
- **Cache Status** : `GET /api/cache/status/`

### Métriques Disponibles
- **Posts créés** : Nombre par jour/semaine
- **Médias uploadés** : Volume et types
- **Interactions** : Likes et commentaires
- **Performance** : Temps de réponse API
- **Cache** : Hit/miss ratio Redis

---

## 🎯 **Bonnes Pratiques**

### Performance
1. **Utilisez la pagination** pour les listes
2. **Cachez les tokens** côté client
3. **Compressez les images** avant upload
4. **Utilisez le CDN** pour les médias

### Sécurité
1. **Renouvelez les tokens** régulièrement
2. **Validez les fichiers** côté client
3. **Limitez la taille** des uploads
4. **Utilisez HTTPS** en production

### Développement
1. **Testez avec Swagger** : `/api/docs/`
2. **Utilisez les exemples** fournis
3. **Gérez les erreurs** côté client
4. **Monitorer les performances**

---

## 🚀 **Déploiement**

### Production
```bash
# Variables d'environnement
DEBUG=False
ALLOWED_HOSTS=your-domain.com
USE_CLOUDINARY=True
REDIS_URL=redis://your-redis-server:6379

# Base de données
DATABASE_URL=postgresql://user:pass@host:5432/db

# Sécurité
SECRET_KEY=your-secret-key
```

### Docker (optionnel)
```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## 📞 **Support**

### Documentation Interactive
- **Swagger UI** : `http://localhost:8000/api/docs/`
- **ReDoc** : `http://localhost:8000/api/redoc/`

### Contact
- **Email** : support@communiconnect.com
- **GitHub** : Issues et discussions
- **Documentation** : Ce guide et la doc interactive

---

**CommuniConnect API** - Documentation complète et interactive ! 📚 
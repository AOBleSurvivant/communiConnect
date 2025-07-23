import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_extensions',
    'cacheops',  # Cache automatique pour les requêtes
    'cloudinary',
    'cloudinary_storage',
    'drf_spectacular',  # Documentation API
    'users',
    'geography',
    'api',
    'posts',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Compression HTTP
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware personnalisés
    'users.middleware.SecurityMiddleware',      # Sécurité renforcée
    'users.middleware.PerformanceMiddleware',   # Monitoring performances
    # 'users.middleware.GeographicAccessMiddleware',  # Désactivé pour le développement
]

ROOT_URLCONF = 'communiconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'communiconnect.wsgi.application'

# Database - SQLite pour le développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache Configuration (Redis en production, local en développement)
REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)

if config('USE_REDIS', default=False, cast=bool):
    # Configuration Redis pour la production
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            },
            'KEY_PREFIX': 'communiconnect',
            'TIMEOUT': 300,  # 5 minutes par défaut
        },
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB + 1}',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'sessions',
        },
        'posts': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB + 2}',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'posts',
            'TIMEOUT': 600,  # 10 minutes pour les posts
        },
    }
    
    # Session avec Redis
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'
    
    # Cache pour les requêtes fréquentes
    CACHEOPS_REDIS = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': REDIS_DB + 3,
        'socket_timeout': 3,
    }
    
    CACHEOPS = {
        'posts.Post': {'timeout': 600},  # 10 minutes
        'posts.Media': {'timeout': 300},  # 5 minutes
        'users.User': {'timeout': 300},   # 5 minutes
        'geography.Quartier': {'timeout': 3600},  # 1 heure
    }
else:
    # Configuration locale pour le développement
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,  # 5 minutes par défaut
        },
        'sessions': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'sessions',
        },
        'posts': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'posts',
            'TIMEOUT': 600,  # 10 minutes pour les posts
        },
    }
    
    # Session configuration (fallback vers base de données)
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Conakry'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration des médias avec CDN Cloudinary
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration Cloudinary CDN
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
    'SECURE': True,
    'MEDIA_TAG': 'communiconnect',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Vidéo non supportée',
    'STATIC_TAG': 'static',
    'MAGIC_FILE_PATH': 'magic',
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr', 'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    'STATIC_VIDEOS_EXTENSIONS': ['mp4', 'webm', 'flv', 'mov', 'ogv', '3gp', '3g2', 'wmv', 'mpeg', 'flv', 'avi'],
}

# Utiliser Cloudinary pour les médias en production, sinon local
if config('USE_CLOUDINARY', default=False, cast=bool):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
else:
    # Fallback vers stockage local pour le développement
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Configuration pour les fichiers uploadés
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Optimisations de performance avancées
GZIP_CONTENT_TYPES = [
    'text/html',
    'text/css',
    'text/javascript',
    'application/javascript',
    'application/json',
    'application/xml',
    'text/xml',
]

# Configuration de la compression
GZIP_MIN_SIZE = 800  # Taille minimale pour la compression

# Configuration des connexions de base de données
DATABASE_CONNECTION_POOL = {
    'max_connections': 20,
    'max_overflow': 30,
    'pool_timeout': 30,
    'pool_recycle': 3600,
}

# Configuration du cache avancé
CACHE_TIMEOUTS = {
    'posts_list': 300,      # 5 minutes
    'post_detail': 120,      # 2 minutes
    'user_profile': 600,     # 10 minutes
    'media_list': 1800,      # 30 minutes
    'analytics': 3600,       # 1 heure
}

# Configuration de la pagination
PAGINATION_PAGE_SIZE = 20
PAGINATION_MAX_PAGE_SIZE = 100

# Configuration des médias optimisés
MEDIA_OPTIMIZATION = {
    'image_quality': 85,
    'max_width': 1920,
    'max_height': 1080,
    'thumbnail_sizes': [150, 300, 600],
    'video_compression': True,
    'auto_webp': True,
}

# Configuration de la sécurité et performance
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Taille maximale des fichiers (50MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Types de fichiers autorisés
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/gif',
    'image/webp'
]

ALLOWED_VIDEO_TYPES = [
    'video/mp4',
    'video/webm',
    'video/quicktime',
    'video/avi'
]

# Configuration de modération (Google Cloud Vision)
GOOGLE_CLOUD_VISION_API_KEY = os.environ.get('GOOGLE_CLOUD_VISION_API_KEY', '')

# Configuration pour le live streaming
RTMP_SERVER_URL = os.environ.get('RTMP_SERVER_URL', 'rtmp://localhost/live')
HLS_SERVER_URL = os.environ.get('HLS_SERVER_URL', 'http://localhost:8080/hls')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Rate limiting pour la sécurité
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'posts': '50/minute',
        'media': '20/minute',
        'auth': '10/minute',
    },
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Documentation API avec drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'CommuniConnect API',
    'DESCRIPTION': '''
    API REST pour la plateforme communautaire CommuniConnect.
    
    ## Fonctionnalités principales
    - **Posts** : Création, lecture, modification, suppression de posts
    - **Médias** : Upload d'images et vidéos avec optimisation CDN
    - **Interactions** : Likes, commentaires, réponses
    - **Live Streaming** : Diffusion en direct avec chat
    - **Géolocalisation** : Posts par quartier et région
    
    ## Authentification
    L'API utilise l'authentification JWT. Incluez le token dans le header :
    ```
    Authorization: Bearer <your-jwt-token>
    ```
    
    ## Optimisations
    - Cache Redis pour les performances
    - CDN Cloudinary pour les médias
    - Compression automatique des images
    - Modération automatique du contenu
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'CONTACT': {
        'name': 'CommuniConnect Team',
        'email': 'support@communiconnect.com',
    },
    'LICENSE': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
    'TAGS': [
        {'name': 'posts', 'description': 'Gestion des posts et publications'},
        {'name': 'media', 'description': 'Upload et gestion des médias'},
        {'name': 'interactions', 'description': 'Likes, commentaires et interactions'},
        {'name': 'live', 'description': 'Live streaming et diffusion'},
        {'name': 'users', 'description': 'Gestion des utilisateurs'},
        {'name': 'geography', 'description': 'Géolocalisation et quartiers'},
    ],
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayRequestDuration': True,
        'filter': True,
    },
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3004",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3004",
]

# CORS additional settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Sécurité renforcée
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Geographic restrictions
GUINEA_COUNTRY_CODE = 'GN'
GUINEA_IP_RANGES = [
    # Add specific IP ranges for Guinea if available
]

# Configuration des logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'posts': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'media': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
} 
"""
Settings pour Render - CommuniConnect
Optimisé pour l'environnement gratuit Render
"""

import os
from .settings import *

# Configuration Render
DEBUG = False
ALLOWED_HOSTS = ['.render.com', 'localhost', '127.0.0.1']

# Base de données PostgreSQL Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'communiconnect'),
        'USER': os.environ.get('DATABASE_USER', 'communiconnect_user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Configuration pour Render
if os.environ.get('RENDER'):
    # Utiliser la variable DATABASE_URL de Render
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )

# Sécurité
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuration des médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration du cache pour Render (limitations gratuites)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configuration des sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 heure

# Configuration des logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Optimisations pour Render (limitations gratuites)
# Désactiver certaines fonctionnalités gourmandes en ressources
PERFORMANCE_MONITORING_ENABLED = False
ANALYTICS_PREDICTIVE_ENABLED = False
SECURITY_ADVANCED_MONITORING = False

# Configuration CORS pour le frontend
CORS_ALLOWED_ORIGINS = [
    "https://communiconnect.onrender.com",
    "https://communiconnect-frontend.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Configuration des middlewares optimisés
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour servir les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration WhiteNoise pour les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration des applications installées (optimisées pour Render)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'users',
    'posts',
    'notifications',
    'geography',
    # Applications avancées (désactivées pour Render gratuit)
    # 'performance',
    # 'analytics', 
    # 'security',
]

# Configuration REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Configuration des URLs
ROOT_URLCONF = 'communiconnect.urls'

# Configuration de la langue et du fuseau horaire
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Conakry'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers de traduction
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Configuration des messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Configuration des tests
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Configuration des migrations
MIGRATION_MODULES = {
    'users': 'users.migrations',
    'posts': 'posts.migrations',
    'notifications': 'notifications.migrations',
    'geography': 'geography.migrations',
}

# Configuration des fixtures
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
]

# Configuration des médias (optimisée pour Render)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Configuration des emails (désactivée pour Render gratuit)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuration des caches (optimisée pour Render)
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'communiconnect'

# Configuration des sessions (optimisée pour Render)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Configuration de sécurité (optimisée pour Render)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuration des fichiers statiques (optimisée pour Render)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuration des logs (optimisée pour Render)
LOGGING_CONFIG = None

import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING) 
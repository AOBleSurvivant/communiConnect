#!/usr/bin/env python
"""
Test simple pour vérifier que l'application Django peut démarrer sur Render
"""
import os
import sys
import django

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings_render')
django.setup()

# Test d'import des modèles
try:
    from django.contrib.auth import get_user_model
    from posts.models import Post
    print("✅ Import des modèles réussi")
except Exception as e:
    print(f"❌ Erreur import modèles: {e}")

# Test de configuration
try:
    from django.conf import settings
    print(f"✅ Settings chargées: DEBUG={settings.DEBUG}")
    print(f"✅ Base de données: {settings.DATABASES['default']['ENGINE']}")
    print(f"✅ Apps installées: {len(settings.INSTALLED_APPS)}")
except Exception as e:
    print(f"❌ Erreur configuration: {e}")

print("🎉 Test de configuration terminé") 
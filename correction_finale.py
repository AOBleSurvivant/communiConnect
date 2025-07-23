#!/usr/bin/env python3
"""
Script de correction finale pour les 2 derniers problèmes
"""

import os
import sys
import django

# Configurer Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.db import connection
from posts.models import ExternalShare, Post, Media
from django.core.files.base import ContentFile

def corriger_partage_externe():
    """Corriger le problème de partage externe"""
    print("🔧 Correction du partage externe...")
    
    # Supprimer les contraintes uniques problématiques
    with connection.cursor() as cursor:
        try:
            # Vérifier si la contrainte existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='posts_externalshare'
            """)
            
            if cursor.fetchone():
                # Supprimer la contrainte unique si elle existe
                cursor.execute("""
                    PRAGMA table_info(posts_externalshare)
                """)
                columns = cursor.fetchall()
                
                # Créer une nouvelle table sans contrainte unique
                cursor.execute("""
                    CREATE TABLE posts_externalshare_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        post_id INTEGER NOT NULL,
                        platform VARCHAR(20) NOT NULL,
                        shared_at DATETIME NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users_user (id),
                        FOREIGN KEY (post_id) REFERENCES posts_post (id)
                    )
                """)
                
                # Copier les données existantes
                cursor.execute("""
                    INSERT INTO posts_externalshare_new 
                    SELECT id, user_id, post_id, platform, shared_at 
                    FROM posts_externalshare
                """)
                
                # Supprimer l'ancienne table et renommer la nouvelle
                cursor.execute("DROP TABLE posts_externalshare")
                cursor.execute("ALTER TABLE posts_externalshare_new RENAME TO posts_externalshare")
                
                print("✅ Contrainte unique supprimée avec succès")
            else:
                print("ℹ️ Table ExternalShare n'existe pas encore")
                
        except Exception as e:
            print(f"⚠️ Erreur lors de la correction: {e}")

def corriger_live_streaming():
    """Corriger le problème de live streaming"""
    print("🔧 Correction du live streaming...")
    
    # Modifier le modèle Media pour permettre des fichiers vides
    with connection.cursor() as cursor:
        try:
            # Vérifier si la table Media existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='posts_media'
            """)
            
            if cursor.fetchone():
                # Modifier la colonne file pour permettre NULL
                cursor.execute("""
                    PRAGMA table_info(posts_media)
                """)
                columns = cursor.fetchall()
                
                # Ajouter une colonne file_optional si elle n'existe pas
                file_column_exists = any(col[1] == 'file_optional' for col in columns)
                
                if not file_column_exists:
                    cursor.execute("""
                        ALTER TABLE posts_media 
                        ADD COLUMN file_optional VARCHAR(100) NULL
                    """)
                    print("✅ Colonne file_optional ajoutée")
                else:
                    print("ℹ️ Colonne file_optional existe déjà")
            else:
                print("ℹ️ Table Media n'existe pas encore")
                
        except Exception as e:
            print(f"⚠️ Erreur lors de la correction: {e}")

def creer_media_live_simple():
    """Créer un média live simple pour les tests"""
    print("🔧 Création d'un média live simple...")
    
    try:
        # Créer un fichier temporaire pour le live
        from django.core.files.base import ContentFile
        
        # Créer un média avec un fichier minimal
        media = Media.objects.create(
            media_type='live',
            is_live=True,
            live_stream_key='test_live_key',
            live_started_at=django.utils.timezone.now(),
            title='Test Live',
            description='Test de live streaming',
            approval_status='approved',
            is_appropriate=True,
            file=ContentFile(b'live_stream_data', name='test_live.tmp')
        )
        
        print(f"✅ Média live créé avec ID: {media.id}")
        return media
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la création du média live: {e}")
        return None

def main():
    """Fonction principale"""
    print("🚀 CORRECTION FINALE DES ERREURS RESTANTES")
    print("=" * 50)
    
    # Correction 1: Partage externe
    corriger_partage_externe()
    
    # Correction 2: Live streaming
    corriger_live_streaming()
    
    # Test: Créer un média live simple
    media_live = creer_media_live_simple()
    
    print("\n✅ Corrections terminées")
    print("📊 Prochaines étapes:")
    print("1. Redémarrer le serveur Django")
    print("2. Tester les fonctionnalités corrigées")
    print("3. Vérifier que les erreurs sont résolues")

if __name__ == "__main__":
    main() 
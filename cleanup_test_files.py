#!/usr/bin/env python
import os
import glob

def cleanup_test_files():
    """Nettoyer les fichiers de test temporaires"""
    print("🧹 Nettoyage des fichiers de test temporaires...")
    
    # Liste des fichiers à supprimer
    test_files = [
        'test_api_posts.py',
        'simple_test.py', 
        'test_media_upload.py',
        'debug_live_streaming.py',
        'test_share_posts.py',
        'test_final_complet.py',
        'fix_live_streaming.py',
        'cleanup_test_files.py'
    ]
    
    # Liste des rapports à conserver
    reports_to_keep = [
        'RAPPORT_FINAL_MEDIAS.md',
        'RAPPORT_FINAL_CORRECTIONS.md',
        'ETAT_ACTUEL_COMMUNICONNECT.md'
    ]
    
    deleted_count = 0
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ Supprimé: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur suppression {file}: {str(e)}")
    
    print(f"\n✅ Nettoyage terminé: {deleted_count} fichiers supprimés")
    print(f"📋 Rapports conservés: {', '.join(reports_to_keep)}")
    
    # Afficher les fichiers restants
    remaining_files = [f for f in os.listdir('.') if f.endswith('.py') or f.endswith('.md')]
    print(f"\n📁 Fichiers restants dans le répertoire:")
    for file in sorted(remaining_files):
        print(f"  📄 {file}")

if __name__ == "__main__":
    cleanup_test_files() 
#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from posts.models import Post, ExternalShare
from users.models import User

def check_external_share_model():
    """Vérifier le modèle ExternalShare"""
    print("🔍 Vérification du modèle ExternalShare...")
    
    try:
        # Vérifier les champs du modèle
        fields = ExternalShare._meta.get_fields()
        field_names = [field.name for field in fields]
        
        print(f"✅ Modèle ExternalShare trouvé")
        print(f"📋 Champs: {field_names}")
        
        # Vérifier les choix de plateforme
        if hasattr(ExternalShare, 'PLATFORM_CHOICES'):
            choices = ExternalShare.PLATFORM_CHOICES
            print(f"🌐 Plateformes supportées: {choices}")
        else:
            print("⚠️ Pas de PLATFORM_CHOICES défini")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur modèle ExternalShare: {str(e)}")
        return False

def test_external_share_creation():
    """Tester la création d'un ExternalShare"""
    print("\n🧪 Test de création d'ExternalShare...")
    
    try:
        # Récupérer un utilisateur et un post
        user = User.objects.get(username='mariam_diallo')
        post = Post.objects.first()
        
        if not post:
            print("❌ Aucun post disponible")
            return False
        
        print(f"👤 Utilisateur: {user.username}")
        print(f"📝 Post: ID {post.id}")
        
        # Créer un ExternalShare
        external_share = ExternalShare.objects.create(
            user=user,
            post=post,
            platform='whatsapp'
        )
        
        print(f"✅ ExternalShare créé avec succès!")
        print(f"🆔 ID: {external_share.id}")
        print(f"🌐 Plateforme: {external_share.platform}")
        
        # Nettoyer
        external_share.delete()
        print("🗑️ ExternalShare supprimé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création ExternalShare: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def check_external_share_view():
    """Vérifier la vue ExternalShareView"""
    print("\n🔍 Vérification de la vue ExternalShareView...")
    
    try:
        from posts.views import ExternalShareView
        
        # Vérifier les attributs de la vue
        print(f"✅ Vue ExternalShareView trouvée")
        print(f"📋 Serializer: {ExternalShareView.serializer_class}")
        print(f"🔐 Permissions: {ExternalShareView.permission_classes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vue ExternalShareView: {str(e)}")
        return False

def main():
    """Diagnostic complet du partage externe"""
    print("🚀 Diagnostic du partage externe")
    print("=" * 50)
    
    # Vérifier le modèle
    model_ok = check_external_share_model()
    
    # Tester la création
    creation_ok = test_external_share_creation()
    
    # Vérifier la vue
    view_ok = check_external_share_view()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    print(f"📋 Modèle ExternalShare: {'✅' if model_ok else '❌'}")
    print(f"🧪 Création ExternalShare: {'✅' if creation_ok else '❌'}")
    print(f"🔍 Vue ExternalShareView: {'✅' if view_ok else '❌'}")
    
    if all([model_ok, creation_ok, view_ok]):
        print("\n🎉 Le partage externe devrait fonctionner!")
        print("Le problème vient probablement de la vue.")
    else:
        print("\n⚠️ Problèmes détectés")
        if not model_ok:
            print("- Le modèle ExternalShare a des problèmes")
        if not creation_ok:
            print("- La création d'ExternalShare échoue")
        if not view_ok:
            print("- La vue ExternalShareView a des problèmes")

if __name__ == "__main__":
    main() 
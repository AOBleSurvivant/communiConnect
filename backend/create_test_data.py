#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from geography.models import Region, Prefecture, Commune, Quartier
from django.contrib.auth import get_user_model
from notifications.models import CommunityAlert

User = get_user_model()

def create_test_data():
    print("🔧 Création des données de test...")
    
    # 1. Récupérer ou créer une région de test
    try:
        region = Region.objects.filter(nom="Conakry").first()
        if not region:
            region = Region.objects.create(
                nom="Conakry",
                code="CONAKRY"
            )
            print(f"✅ Région créée: {region.id} - {region.nom}")
        else:
            print(f"✅ Région existante utilisée: {region.id} - {region.nom}")
    except Exception as e:
        print(f"❌ Erreur création région: {e}")
        return
    
    # 2. Récupérer ou créer une préfecture de test
    try:
        prefecture = Prefecture.objects.filter(region=region, nom="Conakry").first()
        if not prefecture:
            prefecture = Prefecture.objects.create(
                region=region,
                nom="Conakry",
                code="CONAKRY"
            )
            print(f"✅ Préfecture créée: {prefecture.id} - {prefecture.nom}")
        else:
            print(f"✅ Préfecture existante utilisée: {prefecture.id} - {prefecture.nom}")
    except Exception as e:
        print(f"❌ Erreur création préfecture: {e}")
        return
    
    # 3. Récupérer ou créer une commune de test
    try:
        commune = Commune.objects.filter(prefecture=prefecture, nom="Commune de Kaloum").first()
        if not commune:
            commune = Commune.objects.create(
                prefecture=prefecture,
                nom="Commune de Kaloum",
                type="urbaine",
                code="KALOUM"
            )
            print(f"✅ Commune créée: {commune.id} - {commune.nom}")
        else:
            print(f"✅ Commune existante utilisée: {commune.id} - {commune.nom}")
    except Exception as e:
        print(f"❌ Erreur création commune: {e}")
        return
    
    # 4. Récupérer ou créer un quartier de test
    try:
        quartier = Quartier.objects.filter(commune=commune, nom="Quartier Test").first()
        if not quartier:
            quartier = Quartier.objects.create(
                commune=commune,
                nom="Quartier Test",
                code="QT01"
            )
            print(f"✅ Quartier créé: {quartier.id} - {quartier.nom}")
        else:
            print(f"✅ Quartier existant utilisé: {quartier.id} - {quartier.nom}")
    except Exception as e:
        print(f"❌ Erreur création quartier: {e}")
        return
    
    # 5. Récupérer ou créer un utilisateur de test
    try:
        user = User.objects.filter(username="testuser").first()
        if not user:
            user = User.objects.create_user(
                username="testuser",
                email="test@example.com",
                password="testpass123",
                first_name="Test",
                last_name="User"
            )
            user.quartier = quartier
            user.save()
            print(f"✅ Utilisateur créé: {user.username} (ID: {user.id})")
        else:
            print(f"✅ Utilisateur existant utilisé: {user.username} (ID: {user.id})")
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return
    
    # 6. Créer quelques alertes de test (si elles n'existent pas)
    try:
        existing_alerts = CommunityAlert.objects.filter(author=user).count()
        if existing_alerts == 0:
            alert1 = CommunityAlert.objects.create(
                title="Test d'alerte - Fuite de gaz",
                description="Fuite de gaz détectée dans le quartier",
                category="gas_leak",
                status="pending",
                neighborhood="Centre-ville",
                city="Conakry",
                author=user,
                latitude=9.5370,
                longitude=-13.6785
            )
            print(f"✅ Alerte créée: {alert1.title}")
            
            alert2 = CommunityAlert.objects.create(
                title="Test d'alerte - Coupure d'électricité",
                description="Coupure d'électricité dans le secteur",
                category="power_outage",
                status="confirmed",
                neighborhood="Hamdallaye",
                city="Conakry",
                author=user,
                latitude=9.5370,
                longitude=-13.6785
            )
            print(f"✅ Alerte créée: {alert2.title}")
        else:
            print(f"✅ {existing_alerts} alertes existantes trouvées")
        
    except Exception as e:
        print(f"❌ Erreur création alertes: {e}")
    
    # 7. Afficher les statistiques
    print(f"\n📊 Statistiques:")
    print(f"   - Utilisateurs: {User.objects.count()}")
    print(f"   - Régions: {Region.objects.count()}")
    print(f"   - Préfectures: {Prefecture.objects.count()}")
    print(f"   - Communes: {Commune.objects.count()}")
    print(f"   - Quartiers: {Quartier.objects.count()}")
    print(f"   - Alertes: {CommunityAlert.objects.count()}")
    
    print(f"\n🔑 Informations de connexion:")
    print(f"   - Username: testuser")
    print(f"   - Password: testpass123")
    print(f"   - Email: test@example.com")
    
    print(f"\n✅ Données de test créées avec succès!")

if __name__ == "__main__":
    create_test_data() 
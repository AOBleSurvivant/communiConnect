#!/usr/bin/env python
import requests
import time
from datetime import datetime

def verifier_serveur(url, nom):
    """Vérifie si un serveur est accessible"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, f"✅ {nom} accessible (Status: {response.status_code})"
        else:
            return False, f"⚠️ {nom} répond mais avec status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {nom} non accessible (connexion refusée)"
    except requests.exceptions.Timeout:
        return False, f"⏰ {nom} timeout (pas de réponse)"
    except Exception as e:
        return False, f"❌ {nom} erreur: {e}"

def main():
    print("🔍 VÉRIFICATION DES SERVEURS COMMUNICONNECT")
    print("=" * 50)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # URLs à vérifier
    serveurs = [
        ("http://127.0.0.1:8000/admin/", "Backend Django"),
        ("http://127.0.0.1:8000/api/users/geographic-data/", "API Géographie"),
        ("http://localhost:3001", "Frontend React"),
        ("http://localhost:3001/login", "Page Login"),
    ]

    # Vérifier chaque serveur
    resultats = []
    for url, nom in serveurs:
        accessible, message = verifier_serveur(url, nom)
        resultats.append((accessible, message))
        print(message)
        time.sleep(1)  # Pause entre les vérifications

    print()
    print("📊 RÉSUMÉ")
    print("-" * 30)
    
    serveurs_ok = sum(1 for accessible, _ in resultats if accessible)
    total_serveurs = len(resultats)
    
    print(f"✅ Serveurs accessibles: {serveurs_ok}/{total_serveurs}")
    
    if serveurs_ok == total_serveurs:
        print("🎉 TOUS LES SERVEURS FONCTIONNENT !")
        print("🚀 CommuniConnect est prêt à être testé")
    elif serveurs_ok >= 2:
        print("⚠️ La plupart des serveurs fonctionnent")
        print("🔧 Vérifiez les serveurs non accessibles")
    else:
        print("❌ Problèmes détectés")
        print("🔧 Démarrez les serveurs manuellement")

    print()
    print("💡 COMMANDES UTILES:")
    print("   Backend: cd backend && python manage.py runserver")
    print("   Frontend: cd frontend && npm start")
    print("   Test complet: python test_complet_site.py")

if __name__ == "__main__":
    main() 
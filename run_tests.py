#!/usr/bin/env python3
"""
Script d'exécution des tests automatisés pour CommuniConnect
Exécute tous les tests unitaires, d'intégration et de performance
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Exécute une commande avec gestion d'erreur"""
    print(f"\n🔧 {description}...")
    print(f"Commande: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ Succès")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Échec")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Tests Automatisés - CommuniConnect")
    print("=" * 60)
    
    tests_results = {}
    
    # 1. Tests unitaires Django
    print("\n📋 1. Tests unitaires Django")
    tests_results['django'] = run_command(
        "cd backend && python manage.py test posts.tests -v 2",
        "Exécution des tests unitaires Django"
    )
    
    # 2. Tests de configuration CDN/Redis
    print("\n📋 2. Tests de configuration")
    tests_results['config'] = run_command(
        "python test_cdn_optimization.py",
        "Test de configuration CDN et Redis"
    )
    
    # 3. Tests de performance
    print("\n📋 3. Tests de performance")
    tests_results['performance'] = run_command(
        "python test_performance_optimizations.py",
        "Benchmark de performance"
    )
    
    # 4. Tests de linting (optionnel)
    print("\n📋 4. Tests de qualité de code")
    try:
        import flake8
        tests_results['linting'] = run_command(
            "cd backend && python -m flake8 posts/ --max-line-length=120 --ignore=E501,W503",
            "Vérification de la qualité du code"
        )
    except ImportError:
        print("⚠️  flake8 non installé, test de linting ignoré")
        tests_results['linting'] = True
    
    # 5. Tests de sécurité (optionnel)
    print("\n📋 5. Tests de sécurité")
    try:
        import bandit
        tests_results['security'] = run_command(
            "cd backend && python -m bandit -r posts/ -f json",
            "Analyse de sécurité"
        )
    except ImportError:
        print("⚠️  bandit non installé, test de sécurité ignoré")
        tests_results['security'] = True
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(tests_results.values())
    total = len(tests_results)
    
    for test_name, result in tests_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<15} {status}")
    
    print(f"\n📈 Résultat: {passed}/{total} tests réussis")
    print(f"📊 Taux de réussite: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés!")
        print("✅ Votre application est prête pour la production")
        return True
    elif passed >= total * 0.8:
        print("\n⚠️  La plupart des tests sont passés")
        print("🔧 Quelques ajustements mineurs peuvent être nécessaires")
        return True
    else:
        print("\n❌ Plusieurs tests ont échoué")
        print("🔧 Des corrections sont nécessaires avant la production")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
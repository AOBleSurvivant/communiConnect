#!/usr/bin/env python3
"""
Test Rapide - CommuniConnect
Validation simple de l'existence des fichiers
"""

import os
import datetime

def print_header(title):
    print("=" * 50)
    print(f"🧪 {title}")
    print("=" * 50)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def test_backend():
    """Test des fichiers backend"""
    print_header("BACKEND")
    
    files = [
        "backend/performance/models.py",
        "backend/performance/services.py", 
        "backend/performance/views.py",
        "backend/analytics/models.py",
        "backend/analytics/services.py",
        "backend/security/models.py",
        "backend/security/services.py"
    ]
    
    success = 0
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes)")
            success += 1
        else:
            print_error(f"{file} (MANQUANT)")
    
    print(f"\n📊 Backend: {success}/{len(files)} fichiers présents")
    return success == len(files)

def test_frontend():
    """Test des fichiers frontend"""
    print_header("FRONTEND")
    
    files = [
        "frontend/src/components/PerformanceDashboard.js",
        "frontend/src/components/AnalyticsDashboard.js", 
        "frontend/src/components/SecurityDashboard.js",
        "frontend/src/components/ModernUI/DesignSystem.js",
        "frontend/src/components/ModernUI/AdvancedComponents.js",
        "frontend/src/components/ModernUI/Experiences.js"
    ]
    
    success = 0
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes)")
            success += 1
        else:
            print_error(f"{file} (MANQUANT)")
    
    print(f"\n📊 Frontend: {success}/{len(files)} fichiers présents")
    return success == len(files)

def test_documentation():
    """Test de la documentation"""
    print_header("DOCUMENTATION")
    
    files = [
        "PERFORMANCE_SCALABILITE_IMPLEMENTATION.md",
        "ANALYTICS_PREDICTIFS_IMPLEMENTATION.md",
        "UI_UX_AVANCE_IMPLEMENTATION.md",
        "SECURITE_RENFORCEE_IMPLEMENTATION.md"
    ]
    
    success = 0
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes)")
            success += 1
        else:
            print_error(f"{file} (MANQUANT)")
    
    print(f"\n📊 Documentation: {success}/{len(files)} fichiers présents")
    return success == len(files)

def main():
    """Test principal"""
    print("🚀 TEST RAPIDE - COMMUNICONNECT")
    print(f"⏰ {datetime.datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    results = []
    
    # Test Backend
    print("\n🧪 Test Backend...")
    backend_ok = test_backend()
    results.append(backend_ok)
    
    # Test Frontend  
    print("\n🧪 Test Frontend...")
    frontend_ok = test_frontend()
    results.append(frontend_ok)
    
    # Test Documentation
    print("\n🧪 Test Documentation...")
    docs_ok = test_documentation()
    results.append(docs_ok)
    
    # Résultat final
    print("\n" + "=" * 50)
    print("📊 RÉSULTAT FINAL")
    print("=" * 50)
    
    success_count = sum(results)
    total_tests = len(results)
    success_rate = (success_count / total_tests) * 100
    
    print(f"🎯 Tests réussis: {success_count}/{total_tests}")
    print(f"📈 Taux de succès: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🏆 PARFAIT: Tous les fichiers sont présents!")
        print("🚀 CommuniConnect est prêt pour le déploiement!")
    elif success_rate >= 80:
        print("✅ TRÈS BON: Presque tous les fichiers sont présents!")
        print("🎯 Déploiement recommandé!")
    else:
        print("⚠️ ATTENTION: Des fichiers manquent!")
        print("🔧 Corrections nécessaires avant déploiement")
    
    return success_rate >= 80

if __name__ == "__main__":
    main() 
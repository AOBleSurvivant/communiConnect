// Script de test pour les données géographiques dans le frontend
// À exécuter dans la console du navigateur

console.log("🗺️ TEST DES DONNÉES GÉOGRAPHIQUES FRONTEND");
console.log("=" * 50);

// Test de l'API géographique
async function testGeographicAPI() {
    try {
        console.log("🌐 Test de l'API géographique...");
        
        const response = await fetch('http://localhost:8000/api/users/geographic-data/');
        console.log(`Status: ${response.status}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log("✅ Données géographiques récupérées");
            
            const regions = data.regions || [];
            console.log(`📊 Régions disponibles: ${regions.length}`);
            
            if (regions.length > 0) {
                const region = regions[0];
                console.log(`🏛️ Première région: ${region.nom} (${region.code})`);
                
                const prefectures = region.prefectures || [];
                if (prefectures.length > 0) {
                    const prefecture = prefectures[0];
                    console.log(`   - Préfecture: ${prefecture.nom}`);
                    
                    const communes = prefecture.communes || [];
                    if (communes.length > 0) {
                        const commune = communes[0];
                        console.log(`     - Commune: ${commune.nom}`);
                        
                        const quartiers = commune.quartiers || [];
                        if (quartiers.length > 0) {
                            const quartier = quartiers[0];
                            console.log(`       - Quartier: ${quartier.nom} (ID: ${quartier.id})`);
                            console.log("✅ Structure géographique valide");
                        } else {
                            console.log("❌ Aucun quartier trouvé");
                        }
                    } else {
                        console.log("❌ Aucune commune trouvée");
                    }
                } else {
                    console.log("❌ Aucune préfecture trouvée");
                }
            } else {
                console.log("❌ Aucune région trouvée");
            }
        } else {
            console.log(`❌ Erreur API: ${response.status}`);
        }
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
    }
}

// Test du composant GeographicSelector
function testGeographicSelector() {
    console.log("\n🧪 Test du composant GeographicSelector...");
    
    // Vérifier si le composant existe
    if (typeof window.GeographicSelector !== 'undefined') {
        console.log("✅ Composant GeographicSelector disponible");
    } else {
        console.log("⚠️ Composant GeographicSelector non trouvé (normal si pas sur la page d'inscription)");
    }
    
    // Vérifier les données dans localStorage
    const geographicData = localStorage.getItem('geographicData');
    if (geographicData) {
        console.log("✅ Données géographiques en cache");
        try {
            const data = JSON.parse(geographicData);
            console.log(`   - Régions en cache: ${data.regions?.length || 0}`);
        } catch (e) {
            console.log("❌ Erreur parsing données en cache");
        }
    } else {
        console.log("ℹ️ Aucune donnée géographique en cache");
    }
}

// Test de la page d'inscription
function testRegistrationPage() {
    console.log("\n📝 Test de la page d'inscription...");
    
    // Vérifier si on est sur la page d'inscription
    if (window.location.pathname === '/register') {
        console.log("✅ Sur la page d'inscription");
        
        // Vérifier les éléments du formulaire
        const geographicElements = document.querySelectorAll('[data-geographic]');
        console.log(`   - Éléments géographiques trouvés: ${geographicElements.length}`);
        
        // Vérifier les sélecteurs
        const regionSelect = document.querySelector('select[name="region"]');
        const prefectureSelect = document.querySelector('select[name="prefecture"]');
        const communeSelect = document.querySelector('select[name="commune"]');
        const quartierSelect = document.querySelector('select[name="quartier"]');
        
        console.log(`   - Sélecteur région: ${regionSelect ? '✅' : '❌'}`);
        console.log(`   - Sélecteur préfecture: ${prefectureSelect ? '✅' : '❌'}`);
        console.log(`   - Sélecteur commune: ${communeSelect ? '✅' : '❌'}`);
        console.log(`   - Sélecteur quartier: ${quartierSelect ? '✅' : '❌'}`);
    } else {
        console.log("ℹ️ Pas sur la page d'inscription");
        console.log("💡 Allez sur http://localhost:3000/register pour tester");
    }
}

// Exécuter les tests
async function runAllTests() {
    await testGeographicAPI();
    testGeographicSelector();
    testRegistrationPage();
    
    console.log("\n🎯 RÉSUMÉ:");
    console.log("   - API géographique: Testée");
    console.log("   - Composant frontend: Vérifié");
    console.log("   - Page d'inscription: Vérifiée");
    console.log("\n💡 Pour tester complètement:");
    console.log("   1. Allez sur http://localhost:3000/register");
    console.log("   2. Vérifiez que les sélecteurs géographiques fonctionnent");
    console.log("   3. Testez l'inscription avec un quartier sélectionné");
}

// Lancer les tests
runAllTests(); 
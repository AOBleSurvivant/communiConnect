// Script de diagnostic automatique pour les alertes
// À exécuter dans la console du navigateur sur http://localhost:3000

console.log('🔍 Diagnostic Automatique Alertes - CommuniConnect');

// Fonction de diagnostic principal
async function runDiagnostic() {
    console.log('🚀 Démarrage du diagnostic automatique...');
    
    const results = {
        api_accessible: false,
        user_authenticated: false,
        alert_creation_works: false,
        react_components_loaded: false,
        errors: []
    };
    
    // 1. Test de connexion à l'API
    console.log('\n1️⃣ Test de connexion à l\'API...');
    try {
        const response = await fetch('http://localhost:8000/api/health/');
        if (response.ok) {
            console.log('✅ API accessible');
            results.api_accessible = true;
        } else {
            console.log('❌ API non accessible');
            results.errors.push('API non accessible');
        }
    } catch (error) {
        console.log('❌ Erreur connexion API:', error.message);
        results.errors.push('Erreur connexion API');
    }
    
    // 2. Test d'authentification
    console.log('\n2️⃣ Test d\'authentification...');
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        try {
            const userData = JSON.parse(user);
            console.log('✅ Utilisateur connecté:', userData.username);
            results.user_authenticated = true;
        } catch (e) {
            console.log('❌ Données utilisateur corrompues');
            results.errors.push('Données utilisateur corrompues');
        }
    } else {
        console.log('❌ Aucun utilisateur connecté');
        results.errors.push('Aucun utilisateur connecté');
    }
    
    // 3. Test de création d'alerte
    if (results.user_authenticated) {
        console.log('\n3️⃣ Test de création d\'alerte...');
        try {
            const alertData = {
                title: 'Test diagnostic - Alerte automatique',
                description: 'Alerte créée automatiquement par le diagnostic',
                category: 'other',
                latitude: 48.8566,
                longitude: 2.3522,
                address: 'Test Address',
                neighborhood: 'Test Neighborhood',
                city: 'Test City',
                postal_code: '00000'
            };
            
            const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(alertData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ Création d\'alerte réussie');
                results.alert_creation_works = true;
                
                // Nettoyer l'alerte de test
                await fetch(`http://localhost:8000/api/notifications/alerts/${data.alert_id}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                console.log('🧹 Alerte de test nettoyée');
                
            } else {
                console.log('❌ Erreur création alerte:', data);
                results.errors.push(`Erreur création alerte: ${JSON.stringify(data)}`);
            }
        } catch (error) {
            console.log('❌ Erreur test création alerte:', error);
            results.errors.push('Erreur test création alerte');
        }
    }
    
    // 4. Test des composants React
    console.log('\n4️⃣ Test des composants React...');
    if (window.React && window.ReactDOM) {
        console.log('✅ React disponible');
        results.react_components_loaded = true;
    } else {
        console.log('❌ React non disponible');
        results.errors.push('React non disponible');
    }
    
    // 5. Test des services
    console.log('\n5️⃣ Test des services...');
    const services = ['alertService', 'authAPI', 'api'];
    services.forEach(service => {
        if (window[service]) {
            console.log(`✅ ${service} disponible`);
        } else {
            console.log(`❌ ${service} non disponible`);
            results.errors.push(`${service} non disponible`);
        }
    });
    
    // 6. Affichage du rapport
    console.log('\n📊 RAPPORT DE DIAGNOSTIC');
    console.log('========================');
    console.log(`API accessible: ${results.api_accessible ? '✅' : '❌'}`);
    console.log(`Utilisateur authentifié: ${results.user_authenticated ? '✅' : '❌'}`);
    console.log(`Création d'alerte fonctionne: ${results.alert_creation_works ? '✅' : '❌'}`);
    console.log(`Composants React chargés: ${results.react_components_loaded ? '✅' : '❌'}`);
    
    if (results.errors.length > 0) {
        console.log('\n❌ ERREURS DÉTECTÉES:');
        results.errors.forEach((error, index) => {
            console.log(`${index + 1}. ${error}`);
        });
    } else {
        console.log('\n✅ Aucune erreur détectée');
    }
    
    // 7. Recommandations
    console.log('\n💡 RECOMMANDATIONS:');
    if (!results.user_authenticated) {
        console.log('1. Exécutez forceLogin() pour vous connecter');
    }
    if (!results.alert_creation_works && results.user_authenticated) {
        console.log('2. Vérifiez les permissions utilisateur');
    }
    if (results.errors.length === 0) {
        console.log('✅ Système opérationnel - Le problème est dans l\'interface utilisateur');
    }
    
    return results;
}

// Fonction pour corriger automatiquement les problèmes
async function autoFix() {
    console.log('🔧 Tentative de correction automatique...');
    
    const diagnostic = await runDiagnostic();
    
    if (!diagnostic.user_authenticated) {
        console.log('🔧 Correction: Connexion automatique...');
        await forceLogin();
    }
    
    if (!diagnostic.alert_creation_works && diagnostic.user_authenticated) {
        console.log('🔧 Correction: Test de création d\'alerte...');
        await testAlertCreation();
    }
}

// Fonction pour forcer la connexion
async function forceLogin() {
    console.log('🔐 Connexion automatique...');
    
    const timestamp = Date.now();
    const userData = {
        username: `testuser_${timestamp}`,
        email: `test${timestamp}@communiconnect.com`,
        password: 'TestPass123!',
        password_confirm: 'TestPass123!',
        first_name: 'Test',
        last_name: 'User'
    };

    try {
        const response = await fetch('http://localhost:8000/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', data.tokens.access);
            localStorage.setItem('refresh_token', data.tokens.refresh);
            localStorage.setItem('user', JSON.stringify(data.user));
            console.log('✅ Connexion automatique réussie');
            return true;
        } else {
            console.log('❌ Erreur connexion automatique:', data);
            return false;
        }
    } catch (error) {
        console.log('❌ Erreur connexion automatique:', error);
        return false;
    }
}

// Fonction pour tester la création d'alerte
async function testAlertCreation() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        console.log('❌ Aucun token disponible');
        return false;
    }
    
    try {
        const alertData = {
            title: 'Test auto-fix - Alerte',
            description: 'Test automatique',
            category: 'other',
            latitude: 48.8566,
            longitude: 2.3522,
            address: 'Test',
            neighborhood: 'Test',
            city: 'Test',
            postal_code: '00000'
        };
        
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(alertData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('✅ Test création alerte réussi');
            
            // Nettoyer
            await fetch(`http://localhost:8000/api/notifications/alerts/${data.alert_id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            return true;
        } else {
            console.log('❌ Test création alerte échoué:', data);
            return false;
        }
    } catch (error) {
        console.log('❌ Erreur test création alerte:', error);
        return false;
    }
}

// Fonction pour tester l'interface utilisateur
function testUI() {
    console.log('🎨 Test de l\'interface utilisateur...');
    
    // Vérifier si les composants sont présents
    const alertButton = document.querySelector('[data-testid="create-alert-button"]') || 
                       document.querySelector('button[onclick*="alert"]') ||
                       document.querySelector('button:contains("Créer")');
    
    if (alertButton) {
        console.log('✅ Bouton création alerte trouvé');
        console.log('🧪 Test du clic sur le bouton...');
        alertButton.click();
    } else {
        console.log('❌ Bouton création alerte non trouvé');
    }
    
    // Vérifier les modales
    const modals = document.querySelectorAll('.modal, [role="dialog"]');
    console.log(`📋 ${modals.length} modales trouvées`);
    
    // Vérifier les formulaires
    const forms = document.querySelectorAll('form');
    console.log(`📝 ${forms.length} formulaires trouvés`);
}

// Fonction principale
function runCompleteDiagnostic() {
    console.log('🚀 Diagnostic complet des alertes...');
    
    // Diagnostic automatique
    runDiagnostic().then(results => {
        console.log('\n🎯 RÉSUMÉ:');
        if (results.errors.length === 0) {
            console.log('✅ Système opérationnel');
            console.log('Le problème est probablement dans l\'interface utilisateur');
            testUI();
        } else {
            console.log('❌ Problèmes détectés');
            console.log('Tentative de correction automatique...');
            autoFix();
        }
    });
}

// Commandes disponibles
console.log('\n📋 Commandes disponibles:');
console.log('- runCompleteDiagnostic() : Diagnostic complet');
console.log('- runDiagnostic() : Diagnostic de base');
console.log('- autoFix() : Correction automatique');
console.log('- testUI() : Test interface utilisateur');
console.log('- forceLogin() : Connexion forcée');
console.log('- testAlertCreation() : Test création alerte');

// Exécuter automatiquement
runCompleteDiagnostic(); 
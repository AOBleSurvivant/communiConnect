// Script de test pour vérifier la correction GeographicSelector
// À exécuter dans la console du navigateur sur http://localhost:3000

console.log('🧪 Test Correction GeographicSelector - CommuniConnect');

// Fonction pour vérifier les composants React
function checkReactComponents() {
    console.log('🔍 Vérification des composants React...');
    
    // Vérifier si React est disponible
    if (window.React) {
        console.log('✅ React disponible');
    } else {
        console.log('❌ React non disponible');
        return;
    }
    
    // Vérifier les composants spécifiques
    const components = [
        'GeographicSelector',
        'CommunityAlerts',
        'CreateAlertModal'
    ];
    
    components.forEach(component => {
        if (window[component]) {
            console.log(`✅ ${component} disponible`);
        } else {
            console.log(`⚠️ ${component} non disponible (normal si pas sur la bonne page)`);
        }
    });
}

// Fonction pour tester la navigation
function testNavigation() {
    console.log('🧪 Test de navigation...');
    
    // Vérifier l'URL actuelle
    console.log('📍 URL actuelle:', window.location.href);
    
    // Suggestions de navigation
    const pages = [
        { name: 'Inscription', url: '/register' },
        { name: 'Alertes', url: '/alerts' },
        { name: 'Dashboard', url: '/dashboard' }
    ];
    
    console.log('📋 Pages disponibles:');
    pages.forEach(page => {
        console.log(`- ${page.name}: ${page.url}`);
    });
}

// Fonction pour vérifier les erreurs JavaScript
function checkJavaScriptErrors() {
    console.log('🔍 Vérification des erreurs JavaScript...');
    
    // Écouter les erreurs futures
    window.addEventListener('error', (event) => {
        console.error('❌ Erreur JavaScript détectée:', event.error);
    });
    
    // Écouter les erreurs de promesses non gérées
    window.addEventListener('unhandledrejection', (event) => {
        console.error('❌ Promesse rejetée non gérée:', event.reason);
    });
    
    console.log('✅ Écouteurs d\'erreurs configurés');
}

// Fonction pour tester la géolocalisation
function testGeolocation() {
    console.log('🧪 Test de géolocalisation...');
    
    if (navigator.geolocation) {
        console.log('✅ Géolocalisation disponible');
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                console.log('✅ Position obtenue:', {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            (error) => {
                console.log('❌ Erreur géolocalisation:', error.message);
            }
        );
    } else {
        console.log('❌ Géolocalisation non disponible');
    }
}

// Fonction pour tester l'API Nominatim
async function testNominatimAPI() {
    console.log('🧪 Test API Nominatim...');
    
    try {
        const response = await fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=9.5370&lon=-13.6785&addressdetails=1');
        const data = await response.json();
        
        if (data.address) {
            console.log('✅ API Nominatim fonctionne');
            console.log('📍 Adresse testée:', data.display_name);
        } else {
            console.log('❌ Erreur API Nominatim');
        }
    } catch (error) {
        console.log('❌ Erreur connexion API Nominatim:', error.message);
    }
}

// Fonction pour vérifier les props du composant
function checkComponentProps() {
    console.log('🔍 Vérification des props des composants...');
    
    // Simuler les props attendues
    const expectedProps = {
        GeographicSelector: ['onLocationSelect', 'userLocation'],
        CommunityAlerts: ['userLocation', 'alertCategories'],
        CreateAlertModal: ['onClose', 'onSubmit', 'userLocation', 'alertCategories']
    };
    
    Object.entries(expectedProps).forEach(([component, props]) => {
        console.log(`📋 ${component} - Props attendues:`, props);
    });
}

// Fonction pour tester la création d'alerte
function testAlertCreation() {
    console.log('🧪 Test de création d\'alerte...');
    
    // Vérifier l'authentification
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.log('❌ Aucun token d\'authentification');
        console.log('Exécutez forceLogin() d\'abord');
        return;
    }
    
    console.log('✅ Utilisateur authentifié');
    
    // Simuler les données d'alerte
    const alertData = {
        title: 'Test correction - Alerte',
        description: 'Test de création d\'alerte après correction',
        category: 'other',
        latitude: 9.5370,
        longitude: -13.6785,
        address: 'Conakry, Guinée',
        neighborhood: 'Centre-ville',
        city: 'Conakry',
        postal_code: '00000'
    };
    
    console.log('📝 Données d\'alerte simulées:', alertData);
    console.log('✅ Test de création d\'alerte prêt');
}

// Fonction principale
function runGeographicTest() {
    console.log('🚀 Test de correction GeographicSelector...');
    
    checkReactComponents();
    testNavigation();
    checkJavaScriptErrors();
    testGeolocation();
    testNominatimAPI();
    checkComponentProps();
    testAlertCreation();
    
    console.log('\n📋 Commandes disponibles:');
    console.log('- checkReactComponents() : Vérifier les composants');
    console.log('- testNavigation() : Tester la navigation');
    console.log('- testGeolocation() : Tester la géolocalisation');
    console.log('- testNominatimAPI() : Tester l\'API Nominatim');
    console.log('- testAlertCreation() : Tester la création d\'alerte');
}

// Exécuter automatiquement
runGeographicTest(); 
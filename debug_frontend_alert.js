// Debug script pour tester la création d'alertes depuis le frontend
// À exécuter dans la console du navigateur sur http://localhost:3000

console.log('🔍 Debug Frontend Alertes - CommuniConnect');

// Fonction pour récupérer le token depuis localStorage
function getAuthToken() {
    const token = localStorage.getItem('accessToken') || localStorage.getItem('token');
    console.log('Token trouvé:', token ? token.substring(0, 20) + '...' : 'Aucun token');
    return token;
}

// Fonction pour tester l'API d'alertes
async function testAlertAPI() {
    console.log('🧪 Test de l\'API d\'alertes...');
    
    const token = getAuthToken();
    if (!token) {
        console.error('❌ Aucun token d\'authentification trouvé');
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('Status:', response.status);
        const data = await response.json();
        console.log('Réponse:', data);
        
        if (response.ok) {
            console.log('✅ API d\'alertes accessible');
        } else {
            console.error('❌ Erreur API d\'alertes:', data);
        }
    } catch (error) {
        console.error('❌ Erreur connexion:', error);
    }
}

// Fonction pour créer une alerte de test
async function createTestAlert() {
    console.log('🧪 Création d\'une alerte de test...');
    
    const token = getAuthToken();
    if (!token) {
        console.error('❌ Aucun token d\'authentification trouvé');
        return;
    }

    const alertData = {
        title: 'Test d\'alerte - Fuite de gaz',
        description: 'Fuite de gaz détectée dans le quartier. Odeur forte dans la rue principale.',
        category: 'gas_leak',
        latitude: 48.8566,
        longitude: 2.3522,
        address: '123 Rue de la Paix',
        neighborhood: 'Centre-ville',
        city: 'Paris',
        postal_code: '75001'
    };

    try {
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(alertData)
        });

        console.log('Status:', response.status);
        const data = await response.json();
        console.log('Réponse:', data);
        
        if (response.ok) {
            console.log('✅ Alerte créée avec succès!');
        } else {
            console.error('❌ Erreur création alerte:', data);
        }
    } catch (error) {
        console.error('❌ Erreur création alerte:', error);
    }
}

// Fonction pour vérifier l'état de l'authentification
function checkAuthState() {
    console.log('🔍 Vérification de l\'état d\'authentification...');
    
    const token = getAuthToken();
    const user = localStorage.getItem('user');
    
    console.log('Token présent:', !!token);
    console.log('User présent:', !!user);
    
    if (user) {
        try {
            const userData = JSON.parse(user);
            console.log('Données utilisateur:', userData);
        } catch (e) {
            console.log('User data (raw):', user);
        }
    }
}

// Fonction pour simuler la création d'alerte depuis le composant React
function simulateReactAlertCreation() {
    console.log('🧪 Simulation de création d\'alerte depuis React...');
    
    // Simuler les données du formulaire
    const formData = {
        title: 'Test d\'alerte - Fuite de gaz',
        description: 'Fuite de gaz détectée dans le quartier. Odeur forte dans la rue principale.',
        category: 'gas_leak',
        latitude: 48.8566,
        longitude: 2.3522,
        address: '123 Rue de la Paix',
        neighborhood: 'Centre-ville',
        city: 'Paris',
        postal_code: '75001'
    };
    
    console.log('Données du formulaire:', formData);
    
    // Simuler l'appel à l'API
    createTestAlert();
}

// Fonction pour vérifier les services
function checkServices() {
    console.log('🔍 Vérification des services...');
    
    // Vérifier si les services sont disponibles
    if (window.alertService) {
        console.log('✅ alertService disponible');
    } else {
        console.log('❌ alertService non disponible');
    }
    
    if (window.authAPI) {
        console.log('✅ authAPI disponible');
    } else {
        console.log('❌ authAPI non disponible');
    }
}

// Fonction principale de debug
function runDebug() {
    console.log('🚀 Démarrage du debug...');
    
    checkAuthState();
    checkServices();
    testAlertAPI();
    
    console.log('\n📋 Commandes disponibles:');
    console.log('- checkAuthState() : Vérifier l\'état d\'authentification');
    console.log('- testAlertAPI() : Tester l\'API d\'alertes');
    console.log('- createTestAlert() : Créer une alerte de test');
    console.log('- simulateReactAlertCreation() : Simuler la création depuis React');
    console.log('- checkServices() : Vérifier les services disponibles');
}

// Exécuter le debug automatiquement
runDebug(); 
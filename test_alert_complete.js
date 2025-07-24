// Script de test complet pour les alertes
// À exécuter dans la console du navigateur sur http://localhost:3000

console.log('🧪 Test Complet Alertes - CommuniConnect');

// Fonction pour tester la création d'alerte depuis le composant React
async function testReactAlertCreation() {
    console.log('🧪 Test de création d\'alerte depuis React...');
    
    // Vérifier l'authentification
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        console.error('❌ Utilisateur non connecté');
        console.log('Exécutez forceLogin() d\'abord');
        return;
    }
    
    console.log('✅ Utilisateur connecté');
    
    // Simuler les données du formulaire React
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
    
    console.log('📝 Données du formulaire:', formData);
    
    try {
        // Appel à l'API d'alertes
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });
        
        console.log('📡 Status de la réponse:', response.status);
        const data = await response.json();
        console.log('📄 Réponse complète:', data);
        
        if (response.ok) {
            console.log('✅ Alerte créée avec succès!');
            console.log('🆔 ID de l\'alerte:', data.alert_id);
            console.log('📅 Date de création:', data.created_at);
            
            // Tester la récupération de l'alerte
            await testGetAlert(data.alert_id);
            
        } else {
            console.error('❌ Erreur création alerte');
            console.error('Détails:', data);
            
            // Afficher les erreurs spécifiques
            if (data.detail) {
                console.error('Erreur détaillée:', data.detail);
            }
            if (data.errors) {
                console.error('Erreurs de validation:', data.errors);
            }
        }
        
    } catch (error) {
        console.error('❌ Erreur réseau:', error);
    }
}

// Fonction pour récupérer une alerte spécifique
async function testGetAlert(alertId) {
    console.log(`🧪 Test de récupération de l'alerte ${alertId}...`);
    
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`http://localhost:8000/api/notifications/alerts/${alertId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('📡 Status récupération:', response.status);
        const data = await response.json();
        
        if (response.ok) {
            console.log('✅ Alerte récupérée avec succès');
            console.log('📄 Détails de l\'alerte:', data);
        } else {
            console.error('❌ Erreur récupération alerte:', data);
        }
        
    } catch (error) {
        console.error('❌ Erreur récupération alerte:', error);
    }
}

// Fonction pour tester la récupération de toutes les alertes
async function testGetAllAlerts() {
    console.log('🧪 Test de récupération de toutes les alertes...');
    
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('📡 Status récupération:', response.status);
        const data = await response.json();
        
        if (response.ok) {
            const alerts = data.results || data;
            console.log(`✅ ${alerts.length} alertes récupérées`);
            
            alerts.forEach((alert, index) => {
                console.log(`📋 Alerte ${index + 1}:`, {
                    id: alert.alert_id,
                    title: alert.title,
                    category: alert.category,
                    created_at: alert.created_at
                });
            });
        } else {
            console.error('❌ Erreur récupération alertes:', data);
        }
        
    } catch (error) {
        console.error('❌ Erreur récupération alertes:', error);
    }
}

// Fonction pour tester les catégories d'alertes
async function testAlertCategories() {
    console.log('🧪 Test des catégories d\'alertes...');
    
    const categories = [
        'gas_leak',
        'fire',
        'flood',
        'power_outage',
        'road_accident',
        'medical_emergency',
        'security_incident',
        'weather_warning',
        'other'
    ];
    
    console.log('📋 Catégories disponibles:', categories);
    
    // Tester la création d'une alerte de chaque catégorie
    for (const category of categories.slice(0, 3)) { // Tester seulement les 3 premières
        console.log(`🧪 Test création alerte catégorie: ${category}`);
        
        const alertData = {
            title: `Test ${category} - Alerte de test`,
            description: `Description de test pour la catégorie ${category}`,
            category: category,
            latitude: 48.8566,
            longitude: 2.3522,
            address: '123 Rue de la Paix',
            neighborhood: 'Centre-ville',
            city: 'Paris',
            postal_code: '75001'
        };
        
        await createTestAlert(alertData);
        
        // Attendre un peu entre chaque création
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

// Fonction pour créer une alerte de test
async function createTestAlert(alertData) {
    const token = localStorage.getItem('access_token');
    
    try {
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
            console.log(`✅ Alerte ${alertData.category} créée:`, data.alert_id);
        } else {
            console.error(`❌ Erreur création alerte ${alertData.category}:`, data);
        }
        
    } catch (error) {
        console.error(`❌ Erreur création alerte ${alertData.category}:`, error);
    }
}

// Fonction pour nettoyer les alertes de test
async function cleanupTestAlerts() {
    console.log('🧹 Nettoyage des alertes de test...');
    
    const token = localStorage.getItem('access_token');
    
    try {
        // Récupérer toutes les alertes
        const response = await fetch('http://localhost:8000/api/notifications/alerts/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const alerts = data.results || data;
            console.log(`📋 ${alerts.length} alertes trouvées`);
            
            // Supprimer les alertes de test (avec "Test" dans le titre)
            for (const alert of alerts) {
                if (alert.title && alert.title.includes('Test')) {
                    console.log(`🗑️ Suppression de l'alerte: ${alert.title}`);
                    
                    const deleteResponse = await fetch(`http://localhost:8000/api/notifications/alerts/${alert.alert_id}/`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    if (deleteResponse.ok) {
                        console.log(`✅ Alerte supprimée: ${alert.alert_id}`);
                    } else {
                        console.error(`❌ Erreur suppression alerte: ${alert.alert_id}`);
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('❌ Erreur nettoyage:', error);
    }
}

// Fonction principale
function runCompleteTest() {
    console.log('🚀 Démarrage du test complet...');
    
    // Vérifier l'authentification
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        console.log('❌ Utilisateur non connecté');
        console.log('Exécutez forceLogin() d\'abord');
        return;
    }
    
    console.log('✅ Utilisateur connecté, début des tests...');
    
    // Exécuter les tests
    testReactAlertCreation();
    
    console.log('\n📋 Commandes disponibles:');
    console.log('- testReactAlertCreation() : Test création alerte React');
    console.log('- testGetAllAlerts() : Récupérer toutes les alertes');
    console.log('- testAlertCategories() : Tester toutes les catégories');
    console.log('- cleanupTestAlerts() : Nettoyer les alertes de test');
}

// Exécuter automatiquement
runCompleteTest(); 
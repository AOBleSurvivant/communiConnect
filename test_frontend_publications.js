// Test des appels API côté frontend
const API_BASE_URL = 'http://localhost:8000/api';

// Fonction pour obtenir le token depuis localStorage
function getToken() {
    return localStorage.getItem('access_token');
}

// Fonction pour faire un appel API
async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    
    const config = {
        method: options.method || 'GET',
        headers,
        ...options
    };
    
    if (options.body) {
        config.body = JSON.stringify(options.body);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();
        
        return {
            status: response.status,
            data: data,
            ok: response.ok
        };
    } catch (error) {
        console.error('Erreur API:', error);
        return {
            status: 0,
            data: null,
            ok: false,
            error: error.message
        };
    }
}

// Test de récupération des publications
async function testPosts() {
    console.log('🔍 Test récupération publications...');
    
    const result = await apiCall('/posts/');
    console.log('📊 Résultat publications:', result);
    
    if (result.ok) {
        console.log('✅ Publications récupérées avec succès');
        console.log('📊 Structure:', typeof result.data);
        console.log('📊 Clés:', Object.keys(result.data));
        
        if (result.data.results) {
            console.log('📊 Nombre de publications:', result.data.results.length);
            if (result.data.results.length > 0) {
                console.log('📊 Premier post:', result.data.results[0]);
            }
        }
    } else {
        console.log('❌ Erreur récupération publications:', result.status);
    }
}

// Test de récupération des notifications
async function testNotifications() {
    console.log('🔔 Test récupération notifications...');
    
    const result = await apiCall('/notifications/');
    console.log('📊 Résultat notifications:', result);
    
    if (result.ok) {
        console.log('✅ Notifications récupérées avec succès');
        console.log('📊 Structure:', typeof result.data);
        console.log('📊 Clés:', Object.keys(result.data));
        
        if (result.data.results) {
            console.log('📊 Nombre de notifications:', result.data.results.length);
        }
    } else {
        console.log('❌ Erreur récupération notifications:', result.status);
    }
}

// Test du compteur de notifications
async function testNotificationsCount() {
    console.log('📊 Test compteur notifications...');
    
    const result = await apiCall('/notifications/count/');
    console.log('📊 Résultat compteur:', result);
    
    if (result.ok) {
        console.log('✅ Compteur récupéré avec succès');
        console.log('📊 Données:', result.data);
    } else {
        console.log('❌ Erreur compteur:', result.status);
    }
}

// Test avec filtres
async function testPostsWithFilters() {
    console.log('🔍 Test publications avec filtres...');
    
    const filters = [
        { type: 'info' },
        { type: 'event' },
        { type: 'help' },
        { type: 'announcement' },
        { search: 'test' }
    ];
    
    for (const filter of filters) {
        console.log(`📝 Test filtre:`, filter);
        const params = new URLSearchParams(filter);
        const result = await apiCall(`/posts/?${params}`);
        
        if (result.ok) {
            console.log(`✅ Filtre ${JSON.stringify(filter)}: OK`);
            if (result.data.results) {
                console.log(`📊 Publications trouvées: ${result.data.results.length}`);
            }
        } else {
            console.log(`❌ Filtre ${JSON.stringify(filter)}: Erreur ${result.status}`);
        }
    }
}

// Fonction principale
async function runTests() {
    console.log('🧪 TESTS FRONTEND PUBLICATIONS ET NOTIFICATIONS');
    console.log('=' .repeat(60));
    
    // Vérifier si l'utilisateur est connecté
    const token = getToken();
    if (!token) {
        console.log('❌ Aucun token trouvé - utilisateur non connecté');
        return;
    }
    
    console.log('✅ Token trouvé, utilisateur connecté');
    
    // Exécuter les tests
    await testPosts();
    await testPostsWithFilters();
    await testNotifications();
    await testNotificationsCount();
    
    console.log('📊 TESTS TERMINÉS');
    console.log('=' .repeat(60));
}

// Exécuter les tests si le script est chargé dans le navigateur
if (typeof window !== 'undefined') {
    // Attendre que la page soit chargée
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runTests);
    } else {
        runTests();
    }
}

// Exporter pour utilisation dans la console
window.testPublications = runTests; 
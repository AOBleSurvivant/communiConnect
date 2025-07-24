// Script pour forcer la connexion d'un utilisateur dans le frontend
// À exécuter dans la console du navigateur sur http://localhost:3000

console.log('🔐 Force Login - CommuniConnect');

// Fonction pour créer un utilisateur de test et le connecter
async function forceLogin() {
    console.log('🧪 Création et connexion d\'un utilisateur de test...');
    
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
        // 1. Créer l'utilisateur
        console.log('1. Création de l\'utilisateur...');
        const registerResponse = await fetch('http://localhost:8000/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const registerData = await registerResponse.json();
        
        if (registerResponse.ok) {
            console.log('✅ Utilisateur créé avec succès');
            
            // 2. Sauvegarder les données dans localStorage
            const { tokens, user } = registerData;
            
            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);
            localStorage.setItem('user', JSON.stringify(user));
            
            console.log('✅ Données sauvegardées dans localStorage');
            console.log('Token:', tokens.access.substring(0, 20) + '...');
            console.log('User:', user.username);
            
            // 3. Recharger la page pour appliquer l'authentification
            console.log('🔄 Rechargement de la page...');
            window.location.reload();
            
        } else {
            console.error('❌ Erreur création utilisateur:', registerData);
            
            // Si l'utilisateur existe déjà, essayer de se connecter
            console.log('🔄 Tentative de connexion avec l\'utilisateur existant...');
            await forceLoginExisting(userData.email, userData.password);
        }
        
    } catch (error) {
        console.error('❌ Erreur force login:', error);
    }
}

// Fonction pour se connecter avec un utilisateur existant
async function forceLoginExisting(email, password) {
    try {
        const loginResponse = await fetch('http://localhost:8000/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const loginData = await loginResponse.json();
        
        if (loginResponse.ok) {
            console.log('✅ Connexion réussie');
            
            // Sauvegarder les données
            const { tokens, user } = loginData;
            
            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);
            localStorage.setItem('user', JSON.stringify(user));
            
            console.log('✅ Données sauvegardées dans localStorage');
            console.log('Token:', tokens.access.substring(0, 20) + '...');
            console.log('User:', user.username);
            
            // Recharger la page
            console.log('🔄 Rechargement de la page...');
            window.location.reload();
            
        } else {
            console.error('❌ Erreur connexion:', loginData);
        }
        
    } catch (error) {
        console.error('❌ Erreur connexion:', error);
    }
}

// Fonction pour vérifier l'état de l'authentification
function checkAuthState() {
    console.log('🔍 Vérification de l\'état d\'authentification...');
    
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    console.log('Token présent:', !!token);
    console.log('User présent:', !!user);
    
    if (token && user) {
        try {
            const userData = JSON.parse(user);
            console.log('✅ Utilisateur connecté:', userData.username);
            console.log('Token:', token.substring(0, 20) + '...');
            return true;
        } catch (e) {
            console.log('❌ Données utilisateur corrompues');
            return false;
        }
    } else {
        console.log('❌ Aucun utilisateur connecté');
        return false;
    }
}

// Fonction pour tester la création d'alerte après connexion
async function testAlertAfterLogin() {
    if (!checkAuthState()) {
        console.log('❌ Veuillez d\'abord vous connecter avec forceLogin()');
        return;
    }
    
    console.log('🧪 Test de création d\'alerte après connexion...');
    
    const token = localStorage.getItem('access_token');
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
            console.log('ID de l\'alerte:', data.alert_id);
        } else {
            console.error('❌ Erreur création alerte:', data);
        }
    } catch (error) {
        console.error('❌ Erreur création alerte:', error);
    }
}

// Fonction pour nettoyer l'authentification
function clearAuth() {
    console.log('🧹 Nettoyage de l\'authentification...');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    console.log('✅ Authentification nettoyée');
}

// Fonction principale
function runForceLogin() {
    console.log('🚀 Démarrage du force login...');
    
    if (checkAuthState()) {
        console.log('✅ Utilisateur déjà connecté');
        console.log('Vous pouvez maintenant tester la création d\'alertes');
    } else {
        console.log('❌ Aucun utilisateur connecté');
        console.log('Exécution du force login...');
        forceLogin();
    }
    
    console.log('\n📋 Commandes disponibles:');
    console.log('- forceLogin() : Créer et connecter un utilisateur de test');
    console.log('- checkAuthState() : Vérifier l\'état d\'authentification');
    console.log('- testAlertAfterLogin() : Tester la création d\'alerte');
    console.log('- clearAuth() : Nettoyer l\'authentification');
}

// Exécuter automatiquement
runForceLogin(); 
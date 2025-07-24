// Test final du frontend après correction des URLs
console.log('🧪 Test final du frontend...');

async function testFrontendAPIs() {
    const baseURL = 'http://127.0.0.1:8000/api';
    
    console.log('1️⃣ Test de santé du serveur...');
    try {
        const healthResponse = await fetch(`${baseURL}/health/`);
        if (healthResponse.ok) {
            const healthData = await healthResponse.json();
            console.log('✅ Health check:', healthData);
        } else {
            console.log('❌ Health check échoué:', healthResponse.status);
        }
    } catch (error) {
        console.log('❌ Erreur health check:', error);
    }

    console.log('\n2️⃣ Test des quartiers (sans auth)...');
    try {
        const quartiersResponse = await fetch(`${baseURL}/geography/quartiers/`);
        if (quartiersResponse.ok) {
            const quartiersData = await quartiersResponse.json();
            console.log('✅ Quartiers:', quartiersData.length, 'quartiers trouvés');
        } else {
            console.log('❌ Quartiers échoué:', quartiersResponse.status);
        }
    } catch (error) {
        console.log('❌ Erreur quartiers:', error);
    }

    console.log('\n3️⃣ Test des alertes (sans auth)...');
    try {
        const alertsResponse = await fetch(`${baseURL}/notifications/alerts/`);
        if (alertsResponse.ok) {
            const alertsData = await alertsResponse.json();
            console.log('✅ Alertes:', alertsData.count, 'alertes trouvées');
        } else {
            console.log('❌ Alertes échoué:', alertsResponse.status);
        }
    } catch (error) {
        console.log('❌ Erreur alertes:', error);
    }

    console.log('\n4️⃣ Test d\'inscription...');
    try {
        const registerData = {
            username: 'testuser' + Date.now(),
            email: 'test' + Date.now() + '@example.com',
            password: 'TestPassword123!',
            password_confirm: 'TestPassword123!',
            first_name: 'Test',
            last_name: 'User',
            phone_number: '+224123456789',
            quartier: 54
        };

        const registerResponse = await fetch(`${baseURL}/users/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registerData)
        });

        if (registerResponse.ok) {
            const registerResult = await registerResponse.json();
            console.log('✅ Inscription réussie:', registerResult.user.username);
        } else {
            const errorData = await registerResponse.json();
            console.log('❌ Inscription échouée:', errorData);
        }
    } catch (error) {
        console.log('❌ Erreur inscription:', error);
    }

    console.log('\n🎉 Test terminé !');
}

// Exécuter le test
testFrontendAPIs(); 
// Script de débogage pour le stockage des tokens
// À exécuter dans la console du navigateur

console.log("🔍 DÉBOGAGE DU STOCKAGE DES TOKENS");
console.log("=" * 50);

// Vérifier les tokens dans localStorage
const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');
const user = localStorage.getItem('user');

console.log("📊 ÉTAT DU LOCALSTORAGE:");
console.log(`   - access_token: ${accessToken ? '✅ Présent' : '❌ Absent'}`);
console.log(`   - refresh_token: ${refreshToken ? '✅ Présent' : '❌ Absent'}`);
console.log(`   - user: ${user ? '✅ Présent' : '❌ Absent'}`);

if (accessToken) {
    console.log(`   - Token length: ${accessToken.length}`);
    console.log(`   - Token preview: ${accessToken.substring(0, 20)}...`);
}

if (user) {
    try {
        const userData = JSON.parse(user);
        console.log(`   - User ID: ${userData.id}`);
        console.log(`   - User email: ${userData.email}`);
    } catch (e) {
        console.log("   - ❌ Erreur parsing user data");
    }
}

// Test de l'API avec le token actuel
if (accessToken) {
    console.log("\n🧪 TEST DE L'API AVEC LE TOKEN ACTUEL:");
    
    fetch('http://localhost:8000/api/users/my-profile/', {
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log(`   - Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.user) {
            console.log("   - ✅ API accessible avec le token");
            console.log(`   - User: ${data.user.first_name} ${data.user.last_name}`);
        } else {
            console.log("   - ❌ Réponse API invalide");
            console.log("   - Data:", data);
        }
    })
    .catch(error => {
        console.log("   - ❌ Erreur API:", error.message);
    });
} else {
    console.log("\n❌ AUCUN TOKEN TROUVÉ - L'utilisateur n'est pas connecté");
}

// Vérifier la configuration axios
console.log("\n🔧 CONFIGURATION AXIOS:");
console.log("   - Base URL: http://localhost:8000/api");
console.log("   - Intercepteur configuré: ✅");

console.log("\n💡 RECOMMANDATIONS:");
if (!accessToken) {
    console.log("   1. Connectez-vous via http://localhost:3000/auto-login");
    console.log("   2. Ou créez un nouveau compte via http://localhost:3000/register");
} else {
    console.log("   1. Le token est présent, testez l'upload de photo");
    console.log("   2. Allez sur http://localhost:3000/profile");
} 
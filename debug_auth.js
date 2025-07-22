// Script de diagnostic d'authentification
console.log('🔍 DIAGNOSTIC D\'AUTHENTIFICATION');
console.log('=====================================');

// 1. Vérifier le localStorage
const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');
const userData = localStorage.getItem('user');

console.log('1. État du localStorage:');
console.log('   - Access Token:', accessToken ? '✅ Présent' : '❌ Absent');
console.log('   - Refresh Token:', refreshToken ? '✅ Présent' : '❌ Absent');
console.log('   - User Data:', userData ? '✅ Présent' : '❌ Absent');

if (userData) {
  try {
    const user = JSON.parse(userData);
    console.log('   - User ID:', user.id);
    console.log('   - User Email:', user.email);
    console.log('   - User Name:', user.first_name, user.last_name);
  } catch (e) {
    console.log('   - ❌ Erreur parsing user data:', e);
  }
}

// 2. Tester l'API avec le token actuel
console.log('\n2. Test de l\'API avec le token actuel:');
if (accessToken) {
  console.log('   - Token trouvé, test de l\'API...');
  
  fetch('http://localhost:8000/api/users/my-profile/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('   - Status:', response.status);
    console.log('   - OK:', response.ok);
    return response.json();
  })
  .then(data => {
    if (data.error) {
      console.log('   - ❌ Erreur API:', data.error);
    } else {
      console.log('   - ✅ API fonctionnelle');
      console.log('   - User:', data.first_name, data.last_name);
    }
  })
  .catch(error => {
    console.log('   - ❌ Erreur réseau:', error.message);
  });
} else {
  console.log('   - ❌ Aucun token trouvé');
}

// 3. Vérifier les headers de requête
console.log('\n3. Test d\'envoi de requête avec headers:');
const testHeaders = {
  'Authorization': `Bearer ${accessToken || 'NO_TOKEN'}`,
  'Content-Type': 'application/json'
};
console.log('   - Headers:', testHeaders);

// 4. Instructions pour l'utilisateur
console.log('\n4. INSTRUCTIONS:');
if (!accessToken) {
  console.log('   - ❌ Vous n\'êtes pas connecté');
  console.log('   - 📝 Allez sur http://localhost:3000/login');
  console.log('   - 📝 Connectez-vous avec:');
  console.log('     Email: testuser@example.com');
  console.log('     Password: testpass123');
} else {
  console.log('   - ✅ Vous êtes connecté');
  console.log('   - 📝 Testez l\'upload de photo maintenant');
} 
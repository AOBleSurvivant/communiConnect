// Test de l'authentification frontend
console.log('🔐 Test de l\'authentification frontend');

// Vérifier le localStorage
const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');
const user = localStorage.getItem('user');

console.log('Access Token:', accessToken ? 'Présent' : 'Absent');
console.log('Refresh Token:', refreshToken ? 'Présent' : 'Absent');
console.log('User Data:', user ? 'Présent' : 'Absent');

if (user) {
  try {
    const userData = JSON.parse(user);
    console.log('User:', userData);
  } catch (e) {
    console.log('Erreur parsing user data:', e);
  }
}

// Test de l'API avec le token
if (accessToken) {
  fetch('http://localhost:8000/api/users/my-profile/', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('API Profile Status:', response.status);
    return response.json();
  })
  .then(data => {
    console.log('API Profile Response:', data);
  })
  .catch(error => {
    console.error('API Profile Error:', error);
  });
} else {
  console.log('❌ Aucun token trouvé - utilisateur non connecté');
} 
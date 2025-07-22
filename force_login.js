// Script pour forcer la connexion de l'utilisateur de test
console.log('🔐 FORCE LOGIN - UTILISATEUR DE TEST');
console.log('======================================');

// Fonction de connexion
async function forceLogin() {
  try {
    console.log('1. Tentative de connexion...');
    
    const response = await fetch('http://localhost:8000/api/users/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: 'testuser@example.com',
        password: 'testpass123'
      })
    });
    
    console.log('2. Status de la réponse:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('3. Connexion réussie!');
      console.log('4. Sauvegarde des données...');
      
      // Sauvegarder les tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      // Sauvegarder les données utilisateur
      localStorage.setItem('user', JSON.stringify(data.user));
      
      console.log('5. ✅ Données sauvegardées dans localStorage');
      console.log('6. 🔄 Rechargez la page pour voir les changements');
      
      // Recharger la page après 2 secondes
      setTimeout(() => {
        window.location.reload();
      }, 2000);
      
    } else {
      const errorData = await response.json();
      console.log('❌ Erreur de connexion:', errorData);
    }
    
  } catch (error) {
    console.log('❌ Erreur réseau:', error.message);
  }
}

// Exécuter la connexion
forceLogin(); 
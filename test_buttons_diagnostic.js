// Script de diagnostic pour les boutons d'alertes
console.log('🔍 Diagnostic des boutons d\'alertes...');

// Fonction pour tester les boutons
function testButtons() {
    console.log('📋 === DIAGNOSTIC COMPLET ===');
    
    // 1. Vérifier les alertes affichées
    const alertCards = document.querySelectorAll('.bg-white.rounded-lg.shadow-md');
    console.log('📊 Nombre d\'alertes affichées:', alertCards.length);
    
    if (alertCards.length === 0) {
        console.log('❌ Aucune alerte trouvée dans l\'interface');
        return;
    }
    
    // 2. Analyser la première alerte
    const firstAlert = alertCards[0];
    console.log('🔍 Analyse de la première alerte:');
    
    // Récupérer les informations de l'alerte
    const title = firstAlert.querySelector('h3')?.textContent;
    const description = firstAlert.querySelector('p.text-gray-700')?.textContent;
    const statusElement = firstAlert.querySelector('[class*="text-yellow-600"], [class*="text-green-600"], [class*="text-red-600"]');
    const status = statusElement?.textContent;
    
    console.log('📋 Titre:', title);
    console.log('📋 Description:', description);
    console.log('📋 Statut:', status);
    
    // 3. Vérifier les boutons
    const confirmButtons = document.querySelectorAll('[title="Confirmer"]');
    const falseAlarmButtons = document.querySelectorAll('[title="Fausse alerte"]');
    const helpButtons = document.querySelectorAll('button:contains("Je peux aider")');
    
    console.log('🔘 Boutons trouvés:');
    console.log('  - Confirmer:', confirmButtons.length);
    console.log('  - Fausse alerte:', falseAlarmButtons.length);
    console.log('  - Je peux aider:', helpButtons.length);
    
    // 4. Tester le premier bouton confirmer
    if (confirmButtons.length > 0) {
        console.log('🧪 Test du bouton Confirmer...');
        const firstConfirmButton = confirmButtons[0];
        
        // Ajouter un listener temporaire
        const clickHandler = () => {
            console.log('✅ Clic détecté sur Confirmer!');
        };
        
        firstConfirmButton.addEventListener('click', clickHandler, { once: true });
        
        // Cliquer sur le bouton
        console.log('🔘 Clic sur Confirmer...');
        firstConfirmButton.click();
        
        // Nettoyer le listener après 2 secondes
        setTimeout(() => {
            firstConfirmButton.removeEventListener('click', clickHandler);
        }, 2000);
        
    } else {
        console.log('❌ Aucun bouton Confirmer trouvé');
    }
    
    // 5. Vérifier les fonctions React
    console.log('🔍 Vérification des fonctions React...');
    
    // Essayer d'accéder aux fonctions via window
    if (window.reportAlert) {
        console.log('✅ Fonction reportAlert disponible globalement');
    } else {
        console.log('❌ Fonction reportAlert non disponible globalement');
    }
    
    // 6. Test manuel de l'API
    console.log('🌐 Test manuel de l\'API...');
    
    // Récupérer le token
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    console.log('🔑 Token disponible:', !!token);
    
    // Tester une requête API directe
    if (alertCards.length > 0) {
        // Essayer de récupérer l'ID de l'alerte
        const alertId = firstAlert.getAttribute('data-alert-id') || 
                       firstAlert.querySelector('[data-alert-id]')?.getAttribute('data-alert-id');
        
        if (alertId) {
            console.log('📋 ID de l\'alerte trouvé:', alertId);
            
            // Test de l'API de rapport
            fetch(`http://127.0.0.1:8000/api/notifications/alerts/${alertId}/report/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    report_type: 'confirmed',
                    reason: 'Test diagnostic'
                })
            })
            .then(response => {
                console.log('📊 Réponse API test:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('📋 Données API test:', data);
            })
            .catch(error => {
                console.error('❌ Erreur API test:', error);
            });
        } else {
            console.log('❌ Impossible de récupérer l\'ID de l\'alerte');
        }
    }
}

// Exécuter le diagnostic
testButtons();

// Attendre 3 secondes et vérifier les changements
setTimeout(() => {
    console.log('⏰ Vérification après 3 secondes...');
    
    // Vérifier si les alertes ont changé
    const alertCards = document.querySelectorAll('.bg-white.rounded-lg.shadow-md');
    console.log('📊 Nombre d\'alertes après 3s:', alertCards.length);
    
    if (alertCards.length > 0) {
        const firstAlert = alertCards[0];
        const statusElement = firstAlert.querySelector('[class*="text-yellow-600"], [class*="text-green-600"], [class*="text-red-600"]');
        const status = statusElement?.textContent;
        console.log('📋 Statut après 3s:', status);
    }
}, 3000);

console.log('✅ Diagnostic terminé - vérifiez les logs ci-dessus'); 
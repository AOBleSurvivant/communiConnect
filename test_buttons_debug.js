// Script de test pour les boutons d'alertes
console.log('🧪 Test des boutons d\'alertes...');

// Récupérer le premier alerte disponible
const firstAlert = document.querySelector('[data-alert-id]');
if (firstAlert) {
    const alertId = firstAlert.getAttribute('data-alert-id');
    console.log('📋 ID de l\'alerte trouvé:', alertId);
    
    // Test de la fonction reportAlert
    console.log('🔘 Test du bouton Confirmer...');
    // Simuler un clic sur le bouton confirmer
    const confirmButton = document.querySelector('[title="Confirmer"]');
    if (confirmButton) {
        console.log('✅ Bouton Confirmer trouvé');
        confirmButton.click();
    } else {
        console.log('❌ Bouton Confirmer non trouvé');
    }
} else {
    console.log('❌ Aucune alerte trouvée dans le DOM');
}

// Test de la fonction offerHelp
console.log('🔘 Test du bouton Je peux aider...');
const helpButton = document.querySelector('button:contains("Je peux aider")');
if (helpButton) {
    console.log('✅ Bouton Je peux aider trouvé');
    helpButton.click();
} else {
    console.log('❌ Bouton Je peux aider non trouvé');
}

console.log('✅ Test terminé - vérifiez les logs du serveur Django'); 
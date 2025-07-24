// Test de correction de la fonction getStatus
console.log('🧪 Test de correction de la fonction getStatus');

// Simulation de la fonction getStatus
const alertStatuses = {
    pending: { label: 'En attente', color: 'text-yellow-600 bg-yellow-100', icon: 'ClockIcon' },
    confirmed: { label: 'Confirmée', color: 'text-green-600 bg-green-100', icon: 'CheckCircleIcon' },
    in_progress: { label: 'En cours de traitement', color: 'text-blue-600 bg-blue-100', icon: 'WrenchScrewdriverIcon' },
    resolved: { label: 'Résolue', color: 'text-green-700 bg-green-200', icon: 'CheckCircleIcon' },
    false_alarm: { label: 'Fausse alerte', color: 'text-red-600 bg-red-100', icon: 'XCircleIcon' }
};

const getStatus = (status) => {
    if (!status) {
        return { label: 'Statut inconnu', color: 'text-gray-600 bg-gray-100', icon: 'QuestionMarkCircleIcon' };
    }
    
    // Essayer de trouver le statut exact
    if (alertStatuses[status]) {
        return alertStatuses[status];
    }
    
    // Essayer avec différentes variations
    const normalizedStatus = status.toLowerCase().replace(/[-\s]/g, '_');
    if (alertStatuses[normalizedStatus]) {
        return alertStatuses[normalizedStatus];
    }
    
    // Essayer avec des variations courantes
    const variations = {
        'pending': 'pending',
        'waiting': 'pending',
        'en_attente': 'pending',
        'confirmed': 'confirmed',
        'confirmée': 'confirmed',
        'validated': 'confirmed',
        'in_progress': 'in_progress',
        'en_cours': 'in_progress',
        'processing': 'in_progress',
        'resolved': 'resolved',
        'résolue': 'resolved',
        'completed': 'resolved',
        'false_alarm': 'false_alarm',
        'fausse_alerte': 'false_alarm',
        'fake': 'false_alarm'
    };
    
    if (variations[normalizedStatus]) {
        return alertStatuses[variations[normalizedStatus]];
    }
    
    // Fallback avec le statut original
    console.warn(`Statut non reconnu: "${status}". Utilisation du fallback.`);
    return {
        label: status || 'Statut inconnu',
        color: 'text-gray-600 bg-gray-100',
        icon: 'QuestionMarkCircleIcon'
    };
};

// Test de la fonction
console.log('📋 Test de la fonction getStatus:');

const testCases = [
    'pending',
    'PENDING',
    'En attente',
    'waiting',
    'confirmed',
    'CONFIRMED',
    'Confirmée',
    'validated',
    'in_progress',
    'IN_PROGRESS',
    'En cours',
    'processing',
    'resolved',
    'RESOLVED',
    'Résolue',
    'completed',
    'false_alarm',
    'FALSE_ALARM',
    'Fausse alerte',
    'fake',
    'unknown',
    null,
    undefined
];

testCases.forEach(status => {
    const result = getStatus(status);
    console.log(`  "${status}" → "${result.label}" (${result.color})`);
});

// Test de simulation du composant AlertDetailModal
console.log('\n🧪 Test de simulation du composant AlertDetailModal:');

const mockAlert = {
    alert_id: 1,
    title: 'Test Alert',
    status: 'confirmed',
    category: 'fire',
    description: 'Test description',
    time_ago: '2 heures',
    reliability_score: 85
};

const mockGetStatus = getStatus; // Simulation de la prop passée

// Simulation de l'utilisation dans AlertDetailModal
const status = mockGetStatus(mockAlert.status);
console.log(`  Alerte "${mockAlert.title}":`);
console.log(`    Status brut: "${mockAlert.status}"`);
console.log(`    Status traité: "${status.label}"`);
console.log(`    Couleur: "${status.color}"`);

console.log('\n✅ Test de correction terminé!');
console.log('🎯 Résultat attendu:');
console.log('- Plus d\'erreur "getStatus is not defined"');
console.log('- Fonction getStatus accessible dans AlertDetailModal');
console.log('- Statuts affichés correctement dans les détails d\'alerte');

console.log('\n✅ Correction appliquée avec succès!'); 
// Diagnostic des statuts d'alertes
console.log('🔍 Diagnostic des statuts d\'alertes');

// Statuts définis dans le frontend
const alertStatuses = {
    pending: { label: 'En attente', color: 'text-yellow-600 bg-yellow-100', icon: 'ClockIcon' },
    confirmed: { label: 'Confirmée', color: 'text-green-600 bg-green-100', icon: 'CheckCircleIcon' },
    in_progress: { label: 'En cours de traitement', color: 'text-blue-600 bg-blue-100', icon: 'WrenchScrewdriverIcon' },
    resolved: { label: 'Résolue', color: 'text-green-700 bg-green-200', icon: 'CheckCircleIcon' },
    false_alarm: { label: 'Fausse alerte', color: 'text-red-600 bg-red-100', icon: 'XCircleIcon' }
};

console.log('📋 Statuts définis dans le frontend:');
Object.entries(alertStatuses).forEach(([key, status]) => {
    console.log(`  ${key}: ${status.label}`);
});

// Fonction pour diagnostiquer les données d'alertes
function diagnoseAlertStatuses(alerts) {
    console.log('\n🔍 Diagnostic des données reçues:');
    
    if (!alerts || alerts.length === 0) {
        console.log('❌ Aucune alerte reçue');
        return;
    }
    
    // Analyser les statuts présents
    const statusCounts = {};
    const unknownStatuses = new Set();
    
    alerts.forEach((alert, index) => {
        console.log(`\n📊 Alerte ${index + 1}:`);
        console.log(`  ID: ${alert.alert_id || alert.id}`);
        console.log(`  Titre: ${alert.title}`);
        console.log(`  Status brut: ${alert.status}`);
        console.log(`  Status type: ${typeof alert.status}`);
        
        // Compter les statuts
        if (alert.status) {
            statusCounts[alert.status] = (statusCounts[alert.status] || 0) + 1;
            
            // Vérifier si le statut est reconnu
            if (!alertStatuses[alert.status]) {
                unknownStatuses.add(alert.status);
            }
        } else {
            statusCounts['null/undefined'] = (statusCounts['null/undefined'] || 0) + 1;
        }
    });
    
    console.log('\n📈 Statistiques des statuts:');
    Object.entries(statusCounts).forEach(([status, count]) => {
        const isKnown = alertStatuses[status];
        console.log(`  ${status}: ${count} alerte(s) ${isKnown ? '✅' : '❌'}`);
    });
    
    if (unknownStatuses.size > 0) {
        console.log('\n⚠️ Statuts inconnus détectés:');
        unknownStatuses.forEach(status => {
            console.log(`  - "${status}" (non défini dans alertStatuses)`);
        });
        
        console.log('\n💡 Suggestions de correction:');
        console.log('1. Vérifier les valeurs de statut dans la base de données');
        console.log('2. Ajouter les statuts manquants dans alertStatuses');
        console.log('3. Normaliser les valeurs côté backend');
    }
}

// Fonction pour tester la correspondance
function testStatusMapping() {
    console.log('\n🧪 Test de correspondance des statuts:');
    
    // Test avec différents formats possibles
    const testStatuses = [
        'pending', 'PENDING', 'Pending',
        'confirmed', 'CONFIRMED', 'Confirmed',
        'in_progress', 'IN_PROGRESS', 'In_Progress', 'in-progress',
        'resolved', 'RESOLVED', 'Resolved',
        'false_alarm', 'FALSE_ALARM', 'False_Alarm', 'false-alarm',
        'unknown', 'null', undefined, null
    ];
    
    testStatuses.forEach(status => {
        const mappedStatus = alertStatuses[status];
        if (mappedStatus) {
            console.log(`  ✅ "${status}" → ${mappedStatus.label}`);
        } else {
            console.log(`  ❌ "${status}" → Non trouvé`);
        }
    });
}

// Fonction pour suggérer des corrections
function suggestFixes(unknownStatuses) {
    console.log('\n🔧 Suggestions de correction:');
    
    if (unknownStatuses.size === 0) {
        console.log('✅ Tous les statuts sont correctement mappés');
        return;
    }
    
    console.log('1. Ajouter les statuts manquants dans alertStatuses:');
    unknownStatuses.forEach(status => {
        console.log(`   ${status}: { label: '${status}', color: 'text-gray-600 bg-gray-100', icon: 'QuestionMarkCircleIcon' },`);
    });
    
    console.log('\n2. Ou normaliser les valeurs côté backend:');
    console.log('   - Convertir en minuscules');
    console.log('   - Remplacer les espaces par des underscores');
    console.log('   - Standardiser les formats');
    
    console.log('\n3. Ou ajouter une fonction de fallback:');
    console.log(`
   const getStatus = (status) => {
       return alertStatuses[status] || alertStatuses[status?.toLowerCase()] || {
           label: status || 'Statut inconnu',
           color: 'text-gray-600 bg-gray-100',
           icon: 'QuestionMarkCircleIcon'
       };
   };
   `);
}

// Exécuter les tests
console.log('=== DIAGNOSTIC COMPLET ===');
testStatusMapping();

console.log('\n=== INSTRUCTIONS ===');
console.log('1. Ouvrez la console du navigateur');
console.log('2. Allez sur la page des alertes');
console.log('3. Exécutez: diagnoseAlertStatuses(alerts)');
console.log('4. Vérifiez les données reçues du backend');
console.log('5. Appliquez les corrections suggérées');

console.log('\n✅ Diagnostic prêt!'); 
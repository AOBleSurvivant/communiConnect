/**
 * Tests pour le composant LiveTimer
 * 
 * Ce fichier contient des tests simples pour vérifier le bon fonctionnement
 * du chronomètre des lives
 */

import { formatTime, calculateDuration, isLiveActive } from '../utils/timeUtils';

// Tests pour formatTime
console.log('Tests formatTime:');
console.log('formatTime(0) =', formatTime(0)); // "00:00"
console.log('formatTime(65) =', formatTime(65)); // "01:05"
console.log('formatTime(3661) =', formatTime(3661)); // "61:01"

// Tests pour calculateDuration
console.log('\nTests calculateDuration:');
const now = new Date();
const oneMinuteAgo = new Date(now.getTime() - 60000);
const oneHourAgo = new Date(now.getTime() - 3600000);

console.log('calculateDuration(oneMinuteAgo) ≈', calculateDuration(oneMinuteAgo)); // ~60
console.log('calculateDuration(oneHourAgo) ≈', calculateDuration(oneHourAgo)); // ~3600

// Tests pour isLiveActive
console.log('\nTests isLiveActive:');
console.log('isLiveActive(oneMinuteAgo) =', isLiveActive(oneMinuteAgo)); // true
console.log('isLiveActive(null) =', isLiveActive(null)); // false

// Test de simulation d'un live
console.log('\nSimulation d\'un live:');
const liveStartTime = new Date();
console.log('Live démarré à:', liveStartTime.toLocaleTimeString());

// Simuler le passage du temps
setTimeout(() => {
  console.log('Après 5 secondes:');
  console.log('Durée calculée:', calculateDuration(liveStartTime), 'secondes');
  console.log('Durée formatée:', formatTime(calculateDuration(liveStartTime)));
  console.log('Live actif:', isLiveActive(liveStartTime));
}, 5000);

console.log('\n✅ Tous les tests sont prêts !'); 
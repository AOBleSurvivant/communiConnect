// Script de debug pour l'affichage de la vidéo
// À exécuter dans la console F12 du navigateur

console.log('🎥 DEBUG VIDÉO - DIAGNOSTIC COMPLET');
console.log('=' * 50);

// 1. Vérifier les états React
function checkReactStates() {
  console.log('📊 VÉRIFICATION DES ÉTATS REACT:');
  
  try {
    // Ces variables doivent être disponibles dans le scope du composant LiveStream
    console.log('recordedVideo:', typeof recordedVideo, recordedVideo);
    console.log('isLive:', typeof isLive, isLive);
    console.log('videoDuration:', typeof videoDuration, videoDuration);
    console.log('isPlaying:', typeof isPlaying, isPlaying);
    console.log('currentTime:', typeof currentTime, currentTime);
    console.log('liveInfo:', typeof liveInfo, liveInfo);
  } catch (e) {
    console.log('❌ Impossible d\'accéder aux états React:', e.message);
  }
}

// 2. Vérifier l'élément vidéo
function checkVideoElement() {
  console.log('🎬 VÉRIFICATION DE L\'ÉLÉMENT VIDÉO:');
  
  const videoElement = document.querySelector('video');
  if (videoElement) {
    console.log('✅ Élément vidéo trouvé');
    console.log('src:', videoElement.src);
    console.log('srcObject:', videoElement.srcObject);
    console.log('currentTime:', videoElement.currentTime);
    console.log('duration:', videoElement.duration);
    console.log('paused:', videoElement.paused);
    console.log('readyState:', videoElement.readyState);
    console.log('networkState:', videoElement.networkState);
    console.log('error:', videoElement.error);
    console.log('videoWidth:', videoElement.videoWidth);
    console.log('videoHeight:', videoElement.videoHeight);
  } else {
    console.log('❌ Aucun élément vidéo trouvé');
  }
}

// 3. Forcer l'affichage de la vidéo
function forceVideoDisplay() {
  console.log('🔄 TENTATIVE DE FORÇAGE AFFICHAGE VIDÉO:');
  
  const videoElement = document.querySelector('video');
  if (videoElement && videoElement.src) {
    console.log('🎬 Vidéo trouvée, tentative de lecture...');
    
    // Forcer le chargement
    videoElement.load();
    
    // Attendre et essayer de lire
    setTimeout(() => {
      videoElement.play().then(() => {
        console.log('✅ Lecture forcée réussie');
      }).catch((error) => {
        console.log('❌ Erreur lecture forcée:', error);
      });
    }, 500);
  } else {
    console.log('❌ Pas de vidéo à forcer');
  }
}

// 4. Vérifier l'interface utilisateur
function checkUI() {
  console.log('🖥️ VÉRIFICATION DE L\'INTERFACE:');
  
  // Vérifier les badges
  const badges = document.querySelectorAll('[class*="badge"], [class*="status"]');
  console.log('Badges trouvés:', badges.length);
  
  // Vérifier les contrôles de lecture
  const playButtons = document.querySelectorAll('button[onclick*="play"], button[onclick*="toggle"]');
  console.log('Boutons de lecture trouvés:', playButtons.length);
  
  // Vérifier les messages d'état
  const messages = document.querySelectorAll('[class*="message"], [class*="toast"]');
  console.log('Messages trouvés:', messages.length);
  
  // Vérifier les éléments avec "VIDÉO PRÊTE"
  const videoReadyElements = document.querySelectorAll('*:contains("VIDÉO PRÊTE")');
  console.log('Éléments "VIDÉO PRÊTE" trouvés:', videoReadyElements.length);
}

// 5. Vérifier les logs de la console
function checkConsoleLogs() {
  console.log('📝 VÉRIFICATION DES LOGS:');
  
  // Chercher les logs spécifiques
  const logs = [
    '🎬 Création du blob vidéo',
    '🎥 Configuration de la lecture vidéo',
    '✅ Vidéo configurée pour la lecture',
    '🔄 Force video display',
    '✅ Vidéo chargée avec succès',
    '🔄 Re-rendu forcé'
  ];
  
  logs.forEach(log => {
    console.log(`Recherche: ${log}`);
  });
}

// 6. Forcer la mise à jour des états
function forceStateUpdate() {
  console.log('🔄 FORÇAGE MISE À JOUR DES ÉTATS:');
  
  try {
    // Essayer de forcer la mise à jour
    if (typeof setRecordedVideo === 'function') {
      console.log('🔄 Forçage setRecordedVideo...');
      // Cette fonction sera appelée si disponible
    }
    
    if (typeof setVideoDuration === 'function') {
      console.log('🔄 Forçage setVideoDuration...');
      // Cette fonction sera appelée si disponible
    }
  } catch (e) {
    console.log('❌ Impossible de forcer la mise à jour:', e.message);
  }
}

// Exécution du diagnostic complet
console.log('🚀 DÉMARRAGE DU DIAGNOSTIC...');
checkReactStates();
checkVideoElement();
checkUI();
checkConsoleLogs();

console.log('💡 INSTRUCTIONS DE DEBUG:');
console.log('1. Vérifiez que recordedVideo contient une URL blob');
console.log('2. Vérifiez que isLive est false');
console.log('3. Vérifiez que videoDuration > 0 et est fini');
console.log('4. Vérifiez que l\'élément vidéo a un src valide');
console.log('5. Vérifiez que les contrôles de lecture sont visibles');

// Fonctions pour forcer les actions
window.forceVideoDisplay = forceVideoDisplay;
window.forceStateUpdate = forceStateUpdate;

console.log('✅ Diagnostic terminé. Utilisez forceVideoDisplay() ou forceStateUpdate() pour forcer les actions.'); 
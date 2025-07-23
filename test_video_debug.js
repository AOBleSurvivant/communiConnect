// Script de debug pour l'affichage de la vidéo
// À exécuter dans la console F12 du navigateur

console.log('🎥 DEBUG VIDÉO - DIAGNOSTIC COMPLET');
console.log('=' * 50);

// 1. Vérifier les états React
function checkReactStates() {
  console.log('📊 VÉRIFICATION DES ÉTATS REACT:');
  
  // Ces variables doivent être disponibles dans le scope du composant LiveStream
  try {
    console.log('recordedVideo:', typeof recordedVideo, recordedVideo);
    console.log('isLive:', typeof isLive, isLive);
    console.log('videoDuration:', typeof videoDuration, videoDuration);
    console.log('isPlaying:', typeof isPlaying, isPlaying);
    console.log('currentTime:', typeof currentTime, currentTime);
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
  } else {
    console.log('❌ Aucun élément vidéo trouvé');
  }
}

// 3. Vérifier les contrôles de lecture
function checkVideoControls() {
  console.log('🎮 VÉRIFICATION DES CONTRÔLES VIDÉO:');
  
  const controls = document.querySelectorAll('[data-video-control]');
  console.log('Contrôles trouvés:', controls.length);
  
  controls.forEach((control, index) => {
    console.log(`Contrôle ${index + 1}:`, control.textContent, control.className);
  });
}

// 4. Vérifier l'interface utilisateur
function checkUI() {
  console.log('🖥️ VÉRIFICATION DE L\'INTERFACE:');
  
  // Vérifier les messages d'état
  const messages = document.querySelectorAll('[class*="message"], [class*="toast"]');
  console.log('Messages trouvés:', messages.length);
  
  // Vérifier les badges
  const badges = document.querySelectorAll('[class*="badge"], [class*="status"]');
  console.log('Badges trouvés:', badges.length);
  
  // Vérifier les boutons de lecture
  const playButtons = document.querySelectorAll('button[onclick*="play"], button[onclick*="toggle"]');
  console.log('Boutons de lecture trouvés:', playButtons.length);
}

// 5. Forcer la lecture de la vidéo
function forceVideoPlay() {
  console.log('▶️ TENTATIVE DE LECTURE FORCÉE:');
  
  const videoElement = document.querySelector('video');
  if (videoElement && videoElement.src) {
    console.log('🎬 Tentative de lecture...');
    videoElement.play().then(() => {
      console.log('✅ Lecture démarrée avec succès');
    }).catch((error) => {
      console.log('❌ Erreur de lecture:', error);
    });
  } else {
    console.log('❌ Impossible de forcer la lecture - vidéo non disponible');
  }
}

// 6. Vérifier les logs de la console
function checkConsoleLogs() {
  console.log('📝 VÉRIFICATION DES LOGS:');
  
  // Chercher les logs spécifiques
  const logs = [
    '🎬 Création du blob vidéo',
    '🎥 Configuration de la lecture vidéo',
    '✅ Vidéo configurée pour la lecture',
    '🔄 Forçage de la mise à jour'
  ];
  
  logs.forEach(log => {
    console.log(`Recherche: ${log}`);
  });
}

// Exécution du diagnostic complet
console.log('🚀 DÉMARRAGE DU DIAGNOSTIC...');
checkReactStates();
checkVideoElement();
checkVideoControls();
checkUI();
checkConsoleLogs();

console.log('💡 INSTRUCTIONS DE DEBUG:');
console.log('1. Vérifiez que recordedVideo contient une URL blob');
console.log('2. Vérifiez que isLive est false');
console.log('3. Vérifiez que videoDuration > 0');
console.log('4. Vérifiez que l\'élément vidéo a un src valide');
console.log('5. Vérifiez que les contrôles de lecture sont visibles');

// Fonction pour forcer la mise à jour
window.forceVideoUpdate = function() {
  console.log('🔄 FORÇAGE DE LA MISE À JOUR VIDÉO');
  checkVideoElement();
  forceVideoPlay();
};

console.log('✅ Diagnostic terminé. Utilisez forceVideoUpdate() pour forcer la mise à jour.'); 
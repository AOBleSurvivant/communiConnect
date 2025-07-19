/**
 * Utilitaires pour la gestion du temps dans les lives
 */

/**
 * Formate une durée en secondes en format MM:SS
 * @param {number} seconds - Durée en secondes
 * @returns {string} - Durée formatée (ex: "05:32")
 */
export const formatTime = (seconds) => {
  if (!seconds || seconds < 0) return '00:00';
  
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

/**
 * Formate une durée en secondes en format plus détaillé
 * @param {number} seconds - Durée en secondes
 * @returns {string} - Durée formatée (ex: "1h 25m 32s")
 */
export const formatDetailedTime = (seconds) => {
  if (!seconds || seconds < 0) return '0s';
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}h ${minutes.toString().padStart(2, '0')}m ${secs.toString().padStart(2, '0')}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${secs.toString().padStart(2, '0')}s`;
  } else {
    return `${secs}s`;
  }
};

/**
 * Calcule la durée depuis un timestamp de début
 * @param {string|Date} startTime - Timestamp de début
 * @returns {number} - Durée en secondes
 */
export const calculateDuration = (startTime) => {
  if (!startTime) return 0;
  
  const start = new Date(startTime).getTime();
  const now = Date.now();
  return Math.floor((now - start) / 1000);
};

/**
 * Vérifie si un live est actif
 * @param {string|Date} startTime - Timestamp de début
 * @param {string|Date} endTime - Timestamp de fin (optionnel)
 * @returns {boolean} - True si le live est actif
 */
export const isLiveActive = (startTime, endTime = null) => {
  if (!startTime) return false;
  
  const start = new Date(startTime).getTime();
  const now = Date.now();
  
  // Si pas de fin spécifiée, considérer comme actif
  if (!endTime) return true;
  
  const end = new Date(endTime).getTime();
  return now >= start && now <= end;
};

/**
 * Génère un chronomètre en temps réel
 * @param {string|Date} startTime - Timestamp de début
 * @param {function} callback - Fonction appelée avec la durée mise à jour
 * @returns {function} - Fonction pour arrêter le chronomètre
 */
export const createLiveTimer = (startTime, callback) => {
  if (!startTime || !callback) return () => {};
  
  const interval = setInterval(() => {
    const duration = calculateDuration(startTime);
    callback(duration);
  }, 1000);
  
  return () => clearInterval(interval);
}; 
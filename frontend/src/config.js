// Configuration de l'API
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

// Configuration des alertes
export const ALERT_CONFIG = {
    // Rayon par défaut pour les alertes à proximité (en km)
    DEFAULT_RADIUS: 5.0,
    
    // Rayon pour les alertes urgentes (en km)
    URGENT_RADIUS: 10.0,
    
    // Seuil de fiabilité pour considérer une alerte comme fiable
    RELIABILITY_THRESHOLD: 70.0,
    
    // Catégories d'alertes urgentes
    URGENT_CATEGORIES: ['fire', 'medical', 'gas_leak', 'security'],
    
    // Limite de pagination par défaut
    DEFAULT_PAGE_SIZE: 20,
    
    // Timeout pour la géolocalisation (en ms)
    GEOLOCATION_TIMEOUT: 10000,
    
    // Âge maximum des coordonnées GPS (en ms)
    GEOLOCATION_MAX_AGE: 300000, // 5 minutes
};

// Configuration des notifications
export const NOTIFICATION_CONFIG = {
    // Durée d'affichage des toasts (en ms)
    TOAST_DURATION: 5000,
    
    // Types de notifications
    TYPES: {
        COMMUNITY_ALERT: 'community_alert',
        STATUS_UPDATE: 'status_update',
        HELP_OFFER: 'help_offer',
        NEARBY_ALERT: 'nearby_alert'
    }
};

// Configuration de l'interface utilisateur
export const UI_CONFIG = {
    // Nombre d'alertes par page
    ALERTS_PER_PAGE: 12,
    
    // Délai de rafraîchissement automatique (en ms)
    AUTO_REFRESH_DELAY: 30000, // 30 secondes
    
    // Animation de chargement
    LOADING_ANIMATION_DURATION: 1000,
    
    // Couleurs des thèmes
    COLORS: {
        PRIMARY: '#3B82F6',
        SUCCESS: '#10B981',
        WARNING: '#F59E0B',
        DANGER: '#EF4444',
        INFO: '#06B6D4'
    }
};

// Configuration de la géolocalisation
export const GEO_CONFIG = {
    // Options de géolocalisation
    GEOLOCATION_OPTIONS: {
        enableHighAccuracy: true,
        timeout: ALERT_CONFIG.GEOLOCATION_TIMEOUT,
        maximumAge: ALERT_CONFIG.GEOLOCATION_MAX_AGE
    },
    
    // Messages d'erreur de géolocalisation
    ERROR_MESSAGES: {
        PERMISSION_DENIED: 'L\'accès à la géolocalisation a été refusé. Vous pouvez saisir votre position manuellement.',
        POSITION_UNAVAILABLE: 'Impossible d\'obtenir votre position actuelle.',
        TIMEOUT: 'La demande de géolocalisation a expiré.',
        UNKNOWN_ERROR: 'Une erreur inconnue s\'est produite lors de la géolocalisation.'
    }
};

// Configuration des messages
export const MESSAGES = {
    SUCCESS: {
        ALERT_CREATED: 'Alerte créée avec succès !',
        ALERT_UPDATED: 'Alerte mise à jour avec succès !',
        ALERT_DELETED: 'Alerte supprimée avec succès !',
        HELP_OFFERED: 'Offre d\'aide envoyée !',
        ALERT_REPORTED: 'Rapport envoyé avec succès',
        ALERT_CONFIRMED: 'Alerte confirmée avec succès',
        ALERT_RESOLVED: 'Alerte marquée comme résolue'
    },
    ERROR: {
        ALERT_CREATION_FAILED: 'Erreur lors de la création de l\'alerte',
        ALERT_UPDATE_FAILED: 'Erreur lors de la mise à jour de l\'alerte',
        ALERT_DELETION_FAILED: 'Erreur lors de la suppression de l\'alerte',
        HELP_OFFER_FAILED: 'Erreur lors de l\'envoi de l\'offre d\'aide',
        ALERT_REPORT_FAILED: 'Erreur lors de l\'envoi du rapport',
        NETWORK_ERROR: 'Erreur de connexion',
        GEOLOCATION_ERROR: 'Erreur de géolocalisation',
        VALIDATION_ERROR: 'Veuillez vérifier les informations saisies'
    },
    WARNING: {
        GEOLOCATION_UNAVAILABLE: 'Impossible d\'obtenir votre position. Vous pouvez la saisir manuellement.',
        NO_ALERTS_FOUND: 'Aucune alerte trouvée',
        NO_NEARBY_ALERTS: 'Aucune alerte à proximité'
    },
    INFO: {
        LOADING_ALERTS: 'Chargement des alertes...',
        LOADING_STATS: 'Chargement des statistiques...',
        SAVING_ALERT: 'Enregistrement de l\'alerte...',
        SENDING_REPORT: 'Envoi du rapport...'
    }
};

// Configuration des validations
export const VALIDATION_CONFIG = {
    ALERT: {
        TITLE_MIN_LENGTH: 5,
        TITLE_MAX_LENGTH: 200,
        DESCRIPTION_MIN_LENGTH: 10,
        DESCRIPTION_MAX_LENGTH: 1000,
        ADDRESS_MAX_LENGTH: 500,
        NEIGHBORHOOD_MAX_LENGTH: 100,
        CITY_MAX_LENGTH: 100,
        POSTAL_CODE_MAX_LENGTH: 10
    },
    HELP_OFFER: {
        DESCRIPTION_MIN_LENGTH: 10,
        DESCRIPTION_MAX_LENGTH: 500
    },
    REPORT: {
        REASON_MAX_LENGTH: 500
    }
};

// Configuration des permissions
export const PERMISSIONS = {
    CREATE_ALERT: 'can_create_alert',
    EDIT_ALERT: 'can_edit_alert',
    DELETE_ALERT: 'can_delete_alert',
    REPORT_ALERT: 'can_report_alert',
    OFFER_HELP: 'can_offer_help',
    VIEW_STATS: 'can_view_stats',
    MODERATE_ALERTS: 'can_moderate_alerts'
};

// Configuration des rôles
export const ROLES = {
    USER: 'user',
    MODERATOR: 'moderator',
    ADMIN: 'admin',
    EMERGENCY_SERVICES: 'emergency_services'
};

// Configuration des fonctionnalités
export const FEATURES = {
    GEOLOCATION: true,
    PUSH_NOTIFICATIONS: true,
    EMAIL_NOTIFICATIONS: true,
    REAL_TIME_UPDATES: true,
    STATISTICS: true,
    MODERATION: true,
    HELP_SYSTEM: true,
    RELIABILITY_SYSTEM: true
};

// Configuration de l'environnement
export const ENV_CONFIG = {
    IS_DEVELOPMENT: process.env.NODE_ENV === 'development',
    IS_PRODUCTION: process.env.NODE_ENV === 'production',
    IS_TEST: process.env.NODE_ENV === 'test',
    
    // URLs par environnement
    API_URLS: {
        development: 'http://127.0.0.1:8000/api',
        production: process.env.REACT_APP_API_URL || 'https://api.communiconnect.com/api',
        test: 'http://127.0.0.1:8000/api'
    }
};

// Configuration par défaut
export default {
    API_BASE_URL,
    ALERT_CONFIG,
    NOTIFICATION_CONFIG,
    UI_CONFIG,
    GEO_CONFIG,
    MESSAGES,
    VALIDATION_CONFIG,
    PERMISSIONS,
    ROLES,
    FEATURES,
    ENV_CONFIG
}; 
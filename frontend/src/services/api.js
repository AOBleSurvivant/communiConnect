import axios from 'axios';

// Configuration de base d'axios
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://communiconnect-backend.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré, rediriger vers la connexion
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
        window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Service d'authentification
export const authAPI = {
  // Inscription
  register: async (userData) => {
    const response = await api.post('/users/register/', userData);
    return response.data;
  },

  // Connexion
  login: async (email, password) => {
    const response = await api.post('/users/login/', {
      email,
      password,
    });
    return response.data;
  },

  // Déconnexion
  logout: async () => {
    const response = await api.post('/users/logout/');
    return response.data;
  },

  // Rafraîchir le token
  refreshToken: async (refreshToken) => {
    const response = await api.post('/token/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },
};

// Service des utilisateurs
export const userAPI = {
  // Récupérer le profil utilisateur
  getProfile: async () => {
    const response = await api.get('/users/profile/');
    return response.data;
  },

  // Mettre à jour le profil
  updateProfile: async (userData) => {
    const response = await api.patch('/users/profile/', userData);
    return response.data;
  },

  // Récupérer les données du tableau de bord
  getDashboardData: async () => {
    const response = await api.get('/users/dashboard/');
    return response.data;
  },
};

// Service des données géographiques
export const geographyAPI = {
  // Récupérer toutes les données géographiques
  getGeographicData: async () => {
    const response = await api.get('/users/geographic-data/');
    return response.data;
  },

  // Vérification géographique
  verifyGeographic: async () => {
    const response = await api.post('/users/verify-geographic/');
    return response.data;
  },
};

// Service de gestion des tokens
export const tokenService = {
  // Sauvegarder les tokens
  saveTokens: (tokens) => {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  },

  // Récupérer le token d'accès
  getAccessToken: () => {
    return localStorage.getItem('access_token');
  },

  // Récupérer le token de rafraîchissement
  getRefreshToken: () => {
    return localStorage.getItem('refresh_token');
  },

  // Supprimer les tokens
  clearTokens: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // Vérifier si l'utilisateur est connecté
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

// Service de gestion des données utilisateur
export const userService = {
  // Sauvegarder les données utilisateur
  saveUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user));
  },

  // Récupérer les données utilisateur
  getUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Supprimer les données utilisateur
  clearUser: () => {
    localStorage.removeItem('user');
  },
};

// Fonction utilitaire pour gérer les erreurs API
export const handleAPIError = (error) => {
  if (error.response) {
    // Erreur de réponse du serveur
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return {
          type: 'validation',
          message: data.error || 'Données invalides',
          details: data
        };
      case 401:
        return {
          type: 'auth',
          message: 'Non autorisé. Veuillez vous reconnecter.',
        };
      case 403:
        return {
          type: 'geographic',
          message: data.error || 'Accès géographique refusé',
          code: data.code
        };
      case 404:
        return {
          type: 'not_found',
          message: 'Ressource non trouvée',
        };
      case 500:
        return {
          type: 'server',
          message: 'Erreur serveur. Veuillez réessayer plus tard.',
        };
      default:
        return {
          type: 'unknown',
          message: 'Une erreur inattendue s\'est produite.',
        };
    }
  } else if (error.request) {
    // Erreur de réseau
    return {
      type: 'network',
      message: 'Erreur de connexion. Vérifiez votre connexion internet.',
    };
  } else {
    // Autre erreur
    return {
      type: 'unknown',
      message: 'Une erreur inattendue s\'est produite.',
    };
  }
};

// Fonction utilitaire pour valider les données de formulaire
export const validateFormData = (data, rules) => {
  const errors = {};

  Object.keys(rules).forEach(field => {
    const value = data[field];
    const fieldRules = rules[field];

    // Vérification requise
    if (fieldRules.required && (!value || value.trim() === '')) {
      errors[field] = `${fieldRules.label || field} est requis`;
      return;
    }

    // Vérification de longueur minimale
    if (fieldRules.minLength && value && value.length < fieldRules.minLength) {
      errors[field] = `${fieldRules.label || field} doit contenir au moins ${fieldRules.minLength} caractères`;
    }

    // Vérification de longueur maximale
    if (fieldRules.maxLength && value && value.length > fieldRules.maxLength) {
      errors[field] = `${fieldRules.label || field} ne peut pas dépasser ${fieldRules.maxLength} caractères`;
    }

    // Vérification d'email
    if (fieldRules.email && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        errors[field] = 'Format d\'email invalide';
      }
    }

    // Vérification de correspondance
    if (fieldRules.match && value !== data[fieldRules.match]) {
      errors[field] = `${fieldRules.label || field} ne correspond pas`;
    }
  });

  return errors;
};

export default api; 
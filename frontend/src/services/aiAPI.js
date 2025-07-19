import api from './api';

const aiAPI = {
  // Récupérer les recommandations personnalisées
  getRecommendations: async (params = {}) => {
    try {
      const response = await api.get('/ai/recommendations/', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur récupération recommandations IA:', error);
      throw error;
    }
  },

  // Récupérer les insights IA
  getInsights: async () => {
    try {
      const response = await api.get('/ai/insights/');
      return response.data;
    } catch (error) {
      console.error('Erreur récupération insights IA:', error);
      throw error;
    }
  },

  // Récupérer les tendances
  getTrendingTopics: async (quartierId = null, limit = 10) => {
    try {
      const params = { limit };
      if (quartierId) {
        params.quartier_id = quartierId;
      }
      
      const response = await api.get('/ai/trending/', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur récupération tendances:', error);
      throw error;
    }
  },

  // Récupérer l'analyse du comportement utilisateur
  getBehaviorAnalysis: async () => {
    try {
      const response = await api.get('/ai/behavior/');
      return response.data;
    } catch (error) {
      console.error('Erreur analyse comportement:', error);
      throw error;
    }
  },

  // Récupérer les optimisations de contenu
  getContentOptimization: async (contentType = 'posts') => {
    try {
      const response = await api.get('/ai/optimization/', {
        params: { content_type: contentType }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation contenu:', error);
      throw error;
    }
  },

  // Envoyer un feedback sur les recommandations
  sendFeedback: async (feedbackData) => {
    try {
      const response = await api.post('/ai/feedback/', feedbackData);
      return response.data;
    } catch (error) {
      console.error('Erreur envoi feedback:', error);
      throw error;
    }
  },

  // Récupérer les recommandations en temps réel
  getRealTimeRecommendations: async (userId, context = {}) => {
    try {
      const response = await api.get('/ai/recommendations/', {
        params: {
          user_id: userId,
          context: JSON.stringify(context),
          real_time: true
        }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations temps réel:', error);
      throw error;
    }
  },

  // Optimiser le timing des posts
  getOptimalPostingTimes: async () => {
    try {
      const response = await api.get('/ai/optimization/', {
        params: { content_type: 'timing' }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur timing optimal:', error);
      throw error;
    }
  },

  // Analyser les préférences de contenu
  analyzeContentPreferences: async () => {
    try {
      const response = await api.get('/ai/behavior/', {
        params: { analysis_type: 'content_preferences' }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur analyse préférences:', error);
      throw error;
    }
  },

  // Prédire l'engagement d'un post
  predictPostEngagement: async (postData) => {
    try {
      const response = await api.post('/ai/predict-engagement/', postData);
      return response.data;
    } catch (error) {
      console.error('Erreur prédiction engagement:', error);
      throw error;
    }
  },

  // Obtenir des suggestions de contenu
  getContentSuggestions: async (category = null) => {
    try {
      const params = {};
      if (category) {
        params.category = category;
      }
      
      const response = await api.get('/ai/content-suggestions/', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur suggestions contenu:', error);
      throw error;
    }
  },

  // Analyser les patterns d'activité
  analyzeActivityPatterns: async () => {
    try {
      const response = await api.get('/ai/behavior/', {
        params: { analysis_type: 'activity_patterns' }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur analyse patterns:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de connexions
  getConnectionRecommendations: async (limit = 10) => {
    try {
      const response = await api.get('/ai/recommendations/', {
        params: {
          include_users: true,
          include_posts: false,
          limit
        }
      });
      return response.data.users || [];
    } catch (error) {
      console.error('Erreur recommandations connexions:', error);
      throw error;
    }
  },

  // Obtenir des insights de performance
  getPerformanceInsights: async () => {
    try {
      const response = await api.get('/ai/insights/', {
        params: { insights_type: 'performance' }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur insights performance:', error);
      throw error;
    }
  },

  // Optimiser les paramètres de l'utilisateur
  optimizeUserSettings: async (userPreferences) => {
    try {
      const response = await api.post('/ai/optimize-settings/', userPreferences);
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation paramètres:', error);
      throw error;
    }
  },

  // Obtenir des alertes intelligentes
  getIntelligentAlerts: async () => {
    try {
      const response = await api.get('/ai/alerts/');
      return response.data;
    } catch (error) {
      console.error('Erreur alertes intelligentes:', error);
      throw error;
    }
  },

  // Analyser la satisfaction utilisateur
  analyzeUserSatisfaction: async () => {
    try {
      const response = await api.get('/ai/satisfaction-analysis/');
      return response.data;
    } catch (error) {
      console.error('Erreur analyse satisfaction:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de gamification
  getGamificationRecommendations: async () => {
    try {
      const response = await api.get('/ai/gamification/');
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations gamification:', error);
      throw error;
    }
  },

  // Prédire les tendances futures
  predictFutureTrends: async (timeframe = '7d') => {
    try {
      const response = await api.get('/ai/predict-trends/', {
        params: { timeframe }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur prédiction tendances:', error);
      throw error;
    }
  },

  // Optimiser l'expérience utilisateur
  optimizeUserExperience: async (userData) => {
    try {
      const response = await api.post('/ai/optimize-ux/', userData);
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation UX:', error);
      throw error;
    }
  },

  // Analyser les métriques de croissance
  analyzeGrowthMetrics: async () => {
    try {
      const response = await api.get('/ai/growth-metrics/');
      return response.data;
    } catch (error) {
      console.error('Erreur métriques croissance:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de contenu viral
  getViralContentRecommendations: async () => {
    try {
      const response = await api.get('/ai/viral-content/');
      return response.data;
    } catch (error) {
      console.error('Erreur contenu viral:', error);
      throw error;
    }
  },

  // Analyser la concurrence
  analyzeCompetition: async () => {
    try {
      const response = await api.get('/ai/competition-analysis/');
      return response.data;
    } catch (error) {
      console.error('Erreur analyse concurrence:', error);
      throw error;
    }
  },

  // Optimiser les campagnes marketing
  optimizeMarketingCampaigns: async (campaignData) => {
    try {
      const response = await api.post('/ai/optimize-marketing/', campaignData);
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation marketing:', error);
      throw error;
    }
  },

  // Obtenir des insights de rétention
  getRetentionInsights: async () => {
    try {
      const response = await api.get('/ai/retention-insights/');
      return response.data;
    } catch (error) {
      console.error('Erreur insights rétention:', error);
      throw error;
    }
  },

  // Analyser les patterns de conversion
  analyzeConversionPatterns: async () => {
    try {
      const response = await api.get('/ai/conversion-patterns/');
      return response.data;
    } catch (error) {
      console.error('Erreur patterns conversion:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de monétisation
  getMonetizationRecommendations: async () => {
    try {
      const response = await api.get('/ai/monetization/');
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations monétisation:', error);
      throw error;
    }
  },

  // Analyser la santé de la communauté
  analyzeCommunityHealth: async () => {
    try {
      const response = await api.get('/ai/community-health/');
      return response.data;
    } catch (error) {
      console.error('Erreur santé communauté:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de modération
  getModerationRecommendations: async () => {
    try {
      const response = await api.get('/ai/moderation/');
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations modération:', error);
      throw error;
    }
  },

  // Optimiser les algorithmes de recommandation
  optimizeRecommendationAlgorithms: async (algorithmData) => {
    try {
      const response = await api.post('/ai/optimize-algorithms/', algorithmData);
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation algorithmes:', error);
      throw error;
    }
  },

  // Analyser les métriques de performance
  analyzePerformanceMetrics: async () => {
    try {
      const response = await api.get('/ai/performance-metrics/');
      return response.data;
    } catch (error) {
      console.error('Erreur métriques performance:', error);
      throw error;
    }
  },

  // Obtenir des recommandations de sécurité
  getSecurityRecommendations: async () => {
    try {
      const response = await api.get('/ai/security/');
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations sécurité:', error);
      throw error;
    }
  },

  // Analyser les patterns de fraude
  analyzeFraudPatterns: async () => {
    try {
      const response = await api.get('/ai/fraud-patterns/');
      return response.data;
    } catch (error) {
      console.error('Erreur patterns fraude:', error);
      throw error;
    }
  },

  // Optimiser l'accessibilité
  optimizeAccessibility: async (accessibilityData) => {
    try {
      const response = await api.post('/ai/optimize-accessibility/', accessibilityData);
      return response.data;
    } catch (error) {
      console.error('Erreur optimisation accessibilité:', error);
      throw error;
    }
  },

  // Obtenir des insights de localisation
  getLocalizationInsights: async () => {
    try {
      const response = await api.get('/ai/localization-insights/');
      return response.data;
    } catch (error) {
      console.error('Erreur insights localisation:', error);
      throw error;
    }
  },

  // Analyser les patterns de migration
  analyzeMigrationPatterns: async () => {
    try {
      const response = await api.get('/ai/migration-patterns/');
      return response.data;
    } catch (error) {
      console.error('Erreur patterns migration:', error);
      throw error;
    }
  },

  // Obtenir des recommandations d'expansion
  getExpansionRecommendations: async () => {
    try {
      const response = await api.get('/ai/expansion/');
      return response.data;
    } catch (error) {
      console.error('Erreur recommandations expansion:', error);
      throw error;
    }
  }
};

export default aiAPI; 
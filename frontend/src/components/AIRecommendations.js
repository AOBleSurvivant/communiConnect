import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const AIRecommendations = () => {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('recommendations');
  const [feedback, setFeedback] = useState({});

  useEffect(() => {
    loadAIRecommendations();
    loadAIInsights();
  }, []);

  const loadAIRecommendations = async () => {
    try {
      setLoading(true);
      const response = await api.get('/ai/recommendations/', {
        params: {
          limit: 10,
          include_posts: true,
          include_users: true,
          include_content: true,
          include_activities: true
        }
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Erreur chargement recommandations IA:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAIInsights = async () => {
    try {
      const response = await api.get('/ai/insights/');
      setInsights(response.data);
    } catch (error) {
      console.error('Erreur chargement insights IA:', error);
    }
  };

  const handleFeedback = async (recommendationId, feedbackType, recommendationType) => {
    try {
      await api.post('/ai/feedback/', {
        recommendation_id: recommendationId,
        feedback_type: feedbackType,
        recommendation_type: recommendationType
      });
      
      setFeedback(prev => ({
        ...prev,
        [recommendationId]: feedbackType
      }));
    } catch (error) {
      console.error('Erreur feedback:', error);
    }
  };

  const getEngagementColor = (level) => {
    switch (level) {
      case 'Élevé': return 'text-green-600';
      case 'Moyen': return 'text-yellow-600';
      case 'Faible': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 border-red-300 text-red-800';
      case 'medium': return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      case 'low': return 'bg-green-100 border-green-300 text-green-800';
      default: return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow-md p-6">
                  <div className="h-4 bg-gray-300 rounded w-3/4 mb-4"></div>
                  <div className="h-3 bg-gray-300 rounded w-1/2 mb-2"></div>
                  <div className="h-3 bg-gray-300 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🤖 Intelligence Artificielle
          </h1>
          <p className="text-gray-600">
            Découvrez des recommandations personnalisées et des insights basés sur votre activité
          </p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 bg-white rounded-lg p-1 mb-8 shadow-sm">
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'recommendations'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            📋 Recommandations
          </button>
          <button
            onClick={() => setActiveTab('insights')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'insights'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            📊 Insights
          </button>
          <button
            onClick={() => setActiveTab('trending')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'trending'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            🔥 Tendances
          </button>
        </div>

        {/* Content */}
        {activeTab === 'recommendations' && (
          <div className="space-y-8">
            {/* Posts Recommandés */}
            {recommendations?.posts && recommendations.posts.length > 0 && (
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  📝 Posts Recommandés
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.posts.map((post) => (
                    <div key={post.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                      <div className="flex items-center mb-3">
                        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                          {post.author.username.charAt(0).toUpperCase()}
                        </div>
                        <div className="ml-3">
                          <p className="font-semibold text-gray-900">{post.author.username}</p>
                          <p className="text-sm text-gray-500">{post.author.quartier}</p>
                        </div>
                      </div>
                      
                      <p className="text-gray-700 mb-4 line-clamp-3">{post.content}</p>
                      
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <span>❤️ {post.likes_count}</span>
                        <span>💬 {post.comments_count}</span>
                        <span>{new Date(post.created_at).toLocaleDateString()}</span>
                      </div>
                      
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleFeedback(post.id, 'like', 'post')}
                          className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                            feedback[post.id] === 'like'
                              ? 'bg-green-500 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          👍 J'aime
                        </button>
                        <button
                          onClick={() => handleFeedback(post.id, 'dislike', 'post')}
                          className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                            feedback[post.id] === 'dislike'
                              ? 'bg-red-500 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          👎 Pas intéressé
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Utilisateurs Recommandés */}
            {recommendations?.users && recommendations.users.length > 0 && (
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  👥 Utilisateurs Recommandés
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.users.map((user) => (
                    <div key={user.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                      <div className="flex items-center mb-4">
                        <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
                          {user.username.charAt(0).toUpperCase()}
                        </div>
                        <div className="ml-4">
                          <p className="font-semibold text-gray-900">{user.username}</p>
                          <p className="text-sm text-gray-500">{user.quartier}</p>
                        </div>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-4">
                        {user.recommendation_reason}
                      </p>
                      
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleFeedback(user.id, 'like', 'user')}
                          className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                            feedback[user.id] === 'like'
                              ? 'bg-blue-500 text-white'
                              : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                          }`}
                        >
                          👋 Se connecter
                        </button>
                        <button
                          onClick={() => handleFeedback(user.id, 'ignore', 'user')}
                          className="flex-1 py-2 px-3 rounded-md text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
                        >
                          Ignorer
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Activités Suggérées */}
            {recommendations?.suggested_activities && recommendations.suggested_activities.length > 0 && (
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  🎯 Activités Suggérées
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {recommendations.suggested_activities.map((activity, index) => (
                    <div key={index} className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${getPriorityColor(activity.priority).split(' ')[0]}`}>
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-semibold text-gray-900">{activity.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(activity.priority)}`}>
                          {activity.priority === 'high' ? 'Priorité' : activity.priority === 'medium' ? 'Moyen' : 'Faible'}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-4">{activity.description}</p>
                      
                      <button className="w-full py-2 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">
                        Commencer
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'insights' && insights && (
          <div className="space-y-8">
            {/* Engagement Insights */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                📈 Insights d'Engagement
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">
                    {insights.engagement_insights.current_level.toFixed(1)}
                  </div>
                  <p className="text-gray-600">Niveau d'engagement actuel</p>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    {insights.engagement_insights.improvement_potential.toFixed(1)}
                  </div>
                  <p className="text-gray-600">Potentiel d'amélioration</p>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">
                    {insights.engagement_insights.target_level}
                  </div>
                  <p className="text-gray-600">Objectif</p>
                </div>
              </div>
            </div>

            {/* Social Insights */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                👥 Insights Sociaux
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">
                    {insights.social_insights.current_connections}
                  </div>
                  <p className="text-gray-600">Connexions actuelles</p>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    {insights.social_insights.potential_connections}
                  </div>
                  <p className="text-gray-600">Connexions potentielles</p>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">
                    {insights.social_insights.connection_opportunity}
                  </div>
                  <p className="text-gray-600">Opportunités</p>
                </div>
              </div>
            </div>

            {/* Growth Opportunities */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                🚀 Opportunités de Croissance
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {insights.growth_opportunities.map((opportunity, index) => (
                  <div key={index} className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${getPriorityColor(opportunity.priority).split(' ')[0]}`}>
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-gray-900">{opportunity.title}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(opportunity.priority)}`}>
                        {opportunity.priority === 'high' ? 'Priorité' : opportunity.priority === 'medium' ? 'Moyen' : 'Faible'}
                      </span>
                    </div>
                    
                    <p className="text-gray-600 mb-4">{opportunity.description}</p>
                    
                    <button className="w-full py-2 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">
                      Agir maintenant
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'trending' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              🔥 Tendances Actuelles
            </h2>
            <p className="text-gray-600 mb-6">
              Détection des sujets tendance en cours...
            </p>
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="text-gray-500 mt-4">Analyse des tendances en cours...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIRecommendations; 
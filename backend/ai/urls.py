from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    # Recommandations personnalisées
    path('recommendations/', views.get_personalized_recommendations, name='recommendations'),
    
    # Détection de tendances
    path('trending/', views.get_trending_topics, name='trending'),
    
    # Analyse du comportement utilisateur
    path('behavior/', views.get_user_behavior_analysis, name='behavior'),
    
    # Optimisation de contenu
    path('optimization/', views.get_content_optimization, name='optimization'),
    
    # Feedback sur les recommandations
    path('feedback/', views.feedback_recommendation, name='feedback'),
    
    # Insights IA généraux
    path('insights/', views.get_ai_insights, name='insights'),
] 
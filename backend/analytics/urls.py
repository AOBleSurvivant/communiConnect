from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Analytics utilisateur
    path('user/', views.get_user_analytics, name='user_analytics'),
    
    # Analytics géographiques
    path('geographic/', views.get_geographic_analytics, name='geographic_analytics'),
    
    # Insights temps réel
    path('insights/', views.get_real_time_insights, name='real_time_insights'),
    
    # Prédictions
    path('predictions/', views.get_predictions, name='predictions'),
    
    # Tracking d'événements
    path('track-event/', views.track_event, name='track_event'),
    
    # Métriques de performance
    path('performance/', views.get_performance_metrics, name='performance_metrics'),
    
    # Métriques business
    path('business/', views.get_business_metrics, name='business_metrics'),
    
    # Tableau de bord complet
    path('dashboard/', views.get_analytics_dashboard, name='analytics_dashboard'),
] 
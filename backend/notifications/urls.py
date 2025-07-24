from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # Routes existantes pour les notifications
    path('count/', views.notification_count, name='notification_count'),
    path('list/', views.notification_list, name='notification_list'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
    
    # Routes pour les alertes communautaires
    path('alerts/', views.CommunityAlertListCreateView.as_view(), name='community_alert_list_create'),
    path('alerts/<uuid:alert_id>/', views.CommunityAlertDetailView.as_view(), name='community_alert_detail'),
    path('alerts/nearby/', views.NearbyAlertsView.as_view(), name='nearby_alerts'),
    path('alerts/search/', views.AlertSearchView.as_view(), name='alert_search'),
    path('alerts/statistics/', views.AlertStatisticsView.as_view(), name='alert_statistics'),
    
    # Routes pour les rapports d'alertes
    path('alerts/<uuid:alert_id>/report/', views.AlertReportView.as_view(), name='alert_report'),
    
    # Routes pour les offres d'aide
    path('alerts/<uuid:alert_id>/help/', views.HelpOfferView.as_view(), name='help_offers'),
    
    # NOUVELLES ROUTES POUR AMÉLIORATIONS
    path('suggest-category/', views.suggest_alert_category, name='suggest_alert_category'),
    path('analytics/comprehensive-report/', views.comprehensive_analytics_report, name='comprehensive_analytics_report'),
] 
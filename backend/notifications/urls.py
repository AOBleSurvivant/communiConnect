from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Liste des notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    
    # Détails d'une notification
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    
    # Compter les notifications non lues
    path('count/', views.notification_count, name='notification-count'),
    
    # Marquer comme lues
    path('mark-as-read/', views.mark_as_read, name='mark-as-read'),
    
    # Préférences de notifications
    path('preferences/', views.notification_preferences, name='notification-preferences'),
    
    # Supprimer une notification
    path('<int:notification_id>/delete/', views.delete_notification, name='delete-notification'),
    
    # Supprimer toutes les notifications
    path('clear-all/', views.clear_all_notifications, name='clear-all-notifications'),
] 
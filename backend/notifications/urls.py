from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Liste des notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    
    # Détails d'une notification
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    
    # Compter les notifications non lues
    path('count/', views.NotificationCountView.as_view(), name='notification-count'),
    
    # Marquer comme lues
    path('mark-as-read/', views.MarkAsReadView.as_view(), name='mark-as-read'),
    
    # Préférences de notifications
    path('preferences/', views.NotificationPreferencesView.as_view(), name='notification-preferences'),
    
    # Supprimer une notification
    path('<int:pk>/delete/', views.DeleteNotificationView.as_view(), name='delete-notification'),
    
    # Supprimer toutes les notifications
    path('clear-all/', views.ClearAllNotificationsView.as_view(), name='clear-all-notifications'),
] 
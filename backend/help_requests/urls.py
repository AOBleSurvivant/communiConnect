from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HelpRequestViewSet, HelpResponseViewSet, HelpRequestCategoryViewSet

# Configuration du router pour les ViewSets
router = DefaultRouter()
router.register(r'requests', HelpRequestViewSet, basename='help-request')
router.register(r'responses', HelpResponseViewSet, basename='help-response')
router.register(r'categories', HelpRequestCategoryViewSet, basename='help-category')

app_name = 'help_requests'

urlpatterns = [
    # URLs du router pour les ViewSets
    path('api/', include(router.urls)),
    
    # URLs personnalisées pour des actions spécifiques
    path('api/requests/<uuid:pk>/respond/', 
         HelpRequestViewSet.as_view({'post': 'respond'}), 
         name='help-request-respond'),
    
    path('api/requests/<uuid:pk>/accept-response/', 
         HelpRequestViewSet.as_view({'post': 'accept_response'}), 
         name='help-request-accept-response'),
    
    path('api/requests/<uuid:pk>/reject-response/', 
         HelpRequestViewSet.as_view({'post': 'reject_response'}), 
         name='help-request-reject-response'),
    
    path('api/requests/<uuid:pk>/mark-completed/', 
         HelpRequestViewSet.as_view({'post': 'mark_completed'}), 
         name='help-request-mark-completed'),
    
    path('api/requests/<uuid:pk>/mark-cancelled/', 
         HelpRequestViewSet.as_view({'post': 'mark_cancelled'}), 
         name='help-request-mark-cancelled'),
    
    # Endpoint pour récupérer les réponses d'une demande
    path('api/requests/<uuid:pk>/responses/', 
         HelpRequestViewSet.as_view({'get': 'responses'}), 
         name='help-request-responses'),
] 
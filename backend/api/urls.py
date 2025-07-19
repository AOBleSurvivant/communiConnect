from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'API CommuniConnect is running'})

urlpatterns = [
    # Health check
    path('health/', health_check, name='health'),
    
    # API des utilisateurs
    path('users/', include('users.urls')),
    
    # API des posts
    path('posts/', include('posts.urls')),
    
    # API des notifications
    path('notifications/', include('notifications.urls')),
    
    # Refresh token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 
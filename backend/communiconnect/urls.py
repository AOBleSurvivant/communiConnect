from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return JsonResponse({
        'message': 'CommuniConnect API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health/',
            'docs': '/api/docs/',
            'admin': '/admin/',
            'posts': '/api/posts/',
            'users': '/api/users/'
        }
    })

def test_api(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'API test endpoint working',
        'timestamp': '2025-01-19'
    })

urlpatterns = [
    path('', home, name='home'),
    path('test/', test_api, name='test'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Demandes d'aide - Correction de l'URL pour éviter le double préfixe
    path('api/help-requests/', include('help_requests.urls')),
    
    # Documentation API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Frontend React - Catch all route
    path('app/', TemplateView.as_view(template_name='index.html'), name='react-app'),
    path('app/<path:path>', TemplateView.as_view(template_name='index.html'), name='react-app-catch-all'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
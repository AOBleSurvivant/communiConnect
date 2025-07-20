from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
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
    
    # Documentation API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
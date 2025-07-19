import requests
import json
import time
import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import GeographicVerification

logger = logging.getLogger(__name__)

class GeographicAccessMiddleware(MiddlewareMixin):
    """
    Middleware pour vérifier l'accès géographique
    Bloque l'accès aux utilisateurs hors de la Guinée
    """
    
    def process_request(self, request):
        # URLs exemptées de la vérification géographique
        exempt_urls = [
            '/admin/',
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/geography/',
            '/api/health/',
        ]
        
        # Vérifier si l'URL est exemptée
        for exempt_url in exempt_urls:
            if request.path.startswith(exempt_url):
                return None
        
        # Obtenir l'adresse IP du client
        ip_address = self.get_client_ip(request)
        
        # Vérifier si l'IP est en Guinée
        is_guinea = self.check_if_guinea(ip_address)
        
        # Si pas en Guinée, bloquer l'accès
        if not is_guinea:
            return JsonResponse({
                'error': 'Accès refusé',
                'message': 'CommuniConnect est réservé aux résidents de la Guinée.',
                'code': 'GEOGRAPHIC_RESTRICTION'
            }, status=403)
        
        # Si l'utilisateur est connecté, enregistrer la vérification
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.record_verification(request.user, ip_address, is_guinea, 'ip')
        
        return None
    
    def get_client_ip(self, request):
        """Obtenir l'adresse IP réelle du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_if_guinea(self, ip_address):
        """
        Vérifier si l'adresse IP est en Guinée
        Utilise un service de géolocalisation IP
        """
        try:
            # Utiliser un service gratuit de géolocalisation IP
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                country_code = data.get('countryCode', '')
                return country_code == settings.GUINEA_COUNTRY_CODE
        except Exception as e:
            # En cas d'erreur, permettre l'accès mais logger
            print(f"Erreur de géolocalisation IP: {e}")
            return True  # Permettre l'accès par défaut
        
        return False
    
    def record_verification(self, user, ip_address, is_guinea, method):
        """Enregistrer la vérification géographique"""
        try:
            # Obtenir les informations de géolocalisation
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                GeographicVerification.objects.create(
                    user=user,
                    ip_address=ip_address,
                    country_code=data.get('countryCode', ''),
                    country_name=data.get('country', ''),
                    city=data.get('city', ''),
                    latitude=data.get('lat'),
                    longitude=data.get('lon'),
                    is_guinea=is_guinea,
                    verification_method=method
                )
                
                # Mettre à jour le statut de l'utilisateur
                if is_guinea:
                    user.is_geographically_verified = True
                    user.last_login_ip = ip_address
                    user.save(update_fields=['is_geographically_verified', 'last_login_ip'])
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de la vérification: {e}")


class GuineaOnlyMiddleware(MiddlewareMixin):
    """
    Middleware pour restreindre l'accès aux utilisateurs vérifiés de Guinée
    """
    
    def process_request(self, request):
        # URLs qui nécessitent une vérification géographique
        protected_urls = [
            '/api/posts/',
            '/api/community/',
            '/api/messages/',
        ]
        
        # Vérifier si l'URL nécessite une protection
        requires_protection = any(request.path.startswith(url) for url in protected_urls)
        
        if requires_protection and hasattr(request, 'user'):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentification requise',
                    'message': 'Vous devez être connecté pour accéder à cette ressource.',
                    'code': 'AUTHENTICATION_REQUIRED'
                }, status=401)
            
            if not request.user.can_access_guinea_only():
                return JsonResponse({
                    'error': 'Vérification géographique requise',
                    'message': 'Votre localisation doit être vérifiée pour accéder à cette ressource.',
                    'code': 'GEOGRAPHIC_VERIFICATION_REQUIRED'
                }, status=403)
        
        return None 


class PerformanceMiddleware(MiddlewareMixin):
    """Middleware pour optimiser les performances et le monitoring"""
    
    def process_request(self, request):
        """Mesure le temps de traitement de la requête"""
        request.start_time = time.time()
        
        # Cache des en-têtes de performance
        request.performance_headers = {
            'X-Request-ID': f"req_{int(time.time() * 1000)}",
            'X-Start-Time': str(request.start_time)
        }
        
        # Vérification du cache pour les requêtes GET
        if request.method == 'GET' and not request.path.startswith('/admin/'):
            cache_key = self._get_cache_key(request)
            cached_response = cache.get(cache_key)
            
            if cached_response:
                logger.info(f"Cache hit pour {request.path}")
                return JsonResponse(cached_response, status=200)
        
        return None
    
    def process_response(self, request, response):
        """Ajoute les en-têtes de performance et met en cache si nécessaire"""
        if hasattr(request, 'start_time'):
            # Calcul du temps de traitement
            processing_time = time.time() - request.start_time
            
            # Ajout des en-têtes de performance
            response['X-Processing-Time'] = f"{processing_time:.3f}s"
            response['X-Request-ID'] = getattr(request, 'performance_headers', {}).get('X-Request-ID', '')
            
            # Cache des réponses JSON pour les requêtes GET
            if (request.method == 'GET' and 
                response.status_code == 200 and 
                response.get('Content-Type', '').startswith('application/json') and
                not request.path.startswith('/admin/')):
                
                cache_key = self._get_cache_key(request)
                cache_timeout = self._get_cache_timeout(request.path)
                
                try:
                    # Mettre en cache la réponse JSON
                    if hasattr(response, 'content'):
                        import json
                        response_data = json.loads(response.content.decode())
                        cache.set(cache_key, response_data, cache_timeout)
                        logger.info(f"Réponse mise en cache: {request.path}")
                except Exception as e:
                    logger.warning(f"Erreur lors de la mise en cache: {str(e)}")
            
            # Log des performances lentes
            if processing_time > 1.0:  # Plus d'1 seconde
                logger.warning(f"Requête lente: {request.path} - {processing_time:.3f}s")
        
        return response
    
    def _get_cache_key(self, request):
        """Génère une clé de cache unique pour la requête"""
        # Inclure l'utilisateur dans la clé si authentifié
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        
        # Inclure les paramètres de requête importants
        params = []
        for key in ['page', 'type', 'sort', 'search']:
            if key in request.GET:
                params.append(f"{key}={request.GET[key]}")
        
        param_string = "&".join(params) if params else "no_params"
        
        return f"response_cache:{user_id}:{request.path}:{param_string}"
    
    def _get_cache_timeout(self, path):
        """Détermine le timeout de cache selon le type de contenu"""
        if '/posts/' in path:
            return settings.CACHE_TIMEOUTS.get('posts_list', 300)
        elif '/users/profile/' in path:
            return settings.CACHE_TIMEOUTS.get('user_profile', 600)
        elif '/media/' in path:
            return settings.CACHE_TIMEOUTS.get('media_list', 1800)
        else:
            return 300  # 5 minutes par défaut


class DatabaseOptimizationMiddleware(MiddlewareMixin):
    """Middleware pour optimiser les requêtes de base de données"""
    
    def process_request(self, request):
        """Prépare les optimisations de base de données"""
        # Marquer le début de la requête pour le monitoring
        request.db_query_count = 0
        request.db_query_time = 0
        
        return None
    
    def process_response(self, request, response):
        """Analyse et optimise les performances de base de données"""
        if hasattr(request, 'db_query_count') and request.db_query_count > 10:
            logger.warning(f"Nombre élevé de requêtes DB: {request.db_query_count} pour {request.path}")
        
        if hasattr(request, 'db_query_time') and request.db_query_time > 0.5:
            logger.warning(f"Temps DB élevé: {request.db_query_time:.3f}s pour {request.path}")
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware pour ajouter les en-têtes de sécurité"""
    
    def process_response(self, request, response):
        """Ajoute les en-têtes de sécurité"""
        # En-têtes de sécurité
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # En-têtes de performance
        response['Vary'] = 'Accept-Encoding'
        
        # En-têtes de cache pour les ressources statiques
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 an
        
        return response 
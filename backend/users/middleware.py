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


class SecurityMiddleware(MiddlewareMixin):
    """Middleware de sécurité renforcée"""
    
    def process_request(self, request):
        # Rate limiting par IP
        client_ip = self.get_client_ip(request)
        rate_limit_key = f"rate_limit_{client_ip}"
        
        # Vérifier le rate limiting
        if not self.check_rate_limit(rate_limit_key):
            return JsonResponse(
                {'error': 'Trop de requêtes. Veuillez patienter.'},
                status=429
            )
        
        # Headers de sécurité
        request.META['HTTP_X_FRAME_OPTIONS'] = 'DENY'
        request.META['HTTP_X_CONTENT_TYPE_OPTIONS'] = 'nosniff'
        request.META['HTTP_X_XSS_PROTECTION'] = '1; mode=block'
        
        return None
    
    def process_response(self, request, response):
        # Headers de sécurité dans la réponse
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        
        return response
    
    def get_client_ip(self, request):
        """Récupère l'IP réelle du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, key, max_requests=100, window=60):
        """Vérifie le rate limiting"""
        current_time = int(time.time())
        window_start = current_time - window
        
        # Récupérer les requêtes récentes
        requests = cache.get(key, [])
        
        # Filtrer les requêtes dans la fenêtre
        recent_requests = [req for req in requests if req > window_start]
        
        # Vérifier la limite
        if len(recent_requests) >= max_requests:
            return False
        
        # Ajouter la requête actuelle
        recent_requests.append(current_time)
        cache.set(key, recent_requests, window)
        
        return True

class PerformanceMiddleware(MiddlewareMixin):
    """Middleware pour le monitoring des performances"""
    
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Logger les requêtes lentes
            if duration > 1.0:  # Plus d'1 seconde
                logger.warning(f"Requête lente: {request.path} - {duration:.2f}s")
            
            # Ajouter le header de durée
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response


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
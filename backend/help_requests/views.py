from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Min
from django.utils import timezone
from datetime import timedelta
import math

from .models import HelpRequest, HelpResponse, HelpRequestCategory
from .serializers import (
    HelpRequestSerializer, HelpRequestListSerializer, HelpRequestMapSerializer,
    HelpResponseSerializer, HelpRequestStatsSerializer, HelpRequestFilterSerializer,
    HelpRequestCategorySerializer
)
from .permissions import IsOwnerOrReadOnly


class HelpRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les demandes d'aide avec géolocalisation
    Inspiré de Nextdoor - Différent des alertes d'urgence
    """
    
    queryset = HelpRequest.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request_type', 'need_type', 'status', 'is_urgent', 'city', 'neighborhood', 'duration_type', 'proximity_zone']
    search_fields = ['title', 'description', 'address', 'neighborhood', 'city']
    ordering_fields = ['created_at', 'updated_at', 'responses_count', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Retourne le sérialiseur approprié selon l'action"""
        if self.action == 'list':
            return HelpRequestListSerializer
        elif self.action == 'map_data':
            return HelpRequestMapSerializer
        elif self.action == 'stats':
            return HelpRequestStatsSerializer
        return HelpRequestSerializer
    
    def get_queryset(self):
        """Filtre le queryset selon les paramètres"""
        queryset = super().get_queryset()
        
        # Filtres personnalisés
        request_type = self.request.query_params.get('request_type')
        need_type = self.request.query_params.get('need_type')
        status_filter = self.request.query_params.get('status')
        duration_type = self.request.query_params.get('duration_type')
        proximity_zone = self.request.query_params.get('proximity_zone')
        is_urgent = self.request.query_params.get('is_urgent')
        city = self.request.query_params.get('city')
        neighborhood = self.request.query_params.get('neighborhood')
        radius = self.request.query_params.get('radius')
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        search = self.request.query_params.get('search')
        
        # Filtre par type de demande
        if request_type:
            queryset = queryset.filter(request_type=request_type)
        
        # Filtre par type de besoin
        if need_type:
            queryset = queryset.filter(need_type=need_type)
        
        # Filtre par statut
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtre par durée
        if duration_type:
            queryset = queryset.filter(duration_type=duration_type)
        
        # Filtre par zone de proximité
        if proximity_zone:
            queryset = queryset.filter(proximity_zone=proximity_zone)
        
        # Filtre par urgence
        if is_urgent is not None:
            is_urgent_bool = is_urgent.lower() == 'true'
            queryset = queryset.filter(is_urgent=is_urgent_bool)
        
        # Filtre par ville
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filtre par quartier
        if neighborhood:
            queryset = queryset.filter(neighborhood__icontains=neighborhood)
        
        # Filtre par rayon géographique
        if radius and latitude and longitude:
            try:
                radius_km = float(radius)
                lat = float(latitude)
                lng = float(longitude)
                
                # Calcul approximatif du rayon en degrés
                # 1 degré ≈ 111 km à l'équateur
                lat_radius = radius_km / 111.0
                lng_radius = radius_km / (111.0 * math.cos(math.radians(lat)))
                
                queryset = queryset.filter(
                    latitude__range=(lat - lat_radius, lat + lat_radius),
                    longitude__range=(lng - lng_radius, lng + lng_radius)
                )
            except (ValueError, TypeError):
                pass
        
        # Filtre par date
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        # Recherche textuelle
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(address__icontains=search) |
                Q(neighborhood__icontains=search) |
                Q(city__icontains=search)
            )
        
        # Exclure les demandes expirées par défaut
        if not self.request.query_params.get('include_expired'):
            queryset = queryset.filter(
                Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Créer une nouvelle demande d'aide"""
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Récupérer une demande d'aide et incrémenter les vues"""
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Répondre à une demande d'aide"""
        help_request = self.get_object()
        serializer = HelpResponseSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(help_request=help_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def accept_response(self, request, pk=None):
        """Accepter une réponse à une demande d'aide"""
        help_request = self.get_object()
        response_id = request.data.get('response_id')
        
        try:
            response = help_request.responses.get(id=response_id)
            response.accept()
            return Response({'status': 'accepted'})
        except HelpResponse.DoesNotExist:
            return Response({'error': 'Réponse non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def reject_response(self, request, pk=None):
        """Rejeter une réponse à une demande d'aide"""
        help_request = self.get_object()
        response_id = request.data.get('response_id')
        
        try:
            response = help_request.responses.get(id=response_id)
            response.reject()
            return Response({'status': 'rejected'})
        except HelpResponse.DoesNotExist:
            return Response({'error': 'Réponse non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Marquer une demande comme terminée"""
        help_request = self.get_object()
        help_request.status = 'completed'
        help_request.save()
        return Response({'status': 'completed'})
    
    @action(detail=True, methods=['post'])
    def mark_cancelled(self, request, pk=None):
        """Marquer une demande comme annulée"""
        help_request = self.get_object()
        help_request.status = 'cancelled'
        help_request.save()
        return Response({'status': 'cancelled'})
    
    @action(detail=False, methods=['get'])
    def map_data(self, request):
        """Récupérer les données pour l'affichage sur la carte"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Récupère les statistiques des demandes d'aide"""
        queryset = self.get_queryset()
        
        # Statistiques de base
        total_requests = queryset.filter(request_type='request').count()
        total_offers = queryset.filter(request_type='offer').count()
        active_requests = queryset.filter(status='open').count()
        urgent_requests = queryset.filter(is_urgent=True).count()
        
        # Demandes par type de besoin
        requests_by_need_type = queryset.values('need_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Demandes par ville
        requests_by_city = queryset.values('city').annotate(
            count=Count('id')
        ).filter(city__isnull=False).exclude(city='').order_by('-count')[:10]
        
        # Demandes récentes (24h)
        recent_requests = queryset.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        # Temps de réponse moyen (en heures)
        responses_with_time = queryset.filter(
            responses__isnull=False
        ).annotate(
            first_response_time=Min('responses__created_at')
        ).filter(
            first_response_time__isnull=False
        )
        
        if responses_with_time.exists():
            avg_response_time = responses_with_time.aggregate(
                avg_time=Avg(
                    ExtractHour('first_response_time') - ExtractHour('created_at')
                )
            )['avg_time'] or 0
        else:
            avg_response_time = 0
        
        stats = {
            'total_requests': total_requests,
            'total_offers': total_offers,
            'active_requests': active_requests,
            'urgent_requests': urgent_requests,
            'requests_by_need_type': list(requests_by_need_type),
            'requests_by_city': list(requests_by_city),
            'recent_requests': recent_requests,
            'avg_response_time': avg_response_time,
        }
        
        return Response(stats)

    @action(detail=True, methods=['get'])
    def responses(self, request, pk=None):
        """Récupère les réponses d'une demande d'aide spécifique"""
        try:
            help_request = self.get_object()
            responses = HelpResponse.objects.filter(help_request=help_request).order_by('-created_at')
            
            # Pagination simple
            page = self.paginate_queryset(responses)
            if page is not None:
                serializer = HelpResponseSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = HelpResponseSerializer(responses, many=True)
            return Response({
                'results': serializer.data,
                'count': responses.count()
            })
            
        except HelpRequest.DoesNotExist:
            return Response(
                {'error': 'Demande d\'aide non trouvée'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class HelpResponseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les réponses aux demandes d'aide
    """
    
    queryset = HelpResponse.objects.all()
    serializer_class = HelpResponseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['response_type', 'is_accepted', 'is_rejected']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrer les réponses selon les paramètres"""
        queryset = super().get_queryset()
        
        # Filtrer par demande d'aide si spécifié
        help_request_id = self.request.query_params.get('help_request')
        if help_request_id:
            queryset = queryset.filter(help_request_id=help_request_id)
        
        # Filtrer par auteur si spécifié
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Créer une nouvelle réponse"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accepter une réponse"""
        response = self.get_object()
        response.accept()
        return Response({'status': 'accepted'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeter une réponse"""
        response = self.get_object()
        response.reject()
        return Response({'status': 'rejected'})


class HelpRequestCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories de demandes d'aide
    """
    
    queryset = HelpRequestCategory.objects.filter(is_active=True)
    serializer_class = HelpRequestCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name'] 
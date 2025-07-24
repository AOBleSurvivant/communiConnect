from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, F
from django.utils import timezone
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models.functions import Distance
from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
import json
import logging
from datetime import datetime, timedelta
import math
from rest_framework.exceptions import ValidationError

from .models import (
    Notification, 
    NotificationPreference, 
    CommunityAlert, 
    AlertReport, 
    HelpOffer, 
    AlertNotification,
    AlertStatistics
)
from .serializers import (
    NotificationSerializer, 
    NotificationPreferenceSerializer,
    CommunityAlertSerializer,
    CommunityAlertCreateSerializer,
    CommunityAlertUpdateSerializer,
    CommunityAlertListSerializer,
    CommunityAlertDetailSerializer,
    AlertReportSerializer,
    HelpOfferSerializer,
    AlertNotificationSerializer,
    AlertStatisticsSerializer,
    NearbyAlertsSerializer,
    AlertSearchSerializer
)
from .services import NotificationService

logger = logging.getLogger(__name__)


# ============================================================================
# VUES POUR LES NOTIFICATIONS EXISTANTES
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_count(request):
    """Compter les notifications non lues de l'utilisateur"""
    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return Response({
        'unread_count': unread_count,
        'total_count': Notification.objects.filter(recipient=request.user).count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    """Liste des notifications de l'utilisateur"""
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Filtres
    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    is_read = request.GET.get('is_read')
    if is_read is not None:
        is_read = is_read.lower() == 'true'
        notifications = notifications.filter(is_read=is_read)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    serializer = NotificationSerializer(page_obj, many=True)
    
    return Response({
        'notifications': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Marquer une notification comme lue"""
    try:
        notification = Notification.objects.get(
            id=notification_id, 
            recipient=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).update(is_read=True)
    return Response({'status': 'success'})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def notification_preferences(request):
    """Gérer les préférences de notification"""
    if request.method == 'GET':
        preference, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        serializer = NotificationPreferenceSerializer(preference)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        preference, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        serializer = NotificationPreferenceSerializer(
            preference, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================================
# VUES POUR LES ALERTES COMMUNAUTAIRES
# ============================================================================

class CommunityAlertListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des alertes communautaires"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'city', 'neighborhood']
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['created_at', 'reliability_score', 'help_offers_count']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = CommunityAlert.objects.all()
        
        # Filtres supplémentaires
        urgent_only = self.request.query_params.get('urgent_only', 'false').lower() == 'true'
        if urgent_only:
            urgent_categories = ['fire', 'medical', 'gas_leak', 'security']
            queryset = queryset.filter(category__in=urgent_categories)
        
        reliable_only = self.request.query_params.get('reliable_only', 'false').lower() == 'true'
        if reliable_only:
            queryset = queryset.filter(reliability_score__gte=70.0)
        
        # Filtre par date
        date_from = self.request.query_params.get('date_from')
        if date_from:
            try:
                date_from = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__gte=date_from)
            except ValueError:
                pass
        
        date_to = self.request.query_params.get('date_to')
        if date_to:
            try:
                date_to = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__lte=date_to)
            except ValueError:
                pass
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityAlertCreateSerializer
        return CommunityAlertListSerializer
    
    def perform_create(self, serializer):
        alert = serializer.save()
        
        # Envoyer des notifications aux utilisateurs à proximité
        send_nearby_notifications(alert)
        
        logger.info(f"Nouvelle alerte créée: {alert.alert_id} par {self.request.user.username}")


class CommunityAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour afficher, modifier et supprimer une alerte"""
    queryset = CommunityAlert.objects.all()
    lookup_field = 'alert_id'
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommunityAlertUpdateSerializer
        return CommunityAlertDetailSerializer
    
    def perform_update(self, serializer):
        old_status = self.get_object().status
        alert = serializer.save()
        
        # Si le statut a changé, notifier les utilisateurs
        if old_status != alert.status:
            send_status_update_notifications(alert, old_status)
        
        logger.info(f"Alerte mise à jour: {alert.alert_id} par {self.request.user.username}")


class NearbyAlertsView(APIView):
    """Vue pour récupérer les alertes à proximité"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = NearbyAlertsSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Point de référence (sans GDAL pour l'instant)
            # user_point = Point(data['longitude'], data['latitude'])
            
            # Requête de base
            queryset = CommunityAlert.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
            
            # Filtres
            if data.get('category_filter'):
                queryset = queryset.filter(category=data['category_filter'])
            
            if data.get('urgent_only', False):
                urgent_categories = ['fire', 'medical', 'gas_leak', 'security']
                queryset = queryset.filter(category__in=urgent_categories)
            
            # Calculer la distance et filtrer par rayon
            radius_degrees = data['radius_km'] / 111.0  # Approximation: 1 degré ≈ 111 km
            
            queryset = queryset.filter(
                latitude__range=(
                    data['latitude'] - radius_degrees,
                    data['latitude'] + radius_degrees
                ),
                longitude__range=(
                    data['longitude'] - radius_degrees,
                    data['longitude'] + radius_degrees
                )
            )
            
            # Calculer les distances exactes
            alerts_with_distance = []
            for alert in queryset:
                # alert_point = Point(alert.longitude, alert.latitude)
                # distance_km = user_point.distance(alert_point) * 111.0
                distance_km = calculate_distance(
                    data['latitude'], data['longitude'],
                    alert.latitude, alert.longitude
                )
                
                if distance_km <= data['radius_km']:
                    alert.distance_km = distance_km
                    alerts_with_distance.append(alert)
            
            # Trier par distance
            alerts_with_distance.sort(key=lambda x: x.distance_km)
            
            # Sérialiser
            serializer = CommunityAlertListSerializer(alerts_with_distance, many=True)
            
            return Response({
                'alerts': serializer.data,
                'count': len(alerts_with_distance),
                'radius_km': data['radius_km'],
                'user_location': {
                    'latitude': data['latitude'],
                    'longitude': data['longitude']
                }
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertSearchView(APIView):
    """Vue pour rechercher des alertes"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        serializer = AlertSearchSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            queryset = CommunityAlert.objects.all()
            
            # Recherche textuelle
            if data.get('query'):
                query = data['query']
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(address__icontains=query) |
                    Q(neighborhood__icontains=query) |
                    Q(city__icontains=query)
                )
            
            # Filtres
            if data.get('category'):
                queryset = queryset.filter(category=data['category'])
            
            if data.get('status'):
                queryset = queryset.filter(status=data['status'])
            
            if data.get('city'):
                queryset = queryset.filter(city__icontains=data['city'])
            
            if data.get('neighborhood'):
                queryset = queryset.filter(neighborhood__icontains=data['neighborhood'])
            
            if data.get('date_from'):
                queryset = queryset.filter(created_at__gte=data['date_from'])
            
            if data.get('date_to'):
                queryset = queryset.filter(created_at__lte=data['date_to'])
            
            if data.get('urgent_only', False):
                urgent_categories = ['fire', 'medical', 'gas_leak', 'security']
                queryset = queryset.filter(category__in=urgent_categories)
            
            if data.get('reliable_only', False):
                queryset = queryset.filter(reliability_score__gte=70.0)
            
            # Pagination
            page = data.get('page', 1)
            page_size = data.get('page_size', 20)
            
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = CommunityAlertListSerializer(page_obj, many=True)
            
            return Response({
                'alerts': serializer.data,
                'total_count': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertReportView(generics.CreateAPIView):
    """Vue pour signaler une alerte"""
    serializer_class = AlertReportSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Récupérer l'alerte à partir de l'ID dans l'URL
        alert_id = self.kwargs.get('alert_id')
        try:
            alert = CommunityAlert.objects.get(alert_id=alert_id)
            
            # Vérifier si l'utilisateur a déjà rapporté cette alerte
            existing_report = AlertReport.objects.filter(
                alert=alert,
                reporter=self.request.user
            ).first()
            
            if existing_report:
                # Mettre à jour le rapport existant
                existing_report.report_type = serializer.validated_data.get('report_type', existing_report.report_type)
                existing_report.reason = serializer.validated_data.get('reason', existing_report.reason)
                existing_report.save()
                report = existing_report
            else:
                # Créer un nouveau rapport
                report = serializer.save(alert=alert)
            
            logger.info(f"Rapport d'alerte créé/mis à jour: {report.id} par {self.request.user.username}")
        except CommunityAlert.DoesNotExist:
            raise ValidationError("Alerte non trouvée")


class HelpOfferView(generics.ListCreateAPIView):
    """Vue pour gérer les offres d'aide"""
    serializer_class = HelpOfferSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        alert_id = self.kwargs.get('alert_id')
        return HelpOffer.objects.filter(alert__alert_id=alert_id)
    
    def perform_create(self, serializer):
        # Récupérer l'alerte à partir de l'ID dans l'URL
        alert_id = self.kwargs.get('alert_id')
        try:
            alert = CommunityAlert.objects.get(alert_id=alert_id)
            
            # Vérifier si l'utilisateur a déjà offert son aide
            existing_offer = HelpOffer.objects.filter(
                alert=alert,
                helper=self.request.user
            ).first()
            
            if existing_offer:
                # Mettre à jour l'offre existante
                existing_offer.description = serializer.validated_data.get('description', existing_offer.description)
                existing_offer.offer_type = serializer.validated_data.get('offer_type', existing_offer.offer_type)
                existing_offer.contact_info = serializer.validated_data.get('contact_info', existing_offer.contact_info)
                existing_offer.is_active = True
                existing_offer.save()
                help_offer = existing_offer
            else:
                # Créer une nouvelle offre
                help_offer = serializer.save(alert=alert)
            
            logger.info(f"Offre d'aide créée/mise à jour: {help_offer.id} par {self.request.user.username}")
        except CommunityAlert.DoesNotExist:
            raise ValidationError("Alerte non trouvée")


class AlertStatisticsView(APIView):
    """Vue pour les statistiques d'alertes"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Période par défaut: 30 derniers jours
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Paramètres de requête
        period = request.GET.get('period', 'monthly')
        if period == 'weekly':
            start_date = end_date - timedelta(weeks=1)
        elif period == 'daily':
            start_date = end_date - timedelta(days=1)
        elif period == 'yearly':
            start_date = end_date - timedelta(days=365)
        
        # Statistiques de base
        alerts = CommunityAlert.objects.filter(
            created_at__range=[start_date, end_date]
        )
        
        stats = {
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_alerts': alerts.count(),
            'resolved_alerts': alerts.filter(status='resolved').count(),
            'false_alarms': alerts.filter(status='false_alarm').count(),
            'avg_reliability_score': alerts.aggregate(Avg('reliability_score'))['reliability_score__avg'] or 0,
            'reliable_alerts_count': alerts.filter(reliability_score__gte=70.0).count(),
        }
        
        # Statistiques par catégorie
        category_stats = {}
        for category, label in CommunityAlert.ALERT_CATEGORIES:
            count = alerts.filter(category=category).count()
            if count > 0:
                category_stats[category] = {
                    'label': label,
                    'count': count,
                    'percentage': (count / stats['total_alerts']) * 100 if stats['total_alerts'] > 0 else 0
                }
        
        stats['category_stats'] = category_stats
        
        # Statistiques géographiques
        city_stats = alerts.values('city').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        neighborhood_stats = alerts.values('neighborhood').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        stats['city_stats'] = list(city_stats)
        stats['neighborhood_stats'] = list(neighborhood_stats)
        
        # Temps de résolution moyen
        resolved_alerts = alerts.filter(
            status='resolved',
            resolved_at__isnull=False
        )
        
        if resolved_alerts.exists():
            avg_resolution_time = resolved_alerts.aggregate(
                avg_time=Avg(F('resolved_at') - F('created_at'))
            )['avg_time']
            stats['avg_resolution_time_hours'] = avg_resolution_time.total_seconds() / 3600 if avg_resolution_time else 0
        else:
            stats['avg_resolution_time_hours'] = 0
        
        return Response(stats)


# ============================================================================
# NOUVEAUX ENDPOINTS POUR AMÉLIORATIONS
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_alert_category(request):
    """Endpoint pour la suggestion de catégorie IA"""
    try:
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        
        if not title and not description:
            return Response(
                {'error': 'Titre ou description requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Analyse simple basée sur les mots-clés
        content = f"{title} {description}".lower()
        
        # Mots-clés par catégorie
        keywords = {
            'fire': ['incendie', 'feu', 'brûle', 'flamme', 'smoke'],
            'power_outage': ['électricité', 'coupure', 'panne', 'blackout', 'électrique'],
            'road_blocked': ['route', 'bloquée', 'obstacle', 'accident', 'trafic'],
            'security': ['agression', 'vol', 'sécurité', 'danger', 'menace'],
            'medical': ['médical', 'urgence', 'ambulance', 'hôpital', 'maladie'],
            'flood': ['inondation', 'eau', 'pluie', 'débordement', 'noyade'],
            'gas_leak': ['gaz', 'fuite', 'odeur', 'explosion', 'propane'],
            'noise': ['bruit', 'son', 'musique', 'voix', 'nuisance'],
            'vandalism': ['vandalisme', 'dégradation', 'graffiti', 'destruction'],
        }
        
        # Calculer le score pour chaque catégorie
        scores = {}
        for category, words in keywords.items():
            score = sum(1 for word in words if word in content)
            if score > 0:
                scores[category] = score
        
        # Trouver la catégorie avec le score le plus élevé
        suggested_category = 'other'  # Par défaut
        if scores:
            suggested_category = max(scores, key=scores.get)
        
        # Calculer la confiance
        total_matches = sum(scores.values())
        confidence = (scores.get(suggested_category, 0) / max(total_matches, 1)) * 100
        
        return Response({
            'suggested_category': suggested_category,
            'confidence': round(confidence, 2),
            'category_display': dict(CommunityAlert.ALERT_CATEGORIES).get(suggested_category, 'Autre'),
            'alternative_categories': [
                {'category': cat, 'score': score} 
                for cat, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
            ]
        })
        
    except Exception as e:
        logger.error(f"Erreur suggestion catégorie: {e}")
        return Response(
            {'error': 'Erreur lors de la suggestion de catégorie'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comprehensive_analytics_report(request):
    """Endpoint pour le rapport complet d'analytics"""
    try:
        # Période par défaut: 30 derniers jours
        days = int(request.GET.get('days', 30))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Statistiques globales
        total_alerts = CommunityAlert.objects.filter(created_at__range=(start_date, end_date)).count()
        urgent_alerts = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date),
            category__in=['fire', 'medical', 'security', 'gas_leak']
        ).count()
        
        # Statistiques par catégorie
        category_stats = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('category').annotate(
            count=Count('id'),
            avg_reliability=Avg('reliability_score'),
            resolved_count=Count('id', filter=Q(status='resolved')),
            false_alarm_count=Count('id', filter=Q(status='false_alarm'))
        ).order_by('-count')
        
        # Statistiques par statut
        status_stats = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Tendances temporelles (par jour)
        daily_trends = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date)
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id'),
            urgent_count=Count('id', filter=Q(category__in=['fire', 'medical', 'security', 'gas_leak']))
        ).order_by('day')
        
        # Top utilisateurs fiables
        from django.contrib.auth import get_user_model
        User = get_user_model()
        reliable_users = User.objects.filter(
            authored_alerts__created_at__range=(start_date, end_date)
        ).annotate(
            alert_count=Count('authored_alerts'),
            avg_reliability=Avg('authored_alerts__reliability_score')
        ).filter(
            alert_count__gte=3,
            avg_reliability__gte=70
        ).order_by('-avg_reliability')[:10]
        
        # Zones les plus actives
        active_zones = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date)
        ).exclude(
            neighborhood=''
        ).values('neighborhood').annotate(
            alert_count=Count('id'),
            urgent_count=Count('id', filter=Q(category__in=['fire', 'medical', 'security', 'gas_leak']))
        ).order_by('-alert_count')[:10]
        
        # Métriques de performance
        avg_resolution_time = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date),
            status='resolved',
            resolved_at__isnull=False
        ).aggregate(
            avg_time=Avg(F('resolved_at') - F('created_at'))
        )['avg_time']
        
        # Calculer le taux de résolution
        resolved_count = CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date),
            status='resolved'
        ).count()
        
        resolution_rate = (resolved_count / max(total_alerts, 1)) * 100
        
        # Calculer le taux de fausses alertes
        false_alarm_rate = (CommunityAlert.objects.filter(
            created_at__range=(start_date, end_date),
            status='false_alarm'
        ).count() / max(total_alerts, 1)) * 100
        
        return Response({
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'overview': {
                'total_alerts': total_alerts,
                'urgent_alerts': urgent_alerts,
                'urgent_percentage': round((urgent_alerts / max(total_alerts, 1)) * 100, 2),
                'avg_resolution_time_hours': round(avg_resolution_time.total_seconds() / 3600, 2) if avg_resolution_time else 0,
                'resolution_rate': round(resolution_rate, 2),
                'false_alarm_rate': round(false_alarm_rate, 2)
            },
            'category_analysis': list(category_stats),
            'status_analysis': list(status_stats),
            'daily_trends': list(daily_trends),
            'reliable_users': [
                {
                    'user_id': user.id,
                    'username': user.username,
                    'alert_count': user.alert_count,
                    'avg_reliability': round(user.avg_reliability, 2)
                }
                for user in reliable_users
            ],
            'active_zones': list(active_zones),
            'insights': {
                'most_active_category': category_stats[0]['category'] if category_stats else None,
                'most_common_status': status_stats[0]['status'] if status_stats else None,
                'trend': 'increasing' if len(daily_trends) > 1 and daily_trends[-1]['count'] > daily_trends[0]['count'] else 'stable',
                'recommendations': [
                    'Augmenter la surveillance dans les zones les plus actives',
                    'Former les utilisateurs sur la détection de fausses alertes',
                    'Optimiser les temps de réponse pour les alertes urgentes'
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur rapport analytics: {e}")
        return Response(
            {'error': 'Erreur lors de la génération du rapport'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================================================
# MÉTHODES UTILITAIRES
# ============================================================================

def send_nearby_notifications(alert):
    """Envoyer des notifications aux utilisateurs à proximité"""
    if not alert.latitude or not alert.longitude:
        return
    
    # Pour l'instant, on va simplement logger l'alerte créée
    # La fonctionnalité de notification géolocalisée sera implémentée plus tard
    logger.info(f"Alerte créée avec succès: {alert.alert_id} - {alert.title}")
    logger.info(f"Position: {alert.latitude}, {alert.longitude}")
    logger.info(f"Catégorie: {alert.category}")
    
    # TODO: Implémenter la logique de notification géolocalisée
    # - Trouver les utilisateurs dans un rayon de 5km
    # - Créer des notifications pour ces utilisateurs
    # - Envoyer les notifications
    
    # Pour l'instant, on ne fait rien de plus
    pass


def send_status_update_notifications(alert, old_status):
    """Envoyer des notifications de mise à jour de statut"""
    # Notifier l'auteur et les personnes qui ont offert leur aide
    recipients = [alert.author]
    recipients.extend(alert.help_offers.all())
    
    notifications = []
    for user in set(recipients):
        if user.notification_preferences.community_alert_notifications:
            notification = AlertNotification(
                alert=alert,
                recipient=user,
                notification_type='status_update',
                title=f"Statut de l'alerte mis à jour: {alert.get_status_display()}",
                message=f"L'alerte '{alert.title}' est maintenant {alert.get_status_display().lower()}",
                extra_data={'old_status': old_status, 'new_status': alert.status}
            )
            notifications.append(notification)
    
    AlertNotification.objects.bulk_create(notifications)


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculer la distance entre deux points géographiques (formule de Haversine)"""
    R = 6371  # Rayon de la Terre en km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c 
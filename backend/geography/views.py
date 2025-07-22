from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Region, Prefecture, Commune, Quartier
from .serializers import (
    RegionSerializer, 
    PrefectureSerializer, 
    CommuneSerializer, 
    QuartierSerializer
)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les régions de Guinée"""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    @action(detail=True, methods=['get'])
    def prefectures(self, request, pk=None):
        """Récupérer les préfectures d'une région"""
        region = get_object_or_404(Region, pk=pk)
        prefectures = region.prefectures.all()
        serializer = PrefectureSerializer(prefectures, many=True)
        return Response(serializer.data)


class PrefectureViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les préfectures de Guinée"""
    queryset = Prefecture.objects.all()
    serializer_class = PrefectureSerializer

    @action(detail=True, methods=['get'])
    def communes(self, request, pk=None):
        """Récupérer les communes d'une préfecture"""
        prefecture = get_object_or_404(Prefecture, pk=pk)
        communes = prefecture.communes.all()
        serializer = CommuneSerializer(communes, many=True)
        return Response(serializer.data)


class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les communes de Guinée"""
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

    @action(detail=True, methods=['get'])
    def quartiers(self, request, pk=None):
        """Récupérer les quartiers d'une commune"""
        commune = get_object_or_404(Commune, pk=pk)
        quartiers = commune.quartiers.all()
        serializer = QuartierSerializer(quartiers, many=True)
        return Response(serializer.data)


class QuartierViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les quartiers de Guinée"""
    queryset = Quartier.objects.all()
    serializer_class = QuartierSerializer

    @action(detail=True, methods=['get'])
    def full_address(self, request, pk=None):
        """Récupérer l'adresse complète d'un quartier"""
        quartier = get_object_or_404(Quartier, pk=pk)
        return Response({
            'quartier': quartier.nom,
            'commune': quartier.commune.nom,
            'prefecture': quartier.prefecture.nom,
            'region': quartier.region.nom,
            'full_address': quartier.full_address
        })


# Vues pour les formulaires en cascade
def get_prefectures_by_region(request, region_id):
    """Récupérer les préfectures d'une région spécifique"""
    try:
        region = Region.objects.get(id=region_id)
        prefectures = region.prefectures.all()
        serializer = PrefectureSerializer(prefectures, many=True)
        return Response(serializer.data)
    except Region.DoesNotExist:
        return Response(
            {'error': 'Région non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


def get_communes_by_prefecture(request, prefecture_id):
    """Récupérer les communes d'une préfecture spécifique"""
    try:
        prefecture = Prefecture.objects.get(id=prefecture_id)
        communes = prefecture.communes.all()
        serializer = CommuneSerializer(communes, many=True)
        return Response(serializer.data)
    except Prefecture.DoesNotExist:
        return Response(
            {'error': 'Préfecture non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


def get_quartiers_by_commune(request, commune_id):
    """Récupérer les quartiers d'une commune spécifique"""
    try:
        commune = Commune.objects.get(id=commune_id)
        quartiers = commune.quartiers.all()
        serializer = QuartierSerializer(quartiers, many=True)
        return Response(serializer.data)
    except Commune.DoesNotExist:
        return Response(
            {'error': 'Commune non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        ) 
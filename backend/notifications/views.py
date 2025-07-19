from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, 
    NotificationPreferenceSerializer,
    NotificationCountSerializer,
    MarkAsReadSerializer
)
from .services import NotificationService


class NotificationListView(generics.ListAPIView):
    """
    Liste des notifications de l'utilisateur connecté
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user)


class NotificationDetailView(generics.RetrieveAPIView):
    """
    Détails d'une notification
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_count(request):
    """
    Retourne le nombre de notifications non lues
    """
    user = request.user
    unread_count = NotificationService.get_unread_count(user)
    total_count = Notification.objects.filter(recipient=user).count()
    
    data = {
        'unread_count': unread_count,
        'total_count': total_count
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    """
    Marque les notifications comme lues
    """
    serializer = MarkAsReadSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        notification_ids = serializer.validated_data.get('notification_ids', [])
        mark_all = serializer.validated_data.get('mark_all', False)
        
        updated_count = NotificationService.mark_as_read(
            user, 
            notification_ids=notification_ids, 
            mark_all=mark_all
        )
        
        return Response({
            'message': f'{updated_count} notification(s) marquée(s) comme lue(s)',
            'updated_count': updated_count
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def notification_preferences(request):
    """
    Récupère ou met à jour les préférences de notifications
    """
    user = request.user
    
    if request.method == 'GET':
        try:
            preferences = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            preferences = NotificationPreference.objects.create(user=user)
        
        serializer = NotificationPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        try:
            preferences = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            preferences = NotificationPreference.objects.create(user=user)
        
        serializer = NotificationPreferenceSerializer(preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """
    Supprime une notification
    """
    user = request.user
    notification = get_object_or_404(Notification, id=notification_id, recipient=user)
    notification.delete()
    
    return Response({'message': 'Notification supprimée'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_all_notifications(request):
    """
    Supprime toutes les notifications de l'utilisateur
    """
    user = request.user
    count = Notification.objects.filter(recipient=user).count()
    Notification.objects.filter(recipient=user).delete()
    
    return Response({
        'message': f'{count} notification(s) supprimée(s)'
    }, status=status.HTTP_204_NO_CONTENT) 
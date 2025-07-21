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


class NotificationCountView(generics.GenericAPIView):
    """Retourne le nombre de notifications non lues"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationCountSerializer
    
    def get(self, request):
        user = request.user
        unread_count = NotificationService.get_unread_count(user)
        total_count = Notification.objects.filter(recipient=user).count()
        
        data = {
            'unread_count': unread_count,
            'total_count': total_count
        }
        
        return Response(data)


class MarkAsReadView(generics.GenericAPIView):
    """Marque les notifications comme lues"""
    serializer_class = MarkAsReadSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
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


class NotificationPreferencesView(generics.GenericAPIView):
    """Vue pour les préférences de notifications"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer
    
    def get(self, request):
        """Récupère les préférences de notifications"""
        user = request.user
        
        try:
            preferences = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            preferences = NotificationPreference.objects.create(user=user)
        
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        """Met à jour les préférences de notifications"""
        user = request.user
        
        try:
            preferences = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            preferences = NotificationPreference.objects.create(user=user)
        
        serializer = self.get_serializer(preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotificationView(generics.DestroyAPIView):
    """Supprime une notification"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.delete()
        return Response({'message': 'Notification supprimée'}, status=status.HTTP_204_NO_CONTENT)


class ClearAllNotificationsView(generics.GenericAPIView):
    """Supprime toutes les notifications de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationCountSerializer
    
    def delete(self, request):
        user = request.user
        count = Notification.objects.filter(recipient=user).count()
        Notification.objects.filter(recipient=user).delete()
        
        return Response({
            'message': f'{count} notification(s) supprimée(s)'
        }, status=status.HTTP_204_NO_CONTENT) 
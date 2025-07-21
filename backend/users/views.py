from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
import os
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import User, UserProfile, GeographicVerification, UserRelationship
from geography.models import Region, Prefecture, Commune, Quartier
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserProfileSerializer,
    UserRelationshipSerializer, FollowUserSerializer, UnfollowUserSerializer,
    UserSearchSerializer, SuggestedFriendsSerializer, UserStatsSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs avec vérification géographique"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Vérification géographique
            is_guinea = self.verify_geographic_access(request)
            
            if not is_guinea:
                return Response({
                    'error': 'Accès refusé. CommuniConnect est réservé aux habitants de Guinée.',
                    'code': 'GEOGRAPHIC_RESTRICTION'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Création de l'utilisateur
            user = serializer.save()
            
            # Création du profil utilisateur
            UserProfile.objects.create(user=user)
            
            # Génération des tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Inscription réussie !'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_geographic_access(self, request):
        """Vérifie si l'utilisateur est en Guinée"""
        try:
            # Récupération de l'adresse IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Vérification avec GeoIP2 (si disponible)
            try:
                # Chemin vers la base de données GeoIP2 (à configurer)
                geoip_path = os.path.join(os.path.dirname(__file__), '..', '..', 'GeoLite2-Country.mmdb')
                if os.path.exists(geoip_path):
                    reader = Reader(geoip_path)
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    return country_code == 'GN'
                else:
                    # Fallback: vérification basée sur les données de l'utilisateur
                    quartier_id = request.data.get('quartier')
                    if quartier_id:
                        try:
                            quartier = Quartier.objects.get(id=quartier_id)
                            return True  # Si l'utilisateur a sélectionné un quartier valide
                        except Quartier.DoesNotExist:
                            return False
                    return True  # Par défaut, autoriser si pas de vérification IP
            except AddressNotFoundError:
                return True  # Autoriser si l'IP n'est pas trouvée
                
        except Exception as e:
            print(f"Erreur lors de la vérification géographique: {e}")
            return True  # En cas d'erreur, autoriser par défaut


class UserLoginView(generics.GenericAPIView):
    """Vue pour la connexion des utilisateurs"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email et mot de passe requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentification - essayer d'abord avec l'email, puis avec le username
        user = None
        try:
            # Essayer de trouver l'utilisateur par email
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            # Si pas trouvé par email, essayer avec le username
            user = authenticate(username=email, password=password)
        
        if user is None:
            return Response({
                'error': 'Email ou mot de passe incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': 'Compte désactivé'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Vérification géographique
        is_guinea = self.verify_geographic_access(request)
        if not is_guinea:
            return Response({
                'error': 'Accès refusé. Vous devez être en Guinée pour vous connecter.',
                'code': 'GEOGRAPHIC_RESTRICTION'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Génération des tokens
        refresh = RefreshToken.for_user(user)
        
        # Mise à jour de la dernière connexion
        user.last_login = timezone.now()
        user.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Connexion réussie !'
        })

    def verify_geographic_access(self, request):
        """Vérifie si l'utilisateur est en Guinée"""
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Vérification avec GeoIP2
            geoip_path = os.path.join(os.path.dirname(__file__), '..', '..', 'GeoLite2-Country.mmdb')
            if os.path.exists(geoip_path):
                reader = Reader(geoip_path)
                response = reader.country(ip)
                country_code = response.country.iso_code
                return country_code == 'GN'
            else:
                return True  # Autoriser si pas de base de données GeoIP
                
        except Exception as e:
            print(f"Erreur lors de la vérification géographique: {e}")
            return True


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour récupérer et mettre à jour le profil utilisateur"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'Profil mis à jour avec succès !'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GeographicDataView(generics.GenericAPIView):
    """Vue pour récupérer les données géographiques"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get(self, request):
        """Récupère la hiérarchie géographique complète"""
        try:
            regions = Region.objects.prefetch_related(
                'prefectures__communes__quartiers'
            ).all()
            
            data = []
            for region in regions:
                region_data = {
                    'id': region.id,
                    'nom': region.nom,
                    'code': region.code,
                    'prefectures': []
                }
                
                for prefecture in region.prefectures.all():
                    prefecture_data = {
                        'id': prefecture.id,
                        'nom': prefecture.nom,
                        'code': prefecture.code,
                        'communes': []
                    }
                    
                    for commune in prefecture.communes.all():
                        commune_data = {
                            'id': commune.id,
                            'nom': commune.nom,
                            'type': commune.type,
                            'code': commune.code,
                            'quartiers': []
                        }
                        
                        for quartier in commune.quartiers.all():
                            quartier_data = {
                                'id': quartier.id,
                                'nom': quartier.nom,
                                'code': quartier.code,
                                'population_estimee': quartier.population_estimee,
                                'superficie_km2': str(quartier.superficie_km2) if quartier.superficie_km2 else None
                            }
                            commune_data['quartiers'].append(quartier_data)
                        
                        prefecture_data['communes'].append(commune_data)
                    
                    region_data['prefectures'].append(prefecture_data)
                
                data.append(region_data)
            
            return Response({
                'regions': data
            })
        except Exception as e:
            return Response({
                'error': f'Erreur lors de la récupération des données géographiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GeographicVerificationView(generics.GenericAPIView):
    """Vue pour la vérification géographique"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        """Effectue une vérification géographique"""
        try:
            # Récupération de l'IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Vérification avec GeoIP2
            country_code = 'GN'  # Par défaut
            country_name = 'Guinée'
            city = None
            latitude = None
            longitude = None
            is_guinea = True
            
            try:
                geoip_path = os.path.join(os.path.dirname(__file__), '..', '..', 'GeoLite2-Country.mmdb')
                if os.path.exists(geoip_path):
                    reader = Reader(geoip_path)
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    country_name = response.country.name
                    is_guinea = country_code == 'GN'
            except Exception as e:
                print(f"Erreur GeoIP: {e}")
            
            # Création de l'enregistrement de vérification
            verification = GeographicVerification.objects.create(
                user=request.user,
                ip_address=ip,
                country_code=country_code,
                country_name=country_name,
                city=city,
                latitude=latitude,
                longitude=longitude,
                is_guinea=is_guinea,
                verification_method='ip'
            )
            
            # Mise à jour du statut utilisateur
            if is_guinea:
                request.user.is_geographically_verified = True
                request.user.save()
        
            return Response({
                'verification': UserSerializer(verification).data,
                'is_guinea': is_guinea,
                'message': 'Vérification géographique effectuée'
            })
        except Exception as e:
            return Response({
                'error': f'Erreur lors de la vérification: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDashboardDataView(generics.GenericAPIView):
    """Vue pour les données du dashboard utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        """Récupère les données pour le tableau de bord utilisateur"""
        try:
            user = request.user
            
            # Statistiques de base (à enrichir selon les besoins)
            stats = {
                'neighbors': User.objects.filter(
                    quartier=user.quartier,
                    is_active=True
                ).exclude(id=user.id).count(),
                'posts': 0,  # À implémenter avec le système de posts
                'events': 0,  # À implémenter avec le système d'événements
                'messages': 0  # À implémenter avec le système de messages
            }
            
            return Response({
                'user': UserSerializer(user).data,
                'stats': stats
            })
            
        except Exception as e:
            return Response({
                'error': f'Erreur lors de la récupération des données: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(generics.GenericAPIView):
    """Vue pour la déconnexion"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def post(self, request):
        """Déconnexion de l'utilisateur"""
        try:
            # Blacklist du token (si configuré)
            # refresh_token = request.data.get('refresh')
            # if refresh_token:
            #     token = RefreshToken(refresh_token)
            #     token.blacklist()
            
            return Response({
                'message': 'Déconnexion réussie'
            })
        except Exception as e:
            return Response({
                'error': f'Erreur lors de la déconnexion: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class UserDetailView(generics.RetrieveAPIView):
    """Vue pour voir le profil d'un autre utilisateur"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    
    def get_queryset(self):
        return User.objects.filter(is_active=True).select_related('quartier')


class UserSearchView(generics.ListAPIView):
    """Vue pour rechercher des utilisateurs"""
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return User.objects.none()
        
        return User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query),
            is_active=True
        ).select_related('quartier')[:20]


class SuggestedFriendsView(generics.ListAPIView):
    """Vue pour les suggestions d'amis"""
    serializer_class = SuggestedFriendsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return user.get_suggested_friends(limit=10)


class FollowUserView(generics.GenericAPIView):
    """Vue pour suivre un utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_to_follow = get_object_or_404(User, id=serializer.validated_data['user_id'])
            
            if request.user == user_to_follow:
                return Response(
                    {"error": "Vous ne pouvez pas vous suivre vous-même."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Vérifier si la relation existe déjà
            relationship, created = UserRelationship.objects.get_or_create(
                follower=request.user,
                followed=user_to_follow,
                defaults={'status': 'accepted'}
            )
            
            if not created:
                if relationship.status == 'blocked':
                    return Response(
                        {"error": "Vous ne pouvez pas suivre cet utilisateur."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif relationship.status == 'accepted':
                    return Response(
                        {"error": "Vous suivez déjà cet utilisateur."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    relationship.status = 'accepted'
                    relationship.save()
            
            # Mettre à jour les statistiques
            if hasattr(request.user, 'profile'):
                request.user.profile.update_connections_count()
            
            return Response(
                {"message": f"Vous suivez maintenant {user_to_follow.username}"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnfollowUserView(generics.GenericAPIView):
    """Vue pour ne plus suivre un utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnfollowUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_to_unfollow = get_object_or_404(User, id=serializer.validated_data['user_id'])
            
            if request.user == user_to_unfollow:
                return Response(
                    {"error": "Vous ne pouvez pas vous unfollow vous-même."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Supprimer la relation
            relationship = UserRelationship.objects.filter(
                    follower=request.user,
                followed=user_to_unfollow,
                status='accepted'
            ).first()
            
            if relationship:
                relationship.delete()
                return Response(
                    {"message": f"Vous ne suivez plus {user_to_unfollow.username}"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Vous ne suivez pas cet utilisateur."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowersListView(generics.ListAPIView):
    """Vue pour lister les followers d'un utilisateur"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return user.followers.filter(status='accepted').select_related('quartier')


class FollowingListView(generics.ListAPIView):
    """Vue pour lister les utilisateurs suivis"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return user.following.filter(status='accepted').select_related('quartier')


class UserStatsView(generics.RetrieveAPIView):
    """Vue pour les statistiques utilisateur"""
    serializer_class = UserStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)


class PendingFriendsView(generics.ListAPIView):
    """Vue pour les demandes d'amitié en attente"""
    serializer_class = UserRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserRelationship.objects.filter(
            followed=self.request.user,
            status='pending'
        ).select_related('follower', 'followed')


class AcceptFriendRequestView(generics.GenericAPIView):
    """Vue pour accepter une demande d'amitié"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRelationshipSerializer
    
    def post(self, request, relationship_id):
        try:
            relationship = UserRelationship.objects.get(
                id=relationship_id,
                followed=request.user,
                status='pending'
            )
            relationship.status = 'accepted'
            relationship.save()
            
            return Response({
                "message": f"Demande d'amitié de {relationship.follower.username} acceptée"
            }, status=status.HTTP_200_OK)
        except UserRelationship.DoesNotExist:
            return Response(
                {"error": "Demande d'amitié introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )


class RejectFriendRequestView(generics.GenericAPIView):
    """Vue pour refuser une demande d'amitié"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRelationshipSerializer
    
    def post(self, request, relationship_id):
        try:
            relationship = UserRelationship.objects.get(
                id=relationship_id,
                followed=request.user,
                status='pending'
            )
            relationship.delete()
            
            return Response({
                "message": f"Demande d'amitié de {relationship.follower.username} refusée"
            }, status=status.HTTP_200_OK)
        except UserRelationship.DoesNotExist:
            return Response(
                {"error": "Demande d'amitié introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )


class BlockUserView(generics.GenericAPIView):
    """Vue pour bloquer un utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_to_block = get_object_or_404(User, id=serializer.validated_data['user_id'])
            
            if request.user == user_to_block:
                return Response(
                    {"error": "Vous ne pouvez pas vous bloquer vous-même."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            relationship, created = UserRelationship.objects.get_or_create(
                follower=request.user,
                followed=user_to_block,
                defaults={'status': 'blocked'}
            )
            
            if not created:
                relationship.status = 'blocked'
                relationship.save()
            
            return Response(
                {"message": f"Vous avez bloqué {user_to_block.username}"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnblockUserView(generics.GenericAPIView):
    """Vue pour débloquer un utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnfollowUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_to_unblock = get_object_or_404(User, id=serializer.validated_data['user_id'])
            
            try:
                relationship = UserRelationship.objects.get(
                    follower=request.user,
                    followed=user_to_unblock,
                    status='blocked'
                )
                relationship.delete()
                
                return Response(
                    {"message": f"Vous avez débloqué {user_to_unblock.username}"},
                    status=status.HTTP_200_OK
                )
            except UserRelationship.DoesNotExist:
                return Response(
                    {"error": "Cet utilisateur n'est pas bloqué."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRelationshipsStatusView(generics.GenericAPIView):
    """Vue pour le statut des relations utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, user_id):
        """Vue pour obtenir le statut de relation avec un utilisateur"""
        try:
            target_user = User.objects.get(id=user_id)
            
            # Vérifier si l'utilisateur connecté suit l'utilisateur cible
            is_following = request.user.is_following(target_user)
            
            # Vérifier si l'utilisateur cible suit l'utilisateur connecté
            is_followed_by = target_user.is_following(request.user)
            
            # Vérifier si l'un des deux a bloqué l'autre
            blocked_by_me = UserRelationship.objects.filter(
                follower=request.user,
                followed=target_user,
                status='blocked'
            ).exists()
            
            blocked_by_other = UserRelationship.objects.filter(
                follower=target_user,
                followed=request.user,
                status='blocked'
            ).exists()
            
            return Response({
                'is_following': is_following,
                'is_followed_by': is_followed_by,
                'blocked_by_me': blocked_by_me,
                'blocked_by_other': blocked_by_other,
                'can_interact': not (blocked_by_me or blocked_by_other)
            })
            
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable."},
                status=status.HTTP_404_NOT_FOUND
            ) 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import User, UserProfile, GeographicVerification, UserRelationship, CommunityGroup, GroupMembership, CommunityEvent, EventAttendance, UserAchievement, UserSocialScore
from django.shortcuts import get_object_or_404

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    full_name = serializers.SerializerMethodField()
    location_info = serializers.SerializerMethodField()
    is_ambassador = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    can_follow = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'bio', 'profile_picture',
            'quartier', 'role', 'is_verified', 'is_geographically_verified',
            'location_info', 'is_ambassador', 'is_admin',
            'followers_count', 'following_count', 'is_following', 'can_follow',
            'date_joined', 'last_login', 'is_active'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'is_active',
            'followers_count', 'following_count', 'is_following', 'can_follow'
        ]
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return f"{obj.first_name} {obj.last_name}".strip()
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_location_info(self, obj):
        """Retourne les informations de localisation"""
        if obj.quartier:
            return f"{obj.quartier.nom}, {obj.quartier.commune.nom}"
        return "Non spécifié"
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_ambassador(self, obj):
        """Indique si l'utilisateur est ambassadeur"""
        return obj.role == 'ambassador'
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_admin(self, obj):
        """Indique si l'utilisateur est administrateur"""
        return obj.role == 'admin'
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_followers_count(self, obj):
        """Retourne le nombre de followers"""
        return obj.followers.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_following_count(self, obj):
        """Retourne le nombre d'utilisateurs suivis"""
        return obj.following.count()
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_following(self, obj):
        """Vérifie si l'utilisateur connecté suit cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_can_follow(self, obj):
        """Vérifie si l'utilisateur connecté peut suivre cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user != obj and not request.user.is_following(obj)
        return False


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription des utilisateurs"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'quartier', 'bio'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }
    
    def validate(self, attrs):
        """Validation personnalisée"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        # Vérifier que l'email est unique
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        
        # Vérifier que le username est unique
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        
        return attrs
    
    def create(self, validated_data):
        """Création de l'utilisateur avec mot de passe hashé"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil utilisateur"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profession', 'company', 'interests', 'skills',
            'show_phone', 'show_email', 'show_location',
            'posts_count', 'connections_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserRelationshipSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les relations d'amitié"""
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = UserRelationship
        fields = [
            'id', 'follower', 'followed', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'follower', 'followed', 'created_at', 'updated_at']


class FollowUserSerializer(serializers.Serializer):
    """Sérialiseur pour suivre un utilisateur"""
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        """Valide que l'utilisateur existe"""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")
        return value


class UnfollowUserSerializer(serializers.Serializer):
    """Sérialiseur pour ne plus suivre un utilisateur"""
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        """Valide que l'utilisateur existe"""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")
        return value


class UserSearchSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la recherche d'utilisateurs"""
    full_name = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    can_follow = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'profile_picture', 'quartier', 'is_following', 'can_follow'
        ]
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return f"{obj.first_name} {obj.last_name}".strip()
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_following(self, obj):
        """Vérifie si l'utilisateur connecté suit cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_can_follow(self, obj):
        """Vérifie si l'utilisateur connecté peut suivre cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user != obj and not request.user.is_following(obj)
        return False


class SuggestedFriendsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les suggestions d'amis"""
    full_name = serializers.SerializerMethodField()
    quartier_name = serializers.CharField(source='quartier.nom', read_only=True)
    commune_name = serializers.CharField(source='quartier.commune.nom', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'profile_picture', 'quartier_name', 'commune_name'
        ]
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return f"{obj.first_name} {obj.last_name}".strip()


class GeographicVerificationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les vérifications géographiques"""
    
    class Meta:
        model = GeographicVerification
        fields = [
            'id', 'user', 'ip_address', 'country_code', 'country_name',
            'city', 'latitude', 'longitude', 'is_guinea',
            'verification_method', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class UserStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les statistiques utilisateur"""
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    connections_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'followers_count', 'following_count',
            'posts_count', 'connections_count'
        ] 
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_followers_count(self, obj):
        """Retourne le nombre de followers"""
        return obj.followers.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_following_count(self, obj):
        """Retourne le nombre d'utilisateurs suivis"""
        return obj.following.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_posts_count(self, obj):
        """Retourne le nombre de posts"""
        return obj.posts.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_connections_count(self, obj):
        """Retourne le nombre de connexions"""
        return obj.get_followers_count() + obj.get_following_count() 

# ============================================================================
# SÉRIALISEURS POUR GROUPES COMMUNAUTAIRES
# ============================================================================

class CommunityGroupSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les groupes communautaires"""
    creator = UserSerializer(read_only=True)
    admins = UserSerializer(many=True, read_only=True)
    member_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    is_member = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunityGroup
        fields = [
            'id', 'name', 'description', 'group_type', 'privacy_level',
            'quartier', 'creator', 'admins', 'cover_image', 'profile_image',
            'member_count', 'post_count', 'created_at', 'updated_at',
            'is_active', 'is_member', 'is_admin'
        ]
        read_only_fields = ['creator', 'member_count', 'post_count', 'created_at', 'updated_at']
    
    def get_is_member(self, obj):
        """Vérifie si l'utilisateur actuel est membre du groupe"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_member(request.user)
        return False
    
    def get_is_admin(self, obj):
        """Vérifie si l'utilisateur actuel est admin du groupe"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_admin(request.user)
        return False


class GroupMembershipSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les adhésions aux groupes"""
    user = UserSerializer(read_only=True)
    group = CommunityGroupSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GroupMembership
        fields = [
            'id', 'group', 'group_id', 'user', 'status', 'role',
            'joined_at', 'updated_at'
        ]
        read_only_fields = ['user', 'status', 'role', 'joined_at', 'updated_at']
    
    def create(self, validated_data):
        group_id = validated_data.pop('group_id')
        group = get_object_or_404(CommunityGroup, id=group_id)
        validated_data['group'] = group
        return super().create(validated_data)


# ============================================================================
# SÉRIALISEURS POUR ÉVÉNEMENTS COMMUNAUTAIRES
# ============================================================================

class CommunityEventSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les événements communautaires"""
    organizer = UserSerializer(read_only=True)
    group = CommunityGroupSerializer(read_only=True)
    attendee_count = serializers.ReadOnlyField()
    is_attendee = serializers.SerializerMethodField()
    can_join = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunityEvent
        fields = [
            'id', 'title', 'description', 'event_type', 'status',
            'start_date', 'end_date', 'quartier', 'location_details',
            'organizer', 'group', 'cover_image', 'attendee_count',
            'max_attendees', 'created_at', 'updated_at', 'is_public',
            'is_attendee', 'can_join'
        ]
        read_only_fields = ['organizer', 'attendee_count', 'created_at', 'updated_at']
    
    def get_is_attendee(self, obj):
        """Vérifie si l'utilisateur actuel participe à l'événement"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_attendee(request.user)
        return False
    
    def get_can_join(self, obj):
        """Vérifie si l'utilisateur actuel peut rejoindre l'événement"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.can_join(request.user)
        return False


class EventAttendanceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les participations aux événements"""
    user = UserSerializer(read_only=True)
    event = CommunityEventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = EventAttendance
        fields = [
            'id', 'event', 'event_id', 'user', 'status',
            'joined_at', 'updated_at'
        ]
        read_only_fields = ['user', 'joined_at', 'updated_at']
    
    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        event = get_object_or_404(CommunityEvent, id=event_id)
        validated_data['event'] = event
        return super().create(validated_data)


# ============================================================================
# SÉRIALISEURS POUR GAMIFICATION
# ============================================================================

class UserAchievementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les réalisations utilisateur"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'user', 'achievement_type', 'title', 'description',
            'icon', 'points', 'unlocked_at'
        ]
        read_only_fields = ['user', 'unlocked_at']


class UserSocialScoreSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le score social utilisateur"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSocialScore
        fields = [
            'id', 'user', 'total_points', 'level', 'achievements_count',
            'posts_count', 'friends_count', 'groups_count', 'events_count',
            'likes_received', 'comments_received', 'last_updated'
        ]
        read_only_fields = ['user', 'last_updated']


# ============================================================================
# SÉRIALISEURS POUR STATISTIQUES SOCIALES
# ============================================================================

class SocialStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques sociales"""
    user = UserSerializer()
    friends_count = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    events_count = serializers.IntegerField()
    posts_count = serializers.IntegerField()
    achievements_count = serializers.IntegerField()
    social_score = serializers.IntegerField()
    level = serializers.IntegerField()
    
    class Meta:
        fields = [
            'user', 'friends_count', 'groups_count', 'events_count',
            'posts_count', 'achievements_count', 'social_score', 'level'
        ]


# ============================================================================
# SÉRIALISEURS POUR SUGGESTIONS
# ============================================================================

class SuggestedGroupSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les groupes suggérés"""
    creator = UserSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CommunityGroup
        fields = [
            'id', 'name', 'description', 'group_type', 'privacy_level',
            'quartier', 'creator', 'member_count', 'cover_image'
        ]


class SuggestedEventSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les événements suggérés"""
    organizer = UserSerializer(read_only=True)
    attendee_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CommunityEvent
        fields = [
            'id', 'title', 'description', 'event_type', 'start_date',
            'end_date', 'quartier', 'organizer', 'attendee_count',
            'cover_image'
        ]


class SuggestedConnectionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les connexions suggérées"""
    mutual_friends_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'profile_picture', 'quartier', 'mutual_friends_count'
        ]
    
    def get_mutual_friends_count(self, obj):
        """Calcule le nombre d'amis en commun"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_friends = set(request.user.followers.filter(userrelationship__status='accepted').values_list('id', flat=True))
            obj_friends = set(obj.followers.filter(userrelationship__status='accepted').values_list('id', flat=True))
            return len(user_friends.intersection(obj_friends))
        return 0 
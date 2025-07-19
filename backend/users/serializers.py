from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, UserProfile, GeographicVerification, UserRelationship

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    full_name = serializers.ReadOnlyField()
    location_info = serializers.ReadOnlyField()
    is_ambassador = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
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
    
    def get_is_following(self, obj):
        """Vérifie si l'utilisateur connecté suit cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
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
    connections_count = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profession', 'company', 'interests', 'skills',
            'show_phone', 'show_email', 'show_location',
            'posts_count', 'connections_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'posts_count', 'connections_count', 'created_at', 'updated_at']


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
    full_name = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    can_follow = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'profile_picture', 'quartier', 'is_following', 'can_follow'
        ]
    
    def get_is_following(self, obj):
        """Vérifie si l'utilisateur connecté suit cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
    def get_can_follow(self, obj):
        """Vérifie si l'utilisateur connecté peut suivre cet utilisateur"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user != obj and not request.user.is_following(obj)
        return False


class SuggestedFriendsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les suggestions d'amis"""
    full_name = serializers.ReadOnlyField()
    quartier_name = serializers.CharField(source='quartier.nom', read_only=True)
    commune_name = serializers.CharField(source='quartier.commune.nom', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'profile_picture', 'quartier_name', 'commune_name'
        ]


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
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    posts_count = serializers.ReadOnlyField()
    connections_count = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'followers_count', 'following_count',
            'posts_count', 'connections_count'
        ] 
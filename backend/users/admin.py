from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, GeographicVerification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = [
        'username', 'email', 'full_name', 'quartier', 'role', 
        'is_verified', 'is_geographically_verified', 'is_active'
    ]
    list_filter = [
        'role', 'is_verified', 'is_geographically_verified', 
        'is_active', 'quartier__commune__prefecture__region', 'quartier__commune__prefecture'
    ]
    search_fields = [
        'username', 'email', 'first_name', 'last_name', 
        'quartier__nom', 'quartier__commune__nom'
    ]
    readonly_fields = ['created_at', 'updated_at', 'last_login_ip']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'bio')
        }),
        ('Localisation', {
            'fields': ('quartier', 'is_geographically_verified')
        }),
        ('Permissions', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at', 'last_login_ip')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'quartier', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Nom complet'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profession', 'company', 'posts_count', 'connections_count']
    list_filter = ['show_phone', 'show_email', 'show_location']
    search_fields = ['user__username', 'user__email', 'profession', 'company']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GeographicVerification)
class GeographicVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'ip_address', 'country_code', 'country_name', 
        'city', 'is_guinea', 'verification_method', 'created_at'
    ]
    list_filter = ['is_guinea', 'verification_method', 'country_code', 'created_at']
    search_fields = ['user__username', 'user__email', 'ip_address', 'country_name', 'city']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel 
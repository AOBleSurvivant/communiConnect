from django.urls import path
from . import views

app_name = 'internationalization'

urlpatterns = [
    # Langues et traductions
    path('languages/', views.get_supported_languages, name='get_supported_languages'),
    path('user-preferences/', views.get_user_language_preference, name='get_user_language_preference'),
    path('update-preferences/', views.update_user_language_preference, name='update_user_language_preference'),
    path('translate/', views.translate_text, name='translate_text'),
    path('ui-translation/', views.get_ui_translation, name='get_ui_translation'),
    path('translate-content/', views.translate_content, name='translate_content'),
    path('localized-content/', views.get_localized_content, name='get_localized_content'),
    
    # Pays et régions
    path('countries/', views.get_countries, name='get_countries'),
    path('cultural-adaptations/', views.get_cultural_adaptations, name='get_cultural_adaptations'),
    path('payment-methods/', views.get_payment_methods, name='get_payment_methods'),
    path('legal-compliance/', views.get_legal_compliance, name='get_legal_compliance'),
    path('regional-features/', views.get_regional_features, name='get_regional_features'),
    
    # Métriques et analytics
    path('metrics/', views.get_localization_metrics, name='get_localization_metrics'),
    
    # Gestion des traductions
    path('create-translation-key/', views.create_translation_key, name='create_translation_key'),
    
    # Conformité et validation
    path('validate-compliance/', views.validate_legal_compliance, name='validate_legal_compliance'),
    
    # Utilitaires
    path('timezone-info/', views.get_timezone_info, name='get_timezone_info'),
    path('format-currency/', views.format_currency, name='format_currency'),
] 
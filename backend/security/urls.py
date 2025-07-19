from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
    # Audit de sécurité
    path('audit/', views.audit_security_event, name='audit_security_event'),
    path('audits/', views.get_security_audits, name='get_security_audits'),
    
    # Détection de fraude
    path('detect-fraud/', views.detect_fraud, name='detect_fraud'),
    path('fraud-detections/', views.get_fraud_detections, name='get_fraud_detections'),
    
    # Authentification à deux facteurs
    path('setup-2fa/', views.setup_two_factor_auth, name='setup_two_factor_auth'),
    path('verify-2fa/', views.verify_two_factor_code, name='verify_two_factor_code'),
    
    # Empreintes d'appareils
    path('device-fingerprint/', views.create_device_fingerprint, name='create_device_fingerprint'),
    path('device-fingerprints/', views.get_device_fingerprints, name='get_device_fingerprints'),
    
    # Alertes de sécurité
    path('alerts/', views.get_security_alerts, name='get_security_alerts'),
    
    # Paramètres de confidentialité
    path('privacy-settings/', views.get_privacy_settings, name='get_privacy_settings'),
    path('update-privacy/', views.update_privacy_settings, name='update_privacy_settings'),
    
    # Tableau de bord de sécurité
    path('dashboard/', views.get_security_dashboard, name='get_security_dashboard'),
    
    # Chiffrement de données
    path('encrypt/', views.encrypt_data, name='encrypt_data'),
    path('decrypt/', views.decrypt_data, name='decrypt_data'),
] 
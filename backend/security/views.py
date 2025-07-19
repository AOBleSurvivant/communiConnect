from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from .models import (
    SecurityAudit, FraudDetection, TwoFactorAuth, SecurityPolicy,
    DeviceFingerprint, SecurityAlert, DataEncryption, PrivacySettings,
    SecurityMetrics
)
from .services import security_service
from posts.models import Post
from users.models import User
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def audit_security_event(request):
    """
    Endpoint pour auditer un événement de sécurité
    """
    try:
        user = request.user
        event_type = request.data.get('event_type')
        description = request.data.get('description')
        severity = request.data.get('severity', 'low')
        
        if not all([event_type, description]):
            return Response(
                {'error': 'Type d\'événement et description requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Contexte de l'événement
        context = {
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'session_id': request.session.session_key,
            'success': request.data.get('success', True),
            'error_message': request.data.get('error_message', ''),
        }
        
        # Audit de l'événement
        audit = security_service.audit_security_event(
            user=user,
            event_type=event_type,
            description=description,
            severity=severity,
            **context
        )
        
        if not audit:
            return Response(
                {'error': 'Erreur lors de l\'audit de l\'événement'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'audit_id': str(audit.audit_id),
            'event_type': audit.audit_type,
            'severity': audit.severity,
            'risk_score': audit.risk_score,
            'timestamp': audit.timestamp.isoformat(),
            'success': audit.success,
            'message': 'Événement audité avec succès'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Erreur audit événement sécurité: {e}")
        return Response(
            {'error': 'Erreur lors de l\'audit de l\'événement'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_security_audits(request):
    """
    Endpoint pour récupérer les audits de sécurité
    """
    try:
        user = request.user
        audit_type = request.GET.get('audit_type')
        severity = request.GET.get('severity')
        limit = int(request.GET.get('limit', 50))
        
        audits = SecurityAudit.objects.filter(user=user)
        
        if audit_type:
            audits = audits.filter(audit_type=audit_type)
        
        if severity:
            audits = audits.filter(severity=severity)
        
        audits = audits.order_by('-timestamp')[:limit]
        
        audits_data = []
        for audit in audits:
            audits_data.append({
                'audit_id': str(audit.audit_id),
                'event_type': audit.audit_type,
                'severity': audit.severity,
                'description': audit.action_description,
                'risk_score': audit.risk_score,
                'ip_address': audit.ip_address,
                'timestamp': audit.timestamp.isoformat(),
                'success': audit.success,
                'error_message': audit.error_message
            })
        
        response_data = {
            'user_id': user.id,
            'total_audits': len(audits_data),
            'audits': audits_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération audits sécurité: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des audits'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_fraud(request):
    """
    Endpoint pour détecter la fraude
    """
    try:
        user = request.user
        activity_type = request.data.get('activity_type')
        
        if not activity_type:
            return Response(
                {'error': 'Type d\'activité requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Contexte de l'activité
        context = {
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'location': request.data.get('location', ''),
            'device_info': request.data.get('device_info', {}),
        }
        
        # Détection de fraude
        fraud = security_service.detect_fraud(user, activity_type, context)
        
        if fraud:
            response_data = {
                'fraud_id': str(fraud.fraud_id),
                'fraud_type': fraud.fraud_type,
                'confidence_score': fraud.confidence_score,
                'risk_level': fraud.risk_level,
                'description': fraud.description,
                'detection_timestamp': fraud.detection_timestamp.isoformat(),
                'status': fraud.status,
                'message': 'Fraude détectée'
            }
        else:
            response_data = {
                'message': 'Aucune fraude détectée',
                'activity_type': activity_type
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur détection fraude: {e}")
        return Response(
            {'error': 'Erreur lors de la détection de fraude'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fraud_detections(request):
    """
    Endpoint pour récupérer les détections de fraude
    """
    try:
        user = request.user
        fraud_type = request.GET.get('fraud_type')
        status_filter = request.GET.get('status')
        limit = int(request.GET.get('limit', 20))
        
        frauds = FraudDetection.objects.filter(user=user)
        
        if fraud_type:
            frauds = frauds.filter(fraud_type=fraud_type)
        
        if status_filter:
            frauds = frauds.filter(status=status_filter)
        
        frauds = frauds.order_by('-detection_timestamp')[:limit]
        
        frauds_data = []
        for fraud in frauds:
            frauds_data.append({
                'fraud_id': str(fraud.fraud_id),
                'fraud_type': fraud.fraud_type,
                'status': fraud.status,
                'description': fraud.description,
                'confidence_score': fraud.confidence_score,
                'risk_level': fraud.risk_level,
                'detection_timestamp': fraud.detection_timestamp.isoformat(),
                'resolved_timestamp': fraud.resolved_timestamp.isoformat() if fraud.resolved_timestamp else None,
                'ip_address': fraud.ip_address,
                'location': fraud.location
            })
        
        response_data = {
            'user_id': user.id,
            'total_detections': len(frauds_data),
            'fraud_detections': frauds_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération détections fraude: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des détections'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_two_factor_auth(request):
    """
    Endpoint pour configurer l'authentification à deux facteurs
    """
    try:
        user = request.user
        method = request.data.get('method', 'sms')
        
        # Configuration 2FA
        two_factor = security_service.setup_two_factor_auth(user, method)
        
        if not two_factor:
            return Response(
                {'error': 'Erreur lors de la configuration 2FA'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'user_id': user.id,
            'is_enabled': two_factor.is_enabled,
            'primary_method': two_factor.primary_method,
            'backup_codes_count': len(two_factor.backup_codes),
            'message': 'Authentification à deux facteurs configurée'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur configuration 2FA: {e}")
        return Response(
            {'error': 'Erreur lors de la configuration 2FA'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_two_factor_code(request):
    """
    Endpoint pour vérifier un code d'authentification à deux facteurs
    """
    try:
        user = request.user
        code = request.data.get('code')
        method = request.data.get('method', 'sms')
        
        if not code:
            return Response(
                {'error': 'Code requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérification du code
        is_valid = security_service.verify_two_factor_code(user, code, method)
        
        response_data = {
            'user_id': user.id,
            'is_valid': is_valid,
            'method': method,
            'message': 'Code vérifié avec succès' if is_valid else 'Code invalide'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur vérification 2FA: {e}")
        return Response(
            {'error': 'Erreur lors de la vérification du code'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_device_fingerprint(request):
    """
    Endpoint pour créer une empreinte d'appareil
    """
    try:
        user = request.user
        device_info = request.data.get('device_info', {})
        
        # Ajouter les informations de base
        device_info.update({
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'device_type': request.data.get('device_type', 'desktop'),
            'browser': request.data.get('browser', ''),
            'os': request.data.get('os', ''),
            'screen_resolution': request.data.get('screen_resolution', ''),
            'timezone': request.data.get('timezone', ''),
            'language': request.data.get('language', ''),
        })
        
        # Création de l'empreinte
        device_fingerprint = security_service.create_device_fingerprint(user, device_info)
        
        if not device_fingerprint:
            return Response(
                {'error': 'Erreur lors de la création de l\'empreinte'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'fingerprint_id': device_fingerprint.id,
            'fingerprint_hash': device_fingerprint.fingerprint_hash[:16] + '...',
            'device_type': device_fingerprint.device_type,
            'browser': device_fingerprint.browser,
            'os': device_fingerprint.os,
            'is_trusted': device_fingerprint.is_trusted,
            'risk_score': device_fingerprint.risk_score,
            'message': 'Empreinte d\'appareil créée'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Erreur création empreinte appareil: {e}")
        return Response(
            {'error': 'Erreur lors de la création de l\'empreinte'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_device_fingerprints(request):
    """
    Endpoint pour récupérer les empreintes d'appareils
    """
    try:
        user = request.user
        limit = int(request.GET.get('limit', 10))
        
        fingerprints = DeviceFingerprint.objects.filter(user=user).order_by('-last_seen')[:limit]
        
        fingerprints_data = []
        for fp in fingerprints:
            fingerprints_data.append({
                'fingerprint_id': fp.id,
                'device_type': fp.device_type,
                'browser': fp.browser,
                'os': fp.os,
                'ip_address': fp.ip_address,
                'country': fp.country,
                'city': fp.city,
                'is_trusted': fp.is_trusted,
                'is_blocked': fp.is_blocked,
                'risk_score': fp.risk_score,
                'total_sessions': fp.total_sessions,
                'first_seen': fp.first_seen.isoformat(),
                'last_seen': fp.last_seen.isoformat()
            })
        
        response_data = {
            'user_id': user.id,
            'total_devices': len(fingerprints_data),
            'devices': fingerprints_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération empreintes appareils: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des empreintes'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_security_alerts(request):
    """
    Endpoint pour récupérer les alertes de sécurité
    """
    try:
        user = request.user
        alert_type = request.GET.get('alert_type')
        priority = request.GET.get('priority')
        limit = int(request.GET.get('limit', 20))
        
        alerts = SecurityAlert.objects.filter(affected_users=user)
        
        if alert_type:
            alerts = alerts.filter(alert_type=alert_type)
        
        if priority:
            alerts = alerts.filter(priority=priority)
        
        alerts = alerts.order_by('-created_at')[:limit]
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'alert_id': str(alert.alert_id),
                'alert_type': alert.alert_type,
                'priority': alert.priority,
                'title': alert.title,
                'description': alert.description,
                'source_ip': alert.source_ip,
                'is_active': alert.is_active,
                'is_resolved': alert.is_resolved,
                'created_at': alert.created_at.isoformat(),
                'resolved_at': alert.resolved_at.isoformat() if alert.resolved_at else None
            })
        
        response_data = {
            'user_id': user.id,
            'total_alerts': len(alerts_data),
            'alerts': alerts_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération alertes sécurité: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des alertes'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_privacy_settings(request):
    """
    Endpoint pour mettre à jour les paramètres de confidentialité
    """
    try:
        user = request.user
        settings = request.data.get('settings', {})
        
        if not settings:
            return Response(
                {'error': 'Paramètres requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mise à jour des paramètres
        privacy_settings = security_service.update_privacy_settings(user, settings)
        
        if not privacy_settings:
            return Response(
                {'error': 'Erreur lors de la mise à jour des paramètres'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'user_id': user.id,
            'profile_visibility': privacy_settings.profile_visibility,
            'share_location': privacy_settings.share_location,
            'share_activity': privacy_settings.share_activity,
            'share_posts': privacy_settings.share_posts,
            'share_friends': privacy_settings.share_friends,
            'email_notifications': privacy_settings.email_notifications,
            'sms_notifications': privacy_settings.sms_notifications,
            'push_notifications': privacy_settings.push_notifications,
            'allow_data_analysis': privacy_settings.allow_data_analysis,
            'allow_targeted_ads': privacy_settings.allow_targeted_ads,
            'message': 'Paramètres de confidentialité mis à jour'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur mise à jour paramètres confidentialité: {e}")
        return Response(
            {'error': 'Erreur lors de la mise à jour des paramètres'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_privacy_settings(request):
    """
    Endpoint pour récupérer les paramètres de confidentialité
    """
    try:
        user = request.user
        
        privacy_settings, created = PrivacySettings.objects.get_or_create(user=user)
        
        response_data = {
            'user_id': user.id,
            'profile_visibility': privacy_settings.profile_visibility,
            'share_location': privacy_settings.share_location,
            'share_activity': privacy_settings.share_activity,
            'share_posts': privacy_settings.share_posts,
            'share_friends': privacy_settings.share_friends,
            'email_notifications': privacy_settings.email_notifications,
            'sms_notifications': privacy_settings.sms_notifications,
            'push_notifications': privacy_settings.push_notifications,
            'data_retention_days': privacy_settings.data_retention_days,
            'allow_data_analysis': privacy_settings.allow_data_analysis,
            'allow_targeted_ads': privacy_settings.allow_targeted_ads,
            'require_approval_friends': privacy_settings.require_approval_friends,
            'block_unknown_users': privacy_settings.block_unknown_users,
            'hide_online_status': privacy_settings.hide_online_status
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération paramètres confidentialité: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des paramètres'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_security_dashboard(request):
    """
    Endpoint pour récupérer le tableau de bord de sécurité
    """
    try:
        user = request.user
        
        # Données du tableau de bord
        dashboard_data = security_service.get_security_dashboard_data()
        
        # Ajouter les données spécifiques à l'utilisateur
        user_audits = SecurityAudit.objects.filter(user=user).order_by('-timestamp')[:10]
        user_fraud = FraudDetection.objects.filter(user=user).order_by('-detection_timestamp')[:5]
        user_alerts = SecurityAlert.objects.filter(affected_users=user).order_by('-created_at')[:5]
        
        user_data = {
            'recent_audits': [{
                'audit_type': audit.audit_type,
                'severity': audit.severity,
                'risk_score': audit.risk_score,
                'timestamp': audit.timestamp.isoformat()
            } for audit in user_audits],
            'recent_fraud': [{
                'fraud_type': fraud.fraud_type,
                'confidence_score': fraud.confidence_score,
                'status': fraud.status,
                'detection_timestamp': fraud.detection_timestamp.isoformat()
            } for fraud in user_fraud],
            'recent_alerts': [{
                'alert_type': alert.alert_type,
                'priority': alert.priority,
                'title': alert.title,
                'created_at': alert.created_at.isoformat()
            } for alert in user_alerts]
        }
        
        response_data = {
            'user_id': user.id,
            'global_metrics': dashboard_data,
            'user_metrics': user_data,
            'security_score': dashboard_data.get('security_score', 75.0),
            'last_updated': timezone.now().isoformat()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur tableau de bord sécurité: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération du tableau de bord'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def encrypt_data(request):
    """
    Endpoint pour chiffrer des données sensibles
    """
    try:
        data = request.data.get('data')
        encryption_type = request.data.get('encryption_type', 'aes_256')
        
        if not data:
            return Response(
                {'error': 'Données requises'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Chiffrement des données
        encrypted_data = security_service.encrypt_sensitive_data(data, encryption_type)
        
        response_data = {
            'original_data_length': len(data),
            'encrypted_data': encrypted_data,
            'encryption_type': encryption_type,
            'message': 'Données chiffrées avec succès'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur chiffrement données: {e}")
        return Response(
            {'error': 'Erreur lors du chiffrement des données'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrypt_data(request):
    """
    Endpoint pour déchiffrer des données sensibles
    """
    try:
        encrypted_data = request.data.get('encrypted_data')
        
        if not encrypted_data:
            return Response(
                {'error': 'Données chiffrées requises'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Déchiffrement des données
        decrypted_data = security_service.decrypt_sensitive_data(encrypted_data)
        
        response_data = {
            'encrypted_data_length': len(encrypted_data),
            'decrypted_data': decrypted_data,
            'message': 'Données déchiffrées avec succès'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur déchiffrement données: {e}")
        return Response(
            {'error': 'Erreur lors du déchiffrement des données'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
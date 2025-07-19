from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
from .models import (
    SecurityConfig, UserSecurityProfile, SecurityEvent, SecurityThreat,
    SecurityPolicy, SecurityAudit, EncryptionKey, SecurityCompliance, SecurityIncident
)
import hashlib
import secrets
import pyotp
import qrcode
import base64
import os
import logging
from typing import Dict, List, Optional, Tuple
import json
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ipaddress
import geoip2.database
import geoip2.errors
from user_agents import parse
import re

logger = logging.getLogger(__name__)

User = get_user_model()

class SecurityService:
    """Service de sécurité renforcée"""
    
    def __init__(self):
        self.config = self._get_security_config()
        self.geoip_reader = None
        self._init_geoip()
    
    def _get_security_config(self):
        """Récupère la configuration de sécurité active"""
        try:
            return SecurityConfig.objects.filter(is_active=True).first()
        except SecurityConfig.DoesNotExist:
            # Configuration par défaut
            return SecurityConfig.objects.create(
                name="Configuration Sécurité Par Défaut",
                security_level="standard",
                password_min_length=8,
                password_require_uppercase=True,
                password_require_lowercase=True,
                password_require_numbers=True,
                password_require_special=True,
                password_expiry_days=90,
                max_login_attempts=5,
                lockout_duration_minutes=30,
                mfa_required=False,
                session_timeout_minutes=60,
                max_concurrent_sessions=5,
                encryption_enabled=True,
                security_logging_enabled=True,
                anomaly_detection_enabled=True,
                gdpr_compliant=True,
                audit_logging_enabled=True,
                rate_limiting_enabled=True
            )
    
    def _init_geoip(self):
        """Initialise la base de données GeoIP"""
        try:
            # En production, utiliser une vraie base GeoIP
            self.geoip_reader = None
        except Exception as e:
            logger.warning(f"GeoIP non disponible: {e}")
    
    def log_security_event(self, event_type, user=None, description="", **kwargs):
        """Enregistre un événement de sécurité"""
        try:
            event = SecurityEvent.objects.create(
                user=user,
                event_type=event_type,
                description=description,
                ip_address=kwargs.get('ip_address'),
                user_agent=kwargs.get('user_agent', ''),
                location=kwargs.get('location', ''),
                device_info=kwargs.get('device_info', {}),
                session_id=kwargs.get('session_id', ''),
                request_path=kwargs.get('request_path', ''),
                request_method=kwargs.get('request_method', ''),
                metadata=kwargs.get('metadata', {}),
                threat_indicators=kwargs.get('threat_indicators', [])
            )
            
            # Déclencher l'analyse de sécurité
            self._analyze_security_event(event)
            
            return event
            
        except Exception as e:
            logger.error(f"Erreur log événement sécurité: {e}")
            return None
    
    def _analyze_security_event(self, event):
        """Analyse un événement de sécurité pour détecter les menaces"""
        try:
            # Vérifier les patterns suspects
            if self._is_suspicious_event(event):
                self._create_security_threat(event)
            
            # Mettre à jour le profil de sécurité utilisateur
            if event.user:
                self._update_user_security_profile(event.user, event)
            
            # Vérifier les anomalies
            self._detect_anomalies(event)
            
        except Exception as e:
            logger.error(f"Erreur analyse événement sécurité: {e}")
    
    def _is_suspicious_event(self, event):
        """Détermine si un événement est suspect"""
        suspicious_patterns = [
            # Tentatives de connexion multiples
            {'event_type': 'login_failed', 'count': 5, 'timeframe': 300},  # 5 échecs en 5 min
            
            # Activité depuis des IPs suspectes
            {'ip_address': r'^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)', 'suspicious': True},
            
            # User agents suspects
            {'user_agent': r'(bot|crawler|spider|scraper)', 'suspicious': True},
            
            # Localisations suspectes
            {'location': r'(unknown|invalid)', 'suspicious': True},
            
            # Patterns de force brute
            {'event_type': 'login_failed', 'pattern': 'sequential_attempts'},
            
            # Activité anormale
            {'event_type': 'data_access', 'unusual_time': True},
        ]
        
        for pattern in suspicious_patterns:
            if self._matches_suspicious_pattern(event, pattern):
                return True
        
        return False
    
    def _matches_suspicious_pattern(self, event, pattern):
        """Vérifie si un événement correspond à un pattern suspect"""
        try:
            if 'event_type' in pattern and event.event_type == pattern['event_type']:
                if 'count' in pattern and 'timeframe' in pattern:
                    # Vérifier le nombre d'événements dans la fenêtre de temps
                    recent_events = SecurityEvent.objects.filter(
                        user=event.user,
                        event_type=event.event_type,
                        timestamp__gte=timezone.now() - timedelta(seconds=pattern['timeframe'])
                    ).count()
                    
                    return recent_events >= pattern['count']
                
                elif 'pattern' in pattern and pattern['pattern'] == 'sequential_attempts':
                    # Vérifier les tentatives séquentielles
                    return self._is_sequential_attempts(event)
            
            elif 'ip_address' in pattern:
                if event.ip_address and re.search(pattern['ip_address'], event.ip_address):
                    return pattern.get('suspicious', False)
            
            elif 'user_agent' in pattern:
                if event.user_agent and re.search(pattern['user_agent'], event.user_agent, re.IGNORECASE):
                    return pattern.get('suspicious', False)
            
            elif 'location' in pattern:
                if event.location and re.search(pattern['location'], event.location, re.IGNORECASE):
                    return pattern.get('suspicious', False)
            
            elif 'unusual_time' in pattern and pattern['unusual_time']:
                # Vérifier si l'activité est à une heure inhabituelle
                hour = event.timestamp.hour
                return hour < 6 or hour > 22  # Entre 22h et 6h
            
        except Exception as e:
            logger.error(f"Erreur vérification pattern suspect: {e}")
        
        return False
    
    def _is_sequential_attempts(self, event):
        """Vérifie s'il y a des tentatives séquentielles"""
        try:
            if not event.user:
                return False
            
            # Récupérer les dernières tentatives de connexion
            recent_failures = SecurityEvent.objects.filter(
                user=event.user,
                event_type='login_failed',
                timestamp__gte=timezone.now() - timedelta(minutes=10)
            ).order_by('timestamp')
            
            if recent_failures.count() < 3:
                return False
            
            # Vérifier si les tentatives sont rapprochées
            timestamps = [e.timestamp for e in recent_failures]
            intervals = []
            
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)
            
            # Si les intervalles sont très courts (< 30 secondes)
            return all(interval < 30 for interval in intervals)
            
        except Exception as e:
            logger.error(f"Erreur vérification tentatives séquentielles: {e}")
            return False
    
    def _create_security_threat(self, event):
        """Crée une menace de sécurité basée sur un événement"""
        try:
            threat_type = self._determine_threat_type(event)
            threat_level = self._determine_threat_level(event)
            
            threat = SecurityThreat.objects.create(
                threat_type=threat_type,
                threat_level=threat_level,
                title=f"Menace détectée: {event.event_type}",
                description=f"Événement suspect détecté: {event.description}",
                source_ip=event.ip_address,
                source_location=event.location,
                source_user=event.user,
                affected_users=1 if event.user else 0,
                indicators=[event.event_type, event.ip_address, event.user_agent],
                detected_at=event.timestamp
            )
            
            # Déclencher la réponse automatique
            self._respond_to_threat(threat)
            
            return threat
            
        except Exception as e:
            logger.error(f"Erreur création menace: {e}")
            return None
    
    def _determine_threat_type(self, event):
        """Détermine le type de menace basé sur l'événement"""
        threat_mapping = {
            'login_failed': 'brute_force',
            'unauthorized_access': 'session_hijacking',
            'data_access': 'data_exfiltration',
            'suspicious_activity': 'advanced_persistent_threat',
        }
        
        return threat_mapping.get(event.event_type, 'unknown')
    
    def _determine_threat_level(self, event):
        """Détermine le niveau de menace"""
        if event.severity == 'critical':
            return 'critical'
        elif event.severity == 'high':
            return 'high'
        elif event.severity == 'medium':
            return 'medium'
        else:
            return 'low'
    
    def _respond_to_threat(self, threat):
        """Répond automatiquement à une menace"""
        try:
            actions = []
            
            if threat.threat_level in ['high', 'critical']:
                # Bloquer l'IP source
                if threat.source_ip:
                    actions.append(f"Bloquer IP: {threat.source_ip}")
                
                # Verrouiller le compte utilisateur
                if threat.source_user:
                    self._lock_user_account(threat.source_user)
                    actions.append(f"Verrouiller compte: {threat.source_user.username}")
                
                # Envoyer une alerte
                actions.append("Envoyer alerte sécurité")
            
            elif threat.threat_level == 'medium':
                # Augmenter la surveillance
                actions.append("Augmenter surveillance")
                
                # Demander une vérification MFA
                if threat.source_user:
                    actions.append("Demander vérification MFA")
            
            # Enregistrer les actions
            threat.response_actions = actions
            threat.save()
            
        except Exception as e:
            logger.error(f"Erreur réponse menace: {e}")
    
    def _lock_user_account(self, user):
        """Verrouille un compte utilisateur"""
        try:
            profile, created = UserSecurityProfile.objects.get_or_create(user=user)
            profile.account_locked = True
            profile.lockout_until = timezone.now() + timedelta(minutes=self.config.lockout_duration_minutes)
            profile.save()
            
            # Enregistrer l'événement
            self.log_security_event(
                'account_locked',
                user=user,
                description=f"Compte verrouillé automatiquement suite à une menace"
            )
            
        except Exception as e:
            logger.error(f"Erreur verrouillage compte: {e}")
    
    def _update_user_security_profile(self, user, event):
        """Met à jour le profil de sécurité utilisateur"""
        try:
            profile, created = UserSecurityProfile.objects.get_or_create(user=user)
            
            # Mettre à jour les informations de connexion
            if event.event_type == 'login_success':
                profile.last_login_ip = event.ip_address
                profile.last_login_location = event.location
                profile.last_login_device = event.user_agent
                profile.failed_login_attempts = 0
                profile.account_locked = False
                profile.lockout_until = None
            
            elif event.event_type == 'login_failed':
                profile.failed_login_attempts += 1
                
                # Verrouiller le compte si trop d'échecs
                if profile.failed_login_attempts >= self.config.max_login_attempts:
                    profile.account_locked = True
                    profile.lockout_until = timezone.now() + timedelta(minutes=self.config.lockout_duration_minutes)
            
            # Mettre à jour le score de confiance
            profile.trust_score = self._calculate_trust_score(profile, event)
            profile.risk_level = self._determine_risk_level(profile.trust_score)
            
            profile.save()
            
        except Exception as e:
            logger.error(f"Erreur mise à jour profil sécurité: {e}")
    
    def _calculate_trust_score(self, profile, event):
        """Calcule le score de confiance utilisateur"""
        try:
            base_score = profile.trust_score
            
            # Facteurs positifs
            if event.event_type == 'login_success':
                base_score += 5
            elif event.event_type == 'mfa_used':
                base_score += 10
            elif event.event_type == 'password_change':
                base_score += 3
            
            # Facteurs négatifs
            elif event.event_type == 'login_failed':
                base_score -= 10
            elif event.event_type == 'suspicious_activity':
                base_score -= 20
            elif event.event_type == 'account_locked':
                base_score -= 30
            
            # Limiter le score entre 0 et 100
            return max(0, min(100, base_score))
            
        except Exception as e:
            logger.error(f"Erreur calcul score confiance: {e}")
            return 50
    
    def _determine_risk_level(self, trust_score):
        """Détermine le niveau de risque basé sur le score de confiance"""
        if trust_score >= 80:
            return 'low'
        elif trust_score >= 60:
            return 'medium'
        elif trust_score >= 40:
            return 'high'
        else:
            return 'critical'
    
    def _detect_anomalies(self, event):
        """Détecte les anomalies de sécurité"""
        try:
            if not event.user:
                return
            
            # Récupérer les événements récents de l'utilisateur
            recent_events = SecurityEvent.objects.filter(
                user=event.user,
                timestamp__gte=timezone.now() - timedelta(hours=24)
            ).order_by('timestamp')
            
            if recent_events.count() < 5:
                return
            
            # Analyser les patterns
            event_counts = recent_events.values('event_type').annotate(
                count=Count('id')
            )
            
            # Détecter les anomalies
            for event_count in event_counts:
                if event_count['count'] > 50:  # Seuil d'anomalie
                    self.log_security_event(
                        'suspicious_activity',
                        user=event.user,
                        description=f"Activité excessive détectée: {event_count['event_type']} ({event_count['count']} fois)",
                        severity='high'
                    )
                    
        except Exception as e:
            logger.error(f"Erreur détection anomalies: {e}")
    
    def setup_mfa_for_user(self, user, method='totp'):
        """Configure l'authentification multi-facteurs pour un utilisateur"""
        try:
            profile, created = UserSecurityProfile.objects.get_or_create(user=user)
            
            if method == 'totp':
                # Générer le secret TOTP
                secret = profile.generate_totp_secret()
                
                # Générer les codes de sauvegarde
                backup_codes = profile.generate_backup_codes()
                
                return {
                    'secret': secret,
                    'qr_code': profile.get_totp_qr_code(),
                    'backup_codes': backup_codes,
                    'setup_complete': False
                }
            
            elif method == 'sms':
                # Envoyer un code SMS
                sms_code = self._send_sms_code(user)
                return {
                    'sms_sent': True,
                    'setup_complete': False
                }
            
            elif method == 'email':
                # Envoyer un code par email
                email_code = self._send_email_code(user)
                return {
                    'email_sent': True,
                    'setup_complete': False
                }
            
        except Exception as e:
            logger.error(f"Erreur configuration MFA: {e}")
            return None
    
    def _send_sms_code(self, user):
        """Envoie un code SMS (simulé)"""
        # En production, intégrer un service SMS
        code = secrets.token_hex(3).upper()[:6]
        logger.info(f"Code SMS envoyé à {user.phone}: {code}")
        return code
    
    def _send_email_code(self, user):
        """Envoie un code par email (simulé)"""
        # En production, envoyer un vrai email
        code = secrets.token_hex(3).upper()[:6]
        logger.info(f"Code email envoyé à {user.email}: {code}")
        return code
    
    def verify_mfa(self, user, token, method='totp'):
        """Vérifie un token MFA"""
        try:
            profile = UserSecurityProfile.objects.get(user=user)
            
            if method == 'totp':
                return profile.verify_totp(token)
            
            elif method == 'backup_code':
                return profile.verify_backup_code(token)
            
            elif method in ['sms', 'email']:
                # Vérifier le code stocké en cache
                cache_key = f"mfa_{method}_{user.id}"
                stored_code = cache.get(cache_key)
                return stored_code == token
            
        except Exception as e:
            logger.error(f"Erreur vérification MFA: {e}")
            return False
    
    def validate_password(self, password):
        """Valide un mot de passe selon les politiques"""
        try:
            errors = []
            
            # Longueur minimale
            if len(password) < self.config.password_min_length:
                errors.append(f"Le mot de passe doit contenir au moins {self.config.password_min_length} caractères")
            
            # Caractères requis
            if self.config.password_require_uppercase and not re.search(r'[A-Z]', password):
                errors.append("Le mot de passe doit contenir au moins une majuscule")
            
            if self.config.password_require_lowercase and not re.search(r'[a-z]', password):
                errors.append("Le mot de passe doit contenir au moins une minuscule")
            
            if self.config.password_require_numbers and not re.search(r'\d', password):
                errors.append("Le mot de passe doit contenir au moins un chiffre")
            
            if self.config.password_require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append("Le mot de passe doit contenir au moins un caractère spécial")
            
            # Vérifier les mots de passe faibles
            weak_passwords = ['password', '123456', 'admin', 'qwerty', 'letmein']
            if password.lower() in weak_passwords:
                errors.append("Ce mot de passe est trop commun")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Erreur validation mot de passe: {e}")
            return {'valid': False, 'errors': ['Erreur de validation']}
    
    def check_password_expiry(self, user):
        """Vérifie si le mot de passe a expiré"""
        try:
            profile = UserSecurityProfile.objects.get(user=user)
            
            if not profile.password_changed_at:
                return True  # Mot de passe jamais changé
            
            expiry_date = profile.password_changed_at + timedelta(days=self.config.password_expiry_days)
            return timezone.now() > expiry_date
            
        except UserSecurityProfile.DoesNotExist:
            return True  # Pas de profil, forcer le changement
        except Exception as e:
            logger.error(f"Erreur vérification expiration mot de passe: {e}")
            return False
    
    def enforce_password_history(self, user, new_password):
        """Vérifie que le nouveau mot de passe n'est pas dans l'historique"""
        try:
            profile = UserSecurityProfile.objects.get(user=user)
            
            # Vérifier contre l'historique (derniers 5 mots de passe)
            for old_password_hash in profile.password_history[-5:]:
                if hashlib.sha256(new_password.encode()).hexdigest() == old_password_hash:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur vérification historique mot de passe: {e}")
            return True
    
    def check_rate_limit(self, ip_address, action_type):
        """Vérifie les limites de taux"""
        try:
            cache_key = f"rate_limit_{action_type}_{ip_address}"
            current_count = cache.get(cache_key, 0)
            
            # Limites par type d'action
            limits = {
                'login': 5,  # 5 tentatives par minute
                'password_reset': 3,  # 3 demandes par heure
                'mfa_setup': 10,  # 10 tentatives par heure
                'api_call': 100,  # 100 appels par minute
            }
            
            limit = limits.get(action_type, 10)
            
            if current_count >= limit:
                return False
            
            # Incrémenter le compteur
            cache.set(cache_key, current_count + 1, 60)  # Expire en 1 minute
            return True
            
        except Exception as e:
            logger.error(f"Erreur vérification limite taux: {e}")
            return True
    
    def check_ip_restrictions(self, ip_address):
        """Vérifie les restrictions d'IP"""
        try:
            # Vérifier la liste noire
            if ip_address in self.config.ip_blacklist:
                return False
            
            # Vérifier la liste blanche (si configurée)
            if self.config.ip_whitelist and ip_address not in self.config.ip_whitelist:
                return False
            
            # Vérifier les restrictions géographiques
            if self.config.geo_restrictions:
                location = self._get_ip_location(ip_address)
                if location and location not in self.config.geo_restrictions:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur vérification restrictions IP: {e}")
            return True
    
    def _get_ip_location(self, ip_address):
        """Récupère la localisation d'une IP"""
        try:
            if not self.geoip_reader:
                return None
            
            response = self.geoip_reader.city(ip_address)
            return response.country.iso_code
            
        except Exception as e:
            logger.error(f"Erreur récupération localisation IP: {e}")
            return None
    
    def encrypt_sensitive_data(self, data, key_name='default'):
        """Chiffre des données sensibles"""
        try:
            # Récupérer ou créer la clé de chiffrement
            key_obj, created = EncryptionKey.objects.get_or_create(
                name=key_name,
                defaults={
                    'key_type': 'symmetric',
                    'algorithm': 'AES-256'
                }
            )
            
            if created:
                key_obj.generate_key()
            
            # Chiffrer les données
            fernet = key_obj.get_fernet()
            encrypted_data = fernet.encrypt(data.encode())
            
            return base64.b64encode(encrypted_data).decode()
            
        except Exception as e:
            logger.error(f"Erreur chiffrement données: {e}")
            return None
    
    def decrypt_sensitive_data(self, encrypted_data, key_name='default'):
        """Déchiffre des données sensibles"""
        try:
            # Récupérer la clé de chiffrement
            key_obj = EncryptionKey.objects.get(name=key_name, is_active=True)
            
            # Déchiffrer les données
            fernet = key_obj.get_fernet()
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = fernet.decrypt(encrypted_bytes)
            
            return decrypted_data.decode()
            
        except Exception as e:
            logger.error(f"Erreur déchiffrement données: {e}")
            return None
    
    def run_security_audit(self, audit_type='user_access'):
        """Exécute un audit de sécurité"""
        try:
            audit = SecurityAudit.objects.create(
                audit_type=audit_type,
                title=f"Audit {audit_type}",
                description=f"Audit automatique de {audit_type}",
                status='in_progress',
                started_at=timezone.now(),
                automated=True
            )
            
            findings = []
            recommendations = []
            
            if audit_type == 'user_access':
                findings, recommendations = self._audit_user_access()
            elif audit_type == 'data_access':
                findings, recommendations = self._audit_data_access()
            elif audit_type == 'system_config':
                findings, recommendations = self._audit_system_config()
            
            # Finaliser l'audit
            audit.findings = findings
            audit.recommendations = recommendations
            audit.status = 'completed'
            audit.completed_at = timezone.now()
            audit.duration_minutes = int((audit.completed_at - audit.started_at).total_seconds() / 60)
            audit.save()
            
            return audit
            
        except Exception as e:
            logger.error(f"Erreur audit sécurité: {e}")
            return None
    
    def _audit_user_access(self):
        """Audit des accès utilisateur"""
        findings = []
        recommendations = []
        
        try:
            # Vérifier les comptes inactifs
            inactive_users = User.objects.filter(
                last_login__lt=timezone.now() - timedelta(days=90)
            ).count()
            
            if inactive_users > 0:
                findings.append(f"{inactive_users} comptes inactifs détectés")
                recommendations.append("Nettoyer les comptes inactifs")
            
            # Vérifier les comptes sans MFA
            users_without_mfa = UserSecurityProfile.objects.filter(
                mfa_enabled=False
            ).count()
            
            if users_without_mfa > 0:
                findings.append(f"{users_without_mfa} utilisateurs sans MFA")
                recommendations.append("Forcer l'activation MFA")
            
            # Vérifier les mots de passe expirés
            expired_passwords = 0
            for user in User.objects.all():
                if self.check_password_expiry(user):
                    expired_passwords += 1
            
            if expired_passwords > 0:
                findings.append(f"{expired_passwords} mots de passe expirés")
                recommendations.append("Forcer le changement de mots de passe")
            
        except Exception as e:
            logger.error(f"Erreur audit accès utilisateur: {e}")
        
        return findings, recommendations
    
    def _audit_data_access(self):
        """Audit des accès aux données"""
        findings = []
        recommendations = []
        
        try:
            # Vérifier les accès non autorisés
            unauthorized_access = SecurityEvent.objects.filter(
                event_type='unauthorized_access',
                timestamp__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            if unauthorized_access > 0:
                findings.append(f"{unauthorized_access} tentatives d'accès non autorisé")
                recommendations.append("Renforcer les contrôles d'accès")
            
            # Vérifier les exports de données
            data_exports = SecurityEvent.objects.filter(
                event_type='data_export',
                timestamp__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            if data_exports > 10:
                findings.append(f"{data_exports} exports de données détectés")
                recommendations.append("Auditer les exports de données")
            
        except Exception as e:
            logger.error(f"Erreur audit accès données: {e}")
        
        return findings, recommendations
    
    def _audit_system_config(self):
        """Audit de la configuration système"""
        findings = []
        recommendations = []
        
        try:
            # Vérifier la configuration de sécurité
            if not self.config.mfa_required:
                findings.append("MFA non obligatoire")
                recommendations.append("Activer MFA obligatoire")
            
            if self.config.password_min_length < 12:
                findings.append("Longueur minimale mot de passe faible")
                recommendations.append("Augmenter la longueur minimale")
            
            if not self.config.encryption_enabled:
                findings.append("Chiffrement désactivé")
                recommendations.append("Activer le chiffrement")
            
            if not self.config.audit_logging_enabled:
                findings.append("Audit logging désactivé")
                recommendations.append("Activer l'audit logging")
            
        except Exception as e:
            logger.error(f"Erreur audit configuration système: {e}")
        
        return findings, recommendations
    
    def get_security_dashboard_data(self):
        """Récupère les données pour le dashboard de sécurité"""
        try:
            # Statistiques générales
            total_users = User.objects.count()
            users_with_mfa = UserSecurityProfile.objects.filter(mfa_enabled=True).count()
            locked_accounts = UserSecurityProfile.objects.filter(account_locked=True).count()
            
            # Événements de sécurité récents
            recent_events = SecurityEvent.objects.filter(
                timestamp__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            # Menaces détectées
            recent_threats = SecurityThreat.objects.filter(
                detected_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            # Incidents de sécurité
            active_incidents = SecurityIncident.objects.filter(
                status__in=['detected', 'investigating', 'contained']
            ).count()
            
            # Conformité
            compliance_status = SecurityCompliance.objects.filter(
                status='compliant'
            ).count()
            
            return {
                'total_users': total_users,
                'users_with_mfa': users_with_mfa,
                'mfa_adoption_rate': (users_with_mfa / max(total_users, 1)) * 100,
                'locked_accounts': locked_accounts,
                'recent_events': recent_events,
                'recent_threats': recent_threats,
                'active_incidents': active_incidents,
                'compliance_status': compliance_status,
                'security_score': self._calculate_security_score()
            }
            
        except Exception as e:
            logger.error(f"Erreur récupération données dashboard: {e}")
            return {}
    
    def _calculate_security_score(self):
        """Calcule le score de sécurité global"""
        try:
            score = 100
            
            # Facteurs négatifs
            if not self.config.mfa_required:
                score -= 20
            
            if self.config.password_min_length < 12:
                score -= 15
            
            if not self.config.encryption_enabled:
                score -= 25
            
            if not self.config.audit_logging_enabled:
                score -= 10
            
            # Menaces récentes
            recent_threats = SecurityThreat.objects.filter(
                detected_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            score -= recent_threats * 5
            
            return max(0, score)
            
        except Exception as e:
            logger.error(f"Erreur calcul score sécurité: {e}")
            return 50

# Instance globale
security_service = SecurityService() 
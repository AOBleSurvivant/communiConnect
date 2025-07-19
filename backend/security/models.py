from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
import uuid
import json
import hashlib
import secrets
import pyotp
import qrcode
from typing import Dict, List, Optional, Tuple
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

logger = logging.getLogger(__name__)

User = get_user_model()

class SecurityConfig(models.Model):
    """Configuration de sécurité globale"""
    SECURITY_LEVELS = [
        ('basic', 'Basique'),
        ('standard', 'Standard'),
        ('advanced', 'Avancé'),
        ('enterprise', 'Enterprise'),
        ('military', 'Militaire'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    security_level = models.CharField(max_length=20, choices=SECURITY_LEVELS, default='standard')
    
    # Paramètres de sécurité
    password_min_length = models.IntegerField(default=8)
    password_require_uppercase = models.BooleanField(default=True)
    password_require_lowercase = models.BooleanField(default=True)
    password_require_numbers = models.BooleanField(default=True)
    password_require_special = models.BooleanField(default=True)
    password_expiry_days = models.IntegerField(default=90)
    max_login_attempts = models.IntegerField(default=5)
    lockout_duration_minutes = models.IntegerField(default=30)
    
    # MFA Configuration
    mfa_required = models.BooleanField(default=False)
    mfa_methods = models.JSONField(default=list)  # ['totp', 'sms', 'email', 'hardware']
    backup_codes_count = models.IntegerField(default=10)
    
    # Session Security
    session_timeout_minutes = models.IntegerField(default=60)
    max_concurrent_sessions = models.IntegerField(default=5)
    force_logout_on_password_change = models.BooleanField(default=True)
    
    # Encryption
    encryption_enabled = models.BooleanField(default=True)
    encryption_algorithm = models.CharField(max_length=50, default='AES-256')
    key_rotation_days = models.IntegerField(default=30)
    
    # Monitoring
    security_logging_enabled = models.BooleanField(default=True)
    anomaly_detection_enabled = models.BooleanField(default=True)
    threat_intelligence_enabled = models.BooleanField(default=False)
    
    # Compliance
    gdpr_compliant = models.BooleanField(default=True)
    data_retention_days = models.IntegerField(default=365)
    audit_logging_enabled = models.BooleanField(default=True)
    
    # Advanced Security
    rate_limiting_enabled = models.BooleanField(default=True)
    ip_whitelist = models.JSONField(default=list)
    ip_blacklist = models.JSONField(default=list)
    geo_restrictions = models.JSONField(default=list)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuration Sécurité"
        verbose_name_plural = "Configurations Sécurité"
    
    def __str__(self):
        return f"{self.name} ({self.get_security_level_display()})"

class UserSecurityProfile(models.Model):
    """Profil de sécurité utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # MFA Configuration
    mfa_enabled = models.BooleanField(default=False)
    mfa_method = models.CharField(max_length=20, default='totp')  # totp, sms, email, hardware
    totp_secret = models.CharField(max_length=32, blank=True)
    totp_verified = models.BooleanField(default=False)
    
    # Backup Codes
    backup_codes = models.JSONField(default=list)
    backup_codes_used = models.JSONField(default=list)
    
    # Password Security
    password_changed_at = models.DateTimeField(null=True, blank=True)
    password_history = models.JSONField(default=list)
    force_password_change = models.BooleanField(default=False)
    
    # Session Management
    active_sessions = models.JSONField(default=list)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_location = models.CharField(max_length=100, blank=True)
    last_login_device = models.CharField(max_length=200, blank=True)
    
    # Security Status
    account_locked = models.BooleanField(default=False)
    lockout_until = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    suspicious_activity_detected = models.BooleanField(default=False)
    
    # Trust Score
    trust_score = models.FloatField(default=100.0)  # 0-100
    risk_level = models.CharField(max_length=20, default='low')  # low, medium, high, critical
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil Sécurité Utilisateur"
        verbose_name_plural = "Profils Sécurité Utilisateur"
    
    def __str__(self):
        return f"Sécurité - {self.user.username}"
    
    def generate_totp_secret(self):
        """Génère un secret TOTP"""
        self.totp_secret = pyotp.random_base32()
        self.save()
        return self.totp_secret
    
    def get_totp_qr_code(self):
        """Génère le QR code pour TOTP"""
        if not self.totp_secret:
            self.generate_totp_secret()
        
        totp = pyotp.TOTP(self.totp_secret)
        provisioning_uri = totp.provisioning_uri(
            name=self.user.email,
            issuer_name="CommuniConnect"
        )
        
        # Générer QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")
    
    def verify_totp(self, token):
        """Vérifie un token TOTP"""
        if not self.totp_secret:
            return False
        
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(token)
    
    def generate_backup_codes(self, count=10):
        """Génère des codes de sauvegarde"""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()[:8]
            codes.append(code)
        
        self.backup_codes = codes
        self.save()
        return codes
    
    def verify_backup_code(self, code):
        """Vérifie un code de sauvegarde"""
        if code in self.backup_codes and code not in self.backup_codes_used:
            self.backup_codes_used.append(code)
            self.save()
            return True
        return False

class SecurityEvent(models.Model):
    """Événements de sécurité"""
    EVENT_TYPES = [
        ('login_success', 'Connexion Réussie'),
        ('login_failed', 'Connexion Échouée'),
        ('logout', 'Déconnexion'),
        ('password_change', 'Changement Mot de Passe'),
        ('password_reset', 'Réinitialisation Mot de Passe'),
        ('mfa_enabled', 'MFA Activé'),
        ('mfa_disabled', 'MFA Désactivé'),
        ('mfa_used', 'MFA Utilisé'),
        ('account_locked', 'Compte Verrouillé'),
        ('account_unlocked', 'Compte Déverrouillé'),
        ('suspicious_activity', 'Activité Suspecte'),
        ('ip_blocked', 'IP Bloquée'),
        ('geo_blocked', 'Géolocalisation Bloquée'),
        ('rate_limit_exceeded', 'Limite de Taux Dépassée'),
        ('data_access', 'Accès aux Données'),
        ('data_export', 'Export de Données'),
        ('data_deletion', 'Suppression de Données'),
        ('admin_action', 'Action Administrateur'),
        ('security_alert', 'Alerte Sécurité'),
        ('threat_detected', 'Menace Détectée'),
        ('compliance_violation', 'Violation Conformité'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='medium')
    
    # Détails de l'événement
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    device_info = models.JSONField(default=dict)
    
    # Contexte
    session_id = models.CharField(max_length=100, blank=True)
    request_path = models.CharField(max_length=200, blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    
    # Données supplémentaires
    metadata = models.JSONField(default=dict)
    threat_indicators = models.JSONField(default=list)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Événement Sécurité"
        verbose_name_plural = "Événements Sécurité"
        indexes = [
            models.Index(fields=['user', 'event_type', 'timestamp']),
            models.Index(fields=['event_type', 'severity', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.user.username if self.user else 'Anonymous'} - {self.timestamp}"

class SecurityThreat(models.Model):
    """Menaces de sécurité détectées"""
    THREAT_TYPES = [
        ('brute_force', 'Force Brute'),
        ('credential_stuffing', 'Credential Stuffing'),
        ('session_hijacking', 'Détournement Session'),
        ('sql_injection', 'Injection SQL'),
        ('xss', 'Cross-Site Scripting'),
        ('csrf', 'Cross-Site Request Forgery'),
        ('ddos', 'DDoS Attack'),
        ('malware', 'Malware'),
        ('phishing', 'Phishing'),
        ('social_engineering', 'Ingénierie Sociale'),
        ('data_exfiltration', 'Exfiltration Données'),
        ('privilege_escalation', 'Élévation Privilèges'),
        ('insider_threat', 'Menace Interne'),
        ('zero_day', 'Zero Day Exploit'),
        ('advanced_persistent_threat', 'Menace Persistante Avancée'),
    ]
    
    THREAT_LEVELS = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
        ('emergency', 'Urgence'),
    ]
    
    threat_type = models.CharField(max_length=50, choices=THREAT_TYPES)
    threat_level = models.CharField(max_length=20, choices=THREAT_LEVELS)
    
    # Détails de la menace
    title = models.CharField(max_length=200)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    
    # Source de la menace
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    source_location = models.CharField(max_length=100, blank=True)
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Impact
    affected_users = models.IntegerField(default=0)
    affected_systems = models.JSONField(default=list)
    data_compromised = models.BooleanField(default=False)
    
    # Réponse
    is_contained = models.BooleanField(default=False)
    containment_time = models.DateTimeField(null=True, blank=True)
    response_actions = models.JSONField(default=list)
    
    # Analyse
    indicators = models.JSONField(default=list)
    false_positive = models.BooleanField(default=False)
    analyst_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Menace Sécurité"
        verbose_name_plural = "Menaces Sécurité"
        indexes = [
            models.Index(fields=['threat_type', 'threat_level', 'detected_at']),
            models.Index(fields=['source_ip', 'detected_at']),
            models.Index(fields=['is_contained', 'threat_level']),
        ]
    
    def __str__(self):
        return f"{self.threat_type} - {self.title} - {self.detected_at}"

class SecurityPolicy(models.Model):
    """Politiques de sécurité"""
    POLICY_TYPES = [
        ('password', 'Politique Mots de Passe'),
        ('session', 'Politique Sessions'),
        ('access_control', 'Contrôle d\'Accès'),
        ('data_protection', 'Protection Données'),
        ('network_security', 'Sécurité Réseau'),
        ('incident_response', 'Réponse Incidents'),
        ('compliance', 'Conformité'),
        ('audit', 'Audit'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    policy_type = models.CharField(max_length=30, choices=POLICY_TYPES)
    description = models.TextField()
    
    # Règles de la politique
    rules = models.JSONField(default=dict)
    conditions = models.JSONField(default=list)
    actions = models.JSONField(default=list)
    
    # Application
    is_active = models.BooleanField(default=True)
    applies_to_all_users = models.BooleanField(default=True)
    user_groups = models.JSONField(default=list)
    exceptions = models.JSONField(default=list)
    
    # Priorité
    priority = models.IntegerField(default=100)
    override_other_policies = models.BooleanField(default=False)
    
    # Métadonnées
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Politique Sécurité"
        verbose_name_plural = "Politiques Sécurité"
        ordering = ['priority', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_policy_type_display()})"

class SecurityAudit(models.Model):
    """Audits de sécurité"""
    AUDIT_TYPES = [
        ('user_access', 'Accès Utilisateur'),
        ('data_access', 'Accès Données'),
        ('system_config', 'Configuration Système'),
        ('network_traffic', 'Trafic Réseau'),
        ('compliance_check', 'Vérification Conformité'),
        ('penetration_test', 'Test de Pénétration'),
        ('vulnerability_scan', 'Scan Vulnérabilités'),
        ('security_assessment', 'Évaluation Sécurité'),
    ]
    
    AUDIT_STATUS = [
        ('pending', 'En Attente'),
        ('in_progress', 'En Cours'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
    ]
    
    audit_type = models.CharField(max_length=30, choices=AUDIT_TYPES)
    status = models.CharField(max_length=20, choices=AUDIT_STATUS, default='pending')
    
    # Détails de l'audit
    title = models.CharField(max_length=200)
    description = models.TextField()
    scope = models.JSONField(default=dict)
    
    # Exécution
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Résultats
    findings = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    risk_score = models.FloatField(null=True, blank=True)
    
    # Exécuteur
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    automated = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Audit Sécurité"
        verbose_name_plural = "Audits Sécurité"
        indexes = [
            models.Index(fields=['audit_type', 'status', 'created_at']),
            models.Index(fields=['executed_by', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.audit_type} - {self.title} - {self.status}"

class EncryptionKey(models.Model):
    """Clés de chiffrement"""
    KEY_TYPES = [
        ('symmetric', 'Symétrique'),
        ('asymmetric', 'Asymétrique'),
        ('hash', 'Hash'),
        ('hmac', 'HMAC'),
    ]
    
    ALGORITHMS = [
        ('AES-256', 'AES-256'),
        ('RSA-2048', 'RSA-2048'),
        ('RSA-4096', 'RSA-4096'),
        ('ChaCha20', 'ChaCha20'),
        ('SHA-256', 'SHA-256'),
        ('SHA-512', 'SHA-512'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    key_type = models.CharField(max_length=20, choices=KEY_TYPES)
    algorithm = models.CharField(max_length=20, choices=ALGORITHMS)
    
    # Clé chiffrée
    encrypted_key = models.TextField()
    key_iv = models.TextField()  # Initialization Vector
    key_salt = models.TextField()  # Salt pour dérivation
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rotation_count = models.IntegerField(default=0)
    
    # Usage
    usage_count = models.IntegerField(default=0)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Clé Chiffrement"
        verbose_name_plural = "Clés Chiffrement"
    
    def __str__(self):
        return f"{self.name} ({self.algorithm})"
    
    def generate_key(self, password=None):
        """Génère une nouvelle clé"""
        if password:
            # Dérivation de clé à partir du mot de passe
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        else:
            # Génération de clé aléatoire
            key = Fernet.generate_key()
            salt = os.urandom(16)
        
        self.encrypted_key = key.decode()
        self.key_salt = base64.b64encode(salt).decode()
        self.save()
        
        return key
    
    def get_fernet(self):
        """Retourne l'objet Fernet pour chiffrement"""
        return Fernet(self.encrypted_key.encode())

class SecurityCompliance(models.Model):
    """Conformité de sécurité"""
    COMPLIANCE_FRAMEWORKS = [
        ('gdpr', 'RGPD'),
        ('iso27001', 'ISO 27001'),
        ('soc2', 'SOC 2'),
        ('pci_dss', 'PCI DSS'),
        ('hipaa', 'HIPAA'),
        ('sox', 'SOX'),
        ('nist', 'NIST'),
        ('cis', 'CIS Controls'),
    ]
    
    COMPLIANCE_STATUS = [
        ('compliant', 'Conforme'),
        ('non_compliant', 'Non Conforme'),
        ('partial', 'Partiellement Conforme'),
        ('not_applicable', 'Non Applicable'),
        ('under_review', 'En Révision'),
    ]
    
    framework = models.CharField(max_length=20, choices=COMPLIANCE_FRAMEWORKS)
    status = models.CharField(max_length=20, choices=COMPLIANCE_STATUS)
    
    # Détails de conformité
    requirement_id = models.CharField(max_length=100)
    requirement_title = models.CharField(max_length=200)
    requirement_description = models.TextField()
    
    # Évaluation
    assessment_date = models.DateTimeField(auto_now_add=True)
    assessed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    evidence = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    
    # Actions
    remediation_required = models.BooleanField(default=False)
    remediation_plan = models.TextField(blank=True)
    target_compliance_date = models.DateTimeField(null=True, blank=True)
    
    # Métadonnées
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Conformité Sécurité"
        verbose_name_plural = "Conformités Sécurité"
        indexes = [
            models.Index(fields=['framework', 'status']),
            models.Index(fields=['requirement_id', 'status']),
        ]
    
    def __str__(self):
        return f"{self.framework} - {self.requirement_id} - {self.status}"

class SecurityIncident(models.Model):
    """Incidents de sécurité"""
    INCIDENT_TYPES = [
        ('data_breach', 'Fuite de Données'),
        ('unauthorized_access', 'Accès Non Autorisé'),
        ('malware_infection', 'Infection Malware'),
        ('ddos_attack', 'Attaque DDoS'),
        ('phishing_attempt', 'Tentative Phishing'),
        ('social_engineering', 'Ingénierie Sociale'),
        ('physical_security', 'Sécurité Physique'),
        ('insider_threat', 'Menace Interne'),
        ('system_compromise', 'Compromission Système'),
        ('network_intrusion', 'Intrusion Réseau'),
    ]
    
    INCIDENT_SEVERITY = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
        ('catastrophic', 'Catastrophique'),
    ]
    
    INCIDENT_STATUS = [
        ('detected', 'Détecté'),
        ('investigating', 'En Investigation'),
        ('contained', 'Contenu'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]
    
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPES)
    severity = models.CharField(max_length=20, choices=INCIDENT_SEVERITY)
    status = models.CharField(max_length=20, choices=INCIDENT_STATUS, default='detected')
    
    # Détails de l'incident
    title = models.CharField(max_length=200)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    
    # Impact
    affected_users = models.IntegerField(default=0)
    affected_systems = models.JSONField(default=list)
    data_compromised = models.BooleanField(default=False)
    financial_impact = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Réponse
    response_team = models.JSONField(default=list)
    containment_time = models.DateTimeField(null=True, blank=True)
    resolution_time = models.DateTimeField(null=True, blank=True)
    actions_taken = models.JSONField(default=list)
    
    # Investigation
    root_cause = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    prevention_measures = models.JSONField(default=list)
    
    # Métadonnées
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_incidents')
    
    class Meta:
        verbose_name = "Incident Sécurité"
        verbose_name_plural = "Incidents Sécurité"
        indexes = [
            models.Index(fields=['incident_type', 'severity', 'status']),
            models.Index(fields=['detected_at', 'status']),
        ]
    
    def __str__(self):
        return f"{self.incident_type} - {self.title} - {self.severity}" 
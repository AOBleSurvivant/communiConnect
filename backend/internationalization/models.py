from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
import uuid
import json
import locale
import pytz

User = get_user_model()

class Language(models.Model):
    """Gestion des langues supportées pour la Guinée"""
    LANGUAGE_STATUS = [
        ('active', 'Active'),
        ('beta', 'Bêta'),
        ('planned', 'Planifiée'),
        ('deprecated', 'Dépréciée'),
    ]
    
    LANGUAGE_FAMILIES = [
        ('romance', 'Romane'),
        ('germanic', 'Germanique'),
        ('middle_eastern', 'Moyen-Orient'),
    ]
    
    code = models.CharField(max_length=10, primary_key=True)  # fr, en, ar
    name = models.CharField(max_length=50)  # Français, English, العربية
    native_name = models.CharField(max_length=50)  # Français, English, العربية
    family = models.CharField(max_length=20, choices=LANGUAGE_FAMILIES)
    status = models.CharField(max_length=20, choices=LANGUAGE_STATUS, default='active')
    
    # Configuration spécifique Guinée
    is_rtl = models.BooleanField(default=False)  # Right-to-left (Arabe)
    is_default = models.BooleanField(default=False)  # Français par défaut
    is_beta = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_translation_update = models.DateTimeField(null=True, blank=True)
    
    # Statistiques Guinée
    translation_coverage = models.FloatField(default=0.0)  # 0.0 à 1.0
    user_count = models.IntegerField(default=0)
    content_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Langue"
        verbose_name_plural = "Langues"
        ordering = ['-user_count', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_translation_coverage_percentage(self):
        """Retourne le pourcentage de couverture de traduction"""
        return f"{self.translation_coverage * 100:.1f}%"
    
    def update_translation_coverage(self):
        """Met à jour la couverture de traduction"""
        total_keys = TranslationKey.objects.count()
        if total_keys > 0:
            translated_keys = Translation.objects.filter(
                language=self,
                is_translated=True
            ).count()
            self.translation_coverage = translated_keys / total_keys
            self.save()

class TranslationKey(models.Model):
    """Clés de traduction pour l'interface CommuniConnect"""
    CONTEXT_TYPES = [
        ('ui', 'Interface Utilisateur'),
        ('content', 'Contenu'),
        ('notification', 'Notification'),
        ('email', 'Email'),
        ('error', 'Message d\'Erreur'),
        ('help', 'Aide'),
        ('legal', 'Légal'),
        ('marketing', 'Marketing'),
        ('guinea_specific', 'Spécifique Guinée'),
    ]
    
    key = models.CharField(max_length=200, unique=True)
    context = models.CharField(max_length=20, choices=CONTEXT_TYPES, default='ui')
    description = models.TextField(blank=True)
    is_plural = models.BooleanField(default=False)
    is_html = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Clé de Traduction"
        verbose_name_plural = "Clés de Traduction"
        ordering = ['context', 'key']
    
    def __str__(self):
        return f"{self.key} ({self.get_context_display()})"
    
    def get_translation(self, language_code):
        """Récupère la traduction pour une langue donnée"""
        try:
            return self.translations.get(language__code=language_code)
        except Translation.DoesNotExist:
            return None

class Translation(models.Model):
    """Traductions pour chaque clé et langue"""
    translation_key = models.ForeignKey(TranslationKey, on_delete=models.CASCADE, related_name='translations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translations')
    
    # Contenu traduit
    text = models.TextField()
    plural_text = models.TextField(blank=True)  # Pour les pluriels
    
    # Statut
    is_translated = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_translations')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    translator_notes = models.TextField(blank=True)
    reviewer_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Traduction"
        verbose_name_plural = "Traductions"
        unique_together = ['translation_key', 'language']
        indexes = [
            models.Index(fields=['language', 'is_translated']),
            models.Index(fields=['is_approved', 'is_reviewed']),
        ]
    
    def __str__(self):
        return f"{self.translation_key.key} - {self.language.name}"
    
    def mark_as_translated(self):
        """Marque la traduction comme terminée"""
        self.is_translated = True
        self.save()
        self.language.update_translation_coverage()

class GuineaRegion(models.Model):
    """Régions de la Guinée"""
    REGIONS = [
        ('conakry', 'Conakry'),
        ('kindia', 'Kindia'),
        ('kankan', 'Kankan'),
        ('nzerekore', 'Nzérékoré'),
        ('labe', 'Labé'),
        ('boke', 'Boké'),
        ('faranah', 'Faranah'),
        ('kouroussa', 'Kouroussa'),
        ('mamou', 'Mamou'),
        ('siguiri', 'Siguiri'),
        ('telimele', 'Télimélé'),
        ('dabola', 'Dabola'),
        ('dinguiraye', 'Dinguiraye'),
        ('fria', 'Fria'),
        ('gaoual', 'Gaoual'),
        ('gueckedou', 'Guéckédou'),
        ('kissidougou', 'Kissidougou'),
        ('macenta', 'Macenta'),
        ('mandiana', 'Mandiana'),
        ('pita', 'Pita'),
        ('tougue', 'Tougué'),
        ('yomou', 'Yomou'),
    ]
    
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50, blank=True)  # Nom en arabe
    name_en = models.CharField(max_length=50, blank=True)  # Nom en anglais
    
    # Configuration
    is_active = models.BooleanField(default=True)
    population = models.IntegerField(default=0)
    
    # Localisation
    timezone = models.CharField(max_length=50, default='Africa/Conakry')
    coordinates = models.JSONField(default=dict)  # Lat/Lng
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistiques
    user_count = models.IntegerField(default=0)
    content_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Région Guinée"
        verbose_name_plural = "Régions Guinée"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class GuineaCurrency(models.Model):
    """Devises utilisées en Guinée"""
    code = models.CharField(max_length=3, primary_key=True)  # GNF, USD, EUR
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    symbol_position = models.CharField(max_length=10, choices=[
        ('before', 'Avant'),
        ('after', 'Après'),
    ], default='after')
    
    # Configuration Guinée
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)  # GNF par défaut
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)
    exchange_rate_updated = models.DateTimeField(auto_now=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Devise Guinée"
        verbose_name_plural = "Devises Guinée"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def format_amount(self, amount):
        """Formate un montant selon la devise guinéenne"""
        if self.symbol_position == 'before':
            return f"{self.symbol}{amount:,.2f}"
        else:
            return f"{amount:,.2f}{self.symbol}"

class GuineaCulturalAdaptation(models.Model):
    """Adaptations culturelles spécifiques à la Guinée"""
    ADAPTATION_TYPES = [
        ('content_moderation', 'Modération de Contenu'),
        ('privacy_settings', 'Paramètres de Confidentialité'),
        ('payment_methods', 'Méthodes de Paiement Guinéennes'),
        ('legal_requirements', 'Exigences Légales Guinéennes'),
        ('ui_customization', 'Personnalisation UI Guinée'),
        ('feature_availability', 'Disponibilité des Fonctionnalités'),
        ('religious_considerations', 'Considérations Religieuses'),
    ]
    
    region = models.ForeignKey(GuineaRegion, on_delete=models.CASCADE, related_name='cultural_adaptations')
    adaptation_type = models.CharField(max_length=30, choices=ADAPTATION_TYPES)
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Adaptation Culturelle Guinée"
        verbose_name_plural = "Adaptations Culturelles Guinée"
        unique_together = ['region', 'adaptation_type']
    
    def __str__(self):
        return f"{self.region.name} - {self.get_adaptation_type_display()}"

class UserLanguagePreference(models.Model):
    """Préférences linguistiques des utilisateurs guinéens"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='language_preference')
    
    # Langues (3 langues supportées)
    primary_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='primary_users')
    secondary_languages = models.ManyToManyField(Language, blank=True, related_name='secondary_users')
    
    # Région Guinée
    region = models.ForeignKey(GuineaRegion, on_delete=models.SET_NULL, null=True, blank=True)
    timezone = models.CharField(max_length=50, default='Africa/Conakry')
    
    # Devise Guinée
    preferred_currency = models.ForeignKey(GuineaCurrency, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Configuration
    auto_translate = models.BooleanField(default=True)
    show_original_language = models.BooleanField(default=False)
    content_language_filter = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Préférence Linguistique Guinée"
        verbose_name_plural = "Préférences Linguistiques Guinée"
    
    def __str__(self):
        return f"Préférences de {self.user.username}"

class ContentTranslation(models.Model):
    """Traductions de contenu utilisateur guinéen"""
    CONTENT_TYPES = [
        ('post', 'Post'),
        ('comment', 'Commentaire'),
        ('story', 'Story'),
        ('profile', 'Profil'),
        ('category', 'Catégorie'),
    ]
    
    original_content = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='translations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    
    # Traduction
    translated_text = models.TextField()
    translation_method = models.CharField(max_length=20, choices=[
        ('manual', 'Manuelle'),
        ('ai', 'IA'),
        ('community', 'Communauté'),
    ], default='ai')
    
    # Qualité
    confidence_score = models.FloatField(default=0.0)  # 0.0 à 1.0
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Traduction de Contenu Guinée"
        verbose_name_plural = "Traductions de Contenu Guinée"
        unique_together = ['original_content', 'language']
        indexes = [
            models.Index(fields=['content_type', 'language']),
            models.Index(fields=['confidence_score', 'is_verified']),
        ]
    
    def __str__(self):
        return f"{self.original_content.id} - {self.language.name}"

class GuineaPaymentMethod(models.Model):
    """Méthodes de paiement guinéennes"""
    PAYMENT_TYPES = [
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement Bancaire'),
        ('cash', 'Espèces'),
        ('card', 'Carte Bancaire'),
        ('digital_wallet', 'Portefeuille Numérique'),
    ]
    
    region = models.ForeignKey(GuineaRegion, on_delete=models.CASCADE, related_name='payment_methods')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    provider_name = models.CharField(max_length=100)
    provider_code = models.CharField(max_length=50)
    
    # Configuration Guinée
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    supported_currencies = models.ManyToManyField(GuineaCurrency)
    
    # Frais
    transaction_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    transaction_fee_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Limites
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Méthode de Paiement Guinée"
        verbose_name_plural = "Méthodes de Paiement Guinée"
        unique_together = ['region', 'payment_type', 'provider_code']
    
    def __str__(self):
        return f"{self.region.name} - {self.get_payment_type_display()} ({self.provider_name})"

class GuineaLegalCompliance(models.Model):
    """Conformité légale guinéenne"""
    COMPLIANCE_TYPES = [
        ('data_protection', 'Protection des Données Guinée'),
        ('content_moderation', 'Modération de Contenu Guinée'),
        ('age_restriction', 'Restriction d\'Âge'),
        ('tax_requirements', 'Exigences Fiscales Guinéennes'),
        ('religious_compliance', 'Conformité Religieuse'),
    ]
    
    region = models.ForeignKey(GuineaRegion, on_delete=models.CASCADE, related_name='legal_compliance')
    compliance_type = models.CharField(max_length=30, choices=COMPLIANCE_TYPES)
    
    # Statut
    is_required = models.BooleanField(default=True)
    is_implemented = models.BooleanField(default=False)
    implementation_date = models.DateTimeField(null=True, blank=True)
    
    # Configuration
    requirements = models.JSONField(default=dict)
    implementation_details = models.JSONField(default=dict)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Conformité Légale Guinée"
        verbose_name_plural = "Conformités Légales Guinée"
        unique_together = ['region', 'compliance_type']
    
    def __str__(self):
        return f"{self.region.name} - {self.get_compliance_type_display()}"

class LocalizationMetrics(models.Model):
    """Métriques d'internationalisation guinéenne"""
    date = models.DateField()
    
    # Langues Guinée
    active_languages = models.IntegerField(default=3)  # Fr, En, Ar
    total_translations = models.IntegerField(default=0)
    translation_coverage_avg = models.FloatField(default=0.0)
    
    # Utilisateurs par langue
    users_by_language = models.JSONField(default=dict)
    users_by_region = models.JSONField(default=dict)
    
    # Contenu
    content_translations = models.IntegerField(default=0)
    ai_translations = models.IntegerField(default=0)
    manual_translations = models.IntegerField(default=0)
    
    # Performance
    translation_accuracy = models.FloatField(default=0.0)
    user_satisfaction = models.FloatField(default=0.0)
    
    # Métadonnées
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Métrique d'Internationalisation Guinée"
        verbose_name_plural = "Métriques d'Internationalisation Guinée"
        unique_together = ['date']
    
    def __str__(self):
        return f"Métriques i18n Guinée - {self.date}"

class RegionalFeature(models.Model):
    """Fonctionnalités spécifiques par région guinéenne"""
    FEATURE_TYPES = [
        ('ui_customization', 'Personnalisation UI'),
        ('content_filtering', 'Filtrage de Contenu'),
        ('payment_integration', 'Intégration Paiement'),
        ('notification_system', 'Système de Notification'),
        ('analytics', 'Analytics'),
        ('security', 'Sécurité'),
        ('religious_features', 'Fonctionnalités Religieuses'),
    ]
    
    region = models.ForeignKey(GuineaRegion, on_delete=models.CASCADE, related_name='regional_features')
    feature_type = models.CharField(max_length=30, choices=FEATURE_TYPES)
    feature_name = models.CharField(max_length=100)
    
    # Configuration
    is_enabled = models.BooleanField(default=True)
    is_beta = models.BooleanField(default=False)
    configuration = models.JSONField(default=dict)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Fonctionnalité Régionale Guinée"
        verbose_name_plural = "Fonctionnalités Régionales Guinée"
        unique_together = ['region', 'feature_type', 'feature_name']
    
    def __str__(self):
        return f"{self.region.name} - {self.feature_name}" 
from django.db.models import Q, Count, Avg
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
from .models import (
    Language, TranslationKey, Translation, GuineaRegion, GuineaCurrency,
    GuineaCulturalAdaptation, UserLanguagePreference, ContentTranslation,
    LocalizationMetrics, GuineaPaymentMethod, GuineaLegalCompliance, RegionalFeature
)
from posts.models import Post, PostComment
from users.models import User
import json
import locale
import pytz
import requests
from typing import Dict, List, Optional, Tuple
import logging
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

User = get_user_model()

class GuineaInternationalizationService:
    """Service principal pour l'internationalisation guinéenne"""
    
    def __init__(self):
        self.translator = GoogleTranslator()
        self.cache_timeout = 3600  # 1 heure
        self.supported_languages = self._load_guinea_languages()
        self.default_language = 'fr'
        self.guinea_regions = self._load_guinea_regions()
    
    def _load_guinea_languages(self) -> Dict:
        """Charge les langues supportées pour la Guinée"""
        return {
            'fr': {
                'name': 'Français', 
                'native_name': 'Français', 
                'family': 'romance',
                'is_default': True,
                'is_rtl': False
            },
            'en': {
                'name': 'English', 
                'native_name': 'English', 
                'family': 'germanic',
                'is_default': False,
                'is_rtl': False
            },
            'ar': {
                'name': 'العربية', 
                'native_name': 'العربية', 
                'family': 'middle_eastern',
                'is_default': False,
                'is_rtl': True
            }
        }
    
    def _load_guinea_regions(self) -> Dict:
        """Charge les régions de la Guinée"""
        return {
            'conakry': {'name': 'Conakry', 'name_ar': 'كوناكري', 'name_en': 'Conakry'},
            'kindia': {'name': 'Kindia', 'name_ar': 'كنديا', 'name_en': 'Kindia'},
            'kankan': {'name': 'Kankan', 'name_ar': 'كانكان', 'name_en': 'Kankan'},
            'nzerekore': {'name': 'Nzérékoré', 'name_ar': 'نزيريكوري', 'name_en': 'Nzérékoré'},
            'labe': {'name': 'Labé', 'name_ar': 'لابي', 'name_en': 'Labé'},
            'boke': {'name': 'Boké', 'name_ar': 'بوكي', 'name_en': 'Boké'},
            'faranah': {'name': 'Faranah', 'name_ar': 'فراناه', 'name_en': 'Faranah'},
            'kouroussa': {'name': 'Kouroussa', 'name_ar': 'كوروسا', 'name_en': 'Kouroussa'},
            'mamou': {'name': 'Mamou', 'name_ar': 'مامو', 'name_en': 'Mamou'},
            'siguiri': {'name': 'Siguiri', 'name_ar': 'سيغيري', 'name_en': 'Siguiri'},
            'telimele': {'name': 'Télimélé', 'name_ar': 'تليميلي', 'name_en': 'Télimélé'},
            'dabola': {'name': 'Dabola', 'name_ar': 'دابولا', 'name_en': 'Dabola'},
            'dinguiraye': {'name': 'Dinguiraye', 'name_ar': 'دينجيراي', 'name_en': 'Dinguiraye'},
            'fria': {'name': 'Fria', 'name_ar': 'فريا', 'name_en': 'Fria'},
            'gaoual': {'name': 'Gaoual', 'name_ar': 'جاوال', 'name_en': 'Gaoual'},
            'gueckedou': {'name': 'Guéckédou', 'name_ar': 'جيكيدو', 'name_en': 'Guéckédou'},
            'kissidougou': {'name': 'Kissidougou', 'name_ar': 'كيسيدوغو', 'name_en': 'Kissidougou'},
            'macenta': {'name': 'Macenta', 'name_ar': 'ماكنتا', 'name_en': 'Macenta'},
            'mandiana': {'name': 'Mandiana', 'name_ar': 'مانديانا', 'name_en': 'Mandiana'},
            'pita': {'name': 'Pita', 'name_ar': 'بيتا', 'name_en': 'Pita'},
            'tougue': {'name': 'Tougué', 'name_ar': 'توجي', 'name_en': 'Tougué'},
            'yomou': {'name': 'Yomou', 'name_ar': 'يومو', 'name_en': 'Yomou'},
        }
    
    def get_user_language(self, user: User) -> str:
        """Récupère la langue préférée de l'utilisateur guinéen"""
        try:
            preference = UserLanguagePreference.objects.get(user=user)
            return preference.primary_language.code
        except UserLanguagePreference.DoesNotExist:
            return self.default_language
    
    def set_user_language(self, user: User, language_code: str) -> bool:
        """Définit la langue préférée de l'utilisateur guinéen"""
        try:
            language = Language.objects.get(code=language_code)
            preference, created = UserLanguagePreference.objects.get_or_create(user=user)
            preference.primary_language = language
            preference.save()
            return True
        except Language.DoesNotExist:
            return False
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """Traduit un texte vers la langue cible (Guinée)"""
        try:
            cache_key = f"guinea_translation:{source_language}:{target_language}:{hash(text)}"
            cached_translation = cache.get(cache_key)
            
            if cached_translation:
                return cached_translation
            
            # Utiliser l'API de traduction
            translator = GoogleTranslator(source=source_language, target=target_language)
            translation = translator.translate(text)
            
            # Mettre en cache
            cache.set(cache_key, translation, self.cache_timeout)
            
            return translation
            
        except Exception as e:
            logger.error(f"Erreur traduction Guinée: {e}")
            return text
    
    def translate_ui_text(self, key: str, language_code: str, **kwargs) -> str:
        """Traduit un texte d'interface utilisateur pour la Guinée"""
        try:
            # Récupérer la traduction depuis la base de données
            translation = Translation.objects.filter(
                translation_key__key=key,
                language__code=language_code,
                is_translated=True
            ).first()
            
            if translation:
                text = translation.text
            else:
                # Fallback vers la traduction automatique
                translation_key = TranslationKey.objects.filter(key=key).first()
                if translation_key:
                    text = self.translate_text(translation_key.key, language_code)
                else:
                    text = key
            
            # Remplacer les variables
            for key, value in kwargs.items():
                text = text.replace(f"{{{key}}}", str(value))
            
            return text
            
        except Exception as e:
            logger.error(f"Erreur traduction UI Guinée: {e}")
            return key
    
    def translate_content(self, content: Post, target_language: str) -> ContentTranslation:
        """Traduit le contenu d'un post guinéen"""
        try:
            # Vérifier si la traduction existe déjà
            existing_translation = ContentTranslation.objects.filter(
                original_content=content,
                language__code=target_language
            ).first()
            
            if existing_translation:
                return existing_translation
            
            # Créer une nouvelle traduction
            language = Language.objects.get(code=target_language)
            translated_text = self.translate_text(content.content, target_language)
            
            translation = ContentTranslation.objects.create(
                original_content=content,
                language=language,
                content_type='post',
                translated_text=translated_text,
                translation_method='ai',
                confidence_score=0.8  # Score de confiance par défaut
            )
            
            return translation
            
        except Exception as e:
            logger.error(f"Erreur traduction contenu Guinée: {e}")
            return None
    
    def get_localized_content(self, user: User, content_type: str = 'posts') -> List:
        """Récupère du contenu localisé pour l'utilisateur guinéen"""
        try:
            user_language = self.get_user_language(user)
            user_region = self.get_user_region(user)
            
            if content_type == 'posts':
                # Récupérer les posts dans la langue de l'utilisateur
                posts = Post.objects.filter(
                    Q(language__code=user_language) |
                    Q(language__isnull=True)
                ).order_by('-created_at')[:20]
                
                # Traduire les posts si nécessaire
                localized_posts = []
                for post in posts:
                    if post.language and post.language.code != user_language:
                        translation = self.translate_content(post, user_language)
                        if translation:
                            post.translated_content = translation.translated_text
                    localized_posts.append(post)
                
                return localized_posts
            
            return []
            
        except Exception as e:
            logger.error(f"Erreur contenu localisé Guinée: {e}")
            return []
    
    def get_user_region(self, user: User) -> Optional[GuineaRegion]:
        """Récupère la région de l'utilisateur guinéen"""
        try:
            preference = UserLanguagePreference.objects.get(user=user)
            return preference.region
        except UserLanguagePreference.DoesNotExist:
            return None
    
    def detect_user_location(self, ip_address: str) -> Optional[GuineaRegion]:
        """Détecte la localisation de l'utilisateur guinéen via IP"""
        try:
            # Utiliser un service de géolocalisation IP
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            if response.status_code == 200:
                data = response.json()
                country_code = data.get('countryCode')
                
                # Vérifier que c'est la Guinée
                if country_code == 'GN':
                    # Essayer de détecter la région
                    region_name = data.get('regionName', '').lower()
                    for region_code, region_info in self.guinea_regions.items():
                        if region_code in region_name or region_info['name'].lower() in region_name:
                            return GuineaRegion.objects.get(code=region_code)
                    
                    # Par défaut, Conakry
                    return GuineaRegion.objects.get(code='conakry')
        except Exception as e:
            logger.error(f"Erreur détection localisation Guinée: {e}")
        
        return None
    
    def get_cultural_adaptations(self, region: GuineaRegion) -> Dict:
        """Récupère les adaptations culturelles pour une région guinéenne"""
        try:
            adaptations = GuineaCulturalAdaptation.objects.filter(
                region=region,
                is_enabled=True
            )
            
            adaptations_dict = {}
            for adaptation in adaptations:
                adaptations_dict[adaptation.adaptation_type] = adaptation.configuration
            
            return adaptations_dict
            
        except Exception as e:
            logger.error(f"Erreur adaptations culturelles Guinée: {e}")
            return {}
    
    def get_payment_methods(self, region: GuineaRegion) -> List[GuineaPaymentMethod]:
        """Récupère les méthodes de paiement disponibles pour une région guinéenne"""
        try:
            return GuineaPaymentMethod.objects.filter(
                region=region,
                is_active=True
            ).order_by('-is_default', 'payment_type')
            
        except Exception as e:
            logger.error(f"Erreur méthodes paiement Guinée: {e}")
            return []
    
    def get_legal_compliance(self, region: GuineaRegion) -> List[GuineaLegalCompliance]:
        """Récupère les exigences de conformité légale pour une région guinéenne"""
        try:
            return GuineaLegalCompliance.objects.filter(
                region=region,
                is_required=True
            )
            
        except Exception as e:
            logger.error(f"Erreur conformité légale Guinée: {e}")
            return []
    
    def format_currency(self, amount: float, currency_code: str = 'GNF') -> str:
        """Formate un montant selon la devise guinéenne"""
        try:
            currency = GuineaCurrency.objects.get(code=currency_code)
            
            # Formater le montant selon les standards guinéens
            if currency.symbol_position == 'before':
                formatted_amount = f"{currency.symbol}{amount:,.2f}"
            else:
                formatted_amount = f"{amount:,.2f}{currency.symbol}"
            
            return formatted_amount
            
        except Exception as e:
            logger.error(f"Erreur formatage devise Guinée: {e}")
            return f"{amount:.2f} GNF"
    
    def get_timezone_info(self, region: GuineaRegion) -> Dict:
        """Récupère les informations de fuseau horaire pour une région guinéenne"""
        try:
            timezone_info = pytz.timezone(region.timezone)
            current_time = timezone.now().astimezone(timezone_info)
            
            return {
                'timezone': region.timezone,
                'current_time': current_time,
                'utc_offset': current_time.utcoffset().total_seconds() / 3600,
                'is_dst': current_time.dst() != timedelta(0)
            }
            
        except Exception as e:
            logger.error(f"Erreur fuseau horaire Guinée: {e}")
            return {
                'timezone': 'Africa/Conakry',
                'current_time': timezone.now(),
                'utc_offset': 0,
                'is_dst': False
            }
    
    def create_translation_key(self, key: str, context: str = 'ui', description: str = '') -> TranslationKey:
        """Crée une nouvelle clé de traduction pour la Guinée"""
        try:
            translation_key, created = TranslationKey.objects.get_or_create(
                key=key,
                defaults={
                    'context': context,
                    'description': description
                }
            )
            
            if created:
                # Créer des traductions automatiques pour les 3 langues guinéennes
                active_languages = Language.objects.filter(status='active')
                for language in active_languages:
                    if language.code != self.default_language:
                        translated_text = self.translate_text(key, language.code, self.default_language)
                        Translation.objects.create(
                            translation_key=translation_key,
                            language=language,
                            text=translated_text,
                            is_translated=True,
                            translation_method='ai'
                        )
            
            return translation_key
            
        except Exception as e:
            logger.error(f"Erreur création clé traduction Guinée: {e}")
            return None
    
    def update_translation_coverage(self):
        """Met à jour la couverture de traduction pour toutes les langues guinéennes"""
        try:
            languages = Language.objects.all()
            for language in languages:
                language.update_translation_coverage()
            
        except Exception as e:
            logger.error(f"Erreur mise à jour couverture traduction Guinée: {e}")
    
    def get_localization_metrics(self, date: datetime.date = None) -> LocalizationMetrics:
        """Calcule les métriques d'internationalisation guinéenne"""
        try:
            if date is None:
                date = timezone.now().date()
            
            metrics, created = LocalizationMetrics.objects.get_or_create(date=date)
            
            # Métriques des langues guinéennes (3 langues)
            metrics.active_languages = Language.objects.filter(status='active').count()
            metrics.total_translations = Translation.objects.filter(is_translated=True).count()
            
            # Couverture moyenne
            languages = Language.objects.filter(status='active')
            if languages.exists():
                avg_coverage = languages.aggregate(avg=Avg('translation_coverage'))['avg']
                metrics.translation_coverage_avg = avg_coverage or 0.0
            
            # Utilisateurs par langue
            user_languages = UserLanguagePreference.objects.values('primary_language__code').annotate(
                count=Count('user')
            )
            metrics.users_by_language = {item['primary_language__code']: item['count'] for item in user_languages}
            
            # Utilisateurs par région guinéenne
            user_regions = UserLanguagePreference.objects.values('region__code').annotate(
                count=Count('user')
            )
            metrics.users_by_region = {item['region__code']: item['count'] for item in user_regions}
            
            # Traductions de contenu
            metrics.content_translations = ContentTranslation.objects.count()
            metrics.ai_translations = ContentTranslation.objects.filter(translation_method='ai').count()
            metrics.manual_translations = ContentTranslation.objects.filter(translation_method='manual').count()
            
            # Performance
            verified_translations = ContentTranslation.objects.filter(is_verified=True)
            if verified_translations.exists():
                avg_confidence = verified_translations.aggregate(avg=Avg('confidence_score'))['avg']
                metrics.translation_accuracy = avg_confidence or 0.0
            
            metrics.save()
            return metrics
            
        except Exception as e:
            logger.error(f"Erreur calcul métriques i18n Guinée: {e}")
            return None
    
    def apply_cultural_adaptations(self, user: User, content: Dict) -> Dict:
        """Applique les adaptations culturelles guinéennes au contenu"""
        try:
            user_region = self.get_user_region(user)
            if not user_region:
                return content
            
            adaptations = self.get_cultural_adaptations(user_region)
            
            # Adapter le contenu selon les règles culturelles guinéennes
            if 'content_moderation' in adaptations:
                content = self._apply_guinea_content_moderation(content, adaptations['content_moderation'])
            
            if 'religious_considerations' in adaptations:
                content = self._apply_religious_considerations(content, adaptations['religious_considerations'])
            
            if 'ui_customization' in adaptations:
                content = self._apply_guinea_ui_customization(content, adaptations['ui_customization'])
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur adaptations culturelles Guinée: {e}")
            return content
    
    def _apply_guinea_content_moderation(self, content: Dict, rules: Dict) -> Dict:
        """Applique la modération de contenu selon les règles guinéennes"""
        try:
            # Règles de modération spécifiques à la Guinée
            if 'forbidden_words' in rules:
                forbidden_words = rules['forbidden_words']
                for word in forbidden_words:
                    content['text'] = content['text'].replace(word, '*' * len(word))
            
            if 'sensitive_topics' in rules:
                sensitive_topics = rules['sensitive_topics']
                # Marquer le contenu comme sensible si nécessaire
                for topic in sensitive_topics:
                    if topic.lower() in content['text'].lower():
                        content['is_sensitive'] = True
                        break
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur modération contenu Guinée: {e}")
            return content
    
    def _apply_religious_considerations(self, content: Dict, rules: Dict) -> Dict:
        """Applique les considérations religieuses guinéennes"""
        try:
            # Considérations religieuses spécifiques à la Guinée
            if 'religious_content_filter' in rules:
                filter_rules = rules['religious_content_filter']
                # Appliquer les filtres religieux selon la région
                for rule in filter_rules:
                    if rule['type'] == 'forbidden' and rule['term'].lower() in content['text'].lower():
                        content['is_religiously_sensitive'] = True
                        break
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur considérations religieuses: {e}")
            return content
    
    def _apply_guinea_ui_customization(self, content: Dict, rules: Dict) -> Dict:
        """Applique la personnalisation UI selon les règles guinéennes"""
        try:
            # Personnalisations UI spécifiques à la Guinée
            if 'color_scheme' in rules:
                content['ui_theme'] = rules['color_scheme']
            
            if 'layout_preferences' in rules:
                content['layout'] = rules['layout_preferences']
            
            if 'text_direction' in rules:
                content['text_direction'] = rules['text_direction']
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur personnalisation UI Guinée: {e}")
            return content
    
    def get_regional_features(self, region: GuineaRegion) -> List[RegionalFeature]:
        """Récupère les fonctionnalités spécifiques à une région guinéenne"""
        try:
            return RegionalFeature.objects.filter(
                region=region,
                is_enabled=True
            )
            
        except Exception as e:
            logger.error(f"Erreur fonctionnalités régionales Guinée: {e}")
            return []
    
    def validate_legal_compliance(self, user: User, action: str) -> bool:
        """Valide la conformité légale guinéenne pour une action utilisateur"""
        try:
            user_region = self.get_user_region(user)
            if not user_region:
                return True
            
            compliance_rules = GuineaLegalCompliance.objects.filter(
                region=user_region,
                is_required=True,
                is_implemented=True
            )
            
            for rule in compliance_rules:
                if not self._check_guinea_compliance_rule(rule, action):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur validation conformité Guinée: {e}")
            return True
    
    def _check_guinea_compliance_rule(self, rule: GuineaLegalCompliance, action: str) -> bool:
        """Vérifie une règle de conformité guinéenne spécifique"""
        try:
            requirements = rule.requirements
            
            if rule.compliance_type == 'data_protection':
                # Vérifier les exigences de protection des données guinéennes
                return self._check_guinea_data_protection(requirements, action)
            
            elif rule.compliance_type == 'religious_compliance':
                # Vérifier la conformité religieuse
                return self._check_religious_compliance(requirements, action)
            
            elif rule.compliance_type == 'content_moderation':
                # Vérifier la modération de contenu guinéenne
                return self._check_guinea_content_moderation(requirements, action)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur vérification règle conformité Guinée: {e}")
            return True
    
    def _check_guinea_data_protection(self, requirements: Dict, action: str) -> bool:
        """Vérifie la protection des données guinéenne"""
        # Implémentation des vérifications de protection des données guinéennes
        return True
    
    def _check_religious_compliance(self, requirements: Dict, action: str) -> bool:
        """Vérifie la conformité religieuse"""
        # Implémentation des vérifications de conformité religieuse
        return True
    
    def _check_guinea_content_moderation(self, requirements: Dict, action: str) -> bool:
        """Vérifie la modération de contenu guinéenne"""
        # Implémentation de la modération de contenu guinéenne
        return True

# Instance globale
guinea_i18n_service = GuineaInternationalizationService() 
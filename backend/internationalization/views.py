from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from .models import (
    Language, TranslationKey, Translation, Country, Currency,
    CulturalAdaptation, UserLanguagePreference, ContentTranslation,
    LocalizationMetrics, PaymentMethod, LegalCompliance, RegionalFeature
)
from .services import i18n_service
from posts.models import Post
from users.models import User
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

User = get_user_model()

@api_view(['GET'])
def get_supported_languages(request):
    """
    Endpoint pour récupérer les langues supportées
    """
    try:
        languages = Language.objects.filter(status='active').order_by('-user_count', 'name')
        
        languages_data = []
        for language in languages:
            languages_data.append({
                'code': language.code,
                'name': language.name,
                'native_name': language.native_name,
                'family': language.family,
                'is_rtl': language.is_rtl,
                'is_default': language.is_default,
                'translation_coverage': language.get_translation_coverage_percentage(),
                'user_count': language.user_count,
                'content_count': language.content_count
            })
        
        response_data = {
            'languages': languages_data,
            'total_languages': len(languages_data),
            'default_language': 'fr'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération langues supportées: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des langues'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_user_language_preference(request):
    """
    Endpoint pour récupérer les préférences linguistiques de l'utilisateur
    """
    try:
        user = request.user
        preference = UserLanguagePreference.objects.get(user=user)
        
        response_data = {
            'user_id': user.id,
            'primary_language': {
                'code': preference.primary_language.code,
                'name': preference.primary_language.name,
                'native_name': preference.primary_language.native_name
            },
            'secondary_languages': [
                {
                    'code': lang.code,
                    'name': lang.name,
                    'native_name': lang.native_name
                } for lang in preference.secondary_languages.all()
            ],
            'country': {
                'code': preference.country.code,
                'name': preference.country.name,
                'native_name': preference.country.native_name
            } if preference.country else None,
            'timezone': preference.timezone,
            'preferred_currency': {
                'code': preference.preferred_currency.code,
                'name': preference.preferred_currency.name,
                'symbol': preference.preferred_currency.symbol
            } if preference.preferred_currency else None,
            'auto_translate': preference.auto_translate,
            'show_original_language': preference.show_original_language,
            'content_language_filter': preference.content_language_filter
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except UserLanguagePreference.DoesNotExist:
        return Response(
            {'error': 'Préférences linguistiques non trouvées'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Erreur récupération préférences linguistiques: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des préférences'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_language_preference(request):
    """
    Endpoint pour mettre à jour les préférences linguistiques
    """
    try:
        user = request.user
        primary_language = request.data.get('primary_language')
        secondary_languages = request.data.get('secondary_languages', [])
        country_code = request.data.get('country')
        timezone = request.data.get('timezone')
        currency_code = request.data.get('currency')
        auto_translate = request.data.get('auto_translate', True)
        show_original_language = request.data.get('show_original_language', False)
        content_language_filter = request.data.get('content_language_filter', True)
        
        preference, created = UserLanguagePreference.objects.get_or_create(user=user)
        
        # Mettre à jour la langue principale
        if primary_language:
            try:
                language = Language.objects.get(code=primary_language)
                preference.primary_language = language
            except Language.DoesNotExist:
                return Response(
                    {'error': 'Langue non supportée'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Mettre à jour les langues secondaires
        if secondary_languages:
            languages = Language.objects.filter(code__in=secondary_languages)
            preference.secondary_languages.set(languages)
        
        # Mettre à jour le pays
        if country_code:
            try:
                country = Country.objects.get(code=country_code)
                preference.country = country
            except Country.DoesNotExist:
                return Response(
                    {'error': 'Pays non supporté'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Mettre à jour le fuseau horaire
        if timezone:
            preference.timezone = timezone
        
        # Mettre à jour la devise
        if currency_code:
            try:
                currency = Currency.objects.get(code=currency_code)
                preference.preferred_currency = currency
            except Currency.DoesNotExist:
                return Response(
                    {'error': 'Devise non supportée'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Mettre à jour les paramètres
        preference.auto_translate = auto_translate
        preference.show_original_language = show_original_language
        preference.content_language_filter = content_language_filter
        preference.save()
        
        response_data = {
            'user_id': user.id,
            'message': 'Préférences linguistiques mises à jour',
            'primary_language': preference.primary_language.code,
            'country': preference.country.code if preference.country else None,
            'timezone': preference.timezone,
            'currency': preference.preferred_currency.code if preference.preferred_currency else None
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur mise à jour préférences linguistiques: {e}")
        return Response(
            {'error': 'Erreur lors de la mise à jour des préférences'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def translate_text(request):
    """
    Endpoint pour traduire un texte
    """
    try:
        text = request.data.get('text')
        target_language = request.data.get('target_language')
        source_language = request.data.get('source_language', 'auto')
        
        if not text or not target_language:
            return Response(
                {'error': 'Texte et langue cible requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que la langue cible est supportée
        try:
            Language.objects.get(code=target_language, status='active')
        except Language.DoesNotExist:
            return Response(
                {'error': 'Langue cible non supportée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Traduire le texte
        translated_text = i18n_service.translate_text(text, target_language, source_language)
        
        response_data = {
            'original_text': text,
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': target_language,
            'translation_method': 'ai'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur traduction texte: {e}")
        return Response(
            {'error': 'Erreur lors de la traduction'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_ui_translation(request):
    """
    Endpoint pour récupérer une traduction d'interface utilisateur
    """
    try:
        key = request.GET.get('key')
        language_code = request.GET.get('language', 'fr')
        
        if not key:
            return Response(
                {'error': 'Clé de traduction requise'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer la traduction
        translated_text = i18n_service.translate_ui_text(key, language_code)
        
        response_data = {
            'key': key,
            'language': language_code,
            'text': translated_text
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération traduction UI: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération de la traduction'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_content(request):
    """
    Endpoint pour traduire du contenu utilisateur
    """
    try:
        user = request.user
        content_id = request.data.get('content_id')
        content_type = request.data.get('content_type', 'post')
        target_language = request.data.get('target_language')
        
        if not content_id or not target_language:
            return Response(
                {'error': 'ID de contenu et langue cible requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer le contenu
        if content_type == 'post':
            try:
                content = Post.objects.get(id=content_id)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Post non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Type de contenu non supporté'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Traduire le contenu
        translation = i18n_service.translate_content(content, target_language)
        
        if translation:
            response_data = {
                'content_id': content_id,
                'content_type': content_type,
                'original_text': content.content,
                'translated_text': translation.translated_text,
                'target_language': target_language,
                'translation_method': translation.translation_method,
                'confidence_score': translation.confidence_score,
                'is_verified': translation.is_verified
            }
        else:
            response_data = {
                'error': 'Erreur lors de la traduction du contenu'
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur traduction contenu: {e}")
        return Response(
            {'error': 'Erreur lors de la traduction du contenu'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_localized_content(request):
    """
    Endpoint pour récupérer du contenu localisé
    """
    try:
        user = request.user
        content_type = request.GET.get('type', 'posts')
        limit = int(request.GET.get('limit', 20))
        
        # Récupérer le contenu localisé
        localized_content = i18n_service.get_localized_content(user, content_type)
        
        # Limiter le nombre d'éléments
        localized_content = localized_content[:limit]
        
        response_data = {
            'user_id': user.id,
            'content_type': content_type,
            'content': localized_content,
            'total_count': len(localized_content)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération contenu localisé: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération du contenu localisé'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_countries(request):
    """
    Endpoint pour récupérer les pays supportés
    """
    try:
        countries = Country.objects.filter(is_active=True).order_by('name')
        
        countries_data = []
        for country in countries:
            countries_data.append({
                'code': country.code,
                'name': country.name,
                'native_name': country.native_name,
                'region': country.region,
                'timezone': country.timezone,
                'date_format': country.date_format,
                'time_format': country.time_format,
                'currency': {
                    'code': country.currency.code,
                    'name': country.currency.name,
                    'symbol': country.currency.symbol
                } if country.currency else None,
                'default_language': {
                    'code': country.default_language.code,
                    'name': country.default_language.name
                } if country.default_language else None,
                'user_count': country.user_count,
                'content_count': country.content_count
            })
        
        response_data = {
            'countries': countries_data,
            'total_countries': len(countries_data)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération pays: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des pays'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_cultural_adaptations(request):
    """
    Endpoint pour récupérer les adaptations culturelles
    """
    try:
        country_code = request.GET.get('country')
        
        if not country_code:
            return Response(
                {'error': 'Code pays requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {'error': 'Pays non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les adaptations culturelles
        adaptations = i18n_service.get_cultural_adaptations(country)
        
        response_data = {
            'country_code': country_code,
            'country_name': country.name,
            'adaptations': adaptations
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération adaptations culturelles: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des adaptations'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_payment_methods(request):
    """
    Endpoint pour récupérer les méthodes de paiement par pays
    """
    try:
        country_code = request.GET.get('country')
        
        if not country_code:
            return Response(
                {'error': 'Code pays requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {'error': 'Pays non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les méthodes de paiement
        payment_methods = i18n_service.get_payment_methods(country)
        
        payment_methods_data = []
        for method in payment_methods:
            payment_methods_data.append({
                'id': method.id,
                'payment_type': method.payment_type,
                'provider_name': method.provider_name,
                'provider_code': method.provider_code,
                'is_default': method.is_default,
                'supported_currencies': [
                    {
                        'code': currency.code,
                        'name': currency.name,
                        'symbol': currency.symbol
                    } for currency in method.supported_currencies.all()
                ],
                'transaction_fee_percentage': float(method.transaction_fee_percentage),
                'transaction_fee_fixed': float(method.transaction_fee_fixed),
                'min_amount': float(method.min_amount),
                'max_amount': float(method.max_amount)
            })
        
        response_data = {
            'country_code': country_code,
            'country_name': country.name,
            'payment_methods': payment_methods_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération méthodes paiement: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des méthodes de paiement'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_legal_compliance(request):
    """
    Endpoint pour récupérer les exigences de conformité légale
    """
    try:
        country_code = request.GET.get('country')
        
        if not country_code:
            return Response(
                {'error': 'Code pays requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {'error': 'Pays non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les exigences de conformité
        compliance_rules = i18n_service.get_legal_compliance(country)
        
        compliance_data = []
        for rule in compliance_rules:
            compliance_data.append({
                'compliance_type': rule.compliance_type,
                'is_required': rule.is_required,
                'is_implemented': rule.is_implemented,
                'implementation_date': rule.implementation_date.isoformat() if rule.implementation_date else None,
                'requirements': rule.requirements,
                'implementation_details': rule.implementation_details
            })
        
        response_data = {
            'country_code': country_code,
            'country_name': country.name,
            'compliance_rules': compliance_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération conformité légale: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération de la conformité légale'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_regional_features(request):
    """
    Endpoint pour récupérer les fonctionnalités régionales
    """
    try:
        country_code = request.GET.get('country')
        
        if not country_code:
            return Response(
                {'error': 'Code pays requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {'error': 'Pays non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les fonctionnalités régionales
        features = i18n_service.get_regional_features(country)
        
        features_data = []
        for feature in features:
            features_data.append({
                'feature_type': feature.feature_type,
                'feature_name': feature.feature_name,
                'is_enabled': feature.is_enabled,
                'is_beta': feature.is_beta,
                'configuration': feature.configuration
            })
        
        response_data = {
            'country_code': country_code,
            'country_name': country.name,
            'features': features_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération fonctionnalités régionales: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des fonctionnalités régionales'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_localization_metrics(request):
    """
    Endpoint pour récupérer les métriques d'internationalisation
    """
    try:
        date_str = request.GET.get('date')
        
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Format de date invalide (YYYY-MM-DD)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            date = timezone.now().date()
        
        # Récupérer les métriques
        metrics = i18n_service.get_localization_metrics(date)
        
        if metrics:
            response_data = {
                'date': metrics.date.isoformat(),
                'active_languages': metrics.active_languages,
                'total_translations': metrics.total_translations,
                'translation_coverage_avg': metrics.translation_coverage_avg,
                'users_by_language': metrics.users_by_language,
                'users_by_country': metrics.users_by_country,
                'content_translations': metrics.content_translations,
                'ai_translations': metrics.ai_translations,
                'manual_translations': metrics.manual_translations,
                'translation_accuracy': metrics.translation_accuracy,
                'user_satisfaction': metrics.user_satisfaction,
                'calculated_at': metrics.calculated_at.isoformat()
            }
        else:
            response_data = {
                'error': 'Aucune métrique disponible pour cette date'
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération métriques i18n: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des métriques'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_translation_key(request):
    """
    Endpoint pour créer une nouvelle clé de traduction
    """
    try:
        user = request.user
        key = request.data.get('key')
        context = request.data.get('context', 'ui')
        description = request.data.get('description', '')
        
        if not key:
            return Response(
                {'error': 'Clé de traduction requise'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la clé de traduction
        translation_key = i18n_service.create_translation_key(key, context, description)
        
        if translation_key:
            response_data = {
                'key': translation_key.key,
                'context': translation_key.context,
                'description': translation_key.description,
                'is_plural': translation_key.is_plural,
                'is_html': translation_key.is_html,
                'created_at': translation_key.created_at.isoformat(),
                'message': 'Clé de traduction créée avec succès'
            }
        else:
            response_data = {
                'error': 'Erreur lors de la création de la clé de traduction'
            }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Erreur création clé traduction: {e}")
        return Response(
            {'error': 'Erreur lors de la création de la clé de traduction'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_legal_compliance(request):
    """
    Endpoint pour valider la conformité légale d'une action
    """
    try:
        user = request.user
        action = request.data.get('action')
        
        if not action:
            return Response(
                {'error': 'Action requise'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider la conformité
        is_compliant = i18n_service.validate_legal_compliance(user, action)
        
        response_data = {
            'user_id': user.id,
            'action': action,
            'is_compliant': is_compliant,
            'message': 'Action conforme' if is_compliant else 'Action non conforme'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur validation conformité: {e}")
        return Response(
            {'error': 'Erreur lors de la validation de la conformité'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_timezone_info(request):
    """
    Endpoint pour récupérer les informations de fuseau horaire
    """
    try:
        country_code = request.GET.get('country')
        
        if not country_code:
            return Response(
                {'error': 'Code pays requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {'error': 'Pays non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les informations de fuseau horaire
        timezone_info = i18n_service.get_timezone_info(country)
        
        response_data = {
            'country_code': country_code,
            'country_name': country.name,
            'timezone_info': timezone_info
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur récupération fuseau horaire: {e}")
        return Response(
            {'error': 'Erreur lors de la récupération des informations de fuseau horaire'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def format_currency(request):
    """
    Endpoint pour formater un montant selon la devise
    """
    try:
        amount = request.data.get('amount')
        currency_code = request.data.get('currency')
        country_code = request.data.get('country')
        
        if not amount or not currency_code:
            return Response(
                {'error': 'Montant et devise requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Formater le montant
        formatted_amount = i18n_service.format_currency(float(amount), currency_code, country_code)
        
        response_data = {
            'amount': amount,
            'currency': currency_code,
            'country': country_code,
            'formatted_amount': formatted_amount
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur formatage devise: {e}")
        return Response(
            {'error': 'Erreur lors du formatage de la devise'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from posts.models import Post
from geography.models import Quartier
from .recommendations import ai_system
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_recommendations(request):
    """
    Endpoint pour obtenir des recommandations personnalisées basées sur l'IA
    """
    try:
        user = request.user
        
        # Paramètres de requête
        limit = int(request.GET.get('limit', 10))
        include_posts = request.GET.get('include_posts', 'true').lower() == 'true'
        include_users = request.GET.get('include_users', 'true').lower() == 'true'
        include_content = request.GET.get('include_content', 'true').lower() == 'true'
        include_activities = request.GET.get('include_activities', 'true').lower() == 'true'
        
        # Générer les recommandations
        recommendations = ai_system.generate_personalized_recommendations(user.id, limit)
        
        # Préparer la réponse
        response_data = {
            'user_id': user.id,
            'recommendations_generated_at': datetime.now().isoformat(),
            'total_recommendations': 0
        }
        
        if include_posts and 'posts' in recommendations:
            posts_data = []
            for post in recommendations['posts']:
                posts_data.append({
                    'id': post.id,
                    'content': post.content,
                    'author': {
                        'id': post.author.id,
                        'username': post.author.username,
                        'quartier': post.author.quartier.nom if post.author.quartier else None
                    },
                    'likes_count': post.likes_count,
                    'comments_count': post.comments_count,
                    'created_at': post.created_at.isoformat(),
                    'recommendation_reason': 'Basé sur vos intérêts et localisation'
                })
            
            response_data['posts'] = posts_data
            response_data['total_recommendations'] += len(posts_data)
        
        if include_users and 'users' in recommendations:
            users_data = []
            for user_rec in recommendations['users']:
                users_data.append({
                    'id': user_rec.id,
                    'username': user_rec.username,
                    'quartier': user_rec.quartier.nom if user_rec.quartier else None,
                    'avatar': user_rec.avatar.url if user_rec.avatar else None,
                    'recommendation_reason': 'Utilisateur actif dans votre quartier'
                })
            
            response_data['users'] = users_data
            response_data['total_recommendations'] += len(users_data)
        
        if include_content and 'content' in recommendations:
            response_data['content_categories'] = recommendations['content']
        
        if include_activities and 'activities' in recommendations:
            response_data['suggested_activities'] = recommendations['activities']
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur recommandations personnalisées: {e}")
        return Response(
            {'error': 'Erreur lors de la génération des recommandations'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_topics(request):
    """
    Endpoint pour obtenir les sujets tendance
    """
    try:
        # Paramètres de requête
        quartier_id = request.GET.get('quartier_id')
        limit = int(request.GET.get('limit', 10))
        
        quartier = None
        if quartier_id:
            try:
                quartier = Quartier.objects.get(id=quartier_id)
            except Quartier.DoesNotExist:
                return Response(
                    {'error': 'Quartier non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Détecter les tendances
        trending_data = ai_system.detect_trending_topics(quartier, limit)
        
        # Préparer la réponse
        response_data = {
            'trending_detected_at': datetime.now().isoformat(),
            'quartier': quartier.nom if quartier else 'Global',
            'trending_posts': [],
            'trending_keywords': trending_data.get('trending_keywords', []),
            'engagement_metrics': trending_data.get('engagement_metrics', {})
        }
        
        # Formater les posts tendance
        for post in trending_data.get('trending_posts', []):
            response_data['trending_posts'].append({
                'id': post.id,
                'content': post.content,
                'author': {
                    'id': post.author.id,
                    'username': post.author.username,
                    'quartier': post.author.quartier.nom if post.author.quartier else None
                },
                'engagement_score': post.likes_count + post.comments_count,
                'created_at': post.created_at.isoformat()
            })
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur détection tendances: {e}")
        return Response(
            {'error': 'Erreur lors de la détection des tendances'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_behavior_analysis(request):
    """
    Endpoint pour obtenir l'analyse du comportement utilisateur
    """
    try:
        user = request.user
        
        # Analyser le comportement
        behavior = ai_system.analyze_user_behavior(user.id)
        
        # Préparer la réponse
        response_data = {
            'user_id': user.id,
            'analysis_generated_at': datetime.now().isoformat(),
            'behavior_summary': {
                'engagement_level': 'Élevé' if behavior.get('engagement_rate', 0) > 5 else 'Moyen' if behavior.get('engagement_rate', 0) > 2 else 'Faible',
                'social_activity': 'Très actif' if behavior.get('posts_created', 0) > 20 else 'Actif' if behavior.get('posts_created', 0) > 10 else 'Modéré',
                'geographic_engagement': 'Élevé' if behavior.get('geographic_activity', {}).get('geographic_engagement', 0) > 0.5 else 'Moyen' if behavior.get('geographic_activity', {}).get('geographic_engagement', 0) > 0.2 else 'Faible'
            },
            'detailed_metrics': behavior
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur analyse comportement: {e}")
        return Response(
            {'error': 'Erreur lors de l\'analyse du comportement'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_content_optimization(request):
    """
    Endpoint pour obtenir les optimisations de contenu personnalisées
    """
    try:
        user = request.user
        
        # Paramètres de requête
        content_type = request.GET.get('content_type', 'posts')
        
        # Obtenir les optimisations
        optimization = ai_system.optimize_content_delivery(user.id, content_type)
        
        # Préparer la réponse
        response_data = {
            'user_id': user.id,
            'optimization_generated_at': datetime.now().isoformat(),
            'content_type': content_type,
            'optimal_timing': optimization.get('optimal_timing', {}),
            'content_mix': optimization.get('content_mix', {}),
            'engagement_strategies': optimization.get('engagement_strategies', []),
            'personalization_factors': optimization.get('personalization_factors', [])
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur optimisation contenu: {e}")
        return Response(
            {'error': 'Erreur lors de l\'optimisation du contenu'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feedback_recommendation(request):
    """
    Endpoint pour donner un feedback sur les recommandations
    """
    try:
        user = request.user
        recommendation_id = request.data.get('recommendation_id')
        feedback_type = request.data.get('feedback_type')  # 'like', 'dislike', 'click', 'ignore'
        recommendation_type = request.data.get('recommendation_type')  # 'post', 'user', 'content'
        
        if not all([recommendation_id, feedback_type, recommendation_type]):
            return Response(
                {'error': 'Paramètres manquants'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Enregistrer le feedback (pour améliorer l'IA)
        feedback_data = {
            'user_id': user.id,
            'recommendation_id': recommendation_id,
            'feedback_type': feedback_type,
            'recommendation_type': recommendation_type,
            'timestamp': datetime.now().isoformat()
        }
        
        # Ici on pourrait sauvegarder dans une base de données
        logger.info(f"Feedback IA: {feedback_data}")
        
        return Response({
            'message': 'Feedback enregistré avec succès',
            'feedback_id': f"{user.id}_{recommendation_id}_{feedback_type}"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur feedback recommandation: {e}")
        return Response(
            {'error': 'Erreur lors de l\'enregistrement du feedback'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ai_insights(request):
    """
    Endpoint pour obtenir des insights IA généraux
    """
    try:
        user = request.user
        
        # Obtenir les insights
        behavior = ai_system.analyze_user_behavior(user.id)
        recommendations = ai_system.generate_personalized_recommendations(user.id, 5)
        
        insights = {
            'user_id': user.id,
            'insights_generated_at': datetime.now().isoformat(),
            'engagement_insights': {
                'current_level': behavior.get('engagement_rate', 0),
                'target_level': 5.0,
                'improvement_potential': max(0, 5.0 - behavior.get('engagement_rate', 0)),
                'suggested_actions': recommendations.get('activities', [])
            },
            'social_insights': {
                'current_connections': behavior.get('friends_count', 0),
                'potential_connections': behavior.get('geographic_activity', {}).get('local_users_count', 0),
                'connection_opportunity': max(0, behavior.get('geographic_activity', {}).get('local_users_count', 0) - behavior.get('friends_count', 0))
            },
            'content_insights': {
                'preferred_categories': behavior.get('content_preferences', {}).get('content_categories', {}),
                'media_preferences': behavior.get('content_preferences', {}).get('media_preferences', {}),
                'optimal_posting_times': behavior.get('active_hours', {}).get('peak_hours', [])
            },
            'growth_opportunities': [
                {
                    'type': 'engagement_boost',
                    'title': 'Augmenter l\'engagement',
                    'description': f'Votre taux d\'engagement actuel est de {behavior.get("engagement_rate", 0):.1f}. Ciblez 5.0 pour une meilleure visibilité.',
                    'priority': 'high' if behavior.get('engagement_rate', 0) < 3 else 'medium'
                },
                {
                    'type': 'social_expansion',
                    'title': 'Élargir le réseau',
                    'description': f'Connectez-vous avec {behavior.get("geographic_activity", {}).get("local_users_count", 0)} utilisateurs locaux disponibles.',
                    'priority': 'high' if behavior.get('friends_count', 0) < 10 else 'medium'
                },
                {
                    'type': 'content_diversification',
                    'title': 'Diversifier le contenu',
                    'description': 'Essayez différents types de contenu pour augmenter l\'engagement.',
                    'priority': 'medium'
                }
            ]
        }
        
        return Response(insights, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur insights IA: {e}")
        return Response(
            {'error': 'Erreur lors de la génération des insights'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
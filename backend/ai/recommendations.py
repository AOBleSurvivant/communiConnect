import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Avg, F
from posts.models import Post, PostLike, PostComment
from users.models import User, UserRelationship
from geography.models import Quartier, Commune
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class CommuniConnectAI:
    """
    Système d'Intelligence Artificielle pour CommuniConnect
    Recommandations personnalisées basées sur la géolocalisation et les comportements
    """
    
    def __init__(self):
        self.user_model = get_user_model()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='french')
        self.user_clusters = None
        self.content_clusters = None
        
    def analyze_user_behavior(self, user_id):
        """Analyse le comportement utilisateur pour créer un profil IA"""
        try:
            user = self.user_model.objects.get(id=user_id)
            
            # Données de comportement
            behavior_data = {
                'posts_created': Post.objects.filter(author=user).count(),
                'posts_liked': PostLike.objects.filter(user=user).count(),
                'comments_made': PostComment.objects.filter(user=user).count(),
                'friends_count': UserRelationship.objects.filter(
                    Q(user1=user) | Q(user2=user),
                    status='accepted'
                ).count(),
                'avg_posts_per_day': self._calculate_avg_posts_per_day(user),
                'engagement_rate': self._calculate_engagement_rate(user),
                'geographic_activity': self._analyze_geographic_activity(user),
                'content_preferences': self._analyze_content_preferences(user),
                'active_hours': self._analyze_active_hours(user),
                'interaction_patterns': self._analyze_interaction_patterns(user)
            }
            
            return behavior_data
            
        except Exception as e:
            logger.error(f"Erreur analyse comportement utilisateur {user_id}: {e}")
            return {}
    
    def _calculate_avg_posts_per_day(self, user):
        """Calcule la moyenne de posts par jour"""
        posts = Post.objects.filter(author=user)
        if not posts.exists():
            return 0
        
        first_post = posts.earliest('created_at')
        days_active = (datetime.now() - first_post.created_at.replace(tzinfo=None)).days
        return posts.count() / max(days_active, 1)
    
    def _calculate_engagement_rate(self, user):
        """Calcule le taux d'engagement de l'utilisateur"""
        posts = Post.objects.filter(author=user)
        if not posts.exists():
            return 0
        
        total_likes = sum(post.likes.count() for post in posts)
        total_comments = sum(post.comments.count() for post in posts)
        total_posts = posts.count()
        
        return (total_likes + total_comments) / total_posts if total_posts > 0 else 0
    
    def _analyze_geographic_activity(self, user):
        """Analyse l'activité géographique de l'utilisateur"""
        try:
            quartier = user.quartier
            commune = quartier.commune if quartier else None
            
            # Utilisateurs actifs dans le même quartier
            local_users = self.user_model.objects.filter(
                quartier=quartier,
                is_active=True
            ).exclude(id=user.id)
            
            # Posts locaux populaires
            local_posts = Post.objects.filter(
                author__quartier=quartier
            ).exclude(author=user).order_by('-likes_count')[:10]
            
            return {
                'quartier': quartier.nom if quartier else None,
                'commune': commune.nom if commune else None,
                'local_users_count': local_users.count(),
                'local_posts_count': local_posts.count(),
                'geographic_engagement': self._calculate_geographic_engagement(user, quartier)
            }
        except Exception as e:
            logger.error(f"Erreur analyse géographique: {e}")
            return {}
    
    def _calculate_geographic_engagement(self, user, quartier):
        """Calcule l'engagement géographique"""
        if not quartier:
            return 0
        
        local_posts = Post.objects.filter(author__quartier=quartier)
        user_interactions = PostLike.objects.filter(
            user=user,
            post__author__quartier=quartier
        ).count()
        
        return user_interactions / max(local_posts.count(), 1)
    
    def _analyze_content_preferences(self, user):
        """Analyse les préférences de contenu de l'utilisateur"""
        liked_posts = Post.objects.filter(likes__user=user)
        
        # Analyse des mots-clés des posts likés
        content_texts = []
        for post in liked_posts:
            content_texts.append(post.content)
        
        if content_texts:
            try:
                tfidf_matrix = self.vectorizer.fit_transform(content_texts)
                feature_names = self.vectorizer.get_feature_names_out()
                
                # Top mots-clés préférés
                tfidf_sums = np.sum(tfidf_matrix.toarray(), axis=0)
                top_keywords = [feature_names[i] for i in np.argsort(tfidf_sums)[-10:]]
                
                return {
                    'preferred_keywords': top_keywords,
                    'content_categories': self._categorize_content(liked_posts),
                    'media_preferences': self._analyze_media_preferences(liked_posts)
                }
            except Exception as e:
                logger.error(f"Erreur analyse contenu: {e}")
        
        return {}
    
    def _categorize_content(self, posts):
        """Catégorise le contenu des posts"""
        categories = {
            'actualites': 0,
            'culture': 0,
            'sport': 0,
            'business': 0,
            'social': 0,
            'autre': 0
        }
        
        keywords = {
            'actualites': ['actualité', 'nouvelle', 'information', 'événement'],
            'culture': ['culture', 'art', 'musique', 'cinéma', 'littérature'],
            'sport': ['sport', 'football', 'basketball', 'match', 'compétition'],
            'business': ['business', 'commerce', 'entreprise', 'travail', 'emploi'],
            'social': ['ami', 'famille', 'fête', 'célébration', 'rencontre']
        }
        
        for post in posts:
            content_lower = post.content.lower()
            categorized = False
            
            for category, category_keywords in keywords.items():
                if any(keyword in content_lower for keyword in category_keywords):
                    categories[category] += 1
                    categorized = True
                    break
            
            if not categorized:
                categories['autre'] += 1
        
        return categories
    
    def _analyze_media_preferences(self, posts):
        """Analyse les préférences média"""
        media_stats = {
            'text_only': 0,
            'with_images': 0,
            'with_videos': 0,
            'with_audio': 0
        }
        
        for post in posts:
            if post.media.exists():
                media_types = [media.media_type for media in post.media.all()]
                if 'image' in media_types:
                    media_stats['with_images'] += 1
                if 'video' in media_types:
                    media_stats['with_videos'] += 1
                if 'audio' in media_types:
                    media_stats['with_audio'] += 1
            else:
                media_stats['text_only'] += 1
        
        return media_stats
    
    def _analyze_active_hours(self, user):
        """Analyse les heures d'activité de l'utilisateur"""
        posts = Post.objects.filter(author=user)
        likes = PostLike.objects.filter(user=user)
        comments = PostComment.objects.filter(user=user)
        
        all_activities = []
        
        # Posts
        for post in posts:
            all_activities.append(post.created_at.hour)
        
        # Likes
        for like in likes:
            all_activities.append(like.created_at.hour)
        
        # Comments
        for comment in comments:
            all_activities.append(comment.created_at.hour)
        
        if all_activities:
            hour_counts = pd.Series(all_activities).value_counts()
            peak_hours = hour_counts.head(3).index.tolist()
            return {
                'peak_hours': peak_hours,
                'total_activities': len(all_activities),
                'activity_distribution': hour_counts.to_dict()
            }
        
        return {}
    
    def _analyze_interaction_patterns(self, user):
        """Analyse les patterns d'interaction de l'utilisateur"""
        # Interactions avec d'autres utilisateurs
        interactions = PostLike.objects.filter(user=user).select_related('post__author')
        
        interaction_stats = {
            'total_interactions': interactions.count(),
            'unique_users_interacted': len(set(interaction.post.author.id for interaction in interactions)),
            'reciprocal_interactions': 0,
            'interaction_frequency': {}
        }
        
        # Calcul des interactions réciproques
        for interaction in interactions:
            other_user = interaction.post.author
            reciprocal = PostLike.objects.filter(
                user=other_user,
                post__author=user
            ).exists()
            
            if reciprocal:
                interaction_stats['reciprocal_interactions'] += 1
        
        return interaction_stats
    
    def generate_personalized_recommendations(self, user_id, limit=10):
        """Génère des recommandations personnalisées pour un utilisateur"""
        try:
            user = self.user_model.objects.get(id=user_id)
            behavior = self.analyze_user_behavior(user_id)
            
            recommendations = {
                'posts': self._recommend_posts(user, behavior, limit),
                'users': self._recommend_users(user, behavior, limit//2),
                'content': self._recommend_content_categories(user, behavior),
                'activities': self._recommend_activities(user, behavior)
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur génération recommandations: {e}")
            return {}
    
    def _recommend_posts(self, user, behavior, limit):
        """Recommandation de posts personnalisés"""
        # Posts populaires dans le quartier
        quartier_posts = Post.objects.filter(
            author__quartier=user.quartier
        ).exclude(author=user).order_by('-likes_count', '-created_at')[:limit//2]
        
        # Posts basés sur les préférences de contenu
        if 'content_preferences' in behavior and 'preferred_keywords' in behavior['content_preferences']:
            keywords = behavior['content_preferences']['preferred_keywords']
            keyword_posts = Post.objects.filter(
                Q(content__icontains=keywords[0]) | 
                Q(content__icontains=keywords[1]) if len(keywords) > 1 else Q(content__icontains=keywords[0])
            ).exclude(author=user).order_by('-created_at')[:limit//2]
        else:
            keyword_posts = Post.objects.none()
        
        # Combiner et trier par pertinence
        all_recommended = list(quartier_posts) + list(keyword_posts)
        return sorted(all_recommended, key=lambda x: x.likes_count + x.comments_count, reverse=True)[:limit]
    
    def _recommend_users(self, user, behavior, limit):
        """Recommandation d'utilisateurs à connecter"""
        # Utilisateurs du même quartier
        local_users = self.user_model.objects.filter(
            quartier=user.quartier,
            is_active=True
        ).exclude(id=user.id)[:limit//2]
        
        # Utilisateurs avec des intérêts similaires
        if 'content_preferences' in behavior:
            similar_users = self._find_similar_users(user, behavior, limit//2)
        else:
            similar_users = self.user_model.objects.none()
        
        return list(local_users) + list(similar_users)
    
    def _find_similar_users(self, user, behavior, limit):
        """Trouve des utilisateurs avec des intérêts similaires"""
        if 'content_preferences' not in behavior:
            return self.user_model.objects.none()
        
        # Utilisateurs qui ont liké des posts similaires
        user_liked_posts = Post.objects.filter(likes__user=user)
        
        similar_users = self.user_model.objects.filter(
            likes__post__in=user_liked_posts
        ).exclude(id=user.id).annotate(
            common_likes=Count('likes__post', filter=Q(likes__post__in=user_liked_posts))
        ).order_by('-common_likes')[:limit]
        
        return similar_users
    
    def _recommend_content_categories(self, user, behavior):
        """Recommandation de catégories de contenu"""
        if 'content_preferences' not in behavior:
            return {}
        
        categories = behavior['content_preferences'].get('content_categories', {})
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'top_categories': sorted_categories[:3],
            'suggested_categories': self._suggest_new_categories(categories)
        }
    
    def _suggest_new_categories(self, current_categories):
        """Suggère de nouvelles catégories basées sur les préférences actuelles"""
        suggestions = []
        
        if current_categories.get('actualites', 0) > 0:
            suggestions.append('culture')
        if current_categories.get('culture', 0) > 0:
            suggestions.append('actualites')
        if current_categories.get('sport', 0) > 0:
            suggestions.append('business')
        if current_categories.get('business', 0) > 0:
            suggestions.append('social')
        
        return suggestions[:2]
    
    def _recommend_activities(self, user, behavior):
        """Recommandation d'activités personnalisées"""
        activities = []
        
        # Basé sur l'engagement
        if behavior.get('engagement_rate', 0) < 2:
            activities.append({
                'type': 'engagement_boost',
                'title': 'Augmenter votre engagement',
                'description': 'Likez et commentez plus de posts pour améliorer votre visibilité',
                'priority': 'high'
            })
        
        # Basé sur les connexions
        if behavior.get('friends_count', 0) < 5:
            activities.append({
                'type': 'social_connection',
                'title': 'Élargir votre réseau',
                'description': 'Connectez-vous avec plus d\'utilisateurs de votre quartier',
                'priority': 'medium'
            })
        
        # Basé sur l'activité géographique
        if behavior.get('geographic_activity', {}).get('geographic_engagement', 0) < 0.3:
            activities.append({
                'type': 'local_engagement',
                'title': 'Participer à votre communauté',
                'description': 'Interagissez plus avec les posts de votre quartier',
                'priority': 'medium'
            })
        
        return activities
    
    def detect_trending_topics(self, quartier=None, limit=10):
        """Détecte les sujets tendance dans un quartier ou globalement"""
        try:
            # Posts récents avec beaucoup d'engagement
            recent_posts = Post.objects.filter(
                created_at__gte=datetime.now() - timedelta(days=7)
            )
            
            if quartier:
                recent_posts = recent_posts.filter(author__quartier=quartier)
            
            trending_posts = recent_posts.annotate(
                engagement_score=F('likes_count') + F('comments_count') * 2
            ).order_by('-engagement_score')[:limit]
            
            # Extraction des mots-clés tendance
            trending_keywords = self._extract_trending_keywords(trending_posts)
            
            return {
                'trending_posts': trending_posts,
                'trending_keywords': trending_keywords,
                'engagement_metrics': self._calculate_trending_metrics(trending_posts)
            }
            
        except Exception as e:
            logger.error(f"Erreur détection tendances: {e}")
            return {}
    
    def _extract_trending_keywords(self, posts):
        """Extrait les mots-clés tendance des posts"""
        content_texts = [post.content for post in posts]
        
        if not content_texts:
            return []
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(content_texts)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Calcul de l'importance des mots-clés
            tfidf_sums = np.sum(tfidf_matrix.toarray(), axis=0)
            keyword_importance = [(feature_names[i], tfidf_sums[i]) for i in range(len(feature_names))]
            
            # Top mots-clés tendance
            trending_keywords = sorted(keyword_importance, key=lambda x: x[1], reverse=True)[:10]
            
            return [keyword for keyword, score in trending_keywords if score > 0.1]
            
        except Exception as e:
            logger.error(f"Erreur extraction mots-clés: {e}")
            return []
    
    def _calculate_trending_metrics(self, posts):
        """Calcule les métriques de tendance"""
        if not posts:
            return {}
        
        total_likes = sum(post.likes_count for post in posts)
        total_comments = sum(post.comments_count for post in posts)
        total_shares = sum(post.shares_count for post in posts)
        
        return {
            'total_engagement': total_likes + total_comments + total_shares,
            'avg_likes_per_post': total_likes / len(posts),
            'avg_comments_per_post': total_comments / len(posts),
            'engagement_growth_rate': self._calculate_engagement_growth(posts)
        }
    
    def _calculate_engagement_growth(self, posts):
        """Calcule le taux de croissance de l'engagement"""
        if len(posts) < 2:
            return 0
        
        # Comparer l'engagement des posts récents vs anciens
        recent_posts = posts[:len(posts)//2]
        older_posts = posts[len(posts)//2:]
        
        recent_engagement = sum(post.likes_count + post.comments_count for post in recent_posts)
        older_engagement = sum(post.likes_count + post.comments_count for post in older_posts)
        
        if older_engagement == 0:
            return 0
        
        return ((recent_engagement - older_engagement) / older_engagement) * 100
    
    def optimize_content_delivery(self, user_id, content_type='posts'):
        """Optimise la livraison de contenu pour un utilisateur"""
        try:
            user = self.user_model.objects.get(id=user_id)
            behavior = self.analyze_user_behavior(user_id)
            
            optimization = {
                'optimal_timing': self._calculate_optimal_timing(behavior),
                'content_mix': self._optimize_content_mix(behavior),
                'engagement_strategies': self._suggest_engagement_strategies(behavior),
                'personalization_factors': self._identify_personalization_factors(behavior)
            }
            
            return optimization
            
        except Exception as e:
            logger.error(f"Erreur optimisation livraison: {e}")
            return {}
    
    def _calculate_optimal_timing(self, behavior):
        """Calcule le timing optimal pour les interactions"""
        active_hours = behavior.get('active_hours', {})
        peak_hours = active_hours.get('peak_hours', [])
        
        if peak_hours:
            return {
                'best_posting_hours': peak_hours,
                'best_engagement_hours': [(h + 1) % 24 for h in peak_hours],
                'timezone_consideration': 'Africa/Conakry'
            }
        
        return {
            'best_posting_hours': [9, 12, 18, 20],  # Heures par défaut
            'best_engagement_hours': [10, 13, 19, 21],
            'timezone_consideration': 'Africa/Conakry'
        }
    
    def _optimize_content_mix(self, behavior):
        """Optimise le mix de contenu pour l'utilisateur"""
        content_prefs = behavior.get('content_preferences', {})
        media_prefs = content_prefs.get('media_preferences', {})
        
        # Calculer le ratio optimal de types de contenu
        total_content = sum(media_prefs.values()) if media_prefs else 1
        
        if total_content > 0:
            optimal_mix = {
                'text_ratio': media_prefs.get('text_only', 0) / total_content,
                'image_ratio': media_prefs.get('with_images', 0) / total_content,
                'video_ratio': media_prefs.get('with_videos', 0) / total_content,
                'suggested_next_content': self._suggest_next_content_type(media_prefs)
            }
        else:
            optimal_mix = {
                'text_ratio': 0.4,
                'image_ratio': 0.4,
                'video_ratio': 0.2,
                'suggested_next_content': 'image'
            }
        
        return optimal_mix
    
    def _suggest_next_content_type(self, media_prefs):
        """Suggère le prochain type de contenu à créer"""
        if not media_prefs:
            return 'text'
        
        # Trouver le type le moins utilisé
        min_type = min(media_prefs.items(), key=lambda x: x[1])
        
        if min_type[0] == 'text_only':
            return 'image'
        elif min_type[0] == 'with_images':
            return 'video'
        else:
            return 'text'
    
    def _suggest_engagement_strategies(self, behavior):
        """Suggère des stratégies d'engagement personnalisées"""
        strategies = []
        
        engagement_rate = behavior.get('engagement_rate', 0)
        friends_count = behavior.get('friends_count', 0)
        
        if engagement_rate < 1:
            strategies.append({
                'type': 'low_engagement',
                'strategy': 'Interagir avec 5 posts par jour',
                'expected_impact': '+25% visibilité'
            })
        
        if friends_count < 10:
            strategies.append({
                'type': 'social_expansion',
                'strategy': 'Ajouter 3 nouveaux amis par semaine',
                'expected_impact': '+40% interactions'
            })
        
        return strategies
    
    def _identify_personalization_factors(self, behavior):
        """Identifie les facteurs de personnalisation"""
        factors = []
        
        if behavior.get('geographic_activity', {}).get('quartier'):
            factors.append('geographic_localization')
        
        if behavior.get('content_preferences', {}).get('preferred_keywords'):
            factors.append('content_preferences')
        
        if behavior.get('active_hours', {}).get('peak_hours'):
            factors.append('temporal_patterns')
        
        if behavior.get('interaction_patterns', {}).get('reciprocal_interactions', 0) > 0:
            factors.append('social_reciprocity')
        
        return factors

# Instance globale pour réutilisation
ai_system = CommuniConnectAI() 
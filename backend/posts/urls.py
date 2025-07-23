from django.urls import path
from .views import (
    PostListView, PostDetailView, PostLikeView, PostCommentView,
    PostCommentDetailView, PostCommentReplyView, UserPostsView, PostIncrementViewsView,
    MediaUploadView, MediaListView, MediaDetailView, LiveStreamView, PostShareView, PostSharesListView,
    ExternalShareView, ExternalSharesListView, PostAnalyticsView, UserAnalyticsView, CommunityAnalyticsView,
    LiveChatView, LiveVideoUploadView
)

app_name = 'posts'

urlpatterns = [
    # Live streaming et chat (doit être avant les URLs génériques)
    path('live/start/', LiveStreamView.as_view(), name='live-start'),
    path('live/<int:live_id>/stop/', LiveStreamView.as_view(), name='live-stop'),
    path('live/<int:live_id>/upload-video/', LiveVideoUploadView.as_view(), name='live-upload-video'),
    path('live/<int:post_id>/chat/', LiveChatView.as_view(), name='live-chat'),
    path('live/<int:post_id>/chat/messages/', LiveChatView.as_view(), name='live-chat-messages'),
    
    # Posts
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/increment-views/', PostIncrementViewsView.as_view(), name='post-increment-views'),
    
    # Likes
    path('<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    
    # Commentaires
    path('<int:pk>/comments/', PostCommentView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', PostCommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/reply/', PostCommentReplyView.as_view(), name='comment-reply'),
    
    # Posts d'un utilisateur
    path('user/<int:user_id>/', UserPostsView.as_view(), name='user-posts'),
    
    # Médias
    path('media/upload/', MediaUploadView.as_view(), name='media-upload'),
    path('media/', MediaListView.as_view(), name='media-list'),
    path('media/<int:pk>/', MediaDetailView.as_view(), name='media-detail'),

    # Partages
    path('posts/<int:pk>/share/', PostShareView.as_view(), name='post-share'),
    path('posts/<int:pk>/shares/', PostSharesListView.as_view(), name='post-shares'),

    # Partages externes
    path('posts/<int:pk>/share-external/', ExternalShareView.as_view(), name='post-share-external'),
    path('posts/<int:pk>/external-shares/', ExternalSharesListView.as_view(), name='post-external-shares'),

    # Analytics
    path('posts/<int:pk>/analytics/', PostAnalyticsView.as_view(), name='post-analytics'),
    path('analytics/user/', UserAnalyticsView.as_view(), name='user-analytics'),
    path('analytics/community/', CommunityAnalyticsView.as_view(), name='community-analytics'),
] 
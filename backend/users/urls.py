from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Inscription et authentification
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profils utilisateurs
    path('my-profile/', views.UserProfileView.as_view(), name='my-profile'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Recherche et suggestions
    path('search/', views.UserSearchView.as_view(), name='user-search'),
    path('suggested-friends/', views.SuggestedFriendsView.as_view(), name='suggested-friends'),
    
    # Relations d'amitié
    path('follow/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', views.FollowersListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following-list'),
    
    # Demandes d'amitié
    path('pending-friends/', views.PendingFriendsView.as_view(), name='pending-friends'),
    path('accept-friend/<int:relationship_id>/', views.AcceptFriendRequestView.as_view(), name='accept-friend'),
    path('reject-friend/<int:relationship_id>/', views.RejectFriendRequestView.as_view(), name='reject-friend'),
    
    # Blocage d'utilisateurs
    path('block/', views.BlockUserView.as_view(), name='block-user'),
    path('unblock/', views.UnblockUserView.as_view(), name='unblock-user'),
    
    # Statut des relations
    path('relationship-status/<int:user_id>/', views.UserRelationshipsStatusView.as_view(), name='relationship-status'),
    
    # Statistiques
    path('stats/<int:user_id>/', views.UserStatsView.as_view(), name='user-stats'),
    
    # Données géographiques et tableau de bord
    path('geographic-data/', views.GeographicDataView.as_view(), name='geographic-data'),
    path('verify-geographic/', views.GeographicVerificationView.as_view(), name='verify-geographic'),
    path('dashboard/', views.UserDashboardDataView.as_view(), name='dashboard'),

    # ============================================================================
    # URLs POUR GROUPES COMMUNAUTAIRES
    # ============================================================================

    # Groupes
    path('groups/', views.CommunityGroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', views.CommunityGroupDetailView.as_view(), name='group-detail'),
    path('groups/join/', views.GroupMembershipView.as_view(), name='group-join'),
    path('groups/<int:group_id>/members/', views.GroupMembershipListView.as_view(), name='group-members'),
    path('groups/membership/<int:pk>/', views.GroupMembershipActionView.as_view(), name='group-membership-action'),

    # ============================================================================
    # URLs POUR ÉVÉNEMENTS COMMUNAUTAIRES
    # ============================================================================

    # Événements
    path('events/', views.CommunityEventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', views.CommunityEventDetailView.as_view(), name='event-detail'),
    path('events/join/', views.EventAttendanceView.as_view(), name='event-join'),
    path('events/<int:event_id>/attendees/', views.EventAttendanceListView.as_view(), name='event-attendees'),

    # ============================================================================
    # URLs POUR GAMIFICATION ET RÉALISATIONS
    # ============================================================================

    # Réalisations et scores
    path('achievements/<int:user_id>/', views.UserAchievementListView.as_view(), name='user-achievements'),
    path('social-score/<int:user_id>/', views.UserSocialScoreView.as_view(), name='user-social-score'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),

    # ============================================================================
    # URLs POUR SUGGESTIONS INTELLIGENTES
    # ============================================================================

    # Suggestions
    path('suggested-groups/', views.SuggestedGroupsView.as_view(), name='suggested-groups'),
    path('suggested-events/', views.SuggestedEventsView.as_view(), name='suggested-events'),
    path('suggested-connections/', views.SuggestedConnectionsView.as_view(), name='suggested-connections'),

    # ============================================================================
    # URLs POUR STATISTIQUES SOCIALES
    # ============================================================================

    # Statistiques
    path('social-stats/<int:user_id>/', views.SocialStatsView.as_view(), name='social-stats'),
] 
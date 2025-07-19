from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Inscription et authentification
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profils utilisateurs
    path('profile/', views.UserProfileView.as_view(), name='profile'),
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
    path('relationship-status/<int:user_id>/', views.user_relationships_status, name='relationship-status'),
    
    # Statistiques
    path('stats/<int:user_id>/', views.UserStatsView.as_view(), name='user-stats'),
    
    # Données géographiques et tableau de bord
    path('geographic-data/', views.GeographicDataView.as_view(), name='geographic-data'),
    path('verify-geographic/', views.GeographicVerificationView.as_view(), name='verify-geographic'),
    path('dashboard/', views.user_dashboard_data, name='dashboard'),
] 
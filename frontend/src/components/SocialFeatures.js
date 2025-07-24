import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  Users, 
  UserPlus, 
  MessageCircle, 
  Heart, 
  Share, 
  Gift, 
  Award, 
  Star,
  TrendingUp,
  Calendar,
  MapPin,
  Bell,
  CheckCircle,
  Clock,
  Users as GroupIcon,
  MessageSquare,
  Video,
  Camera,
  Mic,
  Phone,
  Mail,
  Send,
  MoreHorizontal,
  Settings,
  Shield,
  Eye,
  EyeOff,
  Lock,
  Globe,
  Hash,
  AtSign
} from 'lucide-react';
import toast from 'react-hot-toast';

const SocialFeatures = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('friends');
  const [friends, setFriends] = useState([]);
  const [groups, setGroups] = useState([]);
  const [events, setEvents] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [showCreateGroup, setShowCreateGroup] = useState(false);
  const [showCreateEvent, setShowCreateEvent] = useState(false);

  // États pour les nouvelles fonctionnalités
  const [onlineFriends, setOnlineFriends] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [suggestedConnections, setSuggestedConnections] = useState([]);
  const [socialScore, setSocialScore] = useState(0);
  const [suggestedGroups, setSuggestedGroups] = useState([]);
  const [suggestedEvents, setSuggestedEvents] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [socialStats, setSocialStats] = useState({});

  useEffect(() => {
    loadSocialData();
    loadSuggestions();
    loadLeaderboard();
    loadSocialStats();
  }, []);

  const loadSocialData = async () => {
    try {
      // Simuler le chargement des données sociales
      setFriends([
        { id: 1, name: 'Mamadou Diallo', avatar: '/default-avatar.svg', status: 'online', mutualFriends: 5 },
        { id: 2, name: 'Fatou Camara', avatar: '/default-avatar.svg', status: 'offline', mutualFriends: 3 },
        { id: 3, name: 'Ibrahima Bah', avatar: '/default-avatar.svg', status: 'online', mutualFriends: 7 }
      ]);

      setGroups([
        { id: 1, name: 'Quartier Kaloum', members: 45, type: 'neighborhood', isAdmin: true },
        { id: 2, name: 'Association des Jeunes', members: 120, type: 'community', isAdmin: false },
        { id: 3, name: 'Groupe de Football', members: 23, type: 'sports', isAdmin: false }
      ]);

      setEvents([
        { id: 1, title: 'Réunion de quartier', date: '2024-01-15', attendees: 25, type: 'meeting' },
        { id: 2, title: 'Match de football', date: '2024-01-20', attendees: 50, type: 'sports' },
        { id: 3, title: 'Fête de fin d\'année', date: '2024-12-31', attendees: 100, type: 'celebration' }
      ]);

      setAchievements([
        { id: 1, name: 'Premier Post', description: 'A publié son premier post', icon: '🌟', unlocked: true },
        { id: 2, name: 'Connecteur', description: 'A ajouté 10 amis', icon: '🤝', unlocked: true },
        { id: 3, name: 'Organisateur', description: 'A créé 3 événements', icon: '📅', unlocked: false }
      ]);

      setSocialStats({
        friends: 15,
        groups: 5,
        events: 8,
        posts: 23,
        likes: 156,
        shares: 34
      });

      setOnlineFriends([
        { id: 1, name: 'Mamadou Diallo', lastSeen: '2 min ago' },
        { id: 2, name: 'Fatou Camara', lastSeen: '5 min ago' }
      ]);

      setRecentActivity([
        { id: 1, type: 'friend_added', user: 'Mamadou Diallo', time: '2 min ago' },
        { id: 2, type: 'event_created', user: 'Fatou Camara', time: '1 heure ago' },
        { id: 3, type: 'post_liked', user: 'Ibrahima Bah', time: '3 heures ago' }
      ]);

      setSuggestedConnections([
        { id: 1, name: 'Aissatou Barry', mutualFriends: 8, reason: 'Même quartier' },
        { id: 2, name: 'Ousmane Keita', mutualFriends: 5, reason: 'Même groupe' },
        { id: 3, name: 'Mariama Sow', mutualFriends: 12, reason: 'Amis en commun' }
      ]);

      setSocialScore(750);
    } catch (error) {
      console.error('Erreur lors du chargement des données sociales:', error);
      toast.error('Erreur lors du chargement des données sociales');
    }
  };

  const loadSuggestions = async () => {
    try {
      // Charger les suggestions de groupes
      const groupsResponse = await fetch('/api/users/suggested-groups/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (groupsResponse.ok) {
        const groupsData = await groupsResponse.json();
        setSuggestedGroups(groupsData);
      }

      // Charger les suggestions d'événements
      const eventsResponse = await fetch('/api/users/suggested-events/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (eventsResponse.ok) {
        const eventsData = await eventsResponse.json();
        setSuggestedEvents(eventsData);
      }

      // Charger les suggestions de connexions
      const connectionsResponse = await fetch('/api/users/suggested-connections/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (connectionsResponse.ok) {
        const connectionsData = await connectionsResponse.json();
        setSuggestedConnections(connectionsData);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des suggestions:', error);
    }
  };

  const loadLeaderboard = async () => {
    try {
      const response = await fetch('/api/users/leaderboard/?limit=10', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setLeaderboard(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du classement:', error);
    }
  };

  const loadSocialStats = async () => {
    try {
      const response = await fetch(`/api/users/social-stats/${user.id}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setSocialStats(data);
        setSocialScore(data.social_score);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error);
    }
  };

  const handleAddFriend = async (friendId) => {
    try {
      // Simuler l'ajout d'ami
      toast.success('Demande d\'ami envoyée !');
    } catch (error) {
      toast.error('Erreur lors de l\'envoi de la demande');
    }
  };

  const handleJoinGroup = async (groupId) => {
    try {
      const response = await fetch('/api/users/groups/join/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ group_id: groupId })
      });

      if (response.ok) {
        toast.success('Demande d\'adhésion envoyée !');
        loadSuggestions(); // Recharger les suggestions
      } else {
        toast.error('Erreur lors de l\'envoi de la demande');
      }
    } catch (error) {
      toast.error('Erreur lors de l\'envoi de la demande');
    }
  };

  const handleJoinEvent = async (eventId) => {
    try {
      const response = await fetch('/api/users/events/join/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ event_id: eventId })
      });

      if (response.ok) {
        toast.success('Participation confirmée !');
        loadSuggestions(); // Recharger les suggestions
      } else {
        toast.error('Erreur lors de la confirmation');
      }
    } catch (error) {
      toast.error('Erreur lors de la confirmation');
    }
  };

  const handleCreateEvent = async (eventData) => {
    try {
      // Simuler la création d'événement
      toast.success('Événement créé avec succès !');
      setShowCreateEvent(false);
    } catch (error) {
      toast.error('Erreur lors de la création de l\'événement');
    }
  };

  const renderFriendsTab = () => (
    <div className="space-y-6">
      {/* Amis en ligne */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Users className="w-5 h-5 mr-2 text-green-600" />
          Amis en ligne ({onlineFriends.length})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {onlineFriends.map(friend => (
            <div key={friend.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="relative">
                <img src={friend.avatar} alt={friend.name} className="w-10 h-10 rounded-full" />
                <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div className="flex-1">
                <p className="font-medium text-sm">{friend.name}</p>
                <p className="text-xs text-gray-500">{friend.lastSeen}</p>
              </div>
              <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg">
                <MessageCircle className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Tous les amis */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Tous mes amis ({friends.length})</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {friends.map(friend => (
            <div key={friend.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="relative">
                <img src={friend.avatar} alt={friend.name} className="w-10 h-10 rounded-full" />
                <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
                  friend.status === 'online' ? 'bg-green-500' : 'bg-gray-400'
                }`}></div>
              </div>
              <div className="flex-1">
                <p className="font-medium text-sm">{friend.name}</p>
                <p className="text-xs text-gray-500">{friend.mutualFriends} amis en commun</p>
              </div>
              <div className="flex space-x-1">
                <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg">
                  <MessageCircle className="w-4 h-4" />
                </button>
                <button className="p-2 text-green-600 hover:bg-green-50 rounded-lg">
                  <Phone className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Suggestions de connexions */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Suggestions de connexions</h3>
        <div className="space-y-3">
          {suggestedConnections.map(suggestion => (
            <div key={suggestion.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <img src="/default-avatar.svg" alt={suggestion.name} className="w-10 h-10 rounded-full" />
                <div>
                  <p className="font-medium text-sm">{suggestion.name}</p>
                  <p className="text-xs text-gray-500">{suggestion.reason} • {suggestion.mutualFriends} amis en commun</p>
                </div>
              </div>
              <button 
                onClick={() => handleAddFriend(suggestion.id)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <UserPlus className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderGroupsTab = () => (
    <div className="space-y-6">
      {/* Mes groupes */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Mes groupes ({groups.length})</h3>
          <button 
            onClick={() => setShowCreateGroup(true)}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Créer un groupe
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {groups.map(group => (
            <div key={group.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold">{group.name}</h4>
                {group.isAdmin && <Award className="w-4 h-4 text-yellow-600" />}
              </div>
              <p className="text-sm text-gray-600 mb-2">{group.members} membres</p>
              <div className="flex items-center space-x-2">
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                  {group.type}
                </span>
                <button className="text-xs text-blue-600 hover:underline">Voir</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Groupes suggérés */}
      {suggestedGroups.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4">Groupes suggérés</h3>
          <div className="space-y-3">
            {suggestedGroups.map(group => (
              <div key={group.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <img src={group.profile_image || "/default-avatar.svg"} alt={group.name} className="w-10 h-10 rounded-full" />
                  <div>
                    <p className="font-medium text-sm">{group.name}</p>
                    <p className="text-xs text-gray-500">{group.member_count} membres • {group.group_type}</p>
                  </div>
                </div>
                <button 
                  onClick={() => handleJoinGroup(group.id)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Rejoindre
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderEventsTab = () => (
    <div className="space-y-6">
      {/* Mes événements */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Mes événements ({events.length})</h3>
          <button 
            onClick={() => setShowCreateEvent(true)}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Créer un événement
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {events.map(event => (
            <div key={event.id} className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold mb-2">{event.title}</h4>
              <p className="text-sm text-gray-600 mb-2">{event.attendees} participants</p>
              <div className="flex items-center space-x-2">
                <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
                  {event.type}
                </span>
                <span className="text-xs text-gray-500">{event.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Événements suggérés */}
      {suggestedEvents.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4">Événements suggérés</h3>
          <div className="space-y-3">
            {suggestedEvents.map(event => (
              <div key={event.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <img src={event.cover_image || "/default-avatar.svg"} alt={event.title} className="w-10 h-10 rounded-full" />
                  <div>
                    <p className="font-medium text-sm">{event.title}</p>
                    <p className="text-xs text-gray-500">{event.attendee_count} participants • {event.event_type}</p>
                  </div>
                </div>
                <button 
                  onClick={() => handleJoinEvent(event.id)}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Participer
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderAchievementsTab = () => (
    <div className="space-y-6">
      {/* Score social */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mon score social</h3>
        <div className="flex items-center space-x-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{socialScore}</div>
            <div className="text-sm text-gray-500">Points totaux</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{socialStats.level || 1}</div>
            <div className="text-sm text-gray-500">Niveau</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">{socialStats.achievements_count || 0}</div>
            <div className="text-sm text-gray-500">Réalisations</div>
          </div>
        </div>
      </div>

      {/* Statistiques détaillées */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mes statistiques</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{socialStats.friends_count || 0}</div>
            <div className="text-sm text-gray-500">Amis</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{socialStats.groups_count || 0}</div>
            <div className="text-sm text-gray-500">Groupes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{socialStats.events_count || 0}</div>
            <div className="text-sm text-gray-500">Événements</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{socialStats.posts_count || 0}</div>
            <div className="text-sm text-gray-500">Posts</div>
          </div>
        </div>
      </div>

      {/* Réalisations */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mes réalisations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {achievements.map(achievement => (
            <div key={achievement.id} className={`p-4 rounded-lg border-2 ${
              achievement.unlocked ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-gray-50'
            }`}>
              <div className="flex items-center space-x-3">
                <div className="text-2xl">{achievement.icon}</div>
                <div>
                  <h4 className="font-semibold">{achievement.title}</h4>
                  <p className="text-sm text-gray-600">{achievement.description}</p>
                  {achievement.unlocked && (
                    <p className="text-xs text-green-600 mt-1">+{achievement.points} points</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Classement */}
      {leaderboard.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4">Classement du quartier</h3>
          <div className="space-y-3">
            {leaderboard.map((user, index) => (
              <div key={user.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {index + 1}
                  </div>
                  <img src={user.user.profile_picture || "/default-avatar.svg"} alt={user.user.username} className="w-10 h-10 rounded-full" />
                  <div>
                    <p className="font-medium text-sm">{user.user.first_name} {user.user.last_name}</p>
                    <p className="text-xs text-gray-500">Niveau {user.level}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-blue-600">{user.total_points}</div>
                  <div className="text-xs text-gray-500">points</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Onglets */}
      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-6">
        {[
          { id: 'friends', label: 'Amis', icon: Users },
          { id: 'groups', label: 'Groupes', icon: GroupIcon },
          { id: 'events', label: 'Événements', icon: Calendar },
          { id: 'achievements', label: 'Réalisations', icon: Award }
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                activeTab === tab.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'friends' && renderFriendsTab()}
      {activeTab === 'groups' && renderGroupsTab()}
      {activeTab === 'events' && renderEventsTab()}
      {activeTab === 'achievements' && renderAchievementsTab()}
    </div>
  );
};

export default SocialFeatures; 
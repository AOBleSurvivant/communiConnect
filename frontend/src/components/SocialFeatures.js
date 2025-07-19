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
  const [socialStats, setSocialStats] = useState({});
  const [showCreateGroup, setShowCreateGroup] = useState(false);
  const [showCreateEvent, setShowCreateEvent] = useState(false);

  // États pour les nouvelles fonctionnalités
  const [onlineFriends, setOnlineFriends] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [suggestedConnections, setSuggestedConnections] = useState([]);
  const [socialScore, setSocialScore] = useState(0);

  useEffect(() => {
    loadSocialData();
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
      // Simuler l'adhésion à un groupe
      toast.success('Demande d\'adhésion envoyée !');
    } catch (error) {
      toast.error('Erreur lors de l\'envoi de la demande');
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
        <div className="space-y-4">
          {events.map(event => (
            <div key={event.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-semibold">{event.title}</h4>
                  <p className="text-sm text-gray-600">{event.date} • {event.attendees} participants</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
                  {event.type}
                </span>
                <button className="text-xs text-blue-600 hover:underline">Gérer</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderAchievementsTab = () => (
    <div className="space-y-6">
      {/* Score social */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mon score social</h3>
        <div className="flex items-center space-x-4">
          <div className="text-3xl font-bold text-blue-600">{socialScore}</div>
          <div className="flex-1">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(socialScore / 1000) * 100}%` }}></div>
            </div>
            <p className="text-sm text-gray-600 mt-1">Niveau {Math.floor(socialScore / 100)}</p>
          </div>
        </div>
      </div>

      {/* Statistiques sociales */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mes statistiques</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{socialStats.friends}</div>
            <div className="text-sm text-gray-600">Amis</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <GroupIcon className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{socialStats.groups}</div>
            <div className="text-sm text-gray-600">Groupes</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <Calendar className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{socialStats.events}</div>
            <div className="text-sm text-gray-600">Événements</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <Heart className="w-8 h-8 text-orange-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{socialStats.likes}</div>
            <div className="text-sm text-gray-600">J'aime</div>
          </div>
        </div>
      </div>

      {/* Réalisations */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Mes réalisations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {achievements.map(achievement => (
            <div key={achievement.id} className={`p-4 rounded-lg border-2 ${
              achievement.unlocked 
                ? 'bg-green-50 border-green-200' 
                : 'bg-gray-50 border-gray-200'
            }`}>
              <div className="flex items-center space-x-3">
                <div className="text-2xl">{achievement.icon}</div>
                <div>
                  <h4 className={`font-semibold ${
                    achievement.unlocked ? 'text-green-800' : 'text-gray-600'
                  }`}>
                    {achievement.name}
                  </h4>
                  <p className="text-sm text-gray-600">{achievement.description}</p>
                </div>
                {achievement.unlocked && <CheckCircle className="w-5 h-5 text-green-600" />}
              </div>
            </div>
          ))}
        </div>
      </div>
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
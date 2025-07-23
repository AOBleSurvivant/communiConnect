import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { postsAPI } from '../services/postsAPI';
import CreatePost from '../components/CreatePost';
import PostCard from '../components/PostCard';
import LiveStream from '../components/LiveStream';
import CameraTest from '../components/CameraTest';
import { 
  Plus, 
  Video, 
  MessageCircle, 
  Calendar,
  HelpCircle,
  AlertCircle,
  Users,
  Search,
  RefreshCw,
  Camera
} from 'lucide-react';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [showLiveStream, setShowLiveStream] = useState(false);
  const [showCameraTest, setShowCameraTest] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const postTypeFilters = [
    { value: 'all', label: 'Tous', icon: MessageCircle },
    { value: 'info', label: 'Informations', icon: AlertCircle },
    { value: 'event', label: 'Événements', icon: Calendar },
    { value: 'help', label: 'Demandes d\'aide', icon: HelpCircle },
    { value: 'announcement', label: 'Annonces', icon: Users },
    { value: 'live', label: 'Lives', icon: Video }
  ];

  const fetchPosts = useCallback(async () => {
    console.log('🔍 fetchPosts appelé avec:', { selectedFilter, searchTerm });
    setIsLoading(true);
    try {
      const params = {};
      if (selectedFilter !== 'all') {
        params.type = selectedFilter;
      }
      if (searchTerm) {
        params.search = searchTerm;
      }
      
      console.log('📝 Appel API avec params:', params);
      const response = await postsAPI.getPosts(params);
      console.log('📊 Réponse API reçue:', response);
      
      // Gérer la structure paginée de l'API et s'assurer que posts est toujours un tableau
      let postsData = [];
      if (response && typeof response === 'object') {
        if (Array.isArray(response)) {
          postsData = response;
          console.log('📊 Réponse est un tableau direct');
        } else if (response.results && Array.isArray(response.results)) {
          postsData = response.results;
          console.log('📊 Réponse contient results');
        } else if (response.data && Array.isArray(response.data)) {
          postsData = response.data;
          console.log('📊 Réponse contient data');
        }
      }
      
      console.log('📊 PostsData final:', postsData);
      console.log('📊 Nombre de posts:', postsData.length);
      setPosts(postsData);
    } catch (error) {
      console.error('❌ Erreur lors du chargement des posts:', error);
      toast.error('Erreur lors du chargement des publications');
      setPosts([]); // S'assurer que posts est un tableau vide en cas d'erreur
    } finally {
      setIsLoading(false);
    }
  }, [selectedFilter, searchTerm]);

  useEffect(() => {
    console.log('👤 useEffect Dashboard - user:', user);
    if (user) { // Assuming user is available from useAuth
      console.log('✅ Utilisateur connecté, appel fetchPosts');
      fetchPosts();
    } else {
      console.log('❌ Utilisateur non connecté');
    }
  }, [user, fetchPosts]); // Ajouté fetchPosts avec useCallback pour éviter la boucle



  const handlePostCreated = (newPost) => {
    setPosts(prev => [newPost, ...prev]);
  };

  const handleLiveStarted = (liveData) => {
    // Le live sera automatiquement ajouté aux posts
    fetchPosts();
  };

  const handleLiveStopped = (stopData) => {
    // Rafraîchir les posts pour afficher la vidéo enregistrée
    console.log('🔄 Live arrêté, rafraîchissement des posts...', stopData);
    fetchPosts();
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchPosts();
  };

  const handleRefresh = () => {
    fetchPosts();
  };

  const filteredPosts = Array.isArray(posts) ? posts.filter(post => {
    if (selectedFilter !== 'all' && post.post_type !== selectedFilter) {
      return false;
    }
    
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return (
        post.content?.toLowerCase().includes(searchLower) ||
        post.title?.toLowerCase().includes(searchLower) ||
        post.author.first_name?.toLowerCase().includes(searchLower) ||
        post.author.last_name?.toLowerCase().includes(searchLower)
      );
    }
    
    return true;
  }) : [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Bonjour, {user?.first_name || 'utilisateur'} !
              </h1>
              <p className="text-gray-600 mt-2">
                Restez connecté avec votre communauté locale
              </p>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowCreatePost(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Nouvelle publication</span>
            </button>
            
            <button
              onClick={() => setShowLiveStream(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Video className="w-4 h-4" />
              <span>Lancer un live</span>
            </button>
            
            <button
              onClick={() => setShowCameraTest(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Camera className="w-4 h-4" />
              <span>Test Caméra</span>
            </button>
          </div>
        </div>

        {/* Filtres et recherche */}
        <div className="mb-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between space-y-4 md:space-y-0">
            {/* Filtres par type */}
            <div className="flex items-center space-x-2 overflow-x-auto pb-2">
              {postTypeFilters.map((filter) => {
                const Icon = filter.icon;
                return (
                  <button
                    key={filter.value}
                    onClick={() => setSelectedFilter(filter.value)}
                    className={`flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                      selectedFilter === filter.value
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{filter.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Recherche */}
            <form onSubmit={handleSearch} className="flex items-center space-x-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Rechercher des publications..."
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Rechercher
              </button>
            </form>
          </div>
        </div>

        {/* Liste des posts */}
        <div className="space-y-6">
          {console.log('🎨 Rendu Dashboard - isLoading:', isLoading, 'filteredPosts:', filteredPosts.length)}
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="flex items-center space-x-2">
                <RefreshCw className="w-6 h-6 animate-spin text-blue-600" />
                <span className="text-gray-600">Chargement des publications...</span>
              </div>
            </div>
          ) : filteredPosts.length > 0 ? (
            filteredPosts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onUpdate={fetchPosts}
              />
            ))
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Aucune publication trouvée
              </h3>
              <p className="text-gray-600 mb-4">
                {searchTerm || selectedFilter !== 'all' 
                  ? 'Essayez de modifier vos filtres ou votre recherche'
                  : 'Soyez le premier à partager quelque chose avec votre communauté !'
                }
              </p>
              <button
                onClick={() => setShowCreatePost(true)}
                className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Créer une publication</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      <CreatePost
        isOpen={showCreatePost}
        onClose={() => setShowCreatePost(false)}
        onPostCreated={handlePostCreated}
      />

      <LiveStream
        isOpen={showLiveStream}
        onClose={() => setShowLiveStream(false)}
        onLiveStarted={handleLiveStarted}
        onLiveStopped={handleLiveStopped}
      />

      <CameraTest
        isOpen={showCameraTest}
        onClose={() => setShowCameraTest(false)}
      />
    </div>
  );
};

export default Dashboard; 
import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { postsAPI, sharePost, repostPost, unsharePost, sharePostExternal, generateShareLinks, getPostAnalytics, updatePost } from '../services/postsAPI';
import MediaGallery from './MediaGallery';
import EditPostModal from './EditPostModal';
import { 
  Heart, 
  MessageCircle, 
  Eye, 
  MoreVertical,
  Calendar,
  HelpCircle,
  AlertCircle,
  Users,
  MessageCircle as DiscussionIcon,
  Video,
  Image,
  Play,
  Globe,
  Users as UsersIcon,
  Lock,
  EyeOff,
  Share,
  Repeat,
  ExternalLink,
  Copy,
  Mail,
  MessageSquare,
  BarChart3,
  Flame,
  Zap,
  TrendingUp,
  Edit,
  Trash2,
  AlertTriangle
} from 'lucide-react';
import toast from 'react-hot-toast';

// Fonction utilitaire pour vérifier si un post peut être modifié
const canEditPost = (post, user) => {
  if (!user || !post) return false;
  if (post.author.id !== user.id) return false;
  
  // Vérifier si le post a moins de 30 minutes
  const postDate = new Date(post.created_at);
  const now = new Date();
  const diffInMinutes = Math.floor((now - postDate) / (1000 * 60));
  
  return diffInMinutes <= 30;
};

const PostCard = ({ post, onUpdate }) => {
  const { user } = useAuth();
  const [isLiking, setIsLiking] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [isAddingComment, setIsAddingComment] = useState(false);
  const [replyingTo, setReplyingTo] = useState(null);
  const [replyContent, setReplyContent] = useState('');
  const [isAddingReply, setIsAddingReply] = useState(false);
  const [isSharing, setIsSharing] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const [shareComment, setShareComment] = useState('');
  const [shareType, setShareType] = useState('share');
  const [showExternalShareModal, setShowExternalShareModal] = useState(false);
  const [isSharingExternal, setIsSharingExternal] = useState(false);
  const [showAnalyticsModal, setShowAnalyticsModal] = useState(false);
  const [postAnalytics, setPostAnalytics] = useState(null);
  const [loadingAnalytics, setLoadingAnalytics] = useState(false);
  
  // États pour la modification
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(post.content || '');
  const [editTitle, setEditTitle] = useState(post.title || '');
  const [editPostType, setEditPostType] = useState(post.post_type || 'info');
  const [isSavingEdit, setIsSavingEdit] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  // États pour la suppression
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);

  // Gestion des clics en dehors du menu
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showMenu]);

  // Safety check for post object - after all hooks
  if (!post) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <p className="text-gray-500 text-center">Post non disponible</p>
      </div>
    );
  }

  // Fonctions pour la modification
  const handleEditPost = () => {
    setEditContent(post.content || '');
    setEditTitle(post.title || '');
    setEditPostType(post.post_type || 'info');
    setShowEditModal(true);
  };

  const handleSaveEdit = async () => {
    if (!editContent.trim() || !post?.id) return;
    
    setIsSavingEdit(true);
    try {
      const updatedPost = await postsAPI.updatePost(post.id, {
        content: editContent,
        title: editTitle,
        post_type: editPostType
      });
      
      toast.success('Post modifié avec succès !');
      setShowEditModal(false);
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors de la modification:', error);
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else {
        toast.error('Erreur lors de la modification du post');
      }
    } finally {
      setIsSavingEdit(false);
    }
  };

  const handleCancelEdit = () => {
    setShowEditModal(false);
    setEditContent(post.content || '');
    setEditTitle(post.title || '');
    setEditPostType(post.post_type || 'info');
  };

  // Fonctions pour la suppression
  const handleDeletePost = () => {
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    if (!post?.id) return;
    
    setIsDeleting(true);
    try {
      await postsAPI.deletePost(post.id);
      toast.success('Post supprimé avec succès !');
      setShowDeleteModal(false);
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else {
        toast.error('Erreur lors de la suppression du post');
      }
    } finally {
      setIsDeleting(false);
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
  };

  // Fonctions pour le menu
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  const closeMenu = () => {
    setShowMenu(false);
  };

  const postTypeIcons = {
    info: AlertCircle,
    event: Calendar,
    help: HelpCircle,
    announcement: Users,
    discussion: DiscussionIcon,
    live: Video
  };

  const postTypeColors = {
    info: 'bg-blue-100 text-blue-800',
    event: 'bg-green-100 text-green-800',
    help: 'bg-red-100 text-red-800',
    announcement: 'bg-purple-100 text-purple-800',
    discussion: 'bg-orange-100 text-orange-800',
    live: 'bg-red-100 text-red-800'
  };

  const postTypeLabels = {
    info: 'Information',
    event: 'Événement',
    help: 'Demande d\'aide',
    announcement: 'Annonce',
    discussion: 'Discussion',
    live: 'Live'
  };

  const privacyIcons = {
    public: Globe,
    friends: UsersIcon,
    private: Lock
  };

  const privacyLabels = {
    public: 'Public',
    friends: 'Amis',
    private: 'Privé'
  };

  const handleLike = async () => {
    if (isLiking || !post?.id) return;
    
    setIsLiking(true);
    try {
      if (post.is_liked_by_user) {
        await postsAPI.unlikePost(post.id);
        toast.success('Like retiré');
      } else {
        await postsAPI.likePost(post.id);
        toast.success('Post liké !');
      }
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors du like:', error);
      toast.error('Erreur lors du like');
    } finally {
      setIsLiking(false);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim() || !post?.id) return;

    setIsAddingComment(true);
    try {
      await postsAPI.addComment(post.id, { content: newComment });
      setNewComment('');
      toast.success('Commentaire ajouté !');
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors de l\'ajout du commentaire:', error);
      toast.error('Erreur lors de l\'ajout du commentaire');
    } finally {
      setIsAddingComment(false);
    }
  };

  const handleReplyToComment = async (e) => {
    e.preventDefault();
    
    if (!replyContent.trim() || !replyingTo) return;
    
    setIsAddingReply(true);
    try {
      await postsAPI.replyToComment(replyingTo.id, { content: replyContent });
      setReplyContent('');
      setReplyingTo(null);
      toast.success('Réponse ajoutée !');
      onUpdate?.();
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la réponse:', error);
      toast.error('Erreur lors de l\'ajout de la réponse');
    } finally {
      setIsAddingReply(false);
    }
  };

  const startReply = (comment) => {
    setReplyingTo(comment);
    setReplyContent('');
  };

  const cancelReply = () => {
    setReplyingTo(null);
    setReplyContent('');
  };

  const handleShare = async () => {
    if (isSharing || !post?.id) return;
    
    setIsSharing(true);
    try {
      if (shareType === 'repost') {
        await repostPost(post.id, { comment: shareComment });
        toast.success('Post reposté avec succès !');
      } else {
        await sharePost(post.id, { comment: shareComment });
        toast.success('Post partagé avec succès !');
      }
      
      setShowShareModal(false);
      setShareComment('');
      setShareType('share');
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors du partage:', error);
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else {
        toast.error('Erreur lors du partage');
      }
    } finally {
      setIsSharing(false);
    }
  };

  const handleUnshare = async () => {
    if (isSharing || !post?.id) return;
    
    setIsSharing(true);
    try {
      await unsharePost(post.id);
      toast.success('Partage supprimé !');
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors de la suppression du partage:', error);
      toast.error('Erreur lors de la suppression du partage');
    } finally {
      setIsSharing(false);
    }
  };

  const handleExternalShare = async (platform) => {
    if (isSharingExternal || !post?.id) return;
    
    setIsSharingExternal(true);
    try {
      // Enregistrer le partage externe
      await sharePostExternal(post.id, platform);
      
      // Générer le lien de partage
      const shareLinks = generateShareLinks(post.id, post.content);
      const shareUrl = shareLinks[platform];
      
      if (platform === 'copy_link') {
        // Copier le lien dans le presse-papiers
        navigator.clipboard.writeText(shareUrl);
        toast.success('Lien copié dans le presse-papiers !');
      } else {
        // Ouvrir le lien de partage
        window.open(shareUrl, '_blank');
        toast.success(`Post partagé sur ${getPlatformName(platform)} !`);
      }
      
      setShowExternalShareModal(false);
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Erreur lors du partage externe:', error);
      toast.error('Erreur lors du partage externe');
    } finally {
      setIsSharingExternal(false);
    }
  };

  const getPlatformName = (platform) => {
    const names = {
      whatsapp: 'WhatsApp',
      facebook: 'Facebook',
      twitter: 'Twitter',
      telegram: 'Telegram',
      email: 'Email',
      copy_link: 'Presse-papiers'
    };
    return names[platform] || platform;
  };

  const handleShowAnalytics = async () => {
    if (!post?.id || loadingAnalytics) return;
    
    setLoadingAnalytics(true);
    try {
      const analytics = await getPostAnalytics(post.id);
      setPostAnalytics(analytics);
      setShowAnalyticsModal(true);
    } catch (error) {
      console.error('Erreur lors du chargement des analytics:', error);
      toast.error('Erreur lors du chargement des statistiques');
    } finally {
      setLoadingAnalytics(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'À l\'instant';
    if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `Il y a ${diffInHours}h`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `Il y a ${diffInDays}j`;
    
    return date.toLocaleDateString('fr-FR');
  };

  const PostTypeIcon = postTypeIcons[post.post_type] || AlertCircle;
  const PrivacyIcon = privacyIcons[post.privacy] || Globe;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="p-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <img
              src={post.author?.profile_picture || '/default-avatar.svg'}
              alt={post.author?.first_name || 'Utilisateur'}
              className="w-10 h-10 rounded-full object-cover"
            />
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <h4 className="text-sm font-semibold text-gray-900">
                {post.is_anonymous ? 'Anonyme' : `${post.author?.first_name || 'Utilisateur'} ${post.author?.last_name || ''}`}
              </h4>
              
              {/* Badge Live */}
              {post.is_live_post && (
                <div className="flex items-center space-x-1 bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-medium">
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
                  <span>EN DIRECT</span>
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-2 text-xs text-gray-500 mt-1">
              <span>{formatTimestamp(post.created_at)}</span>
              <span>•</span>
              <span>{post.quartier?.nom || 'Quartier inconnu'}, {post.quartier?.commune?.nom || 'Commune inconnue'}</span>
              <span>•</span>
              <div className="flex items-center space-x-1">
                <PrivacyIcon className="w-3 h-3" />
                <span>{privacyLabels[post.privacy]}</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${postTypeColors[post.post_type]}`}>
              <PostTypeIcon className="w-3 h-3 mr-1" />
              {postTypeLabels[post.post_type]}
            </span>
            
            {/* Menu des actions pour l'auteur du post */}
            {user && post.author?.id === user.id && (
              <div className="relative" ref={menuRef}>
                <button 
                  onClick={toggleMenu}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <MoreVertical className="w-4 h-4" />
                </button>
                
                {/* Menu déroulant */}
                {showMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                    <div className="py-1">
                      {/* Bouton Modifier */}
                      {canEditPost(post, user) && (
                        <button
                          onClick={() => {
                            closeMenu();
                            handleEditPost();
                          }}
                          className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                        >
                          <Edit className="w-4 h-4 mr-2" />
                          Modifier
                        </button>
                      )}
                      
                      {/* Bouton Supprimer */}
                      <button
                        onClick={() => {
                          closeMenu();
                          handleDeletePost();
                        }}
                        className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Supprimer
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {/* Bouton menu simple pour les autres utilisateurs */}
            {(!user || post.author?.id !== user.id) && (
              <button className="text-gray-400 hover:text-gray-600 transition-colors">
                <MoreVertical className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Contenu */}
      {post.content && (
        <div className="px-4 pb-4">
          <p className="text-gray-900 whitespace-pre-wrap">{post.content}</p>
        </div>
      )}

      {/* Médias */}
      {post.has_media && post.media_files && post.media_files.length > 0 && (
        <div className="px-4 pb-4">
          <MediaGallery 
            media={post.media_files} 
            className="rounded-lg overflow-hidden"
          />
        </div>
      )}

      {/* Live Stream */}
      {post.live_stream && post.live_stream.id && (
        <div className="px-4 pb-4">
          <MediaGallery 
            media={[post.live_stream]} 
            className="rounded-lg overflow-hidden"
          />
        </div>
      )}

      {/* Statistiques */}
      <div className="px-4 py-3 border-t border-gray-100">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center space-x-4">
            {post.likes_count > 0 && (
              <span>{post.likes_count} j'aime</span>
            )}
            {post.comments_count > 0 && (
              <span>{post.comments_count} commentaires</span>
            )}
            {post.views_count > 0 && (
              <span>{post.views_count} vues</span>
            )}
          </div>
          
          <div className="flex items-center space-x-1">
            <Eye className="w-4 h-4" />
            <span>{post.views_count}</span>
          </div>
          
          {post.shares_count > 0 && (
            <div className="flex items-center space-x-1">
              <Share className="w-4 h-4" />
              <span>{post.shares_count}</span>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="px-4 py-2 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <button
            onClick={handleLike}
            disabled={isLiking || !post?.id}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              post.is_liked_by_user
                ? 'text-red-600 bg-red-50 hover:bg-red-100'
                : 'text-gray-600 hover:bg-gray-100'
            } ${!post?.id ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <Heart className={`w-4 h-4 ${post.is_liked_by_user ? 'fill-current' : ''}`} />
            <span className="text-sm font-medium">J'aime</span>
          </button>
          
          <button
            onClick={() => setShowComments(!showComments)}
            disabled={!post?.id}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors ${!post?.id ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <MessageCircle className="w-4 h-4" />
            <span className="text-sm font-medium">Commenter</span>
          </button>
          
          <button
            onClick={() => setShowShareModal(true)}
            disabled={!post?.id}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors ${!post?.id ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <Share className="w-4 h-4" />
            <span className="text-sm font-medium">Partager</span>
          </button>
          
          <button
            onClick={() => setShowExternalShareModal(true)}
            disabled={!post?.id || isSharingExternal}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-blue-600 hover:bg-blue-50 transition-colors ${!post?.id || isSharingExternal ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <ExternalLink className="w-4 h-4" />
            <span className="text-sm font-medium">Partager Externe</span>
          </button>
          
          <button
            onClick={handleShowAnalytics}
            disabled={!post?.id || loadingAnalytics}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-green-600 hover:bg-green-50 transition-colors ${!post?.id || loadingAnalytics ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <BarChart3 className="w-4 h-4" />
            <span className="text-sm font-medium">Analytics</span>
          </button>
        </div>
      </div>

      {/* Commentaires */}
      {showComments && (
        <div className="border-t border-gray-100">
          {/* Liste des commentaires */}
          <div className="px-4 py-3 max-h-64 overflow-y-auto">
            {post.comments && Array.isArray(post.comments) && post.comments.length > 0 ? (
              <div className="space-y-3">
                {post.comments.map((comment) => (
                  <div key={comment.id} className="space-y-2">
                    {/* Commentaire principal */}
                    <div className="flex space-x-3">
                    <img
                      src={comment.author?.profile_picture || '/default-avatar.svg'}
                      alt={comment.author?.first_name || 'Utilisateur'}
                      className="w-6 h-6 rounded-full object-cover flex-shrink-0"
                    />
                    <div className="flex-1">
                      <div className="bg-gray-50 rounded-lg px-3 py-2">
                          <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-medium text-gray-900">
                            {comment.is_anonymous ? 'Anonyme' : `${comment.author?.first_name || 'Utilisateur'} ${comment.author?.last_name || ''}`}
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatTimestamp(comment.created_at)}
                          </span>
                            </div>
                            <button
                              onClick={() => startReply(comment)}
                              className="text-xs text-blue-600 hover:text-blue-800 transition-colors"
                            >
                              Répondre
                            </button>
                        </div>
                        <p className="text-sm text-gray-700 mt-1">{comment.content}</p>
                        </div>
                      </div>
                    </div>

                    {/* Réponses au commentaire */}
                    {comment.replies && Array.isArray(comment.replies) && comment.replies.length > 0 && (
                      <div className="ml-9 space-y-2">
                        {comment.replies.map((reply) => (
                          <div key={reply.id} className="flex space-x-3">
                            <img
                              src={reply.author?.profile_picture || '/default-avatar.svg'}
                              alt={reply.author?.first_name || 'Utilisateur'}
                              className="w-5 h-5 rounded-full object-cover flex-shrink-0"
                            />
                            <div className="flex-1">
                              <div className="bg-gray-100 rounded-lg px-3 py-2">
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center space-x-2">
                                    <span className="text-sm font-medium text-gray-900">
                                      {reply.is_anonymous ? 'Anonyme' : `${reply.author?.first_name || 'Utilisateur'} ${reply.author?.last_name || ''}`}
                                    </span>
                                    <span className="text-xs text-gray-500">
                                      {formatTimestamp(reply.created_at)}
                                    </span>
                                  </div>
                                  {reply.level < 3 && (
                                    <button
                                      onClick={() => startReply(reply)}
                                      className="text-xs text-blue-600 hover:text-blue-800 transition-colors"
                                    >
                                      Répondre
                                    </button>
                                  )}
                                </div>
                                <p className="text-sm text-gray-700 mt-1">{reply.content}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Formulaire de réponse */}
                    {replyingTo && replyingTo.id === comment.id && (
                      <div className="ml-9">
                        <form onSubmit={handleReplyToComment} className="flex space-x-2">
                          <img
                            src={user?.profile_picture || '/default-avatar.svg'}
                            alt={user?.first_name || 'Utilisateur'}
                            className="w-5 h-5 rounded-full object-cover flex-shrink-0"
                          />
                          <div className="flex-1">
                            <input
                              type="text"
                              value={replyContent}
                              onChange={(e) => setReplyContent(e.target.value)}
                              placeholder={`Répondre à ${replyingTo.author?.first_name || 'Utilisateur'}...`}
                              className="w-full px-2 py-1 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-blue-500 focus:border-transparent"
                              disabled={isAddingReply}
                            />
                          </div>
                          <div className="flex space-x-1">
                            <button
                              type="submit"
                              disabled={!replyContent.trim() || isAddingReply}
                              className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                              {isAddingReply ? 'Envoi...' : 'Envoyer'}
                            </button>
                            <button
                              type="button"
                              onClick={cancelReply}
                              className="px-2 py-1 text-xs text-gray-600 hover:text-gray-800 transition-colors"
                            >
                              Annuler
                            </button>
                          </div>
                        </form>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500 text-center py-4">
                Aucun commentaire pour le moment
              </p>
            )}
          </div>

          {/* Formulaire de commentaire */}
          <div className="px-4 py-3 border-t border-gray-100">
            <form onSubmit={handleAddComment} className="flex space-x-3">
              <img
                src={user?.profile_picture || '/default-avatar.svg'}
                alt={user?.first_name || 'Utilisateur'}
                className="w-8 h-8 rounded-full object-cover flex-shrink-0"
              />
              <div className="flex-1">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Ajouter un commentaire..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  disabled={isAddingComment}
                />
              </div>
              <button
                type="submit"
                disabled={!newComment.trim() || isAddingComment}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
              >
                {isAddingComment ? 'Envoi...' : 'Envoyer'}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Modal de Partage */}
      {showShareModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Partager ce post
              </h3>
              <button
                onClick={() => setShowShareModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              {/* Type de partage */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Type de partage
                </label>
                <select 
                  value={shareType} 
                  onChange={(e) => setShareType(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="share">Partage simple</option>
                  <option value="repost">Repost avec commentaire</option>
                </select>
              </div>

              {/* Commentaire pour repost */}
              {shareType === 'repost' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Votre commentaire
                  </label>
                  <textarea
                    value={shareComment}
                    onChange={(e) => setShareComment(e.target.value)}
                    placeholder="Ajoutez votre commentaire sur ce post..."
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 h-20 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    maxLength={500}
                  />
                  <div className="text-xs text-gray-500 mt-1 text-right">
                    {shareComment.length}/500
                  </div>
                </div>
              )}

              {/* Boutons d'action */}
              <div className="flex space-x-3 pt-4">
                <button
                  onClick={handleShare}
                  disabled={isSharing || (shareType === 'repost' && !shareComment.trim())}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isSharing ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Partage...
                    </span>
                  ) : (
                    shareType === 'repost' ? 'Reposter' : 'Partager'
                  )}
                </button>
                
                <button
                  onClick={() => {
                    setShowShareModal(false);
                    setShareComment('');
                    setShareType('share');
                  }}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors font-medium"
                >
                  Annuler
                </button>
              </div>

              {/* Informations */}
              <div className="text-xs text-gray-500 text-center">
                {shareType === 'share' ? 
                  'Ce post sera partagé avec votre communauté' : 
                  'Vous reposterez ce contenu avec votre commentaire'
                }
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Partage Externe */}
      {showExternalShareModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Partager sur les réseaux sociaux
              </h3>
              <button
                onClick={() => setShowExternalShareModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-3">
              <p className="text-sm text-gray-600 mb-4">
                Partagez ce post sur vos réseaux sociaux préférés
              </p>
              
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => handleExternalShare('whatsapp')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <MessageSquare className="w-5 h-5" />
                  <span className="text-sm font-medium">WhatsApp</span>
                </button>
                
                <button
                  onClick={() => handleExternalShare('facebook')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                  <span className="text-sm font-medium">Facebook</span>
                </button>
                
                <button
                  onClick={() => handleExternalShare('twitter')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                  </svg>
                  <span className="text-sm font-medium">Twitter</span>
                </button>
                
                <button
                  onClick={() => handleExternalShare('telegram')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
                  </svg>
                  <span className="text-sm font-medium">Telegram</span>
                </button>
                
                <button
                  onClick={() => handleExternalShare('email')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Mail className="w-5 h-5" />
                  <span className="text-sm font-medium">Email</span>
                </button>
                
                <button
                  onClick={() => handleExternalShare('copy_link')}
                  disabled={isSharingExternal}
                  className="flex items-center justify-center space-x-2 p-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Copy className="w-5 h-5" />
                  <span className="text-sm font-medium">Copier le lien</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal Analytics */}
      {showAnalyticsModal && postAnalytics && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Analytics du Post
              </h3>
              <button
                onClick={() => setShowAnalyticsModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Métriques de base */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-blue-50 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-600">Vues</p>
                      <p className="text-lg font-bold text-blue-600">{postAnalytics.total_views}</p>
                    </div>
                    <Eye className="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                
                <div className="bg-red-50 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-600">Likes</p>
                      <p className="text-lg font-bold text-red-600">{postAnalytics.total_likes}</p>
                    </div>
                    <Heart className="w-5 h-5 text-red-600" />
                  </div>
                </div>
                
                <div className="bg-green-50 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-600">Commentaires</p>
                      <p className="text-lg font-bold text-green-600">{postAnalytics.total_comments}</p>
                    </div>
                    <MessageCircle className="w-5 h-5 text-green-600" />
                  </div>
                </div>
                
                <div className="bg-purple-50 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-600">Partages</p>
                      <p className="text-lg font-bold text-purple-600">{postAnalytics.total_shares}</p>
                    </div>
                    <Share className="w-5 h-5 text-purple-600" />
                  </div>
                </div>
              </div>
              
              {/* Score Viral */}
              <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Score Viral</p>
                    <p className="text-xl font-bold text-orange-600">{postAnalytics.viral_score_formatted}</p>
                  </div>
                  {postAnalytics.viral_score >= 80 ? (
                    <Flame className="w-6 h-6 text-red-600" />
                  ) : postAnalytics.viral_score >= 50 ? (
                    <Zap className="w-6 h-6 text-orange-600" />
                  ) : (
                    <TrendingUp className="w-6 h-6 text-blue-600" />
                  )}
                </div>
              </div>
              
              {/* Taux d'Engagement */}
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Taux d'Engagement</p>
                    <p className="text-xl font-bold text-blue-600">{postAnalytics.engagement_rate_formatted}</p>
                  </div>
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                </div>
              </div>
              
              {/* Partages Externes */}
              {postAnalytics.total_external_shares > 0 && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">Partages Externes</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(postAnalytics.external_shares_breakdown).map(([platform, count]) => (
                      count > 0 && (
                        <div key={platform} className="text-center">
                          <p className="text-xs text-gray-600 capitalize">{platform}</p>
                          <p className="text-sm font-bold text-gray-900">{count}</p>
                        </div>
                      )
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Modal de Confirmation de Suppression */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Confirmer la suppression
              </h3>
              <button
                onClick={handleCancelDelete}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Icône d'avertissement */}
              <div className="flex justify-center">
                <div className="bg-red-100 rounded-full p-3">
                  <AlertTriangle className="w-8 h-8 text-red-600" />
                </div>
              </div>
              
              {/* Message de confirmation */}
              <div className="text-center">
                <p className="text-gray-700 mb-2">
                  Êtes-vous sûr de vouloir supprimer ce post ?
                </p>
                <p className="text-sm text-gray-500">
                  Cette action est irréversible et supprimera définitivement le post et tous ses commentaires.
                </p>
              </div>
              
              {/* Boutons d'action */}
              <div className="flex space-x-3 pt-4">
                <button
                  onClick={handleCancelDelete}
                  disabled={isDeleting}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  Annuler
                </button>
                <button
                  onClick={handleConfirmDelete}
                  disabled={isDeleting}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isDeleting ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Suppression...
                    </span>
                  ) : (
                    'Supprimer'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostCard; 
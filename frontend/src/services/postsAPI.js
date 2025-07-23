import api from './api';

// Service pour les posts
export const postsAPI = {
  // Récupérer tous les posts
  getPosts: async (params = {}) => {
    const response = await api.get('/posts/', { params });
    return response.data;
  },

  // Récupérer un post spécifique
  getPost: async (postId) => {
    const response = await api.get(`/posts/${postId}/`);
    return response.data;
  },

  // Créer un nouveau post
  createPost: async (postData) => {
    // Si postData est un FormData (avec image), ne pas définir Content-Type
    // Axios le définira automatiquement avec la boundary appropriée
    const config = {};
    if (postData instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data',
      };
    }
    
    const response = await api.post('/posts/', postData, config);
    return response.data;
  },

  // Modifier un post
  updatePost: async (postId, postData) => {
    const response = await api.put(`/posts/${postId}/`, postData);
    return response.data;
  },

  // Supprimer un post
  deletePost: async (postId) => {
    const response = await api.delete(`/posts/${postId}/`);
    return response.data;
  },

  // Liker/unliker un post
  likePost: async (postId) => {
    const response = await api.post(`/posts/${postId}/like/`);
    return response.data;
  },

  // Unliker un post
  unlikePost: async (postId) => {
    const response = await api.delete(`/posts/${postId}/like/`);
    return response.data;
  },

  // Récupérer les commentaires d'un post
  getComments: async (postId) => {
    const response = await api.get(`/posts/${postId}/comments/`);
    return response.data;
  },

  // Ajouter un commentaire
  addComment: async (postId, commentData) => {
    const response = await api.post(`/posts/${postId}/comments/`, commentData);
    return response.data;
  },

  // Répondre à un commentaire
  replyToComment: async (commentId, replyData) => {
    const response = await api.post(`/posts/comments/${commentId}/reply/`, replyData);
    return response.data;
  },

  // Modifier un commentaire
  updateComment: async (commentId, commentData) => {
    const response = await api.put(`/posts/comments/${commentId}/`, commentData);
    return response.data;
  },

  // Supprimer un commentaire
  deleteComment: async (commentId) => {
    const response = await api.delete(`/posts/comments/${commentId}/`);
    return response.data;
  },

  // Récupérer les posts d'un utilisateur
  getUserPosts: async (userId) => {
    const response = await api.get(`/posts/user/${userId}/`);
    return response.data;
  },

  // Incrémenter les vues d'un post
  incrementViews: async (postId) => {
    const response = await api.post(`/posts/posts/${postId}/increment-views/`);
    return response.data;
  },
};

// Fonctions de partage
export const sharePost = async (postId, shareData = {}) => {
  try {
    const response = await api.post(`/posts/posts/${postId}/share/`, {
      share_type: 'share',
      comment: shareData.comment || '',
      ...shareData
    });
    return response.data;
  } catch (error) {
    console.error('Erreur lors du partage:', error);
    throw error;
  }
};

export const repostPost = async (postId, repostData = {}) => {
  try {
    const response = await api.post(`/posts/posts/${postId}/share/`, {
      share_type: 'repost',
      comment: repostData.comment || '',
      ...repostData
    });
    return response.data;
  } catch (error) {
    console.error('Erreur lors du repost:', error);
    throw error;
  }
};

export const unsharePost = async (postId, shareType = 'share') => {
  try {
    const response = await api.delete(`/posts/posts/${postId}/share/`, {
      data: { share_type: shareType }
    });
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la suppression du partage:', error);
    throw error;
  }
};

export const getPostShares = async (postId) => {
  try {
    const response = await api.get(`/posts/posts/${postId}/shares/`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des partages:', error);
    throw error;
  }
}; 

// Fonctions de partage externe
export const sharePostExternal = async (postId, platform) => {
  try {
    const response = await api.post(`/posts/posts/${postId}/share-external/`, {
      platform: platform
    });
    return response.data;
  } catch (error) {
    console.error('Erreur lors du partage externe:', error);
    throw error;
  }
};

export const getExternalShares = async (postId) => {
  try {
    const response = await api.get(`/posts/posts/${postId}/external-shares/`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des partages externes:', error);
    throw error;
  }
};

// Fonctions utilitaires pour les liens de partage
export const generateShareLinks = (postId, postContent) => {
  const baseUrl = window.location.origin;
  const postUrl = `${baseUrl}/post/${postId}`;
  const encodedContent = encodeURIComponent(postContent);
  const encodedUrl = encodeURIComponent(postUrl);
  
  return {
    whatsapp: `https://wa.me/?text=${encodedContent}%20${encodedUrl}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
    twitter: `https://twitter.com/intent/tweet?text=${encodedContent}&url=${encodedUrl}`,
    telegram: `https://t.me/share/url?url=${encodedUrl}&text=${encodedContent}`,
    email: `mailto:?subject=Post CommuniConnect&body=${encodedContent}%20${encodedUrl}`,
    copy_link: postUrl
  };
}; 

// Fonctions d'analytics
export const getPostAnalytics = async (postId) => {
  try {
    const response = await api.get(`/posts/posts/${postId}/analytics/`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des analytics:', error);
    throw error;
  }
};

export const getUserAnalytics = async (days = 30) => {
  try {
    const response = await api.get(`/analytics/user/?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des analytics utilisateur:', error);
    throw error;
  }
};

export const getCommunityAnalytics = async (days = 30) => {
  try {
    const response = await api.get(`/analytics/community/?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des analytics communautaires:', error);
    throw error;
  }
}; 

// Fonction pour modifier un post
export const updatePost = async (postId, postData) => {
  try {
    const response = await api.put(`/posts/${postId}/`, postData);
    return response.data;
  } catch (error) {
    throw error;
  }
}; 
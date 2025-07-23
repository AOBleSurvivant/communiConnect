import api from './api';

// Service pour les messages de chat live
export const liveChatAPI = {
  // Envoyer un message dans le chat live
  sendMessage: async (postId, messageData) => {
    const response = await api.post(`/posts/live/${postId}/chat/`, messageData);
    return response.data;
  },

  // Récupérer les messages d'un live
  getMessages: async (postId) => {
    const response = await api.get(`/posts/live/${postId}/chat/messages/`);
    return response.data;
  },

  // Récupérer les messages avec pagination
  getMessagesPaginated: async (postId, page = 1, pageSize = 50) => {
    const response = await api.get(`/posts/live/${postId}/chat/messages/`, {
      params: { page, page_size: pageSize }
    });
    return response.data;
  }
}; 
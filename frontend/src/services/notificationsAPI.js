import api from './api';

const NOTIFICATIONS_API = '/notifications/';

export const notificationsAPI = {
  // Récupérer toutes les notifications
  getNotifications: async (page = 1, pageSize = 20) => {
    try {
      const response = await api.get(`${NOTIFICATIONS_API}`, {
        params: { page, page_size: pageSize }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des notifications:', error);
      throw error;
    }
  },

  // Récupérer les notifications non lues
  getUnreadNotifications: async () => {
    try {
      const response = await api.get(`${NOTIFICATIONS_API}`, {
        params: { unread: true }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des notifications non lues:', error);
      throw error;
    }
  },

  // Marquer une notification comme lue
  markAsRead: async (notificationId) => {
    try {
      const response = await api.patch(`${NOTIFICATIONS_API}mark-as-read/`, {
        notification_ids: [notificationId]
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors du marquage de la notification:', error);
      throw error;
    }
  },

  // Marquer toutes les notifications comme lues
  markAllAsRead: async () => {
    try {
      const response = await api.patch(`${NOTIFICATIONS_API}mark-as-read/`, {
        mark_all: true
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors du marquage de toutes les notifications:', error);
      throw error;
    }
  },

  // Supprimer une notification
  deleteNotification: async (notificationId) => {
    try {
      const response = await api.delete(`${NOTIFICATIONS_API}${notificationId}/delete/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la suppression de la notification:', error);
      throw error;
    }
  },

  // Récupérer les préférences de notifications
  getNotificationPreferences: async () => {
    try {
      const response = await api.get(`${NOTIFICATIONS_API}preferences/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des préférences:', error);
      throw error;
    }
  },

  // Mettre à jour les préférences de notifications
  updateNotificationPreferences: async (preferences) => {
    try {
      const response = await api.patch(`${NOTIFICATIONS_API}preferences/`, preferences);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la mise à jour des préférences:', error);
      throw error;
    }
  },

  // Récupérer le nombre de notifications non lues
  getUnreadCount: async () => {
    try {
      const response = await api.get(`${NOTIFICATIONS_API}count/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération du nombre de notifications:', error);
      throw error;
    }
  }
};

export default notificationsAPI; 
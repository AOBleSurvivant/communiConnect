import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import notificationsAPI from '../services/notificationsAPI';

const NotificationBell = () => {
  const [unreadCount, setUnreadCount] = useState(0);
  const [recentNotifications, setRecentNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const dropdownRef = useRef(null);

  const fetchUnreadCount = async () => {
    try {
      const response = await notificationsAPI.getUnreadCount();
      setUnreadCount(response.unread_count);
    } catch (error) {
      console.error('Erreur lors du chargement du nombre de notifications:', error);
    }
  };

  const fetchRecentNotifications = async () => {
    try {
      setLoading(true);
      const response = await notificationsAPI.getNotifications(1, 5);
      setRecentNotifications(response.results);
    } catch (error) {
      console.error('Erreur lors du chargement des notifications récentes:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUnreadCount();
    
    // Mettre à jour toutes les 30 secondes
    const interval = setInterval(fetchUnreadCount, 30000);
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isOpen) {
      fetchRecentNotifications();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleMarkAsRead = async (notificationId) => {
    try {
      await notificationsAPI.markAsRead(notificationId);
      
      // Mettre à jour l'état local
      setRecentNotifications(prev => 
        prev.map(notif => 
          notif.id === notificationId 
            ? { ...notif, is_read: true }
            : notif
        )
      );
      
      // Mettre à jour le compteur
      fetchUnreadCount();
    } catch (error) {
      console.error('Erreur lors du marquage comme lu:', error);
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'like':
        return '❤️';
      case 'comment':
        return '💬';
      case 'follow':
        return '👥';
      case 'live_started':
        return '📺';
      case 'live_ended':
        return '⏹️';
      case 'mention':
        return '📢';
      case 'system':
        return '🔔';
      default:
        return '📌';
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Bouton de la cloche */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-600 hover:text-gray-800 transition-colors"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17h6m-6-4h6m-6-4h6m-6-4h6" />
        </svg>
        
        {/* Badge pour les notifications non lues */}
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          {/* En-tête */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
              Notifications
            </h3>
            <Link
              to="/notifications"
              onClick={() => setIsOpen(false)}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              Voir tout
            </Link>
          </div>

          {/* Liste des notifications */}
          <div className="max-h-96 overflow-y-auto">
            {loading ? (
              <div className="p-4 text-center">
                <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <p className="mt-2 text-sm text-gray-600">Chargement...</p>
              </div>
            ) : recentNotifications.length === 0 ? (
              <div className="p-4 text-center">
                <div className="text-4xl mb-2">🔔</div>
                <p className="text-sm text-gray-600">Aucune notification</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-100">
                {recentNotifications.map(notification => (
                  <div
                    key={notification.id}
                    className={`p-4 hover:bg-gray-50 transition-colors cursor-pointer ${
                      !notification.is_read ? 'bg-blue-50' : ''
                    }`}
                    onClick={() => handleMarkAsRead(notification.id)}
                  >
                    <div className="flex items-start space-x-3">
                      {/* Icône */}
                      <div className="flex-shrink-0 text-lg">
                        {getNotificationIcon(notification.notification_type)}
                      </div>

                      {/* Contenu */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-medium text-gray-900">
                            {notification.title}
                          </h4>
                          {!notification.is_read && (
                            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          )}
                        </div>
                        
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                          {notification.message}
                        </p>

                        <p className="text-xs text-gray-500 mt-2">
                          {new Date(notification.created_at).toLocaleDateString('fr-FR', {
                            day: 'numeric',
                            month: 'short',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Pied de page */}
          {recentNotifications.length > 0 && (
            <div className="p-4 border-t border-gray-200">
              <Link
                to="/notifications"
                onClick={() => setIsOpen(false)}
                className="block w-full text-center text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Voir toutes les notifications
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell; 
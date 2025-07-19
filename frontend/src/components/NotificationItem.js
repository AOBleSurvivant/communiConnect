import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const NotificationItem = ({ notification, onMarkAsRead, onDelete }) => {
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

  const getNotificationColor = (type) => {
    switch (type) {
      case 'like':
        return 'bg-red-50 border-red-200';
      case 'comment':
        return 'bg-blue-50 border-blue-200';
      case 'follow':
        return 'bg-green-50 border-green-200';
      case 'live_started':
        return 'bg-purple-50 border-purple-200';
      case 'live_ended':
        return 'bg-gray-50 border-gray-200';
      case 'mention':
        return 'bg-yellow-50 border-yellow-200';
      case 'system':
        return 'bg-indigo-50 border-indigo-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const handleMarkAsRead = async () => {
    if (!notification.is_read) {
      try {
        await onMarkAsRead(notification.id);
      } catch (error) {
        console.error('Erreur lors du marquage comme lu:', error);
      }
    }
  };

  const handleDelete = async () => {
    try {
      await onDelete(notification.id);
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  return (
    <div 
      className={`p-4 border-l-4 transition-all duration-200 hover:shadow-md ${
        notification.is_read 
          ? 'bg-white border-gray-300 opacity-75' 
          : `bg-white border-l-4 ${getNotificationColor(notification.notification_type)}`
      }`}
      onClick={handleMarkAsRead}
    >
      <div className="flex items-start space-x-3">
        {/* Icône */}
        <div className="flex-shrink-0 text-2xl">
          {getNotificationIcon(notification.notification_type)}
        </div>

        {/* Contenu */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium text-gray-900">
              {notification.title}
            </h4>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-gray-500">
                {formatDistanceToNow(new Date(notification.created_at), {
                  addSuffix: true,
                  locale: fr
                })}
              </span>
              {!notification.is_read && (
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              )}
            </div>
          </div>
          
          <p className="text-sm text-gray-600 mt-1">
            {notification.message}
          </p>

          {/* Données supplémentaires */}
          {notification.extra_data && Object.keys(notification.extra_data).length > 0 && (
            <div className="mt-2 text-xs text-gray-500">
              {notification.extra_data.post_title && (
                <p>Post: {notification.extra_data.post_title}</p>
              )}
              {notification.extra_data.comment_content && (
                <p>Commentaire: {notification.extra_data.comment_content}</p>
              )}
              {notification.extra_data.live_title && (
                <p>Live: {notification.extra_data.live_title}</p>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center justify-between mt-3">
            <div className="flex items-center space-x-2">
              {!notification.is_read && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleMarkAsRead();
                  }}
                  className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                >
                  Marquer comme lu
                </button>
              )}
            </div>
            
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDelete();
              }}
              className="text-xs text-red-600 hover:text-red-800 font-medium"
            >
              Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationItem; 
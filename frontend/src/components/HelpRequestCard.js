import React from 'react';
import { 
    MapPinIcon, ClockIcon, ExclamationTriangleIcon, UserIcon,
    HeartIcon, PhoneIcon, EnvelopeIcon, ChatBubbleLeftIcon
} from '@heroicons/react/24/outline';

const HelpRequestCard = ({ request, needTypes, onClick }) => {
    const needType = needTypes[request.need_type] || needTypes.other;
    const isRequest = request.request_type === 'request';
    
    // Fonction pour formater la date
    const formatTimeAgo = (timeAgo) => {
        if (!timeAgo) return '';
        return timeAgo;
    };
    
    // Fonction pour tronquer le texte
    const truncateText = (text, maxLength = 100) => {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    };
    
    return (
        <div 
            onClick={onClick}
            className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
        >
            {/* En-tête de la carte */}
            <div className="p-4 border-b border-gray-100">
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                        {/* Icône du type d'aide */}
                        <div className={`p-2 rounded-full ${needType.color}`}>
                            <span className="text-lg">{needType.icon}</span>
                        </div>
                        
                        <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 line-clamp-2">
                                {request.title}
                            </h3>
                            <p className="text-sm text-gray-500">
                                {formatTimeAgo(request.time_ago)}
                            </p>
                        </div>
                    </div>
                    
                    {/* Badges */}
                    <div className="flex items-center space-x-2">
                        {request.is_urgent && (
                            <span className="px-2 py-1 text-xs font-medium text-red-700 bg-red-100 rounded-full flex items-center">
                                <ExclamationTriangleIcon className="w-3 h-3 mr-1" />
                                URGENT
                            </span>
                        )}
                        
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                            isRequest 
                                ? 'text-blue-700 bg-blue-100' 
                                : 'text-green-700 bg-green-100'
                        }`}>
                            {isRequest ? 'Demande' : 'Offre'}
                        </span>
                    </div>
                </div>
                
                {/* Description */}
                <p className="text-gray-700 text-sm line-clamp-2">
                    {truncateText(request.description)}
                </p>
            </div>
            
            {/* Informations de localisation */}
            {request.neighborhood || request.city ? (
                <div className="px-4 py-2 border-b border-gray-100">
                    <div className="flex items-center text-sm text-gray-500">
                        <MapPinIcon className="w-4 h-4 mr-1" />
                        <span>
                            {request.neighborhood && request.city 
                                ? `${request.neighborhood}, ${request.city}`
                                : (request.neighborhood || request.city)
                            }
                        </span>
                    </div>
                </div>
            ) : null}
            
            {/* Métadonnées */}
            <div className="px-4 py-3">
                <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-4">
                        {/* Auteur */}
                        <div className="flex items-center">
                            <UserIcon className="w-4 h-4 mr-1" />
                            <span>
                                {request.author?.first_name && request.author?.last_name
                                    ? `${request.author.first_name} ${request.author.last_name}`
                                    : request.author?.username || 'Utilisateur'
                                }
                            </span>
                        </div>
                        
                        {/* Réponses */}
                        <div className="flex items-center">
                            <ChatBubbleLeftIcon className="w-4 h-4 mr-1" />
                            <span>{request.responses_count || 0} réponse{(request.responses_count || 0) > 1 ? 's' : ''}</span>
                        </div>
                        
                        {/* Vues */}
                        <div className="flex items-center">
                            <HeartIcon className="w-4 h-4 mr-1" />
                            <span>{request.views_count || 0} vue{(request.views_count || 0) > 1 ? 's' : ''}</span>
                        </div>
                    </div>
                    
                    {/* Statut */}
                    <div className="flex items-center">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                            request.status === 'active' ? 'text-green-700 bg-green-100' :
                            request.status === 'in_progress' ? 'text-blue-700 bg-blue-100' :
                            request.status === 'completed' ? 'text-gray-700 bg-gray-100' :
                            'text-red-700 bg-red-100'
                        }`}>
                            {request.status === 'active' ? 'Active' :
                             request.status === 'in_progress' ? 'En cours' :
                             request.status === 'completed' ? 'Terminée' :
                             request.status === 'cancelled' ? 'Annulée' :
                             request.status === 'expired' ? 'Expirée' : request.status}
                        </span>
                    </div>
                </div>
            </div>
            
            {/* Actions rapides */}
            <div className="px-4 py-3 bg-gray-50 rounded-b-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        {/* Type d'aide */}
                        <span className="text-xs text-gray-600">
                            {needType.label}
                        </span>
                    </div>
                    
                    {/* Bouton d'action */}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onClick();
                        }}
                        className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                            isRequest
                                ? 'text-blue-600 bg-blue-100 hover:bg-blue-200'
                                : 'text-green-600 bg-green-100 hover:bg-green-200'
                        }`}
                    >
                        {isRequest ? 'Je peux aider' : 'Contacter'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default HelpRequestCard; 
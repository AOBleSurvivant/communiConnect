import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { 
    XMarkIcon, MapPinIcon, ClockIcon, ExclamationTriangleIcon, UserIcon,
    HeartIcon, PhoneIcon, EnvelopeIcon, ChatBubbleLeftIcon, CheckCircleIcon,
    XCircleIcon, CameraIcon, GlobeAltIcon, CalendarIcon, UsersIcon,
    HandRaisedIcon, TruckIcon, AcademicCapIcon, WrenchScrewdriverIcon,
    ShoppingBagIcon, EyeIcon, UserGroupIcon
} from '@heroicons/react/24/outline';


// Types de besoins avec icônes
const NEED_TYPES = {
    material: { 
        label: 'Matériel', 
        icon: '📦', 
        color: 'text-blue-600 bg-blue-100',
        heroIcon: TruckIcon
    },
    presence: { 
        label: 'Présence/Accompagnement', 
        icon: '👥', 
        color: 'text-green-600 bg-green-100',
        heroIcon: UsersIcon
    },
    service: { 
        label: 'Service', 
        icon: '🛠️', 
        color: 'text-purple-600 bg-purple-100',
        heroIcon: HandRaisedIcon
    },
    transport: { 
        label: 'Transport', 
        icon: '🚗', 
        color: 'text-indigo-600 bg-indigo-100',
        heroIcon: TruckIcon
    },
    shopping: { 
        label: 'Courses', 
        icon: '🛒', 
        color: 'text-orange-600 bg-orange-100',
        heroIcon: ShoppingBagIcon
    },
    technical: { 
        label: 'Aide technique', 
        icon: '🔧', 
        color: 'text-yellow-600 bg-yellow-100',
        heroIcon: WrenchScrewdriverIcon
    },
    education: { 
        label: 'Aide éducative', 
        icon: '📚', 
        color: 'text-teal-600 bg-teal-100',
        heroIcon: AcademicCapIcon
    },
    other: { 
        label: 'Autre', 
        icon: '🤝', 
        color: 'text-gray-600 bg-gray-100',
        heroIcon: HandRaisedIcon
    },
};

// Options pour "pour qui"
const FOR_WHO_OPTIONS = {
    myself: { label: 'Moi-même', icon: '👤' },
    family: { label: 'Ma famille', icon: '👨‍👩‍👧‍👦' },
    neighbor: { label: 'Mon voisin', icon: '🏠' },
    community: { label: 'La communauté', icon: '🌍' },
    other: { label: 'Autre', icon: '🤝' },
};

const HelpRequestDetail = ({ request, onClose, onRespond, needTypes = NEED_TYPES }) => {
    const [showResponseForm, setShowResponseForm] = useState(false);
    const [responseData, setResponseData] = useState({
        response_type: 'offer_help',
        message: '',
        contact_phone: '',
        contact_email: '',
    });
    const [submitting, setSubmitting] = useState(false);
    const [responses, setResponses] = useState([]);
    const [loadingResponses, setLoadingResponses] = useState(false);
    
    const needType = needTypes[request.need_type] || needTypes.other;
    const isRequest = request.request_type === 'request';
    const forWho = FOR_WHO_OPTIONS[request.for_who] || FOR_WHO_OPTIONS.other;
    
    // Fonction pour formater la date
    const formatTimeAgo = (timeAgo) => {
        if (!timeAgo) return '';
        return timeAgo;
    };
    
    // Charger les réponses à la demande
    const loadResponses = async () => {
        try {
            setLoadingResponses(true);
            const response = await fetch(`http://127.0.0.1:8000/api/help-requests/api/requests/${request.id}/responses/`);
            if (response.ok) {
                const data = await response.json();
                setResponses(data.results || data || []);
            }
        } catch (error) {
            console.error('Erreur chargement réponses:', error);
        } finally {
            setLoadingResponses(false);
        }
    };
    
    // Charger les réponses au montage du composant
    useEffect(() => {
        loadResponses();
    }, [request.id]);
    
    // Gérer les changements dans le formulaire de réponse
    const handleResponseChange = (field, value) => {
        setResponseData(prev => ({
            ...prev,
            [field]: value
        }));
    };
    
    // Soumettre la réponse
    const handleSubmitResponse = async (e) => {
        e.preventDefault();
        
        if (!responseData.message.trim()) {
            toast.error('Veuillez saisir un message');
            return;
        }
        
        console.log('🔍 Début handleSubmitResponse');
        console.log('📋 responseData:', responseData);
        console.log('📤 request.id:', request.id);
        
        setSubmitting(true);
        
        try {
            await onRespond(request.id, responseData);
            setShowResponseForm(false);
            setResponseData({
                response_type: 'offer_help',
                message: '',
                contact_phone: '',
                contact_email: '',
            });
            // Recharger les réponses après envoi
            await loadResponses();
        } catch (error) {
            console.error('❌ Erreur envoi réponse:', error);
            console.error('❌ Status:', error.response?.status);
            console.error('❌ Détails erreur:', JSON.stringify(error.response?.data, null, 2));
            console.error('❌ Erreur complète:', JSON.stringify(error.response, null, 2));
            alert('Erreur API : ' + JSON.stringify(error.response?.data, null, 2));
        } finally {
            setSubmitting(false);
        }
    };
    
    // Centrer la carte sur la position de la demande
    const mapCenter = request.latitude && request.longitude 
        ? [request.latitude, request.longitude] 
        : [9.5370, -13.6785];
    
    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-10 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    {/* En-tête */}
                    <div className="flex justify-between items-start mb-6">
                        <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${needType.color}`}>
                                    {needType.icon} {needType.label}
                                </span>
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                                    isRequest ? 'text-blue-600 bg-blue-100' : 'text-green-600 bg-green-100'
                                }`}>
                                    {isRequest ? 'Demande' : 'Offre'}
                                </span>
                                {request.is_urgent && (
                                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium text-red-600 bg-red-100">
                                        ⚡ Urgent
                                    </span>
                                )}
                            </div>
                            <h3 className="text-2xl font-bold text-gray-900">{request.title}</h3>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <XMarkIcon className="w-6 h-6" />
                        </button>
                    </div>
                    
                    {/* Contenu principal */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Colonne principale */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Description */}
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
                                <p className="text-gray-700 whitespace-pre-wrap">{request.description}</p>
                            </div>
                            
                            {/* Détails */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {/* Pour qui */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center space-x-2 mb-2">
                                        <UserGroupIcon className="w-5 h-5 text-gray-500" />
                                        <h4 className="font-semibold text-gray-900">Pour qui</h4>
                                    </div>
                                    <p className="text-gray-700">{forWho.icon} {forWho.label}</p>
                                    {request.custom_for_who && (
                                        <p className="text-sm text-gray-500 mt-1">{request.custom_for_who}</p>
                                    )}
                                </div>
                                
                                {/* Durée */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center space-x-2 mb-2">
                                        <ClockIcon className="w-5 h-5 text-gray-500" />
                                        <h4 className="font-semibold text-gray-900">Durée</h4>
                                    </div>
                                    <p className="text-gray-700">{request.duration_display}</p>
                                    {request.estimated_hours && (
                                        <p className="text-sm text-gray-500 mt-1">
                                            Durée estimée : {request.estimated_hours} heure{request.estimated_hours > 1 ? 's' : ''}
                                        </p>
                                    )}
                                </div>
                                
                                {/* Zone de proximité */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center space-x-2 mb-2">
                                        <GlobeAltIcon className="w-5 h-5 text-gray-500" />
                                        <h4 className="font-semibold text-gray-900">Zone</h4>
                                    </div>
                                    <p className="text-gray-700">
                                        {request.proximity_zone === 'local' && '🏠 Quartier'}
                                        {request.proximity_zone === 'city' && '🏙️ Ville'}
                                        {request.proximity_zone === 'region' && '🌍 Région'}
                                    </p>
                                </div>
                                
                                {/* Contact */}
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center space-x-2 mb-2">
                                        <ChatBubbleLeftIcon className="w-5 h-5 text-gray-500" />
                                        <h4 className="font-semibold text-gray-900">Contact</h4>
                                    </div>
                                    <p className="text-gray-700">
                                        {request.contact_preference === 'message' && '💬 Message privé'}
                                        {request.contact_preference === 'phone' && '📞 Téléphone'}
                                        {request.contact_preference === 'email' && '📧 Email'}
                                        {request.contact_preference === 'any' && '✅ N\'importe lequel'}
                                    </p>
                                </div>
                            </div>
                            
                            {/* Photo */}
                            {request.photo && (
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <h4 className="font-semibold text-gray-900 mb-3">Photo</h4>
                                    <img 
                                        src={request.photo} 
                                        alt="Photo de la demande" 
                                        className="w-full max-w-md rounded-lg object-cover"
                                    />
                                </div>
                            )}
                            
                            {/* Localisation */}
                            {request.latitude && request.longitude && (
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <h4 className="font-semibold text-gray-900 mb-3">Localisation</h4>
                                    <div className="p-4 bg-white rounded-lg border">
                                        <div className="flex items-center space-x-2">
                                            <MapPinIcon className="w-5 h-5 text-gray-400" />
                                            <span className="text-sm text-gray-600">
                                                {request.location_display || `${request.latitude}, ${request.longitude}`}
                                            </span>
                                        </div>
                                        {request.neighborhood && (
                                            <p className="text-sm text-gray-500 mt-1">
                                                Quartier: {request.neighborhood}
                                            </p>
                                        )}
                                        {request.city && (
                                            <p className="text-sm text-gray-500">
                                                Ville: {request.city}
                                            </p>
                                        )}
                                    </div>
                                </div>
                            )}
                                    </div>
                                    
                        {/* Colonne latérale */}
                        <div className="space-y-6">
                            {/* Auteur */}
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-semibold text-gray-900 mb-3">Auteur</h4>
                                <div className="flex items-center space-x-3">
                                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                                        <UserIcon className="w-6 h-6 text-blue-600" />
                                    </div>
                                    <div>
                                        <p className="font-medium text-gray-900">{request.author_name}</p>
                                        <p className="text-sm text-gray-500">{formatTimeAgo(request.time_ago)}</p>
                                    </div>
                                </div>
                            </div>
                            
                            {/* Statistiques */}
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-semibold text-gray-900 mb-3">Statistiques</h4>
                                <div className="space-y-2">
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm text-gray-600">Vues</span>
                                        <span className="font-medium text-gray-900">{request.views_count}</span>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm text-gray-600">Réponses</span>
                                        <span className="font-medium text-gray-900">{request.responses_count}</span>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm text-gray-600">Statut</span>
                                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                            request.status === 'open' ? 'text-green-600 bg-green-100' :
                                            request.status === 'in_progress' ? 'text-yellow-600 bg-yellow-100' :
                                            request.status === 'completed' ? 'text-blue-600 bg-blue-100' :
                                            'text-gray-600 bg-gray-100'
                                        }`}>
                                            {request.status === 'open' && 'Ouverte'}
                                            {request.status === 'in_progress' && 'En cours'}
                                            {request.status === 'completed' && 'Clôturée'}
                                            {request.status === 'cancelled' && 'Annulée'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            
                            {/* Réponses */}
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-semibold text-gray-900 mb-3">Réponses ({responses.length})</h4>
                                {loadingResponses ? (
                                    <div className="text-center py-4">
                                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
                                        <p className="text-sm text-gray-500 mt-2">Chargement...</p>
                                    </div>
                                ) : responses.length > 0 ? (
                                    <div className="space-y-3 max-h-64 overflow-y-auto">
                                        {responses.map((response, index) => (
                                            <div key={response.id || index} className="bg-white rounded-lg p-3 border">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <div className="flex items-center space-x-2 mb-1">
                                                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                                                response.response_type === 'offer_help' ? 'text-green-600 bg-green-100' :
                                                                response.response_type === 'need_help' ? 'text-blue-600 bg-blue-100' :
                                                                response.response_type === 'contact' ? 'text-purple-600 bg-purple-100' :
                                                                'text-gray-600 bg-gray-100'
                                                            }`}>
                                                                {response.response_type === 'offer_help' && 'Je peux aider'}
                                                                {response.response_type === 'need_help' && 'J\'ai besoin d\'aide'}
                                                                {response.response_type === 'contact' && 'Contacter'}
                                                                {response.response_type === 'question' && 'Question'}
                                                            </span>
                                                            <span className="text-xs text-gray-500">
                                                                {response.created_at ? new Date(response.created_at).toLocaleDateString() : 'Aujourd\'hui'}
                                                            </span>
                                                        </div>
                                                        <p className="text-sm text-gray-700 mb-2">{response.message}</p>
                                                        {(response.contact_phone || response.contact_email) && (
                                                            <div className="text-xs text-gray-500">
                                                                {response.contact_phone && (
                                                                    <div className="flex items-center space-x-1">
                                                                        <PhoneIcon className="w-3 h-3" />
                                                                        <span>{response.contact_phone}</span>
                                                                    </div>
                                                                )}
                                                                {response.contact_email && (
                                                                    <div className="flex items-center space-x-1">
                                                                        <EnvelopeIcon className="w-3 h-3" />
                                                                        <span>{response.contact_email}</span>
                                                                    </div>
                                                                )}
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="text-center py-4">
                                        <ChatBubbleLeftIcon className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                                        <p className="text-sm text-gray-500">Aucune réponse pour le moment</p>
                                    </div>
                                )}
                            </div>
                            
                            {/* Actions */}
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-semibold text-gray-900 mb-3">Actions</h4>
                                    <div className="space-y-3">
                                            <button
                                                onClick={() => {
                                                    console.log('🔘 Bouton "Je peux aider" cliqué');
                                                    console.log('📋 showResponseForm avant:', showResponseForm);
                                                    setShowResponseForm(true);
                                                    console.log('📋 showResponseForm après:', true);
                                                }}
                                        className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
                                            >
                                        <HeartIcon className="w-4 h-4 mr-2" />
                                        {isRequest ? 'Je peux aider' : 'J\'ai besoin d\'aide'}
                                            </button>
                                    
                                            <button
                                        onClick={() => {
                                            // Ouvrir la messagerie
                                            toast.info('Fonctionnalité de messagerie à venir');
                                        }}
                                        className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                                    >
                                        <ChatBubbleLeftIcon className="w-4 h-4 mr-2" />
                                                Contacter
                                            </button>
                                        
                                        <button
                                            onClick={() => {
                                            // Partager
                                                if (navigator.share) {
                                                    navigator.share({
                                                        title: request.title,
                                                        text: request.description,
                                                        url: window.location.href
                                                    });
                                                } else {
                                                    navigator.clipboard.writeText(window.location.href);
                                                    toast.success('Lien copié dans le presse-papiers');
                                                }
                                            }}
                                        className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                                        >
                                        <EyeIcon className="w-4 h-4 mr-2" />
                                            Partager
                                        </button>
                                    </div>
                            </div>
                        </div>
                    </div>
                    
                    {/* Formulaire de réponse */}
                    {showResponseForm && (
                        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                            {console.log('📋 Formulaire de réponse affiché')}
                            <div className="relative top-10 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
                                <div className="mt-3">
                                    <div className="flex justify-between items-start mb-6">
                                        <div>
                                            <h3 className="text-xl font-bold text-gray-900">
                                                {isRequest ? 'Je peux aider' : 'J\'ai besoin d\'aide'}
                                            </h3>
                                            <p className="text-sm text-gray-500 mt-1">
                                                Contactez {request.author_name} pour cette demande
                                            </p>
                                        </div>
                                        <button
                                            onClick={() => setShowResponseForm(false)}
                                            className="text-gray-400 hover:text-gray-600"
                                        >
                                            <XMarkIcon className="w-6 h-6" />
                                        </button>
                                    </div>
                            
                            <form onSubmit={handleSubmitResponse} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Type de réponse
                                    </label>
                                    <select
                                        value={responseData.response_type}
                                        onChange={(e) => handleResponseChange('response_type', e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="offer_help">Je peux aider</option>
                                        <option value="need_help">J'ai besoin d'aide</option>
                                        <option value="contact">Contacter</option>
                                        <option value="question">Question</option>
                                    </select>
                                </div>
                                
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Message *
                                    </label>
                                    <textarea
                                        value={responseData.message}
                                        onChange={(e) => handleResponseChange('message', e.target.value)}
                                                placeholder="Décrivez comment vous pouvez aider ou ce dont vous avez besoin..."
                                        rows={4}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                        required
                                    />
                                </div>
                                
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                    Téléphone (optionnel)
                                            </label>
                                            <input
                                                type="tel"
                                                value={responseData.contact_phone}
                                                onChange={(e) => handleResponseChange('contact_phone', e.target.value)}
                                                    placeholder="Votre numéro"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                                        </div>
                                        
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                    Email (optionnel)
                                            </label>
                                            <input
                                                type="email"
                                                value={responseData.contact_email}
                                                onChange={(e) => handleResponseChange('contact_email', e.target.value)}
                                                    placeholder="Votre email"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                                        </div>
                                    </div>
                                
                                        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
                                    <button
                                        type="button"
                                        onClick={() => setShowResponseForm(false)}
                                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                                    >
                                        Annuler
                                    </button>
                                    <button
                                        type="submit"
                                        disabled={submitting}
                                                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                                    >
                                        {submitting ? 'Envoi...' : 'Envoyer la réponse'}
                                    </button>
                                </div>
                            </form>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default HelpRequestDetail; 
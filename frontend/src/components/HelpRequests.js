import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { 
    MapPinIcon, PlusIcon, MagnifyingGlassIcon, FunnelIcon,
    HeartIcon, ClockIcon, ExclamationTriangleIcon, CheckCircleIcon,
    XCircleIcon, UserGroupIcon, PhoneIcon, EnvelopeIcon,
    CameraIcon, GlobeAltIcon, AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import api from '../services/api';
import HelpRequestForm from './HelpRequestForm';
import HelpRequestDetail from './HelpRequestDetail';
import HelpRequestCard from './HelpRequestCard';

// Composant principal des demandes d'aide
const HelpRequests = () => {
    // États principaux
    const [helpRequests, setHelpRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [userLocation, setUserLocation] = useState(null);
    
    // États pour les modals et formulaires
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [selectedRequest, setSelectedRequest] = useState(null);
    const [showDetailModal, setShowDetailModal] = useState(false);
    
    // États pour les filtres
    const [filters, setFilters] = useState({
        request_type: '',
        need_type: '',
        status: 'open',
        is_urgent: false,
        search: '',
        radius: 10, // km
    });
    
    // États pour l'affichage
    const [showFilters, setShowFilters] = useState(false);
    
    // Types d'aide disponibles
    const needTypes = {
        material: { label: 'Matériel', icon: '📦', color: 'text-blue-600 bg-blue-100' },
        presence: { label: 'Présence/Accompagnement', icon: '👥', color: 'text-green-600 bg-green-100' },
        service: { label: 'Service', icon: '🛠️', color: 'text-purple-600 bg-purple-100' },
        transport: { label: 'Transport', icon: '🚗', color: 'text-orange-600 bg-orange-100' },
        shopping: { label: 'Courses', icon: '🛒', color: 'text-yellow-600 bg-yellow-100' },
        technical: { label: 'Aide technique', icon: '🔧', color: 'text-indigo-600 bg-indigo-100' },
        education: { label: 'Aide éducative', icon: '📚', color: 'text-teal-600 bg-teal-100' },
        other: { label: 'Autre', icon: '🤝', color: 'text-gray-600 bg-gray-100' },
    };
    
    // Récupérer la géolocalisation de l'utilisateur
    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setUserLocation({ latitude, longitude });
                    console.log('📍 Position utilisateur:', { latitude, longitude });
                },
                (error) => {
                    console.log('❌ Erreur géolocalisation:', error);
                    toast.warning('Impossible d\'obtenir votre position. Utilisation de la position par défaut.');
                }
            );
        }
    }, []);
    
    // Charger les demandes d'aide
    const loadHelpRequests = useCallback(async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams(); // Initialize params here
            
            // Ajouter les filtres (sauf radius qui sera ajouté avec la géolocalisation)
            Object.entries(filters).forEach(([key, value]) => {
                if (value && value !== '' && key !== 'radius') {
                    params.append(key, value);
                }
            });
            
            // Ajouter la position de l'utilisateur pour le filtrage par rayon
            if (userLocation) {
                params.append('latitude', parseFloat(userLocation.latitude.toFixed(6)));
                params.append('longitude', parseFloat(userLocation.longitude.toFixed(6)));
                params.append('radius', filters.radius);
            }
            
            const response = await api.get(`/help-requests/api/requests/?${params}`);
            setHelpRequests(response.data.results || response.data);
            console.log('✅ Demandes d\'aide chargées:', response.data.results?.length || response.data.length);
        } catch (error) {
            console.error('❌ Erreur chargement demandes:', error);
            toast.error('Erreur lors du chargement des demandes d\'aide');
        } finally {
            setLoading(false);
        }
    }, [filters, userLocation]);
    
    // Charger les données au montage et quand les filtres changent
    useEffect(() => {
        loadHelpRequests();
    }, [loadHelpRequests]);
    
    // Créer une nouvelle demande d'aide
    const createHelpRequest = async (requestData) => {
        console.log('🔍 Début createHelpRequest');
        console.log('📤 requestData:', requestData);
        console.log('🔗 URL appelée:', '/help-requests/api/requests/');
        
        // Vérifier l'authentification
        const token = localStorage.getItem('access_token');
        console.log('🔑 Token présent:', !!token);
        if (!token) {
            toast.error('Vous devez être connecté pour créer une demande d\'aide');
            return;
        }
        
        try {
            // Envoyer les données
            if (requestData instanceof FormData) {
                console.log('📤 Envoi FormData');
                // Pour FormData, ne pas définir Content-Type - Axios le fera automatiquement
                const config = {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        // Ne pas définir Content-Type pour FormData
                    }
                };
                console.log('📋 Headers config:', config);
                const response = await api.post('/help-requests/api/requests/', requestData, config);
                console.log('✅ Réponse API:', response.data);
                toast.success('Demande d\'aide créée avec succès !');
                setShowCreateModal(false);
                loadHelpRequests(); // Recharger la liste
                return response.data;
            } else {
                console.log('📤 Envoi JSON');
                const config = {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                };
                console.log('📋 Headers config:', config);
                const response = await api.post('/help-requests/api/requests/', requestData, config);
                console.log('✅ Réponse API:', response.data);
                toast.success('Demande d\'aide créée avec succès !');
                setShowCreateModal(false);
                loadHelpRequests(); // Recharger la liste
                return response.data;
            }
        } catch (error) {
            console.error('❌ Erreur création demande:', error);
            console.error('❌ Status:', error.response?.status);
            console.error('❌ Détails erreur:', error.response?.data);
            console.error('❌ Headers:', error.response?.headers);
            console.error('❌ Erreur complète:', JSON.stringify(error.response?.data, null, 2));
            
            // Afficher un message d'erreur plus détaillé
            let errorMessage = 'Erreur lors de la création de la demande d\'aide';
            if (error.response?.data) {
                if (typeof error.response.data === 'object') {
                    errorMessage += ': ' + JSON.stringify(error.response.data);
                } else {
                    errorMessage += ': ' + error.response.data;
                }
            }
            toast.error(errorMessage);
            throw error;
        }
    };
    
    // Répondre à une demande
    const respondToRequest = async (requestId, responseData) => {
        try {
            console.log('🔍 Début respondToRequest');
            console.log('📤 requestId:', requestId);
            console.log('📋 responseData (avant ajout help_request):', responseData);
            // Ajout du champ help_request attendu par le backend
            const payload = {
                ...responseData,
                help_request: requestId
            };
            console.log('📋 payload (après ajout help_request):', payload);
            const response = await api.post(`/help-requests/api/requests/${requestId}/respond/`, payload);
            console.log('✅ Réponse API:', response.data);
            toast.success('Réponse envoyée avec succès !');
            setShowDetailModal(false);
            loadHelpRequests(); // Recharger la liste
            return response.data;
        } catch (error) {
            console.error('❌ Erreur réponse:', error);
            console.error('❌ Status:', error.response?.status);
            console.error('❌ Détails erreur:', JSON.stringify(error.response?.data, null, 2));
            console.error('❌ Erreur complète:', JSON.stringify(error.response, null, 2));
            alert('Erreur API : ' + JSON.stringify(error.response?.data, null, 2));
            throw error;
        }
    };
    
    // Gérer les changements de filtres
    const handleFilterChange = (newFilters) => {
        setFilters(prev => ({ ...prev, ...newFilters }));
    };
    
    // Filtrer les demandes côté client pour l'affichage
    const filteredRequests = helpRequests.filter(request => {
        if (filters.search && !request.title.toLowerCase().includes(filters.search.toLowerCase()) && 
            !request.description.toLowerCase().includes(filters.search.toLowerCase())) {
            return false;
        }
        if (filters.request_type && request.request_type !== filters.request_type) {
            return false;
        }
        if (filters.need_type && request.need_type !== filters.need_type) {
            return false;
        }
        if (filters.status && request.status !== filters.status) {
            return false;
        }
        if (filters.is_urgent && !request.is_urgent) {
            return false;
        }
        return true;
    });
    
    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* En-tête */}
                <div className="mb-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                Demandes d'aide
                            </h1>
                            <p className="text-gray-600">Entraide et solidarité locale</p>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                            {/* Bouton filtres */}
                            <button
                                onClick={() => setShowFilters(!showFilters)}
                                className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                            >
                                <FunnelIcon className="w-4 h-4 mr-2" />
                                Filtres
                            </button>
                            
                            {/* Bouton créer */}
                            <button
                                onClick={() => setShowCreateModal(true)}
                                className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                            >
                                <PlusIcon className="w-4 h-4 mr-2" />
                                Créer une demande
                            </button>
                        </div>
                    </div>
                    
                    {/* Filtres */}
                    {showFilters && (
                        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                {/* Type de demande */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Type
                                    </label>
                                    <select
                                        value={filters.request_type}
                                        onChange={(e) => handleFilterChange({ request_type: e.target.value })}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="">Tous les types</option>
                                        <option value="request">Demandes d'aide</option>
                                        <option value="offer">Offres d'aide</option>
                                    </select>
                                </div>
                                
                                {/* Type d'aide */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Type d'aide
                                    </label>
                                    <select
                                        value={filters.need_type}
                                        onChange={(e) => handleFilterChange({ need_type: e.target.value })}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="">Tous les types</option>
                                        {Object.entries(needTypes).map(([key, type]) => (
                                            <option key={key} value={key}>
                                                {type.icon} {type.label}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                
                                {/* Recherche */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Recherche
                                    </label>
                                    <div className="relative">
                                        <input
                                            type="text"
                                            value={filters.search}
                                            onChange={(e) => handleFilterChange({ search: e.target.value })}
                                            placeholder="Rechercher..."
                                            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                        />
                                        <MagnifyingGlassIcon className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                    </div>
                                </div>
                                
                                {/* Urgent uniquement */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Priorité
                                    </label>
                                    <div className="flex items-center">
                                        <input
                                            type="checkbox"
                                            id="urgent"
                                            checked={filters.is_urgent}
                                            onChange={(e) => handleFilterChange({ is_urgent: e.target.checked })}
                                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                        />
                                        <label htmlFor="urgent" className="ml-2 text-sm text-gray-700">
                                            Urgent uniquement
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
                
                {/* Statistiques */}
                <div className="mb-6 flex items-center justify-between">
                    <div className="text-sm text-gray-600">
                        {filteredRequests.length} demande{filteredRequests.length > 1 ? 's' : ''} trouvée{filteredRequests.length > 1 ? 's' : ''}
                    </div>
                </div>
                
                {/* Affichage des demandes */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-2 text-gray-600">Chargement des demandes d'aide...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredRequests.length > 0 ? (
                            filteredRequests.map((request) => (
                                <HelpRequestCard
                                    key={request.id}
                                    request={request}
                                    needTypes={needTypes}
                                    onClick={() => {
                                        setSelectedRequest(request);
                                        setShowDetailModal(true);
                                    }}
                                />
                            ))
                        ) : (
                            <div className="col-span-full text-center py-12">
                                <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-gray-400" />
                                <h3 className="mt-2 text-sm font-medium text-gray-900">
                                    Aucune demande trouvée
                                </h3>
                                <p className="mt-1 text-sm text-gray-500">
                                    {filters.search || Object.values(filters).some(f => f) 
                                        ? 'Essayez de modifier vos filtres de recherche.' 
                                        : 'Soyez le premier à créer une demande d\'aide !'
                                    }
                                </p>
                            </div>
                        )}
                    </div>
                )}
            </div>
            
            {/* Modals */}
            {showCreateModal && (
                <HelpRequestForm
                    onClose={() => setShowCreateModal(false)}
                    onSubmit={createHelpRequest}
                    userLocation={userLocation}
                    needTypes={needTypes}
                />
            )}
            
            {showDetailModal && selectedRequest && (
                <HelpRequestDetail
                    request={selectedRequest}
                    onClose={() => {
                        setShowDetailModal(false);
                        setSelectedRequest(null);
                    }}
                    onRespond={respondToRequest}
                    needTypes={needTypes}
                />
            )}
        </div>
    );
};

export default HelpRequests; 
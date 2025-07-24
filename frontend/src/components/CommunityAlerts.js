import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { 
    MapPinIcon, 
    ExclamationTriangleIcon, 
    CheckCircleIcon,
    ClockIcon,
    XCircleIcon,
    HeartIcon,
    UserGroupIcon,
    ChartBarIcon,
    PlusIcon,
    MagnifyingGlassIcon,
    QuestionMarkCircleIcon
} from '@heroicons/react/24/outline';
import { 
    FireIcon, 
    BoltIcon, 
    ExclamationTriangleIcon as ExclamationTriangleSolid,
    ShieldExclamationIcon,
    HeartIcon as HeartSolid,
    WrenchScrewdriverIcon,
    SpeakerWaveIcon,
    PaintBrushIcon,
    DocumentTextIcon
} from '@heroicons/react/24/solid';
import api from '../services/api';

const CommunityAlerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [showStatsModal, setShowStatsModal] = useState(false);
    const [selectedAlert, setSelectedAlert] = useState(null);
    const [userLocation, setUserLocation] = useState(null);
    const [filters, setFilters] = useState({
        category: '',
        status: '',
        urgentOnly: false,
        reliableOnly: false
    });
    const [searchQuery, setSearchQuery] = useState('');
    const [stats, setStats] = useState(null);

    // Catégories d'alertes avec icônes
    const alertCategories = {
        fire: { icon: FireIcon, label: 'Incendie 🔥', color: 'text-red-600 bg-red-100' },
        power_outage: { icon: BoltIcon, label: 'Coupure d\'électricité ⚡', color: 'text-yellow-600 bg-yellow-100' },
        road_blocked: { icon: ExclamationTriangleSolid, label: 'Route bloquée 🚧', color: 'text-orange-600 bg-orange-100' },
        security: { icon: ShieldExclamationIcon, label: 'Agression ou sécurité 🚨', color: 'text-red-700 bg-red-200' },
        medical: { icon: HeartSolid, label: 'Urgence médicale 🏥', color: 'text-pink-600 bg-pink-100' },
        flood: { icon: '🌊', label: 'Inondation 🌊', color: 'text-blue-600 bg-blue-100' },
        gas_leak: { icon: '⛽', label: 'Fuite de gaz ⛽', color: 'text-orange-700 bg-orange-200' },
        noise: { icon: SpeakerWaveIcon, label: 'Bruit excessif 🔊', color: 'text-purple-600 bg-purple-100' },
        vandalism: { icon: PaintBrushIcon, label: 'Vandalisme 🎨', color: 'text-gray-600 bg-gray-100' },
        other: { icon: DocumentTextIcon, label: 'Autre 📋', color: 'text-gray-500 bg-gray-50' }
    };

    // Statuts d'alerte
    const alertStatuses = {
        pending: { label: 'En attente', color: 'text-yellow-600 bg-yellow-100', icon: ClockIcon },
        confirmed: { label: 'Confirmée', color: 'text-green-600 bg-green-100', icon: CheckCircleIcon },
        in_progress: { label: 'En cours de traitement', color: 'text-blue-600 bg-blue-100', icon: WrenchScrewdriverIcon },
        resolved: { label: 'Résolue', color: 'text-green-700 bg-green-200', icon: CheckCircleIcon },
        false_alarm: { label: 'Fausse alerte', color: 'text-red-600 bg-red-100', icon: XCircleIcon }
    };

    // Fonction robuste pour récupérer le statut
    const getStatus = (status) => {
        if (!status) {
            return { label: 'Statut inconnu', color: 'text-gray-600 bg-gray-100', icon: QuestionMarkCircleIcon };
        }
        
        // Essayer de trouver le statut exact
        if (alertStatuses[status]) {
            return alertStatuses[status];
        }
        
        // Essayer avec différentes variations
        const normalizedStatus = status.toLowerCase().replace(/[-\s]/g, '_');
        if (alertStatuses[normalizedStatus]) {
            return alertStatuses[normalizedStatus];
        }
        
        // Essayer avec des variations courantes
        const variations = {
            'pending': 'pending',
            'waiting': 'pending',
            'en_attente': 'pending',
            'confirmed': 'confirmed',
            'confirmée': 'confirmed',
            'validated': 'confirmed',
            'in_progress': 'in_progress',
            'en_cours': 'in_progress',
            'processing': 'in_progress',
            'resolved': 'resolved',
            'résolue': 'resolved',
            'completed': 'resolved',
            'false_alarm': 'false_alarm',
            'fausse_alerte': 'false_alarm',
            'fake': 'false_alarm'
        };
        
        if (variations[normalizedStatus]) {
            return alertStatuses[variations[normalizedStatus]];
        }
        
        // Fallback avec le statut original
        console.warn(`Statut non reconnu: "${status}". Utilisation du fallback.`);
        return {
            label: status || 'Statut inconnu',
            color: 'text-gray-600 bg-gray-100',
            icon: QuestionMarkCircleIcon
        };
    };

    // Récupérer la géolocalisation de l'utilisateur
    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setUserLocation({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                },
                (error) => {
                    console.log('Erreur géolocalisation:', error);
                    toast.warning('Impossible d\'obtenir votre position. Vous pouvez la saisir manuellement.');
                }
            );
        }
    }, []);

    // Charger les alertes
    const loadAlerts = useCallback(async () => {
        setLoading(true);
        try {
            // Debug: vérifier l'authentification
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            console.log('Token disponible:', !!token);
            
            const response = await api.get('/notifications/alerts/');
            const data = response.data;
            const alertsData = data.results || data;
            
            // Debug: analyser les statuts reçus
            console.log('🔍 Analyse des statuts d\'alertes reçus:');
            if (alertsData && alertsData.length > 0) {
                const statusCounts = {};
                alertsData.forEach(alert => {
                    const status = alert.status;
                    statusCounts[status] = (statusCounts[status] || 0) + 1;
                    console.log(`  Alerte "${alert.title}": status="${status}" (type: ${typeof status})`);
                });
                console.log('📊 Répartition des statuts:', statusCounts);
            } else {
                console.log('❌ Aucune alerte reçue');
            }
            
            setAlerts(alertsData);
        } catch (error) {
            console.error('Erreur détaillée:', error.response?.data || error.message);
            toast.error('Erreur lors du chargement des alertes');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadAlerts();
    }, [loadAlerts]);

    // Charger les statistiques
    const loadStats = async () => {
        try {
            const response = await api.get('/notifications/alerts/statistics/');
            const data = response.data;
            setStats(data);
        } catch (error) {
            console.error('Erreur chargement stats:', error);
        }
    };

    // Suggestion de catégorie IA
    const suggestCategory = async (title, description) => {
        try {
            const response = await api.post('/notifications/suggest-category/', {
                title, description
            });
            const suggestion = response.data;
            return suggestion;
        } catch (error) {
            console.error('Erreur:', error);
            return null;
        }
    };

    // Charger le rapport complet d'analytics
    const loadComprehensiveReport = async () => {
        try {
            const response = await api.get('/notifications/analytics/comprehensive-report/');
            const report = response.data;
            setStats(report);
            setShowStatsModal(true);
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur de connexion');
        }
    };

    // Créer une nouvelle alerte avec suggestion IA
    const createAlertWithAI = async (alertData) => {
        try {
            // Vérifier l'authentification
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            if (!token) {
                toast.error('Vous devez être connecté pour créer une alerte');
                return;
            }

            // Debug: afficher les données envoyées
            console.log('📤 Données envoyées:', JSON.stringify(alertData, null, 2));

            // Suggestion de catégorie si pas spécifiée
            if (!alertData.category && alertData.title) {
                const suggestion = await suggestCategory(alertData.title, alertData.description || '');
                if (suggestion && suggestion.confidence > 50) {
                    alertData.category = suggestion.suggested_category;
                    toast.info(`Catégorie suggérée: ${suggestion.category_display} (${suggestion.confidence}% de confiance)`);
                }
            }

            const response = await api.post('/notifications/alerts/', alertData);
            toast.success('Alerte créée avec succès !');
            setShowCreateModal(false);
            loadAlerts();
        } catch (error) {
            console.error('❌ Erreur détaillée:', JSON.stringify(error.response?.data, null, 2));
            console.error('📊 Status:', error.response?.status);
            console.error('📋 Headers:', error.response?.headers);
            toast.error(`Erreur lors de la création de l'alerte: ${error.response?.data?.message || error.message}`);
        }
    };

    // Filtrer les alertes
    const filteredAlerts = alerts.filter(alert => {
        const matchesCategory = !filters.category || alert.category === filters.category;
        const matchesStatus = !filters.status || alert.status === filters.status;
        const matchesUrgent = !filters.urgentOnly || alert.is_urgent;
        const matchesReliable = !filters.reliableOnly || alert.is_reliable;
        const matchesSearch = !searchQuery || 
            alert.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            alert.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            alert.neighborhood?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            alert.city?.toLowerCase().includes(searchQuery.toLowerCase());

        return matchesCategory && matchesStatus && matchesUrgent && matchesReliable && matchesSearch;
    });

    // Créer une nouvelle alerte
    const createAlert = async (alertData) => {
        try {
            const response = await api.post('/notifications/alerts/', alertData);
            toast.success('Alerte créée avec succès !');
            setShowCreateModal(false);
            loadAlerts();
        } catch (error) {
            console.error('Erreur:', error);
            toast.error('Erreur de connexion');
        }
    };

    // Signaler une alerte
    const reportAlert = async (alertId, reportType, reason = '') => {
        console.log('📤 reportAlert appelé avec:', { alertId, reportType, reason });
        try {
            const response = await api.post(`/notifications/alerts/${alertId}/report/`, {
                report_type: reportType,
                reason
            });
            console.log('✅ Rapport envoyé avec succès:', response.status);
            toast.success('Rapport envoyé avec succès');
            loadAlerts();
        } catch (error) {
            console.error('❌ Erreur rapport:', error.response?.data || error.message);
            toast.error('Erreur lors de l\'envoi du rapport');
        }
    };

    // Offrir de l'aide
    const offerHelp = async (alertId, offerData) => {
        try {
            const response = await api.post(`/notifications/alerts/${alertId}/help/`, offerData);
            toast.success('Offre d\'aide envoyée !');
            loadAlerts();
        } catch (error) {
            console.error('Erreur offre d\'aide:', error.response?.data || error.message);
            toast.error('Erreur lors de l\'envoi de l\'offre d\'aide');
        }
    };

    // Rendu d'une alerte
    const renderAlertCard = (alert) => {
        const category = alertCategories[alert.category];
        const status = getStatus(alert.status); // Utiliser la nouvelle fonction getStatus
        const CategoryIcon = category.icon;

        return (
            <div key={alert.alert_id} className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
                <div className="p-4">
                    {/* En-tête de l'alerte */}
                    <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                            <div className={`p-2 rounded-full ${category.color}`}>
                                {typeof CategoryIcon === 'string' ? (
                                    <span className="text-lg">{CategoryIcon}</span>
                                ) : (
                                    <CategoryIcon className="w-5 h-5" />
                                )}
                            </div>
                            <div>
                                <h3 className="font-semibold text-gray-900">{alert.title}</h3>
                                <p className="text-sm text-gray-500">{alert.time_ago}</p>
                            </div>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                            {alert.is_urgent && (
                                <span className="px-2 py-1 text-xs font-medium text-red-700 bg-red-100 rounded-full">
                                    URGENT
                                </span>
                            )}
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${status.color}`}>
                                {status.label}
                            </span>
                        </div>
                    </div>

                    {/* Description */}
                    <p className="text-gray-700 mb-3 line-clamp-2">{alert.description}</p>

                    {/* Localisation */}
                    {(alert.neighborhood || alert.city) && (
                        <div className="flex items-center text-sm text-gray-500 mb-3">
                            <MapPinIcon className="w-4 h-4 mr-1" />
                            {alert.neighborhood && alert.city ? 
                                `${alert.neighborhood}, ${alert.city}` : 
                                (alert.neighborhood || alert.city)
                            }
                        </div>
                    )}

                    {/* Métadonnées */}
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                        <div className="flex items-center space-x-4">
                            <span className="flex items-center">
                                <UserGroupIcon className="w-4 h-4 mr-1" />
                                {alert.author?.first_name || alert.author?.username}
                            </span>
                            <span className="flex items-center">
                                <HeartIcon className="w-4 h-4 mr-1" />
                                {alert.help_offers_count} aide(s)
                            </span>
                            <span className="flex items-center">
                                <CheckCircleIcon className="w-4 h-4 mr-1" />
                                {alert.verified_by_count} confirmation(s)
                            </span>
                        </div>
                        
                        <div className="flex items-center">
                            <span className={`px-2 py-1 text-xs rounded-full ${
                                alert.reliability_score >= 70 ? 'text-green-700 bg-green-100' :
                                alert.reliability_score >= 40 ? 'text-yellow-700 bg-yellow-100' :
                                'text-red-700 bg-red-100'
                            }`}>
                                {alert.reliability_score.toFixed(0)}% fiable
                            </span>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                        <div className="flex space-x-2">
                            <button
                                onClick={() => setSelectedAlert(alert)}
                                className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
                            >
                                Voir détails
                            </button>
                            <button
                                onClick={() => offerHelp(alert.alert_id, {
                                    offer_type: 'physical_help',
                                    description: 'Je peux aider sur place'
                                })}
                                className="px-3 py-1 text-sm text-green-600 hover:text-green-800 hover:bg-green-50 rounded-md transition-colors"
                            >
                                Je peux aider
                            </button>
                        </div>
                        
                        <div className="flex space-x-1">
                            <button
                                onClick={() => {
                                    console.log('🔘 Bouton Confirmer cliqué pour alerte:', alert.alert_id);
                                    reportAlert(alert.alert_id, 'confirmed');
                                }}
                                className="p-1 text-green-600 hover:text-green-800 hover:bg-green-50 rounded transition-colors"
                                title="Confirmer"
                            >
                                <CheckCircleIcon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => {
                                    console.log('🔘 Bouton Fausse alerte cliqué pour alerte:', alert.alert_id);
                                    reportAlert(alert.alert_id, 'false_alarm');
                                }}
                                className="p-1 text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
                                title="Fausse alerte"
                            >
                                <XCircleIcon className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* En-tête */}
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Alertes Communautaires</h1>
                        <p className="mt-2 text-gray-600">
                            Restez informé des événements importants dans votre quartier
                        </p>
                    </div>
                    
                    <div className="flex space-x-3">
                        <button
                            onClick={() => setShowStatsModal(true)}
                            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                            <ChartBarIcon className="w-4 h-4 mr-2" />
                            Statistiques
                        </button>
                        <button
                            onClick={() => {
                                console.log('🔘 Bouton Nouvelle Alerte cliqué');
                                setShowCreateModal(true);
                            }}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        >
                            <PlusIcon className="w-4 h-4 mr-2" />
                            Nouvelle Alerte
                        </button>
                    </div>
                </div>
            </div>

            {/* Filtres et recherche */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {/* Recherche */}
                    <div className="relative">
                        <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Rechercher..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* Filtre catégorie */}
                    <select
                        value={filters.category}
                        onChange={(e) => setFilters(prev => ({ ...prev, category: e.target.value }))}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="">Toutes les catégories</option>
                        {Object.entries(alertCategories).map(([key, category]) => (
                            <option key={key} value={key}>{category.label}</option>
                        ))}
                    </select>

                    {/* Filtre statut */}
                    <select
                        value={filters.status}
                        onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="">Tous les statuts</option>
                        {Object.entries(alertStatuses).map(([key, status]) => (
                            <option key={key} value={key}>{status.label}</option>
                        ))}
                    </select>

                    {/* Filtres booléens */}
                    <div className="flex space-x-2">
                        <label className="flex items-center">
                            <input
                                type="checkbox"
                                checked={filters.urgentOnly}
                                onChange={(e) => setFilters(prev => ({ ...prev, urgentOnly: e.target.checked }))}
                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="ml-2 text-sm text-gray-700">Urgentes seulement</span>
                        </label>
                        <label className="flex items-center">
                            <input
                                type="checkbox"
                                checked={filters.reliableOnly}
                                onChange={(e) => setFilters(prev => ({ ...prev, reliableOnly: e.target.checked }))}
                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="ml-2 text-sm text-gray-700">Fiables seulement</span>
                        </label>
                    </div>
                </div>
            </div>

            {/* Liste des alertes */}
            <div className="space-y-4">
                {loading ? (
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-2 text-gray-600">Chargement des alertes...</p>
                    </div>
                ) : filteredAlerts.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredAlerts.map(renderAlertCard)}
                    </div>
                ) : (
                    <div className="text-center py-12">
                        <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-gray-400" />
                        <h3 className="mt-2 text-sm font-medium text-gray-900">Aucune alerte trouvée</h3>
                        <p className="mt-1 text-sm text-gray-500">
                            {searchQuery || Object.values(filters).some(f => f) 
                                ? 'Essayez de modifier vos filtres de recherche.' 
                                : 'Soyez le premier à créer une alerte pour votre quartier !'
                            }
                        </p>
                    </div>
                )}
            </div>

            {/* Modals */}
            {showCreateModal && (
                <CreateAlertModal
                    onClose={() => {
                        console.log('❌ Modal fermé');
                        setShowCreateModal(false);
                    }}
                    onSubmit={createAlertWithAI}
                    userLocation={userLocation}
                    alertCategories={alertCategories}
                />
            )}

            {showStatsModal && (
                <AlertStatsModal
                    onClose={() => setShowStatsModal(false)}
                    stats={stats}
                    loadStats={loadStats}
                    alertCategories={alertCategories}
                />
            )}

            {selectedAlert && (
                <AlertDetailModal
                    alert={selectedAlert}
                    onClose={() => setSelectedAlert(null)}
                    onReport={reportAlert}
                    onOfferHelp={offerHelp}
                    alertCategories={alertCategories}
                    alertStatuses={alertStatuses}
                    getStatus={getStatus}
                />
            )}
        </div>
    );
};

// Composant modal pour créer une alerte
const CreateAlertModal = ({ onClose, onSubmit, userLocation, alertCategories }) => {
    console.log('🎨 Modal CreateAlertModal rendu');
    
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: '',
        latitude: userLocation?.latitude ? parseFloat(userLocation.latitude.toFixed(6)) : '',
        longitude: userLocation?.longitude ? parseFloat(userLocation.longitude.toFixed(6)) : '',
        address: '',
        neighborhood: '',
        city: '',
        postal_code: ''
    });
    const [isDetectingLocation, setIsDetectingLocation] = useState(false);

    // Détecter automatiquement l'adresse depuis les coordonnées
    const detectAddressFromCoordinates = async (lat, lng) => {
        setIsDetectingLocation(true);
        try {
            // Formater les coordonnées avec 6 décimales maximum
            const formattedLat = parseFloat(lat.toFixed(6));
            const formattedLng = parseFloat(lng.toFixed(6));
            
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${formattedLat}&lon=${formattedLng}&addressdetails=1`);
            const data = await response.json();
            
            if (data.address) {
                setFormData(prev => ({
                    ...prev,
                    latitude: formattedLat,
                    longitude: formattedLng,
                    address: data.display_name || '',
                    neighborhood: data.address.suburb || data.address.neighbourhood || '',
                    city: data.address.city || data.address.town || data.address.village || '',
                    postal_code: data.address.postcode || ''
                }));
            }
        } catch (error) {
            console.error('Erreur détection adresse:', error);
        } finally {
            setIsDetectingLocation(false);
        }
    };

    // Détecter automatiquement la position et l'adresse
    useEffect(() => {
        if (userLocation?.latitude && userLocation?.longitude) {
            detectAddressFromCoordinates(userLocation.latitude, userLocation.longitude);
        }
    }, [userLocation]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.title || !formData.description || !formData.category) {
            toast.error('Veuillez remplir tous les champs obligatoires');
            return;
        }
        onSubmit(formData);
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Créer une nouvelle alerte</h3>
                    
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Titre *</label>
                            <input
                                type="text"
                                value={formData.title}
                                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Titre de l'alerte"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Description *</label>
                            <textarea
                                value={formData.description}
                                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                                rows={3}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Décrivez la situation..."
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Catégorie *</label>
                            <select
                                value={formData.category}
                                onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value }))}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="">Sélectionner une catégorie</option>
                                {Object.entries(alertCategories).map(([key, category]) => (
                                    <option key={key} value={key}>{category.label}</option>
                                ))}
                            </select>
                        </div>

                        {/* Section Localisation - Plus simple pour l'utilisateur */}
                        <div className="border-t pt-4">
                            <h4 className="text-sm font-medium text-gray-700 mb-3">📍 Localisation de l'alerte</h4>
                            
                            {isDetectingLocation && (
                                <div className="mb-3 p-2 bg-blue-50 rounded-md">
                                    <div className="flex items-center text-blue-600 text-sm">
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                                        Détection automatique de votre position...
                                    </div>
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Adresse</label>
                                <input
                                    type="text"
                                    value={formData.address}
                                    onChange={(e) => setFormData(prev => ({ ...prev, address: e.target.value }))}
                                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Adresse de l'alerte"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4 mt-3">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Quartier</label>
                                    <input
                                        type="text"
                                        value={formData.neighborhood}
                                        onChange={(e) => setFormData(prev => ({ ...prev, neighborhood: e.target.value }))}
                                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="Quartier"
                                    />
                                </div>
                                
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Ville</label>
                                    <input
                                        type="text"
                                        value={formData.city}
                                        onChange={(e) => setFormData(prev => ({ ...prev, city: e.target.value }))}
                                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="Ville"
                                    />
                                </div>
                            </div>

                            <div className="mt-3">
                                <label className="block text-sm font-medium text-gray-700">Code postal</label>
                                <input
                                    type="text"
                                    value={formData.postal_code}
                                    onChange={(e) => setFormData(prev => ({ ...prev, postal_code: e.target.value }))}
                                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Code postal"
                                />
                            </div>

                            {/* Informations techniques cachées */}
                            <div className="mt-3 p-2 bg-gray-50 rounded-md text-xs text-gray-500">
                                <div className="flex justify-between">
                                    <span>Position détectée automatiquement</span>
                                    <span>📍 GPS activé</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-end space-x-3 pt-4">
                            <button
                                type="button"
                                onClick={onClose}
                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
                            >
                                Annuler
                            </button>
                            <button
                                type="submit"
                                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
                            >
                                Créer l'alerte
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

// Composant modal pour les statistiques
const AlertStatsModal = ({ onClose, stats, loadStats, alertCategories }) => {
    useEffect(() => {
        if (!stats) {
            loadStats();
        }
    }, [stats, loadStats]);

    if (!stats) {
        return (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-2 text-gray-600">Chargement des statistiques...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-10 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-medium text-gray-900">Statistiques des Alertes</h3>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <XCircleIcon className="w-6 h-6" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        <div className="bg-blue-50 p-4 rounded-lg">
                            <h4 className="text-sm font-medium text-blue-600">Total Alertes</h4>
                            <p className="text-2xl font-bold text-blue-900">
                                {(() => {
                                    const total = stats.total_alerts;
                                    if (typeof total === 'number') return total;
                                    if (typeof total === 'string') return parseInt(total) || 0;
                                    if (typeof total === 'object' && total !== null) {
                                        const value = total.count || total.total || total;
                                        return typeof value === 'number' ? value : (parseInt(value) || 0);
                                    }
                                    return 0;
                                })()}
                            </p>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                            <h4 className="text-sm font-medium text-green-600">Résolues</h4>
                            <p className="text-2xl font-bold text-green-900">
                                {(() => {
                                    const resolved = stats.resolved_alerts;
                                    if (typeof resolved === 'number') return resolved;
                                    if (typeof resolved === 'string') return parseInt(resolved) || 0;
                                    if (typeof resolved === 'object' && resolved !== null) {
                                        const value = resolved.count || resolved.resolved || resolved;
                                        return typeof value === 'number' ? value : (parseInt(value) || 0);
                                    }
                                    return 0;
                                })()}
                            </p>
                        </div>
                        <div className="bg-red-50 p-4 rounded-lg">
                            <h4 className="text-sm font-medium text-red-600">Fausses Alertes</h4>
                            <p className="text-2xl font-bold text-red-900">
                                {(() => {
                                    const falseAlarms = stats.false_alarms;
                                    if (typeof falseAlarms === 'number') return falseAlarms;
                                    if (typeof falseAlarms === 'string') return parseInt(falseAlarms) || 0;
                                    if (typeof falseAlarms === 'object' && falseAlarms !== null) {
                                        const value = falseAlarms.count || falseAlarms.false || falseAlarms;
                                        return typeof value === 'number' ? value : (parseInt(value) || 0);
                                    }
                                    return 0;
                                })()}
                            </p>
                        </div>
                        <div className="bg-yellow-50 p-4 rounded-lg">
                            <h4 className="text-sm font-medium text-yellow-600">Fiabilité Moyenne</h4>
                            <p className="text-2xl font-bold text-yellow-900">
                                {(() => {
                                    const reliability = stats.avg_reliability_score;
                                    if (typeof reliability === 'number') {
                                        return reliability.toFixed(1);
                                    } else if (typeof reliability === 'string') {
                                        const parsed = parseFloat(reliability);
                                        return isNaN(parsed) ? '0.0' : parsed.toFixed(1);
                                    } else if (typeof reliability === 'object' && reliability !== null) {
                                        // Si c'est un objet, essayer d'extraire la valeur
                                        const value = reliability.score || reliability.value || reliability;
                                        const parsed = typeof value === 'number' ? value : parseFloat(value);
                                        return isNaN(parsed) ? '0.0' : parsed.toFixed(1);
                                    }
                                    return '0.0';
                                })()}%
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Statistiques par catégorie */}
                        <div>
                            <h4 className="text-lg font-medium text-gray-900 mb-4">Par Catégorie</h4>
                            <div className="space-y-3">
                                {Object.entries(stats.category_stats || {}).map(([category, data]) => {
                                    // Gérer le cas où data pourrait être un objet ou un nombre
                                    const count = typeof data === 'object' ? data.count || data : data;
                                    const percentage = typeof data === 'object' ? data.percentage || 0 : 0;
                                    const displayCount = typeof count === 'number' ? count : (typeof count === 'string' ? parseInt(count) || 0 : 0);
                                    const displayPercentage = typeof percentage === 'number' ? percentage : (typeof percentage === 'string' ? parseFloat(percentage) || 0 : 0);
                                    
                                    return (
                                        <div key={category} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                            <div className="flex items-center">
                                                <span className="mr-2">{alertCategories[category]?.label || category}</span>
                                            </div>
                                            <div className="text-right">
                                                <p className="font-semibold">{displayCount}</p>
                                                <p className="text-sm text-gray-500">{displayPercentage.toFixed(1)}%</p>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* Statistiques géographiques */}
                        <div>
                            <h4 className="text-lg font-medium text-gray-900 mb-4">Par Localisation</h4>
                            <div className="space-y-3">
                                {Object.entries(stats.city_stats || {}).slice(0, 5).map(([city, countData]) => {
                                    // Gérer le cas où countData pourrait être un objet ou un nombre
                                    const count = typeof countData === 'object' ? countData.count || countData : countData;
                                    const displayCount = typeof count === 'number' ? count : (typeof count === 'string' ? parseInt(count) || 0 : 0);
                                    
                                    return (
                                        <div key={city} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                            <span className="font-medium">{city || 'Ville inconnue'}</span>
                                            <span className="text-lg font-semibold">{displayCount}</span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Composant modal pour les détails d'une alerte
const AlertDetailModal = ({ alert, onClose, onReport, onOfferHelp, alertCategories, alertStatuses, getStatus }) => {
    const [showHelpForm, setShowHelpForm] = useState(false);
    const [helpData, setHelpData] = useState({
        offer_type: 'physical_help',
        description: '',
        contact_info: { phone: '', email: '' }
    });

    const category = alertCategories[alert.category];
    const status = getStatus(alert.status); // Utiliser la nouvelle fonction getStatus
    const CategoryIcon = category.icon;

    const handleOfferHelp = () => {
        if (!helpData.description) {
            toast.error('Veuillez décrire votre offre d\'aide');
            return;
        }
        onOfferHelp(alert.alert_id, helpData);
        setShowHelpForm(false);
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-10 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    <div className="flex justify-between items-start mb-6">
                        <div className="flex items-center space-x-3">
                            <div className={`p-3 rounded-full ${category.color}`}>
                                {typeof CategoryIcon === 'string' ? (
                                    <span className="text-2xl">{CategoryIcon}</span>
                                ) : (
                                    <CategoryIcon className="w-8 h-8" />
                                )}
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-gray-900">{alert.title}</h3>
                                <p className="text-sm text-gray-500">Créée {alert.time_ago}</p>
                            </div>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <XCircleIcon className="w-6 h-6" />
                        </button>
                    </div>

                    <div className="space-y-6">
                        {/* Description */}
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                            <p className="text-gray-700">{alert.description}</p>
                        </div>

                        {/* Localisation */}
                        {(alert.neighborhood || alert.city) && (
                            <div>
                                <h4 className="font-medium text-gray-900 mb-2">Localisation</h4>
                                <div className="flex items-center text-gray-700">
                                    <MapPinIcon className="w-5 h-5 mr-2" />
                                    {alert.address && <span>{alert.address}, </span>}
                                    {alert.neighborhood && <span>{alert.neighborhood}, </span>}
                                    {alert.city && <span>{alert.city}</span>}
                                    {alert.postal_code && <span> {alert.postal_code}</span>}
                                </div>
                            </div>
                        )}

                        {/* Statut et fiabilité */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <h4 className="font-medium text-gray-900 mb-2">Statut</h4>
                                <span className={`px-3 py-1 text-sm font-medium rounded-full ${status.color}`}>
                                    {status.label}
                                </span>
                            </div>
                            <div>
                                <h4 className="font-medium text-gray-900 mb-2">Fiabilité</h4>
                                <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                                    alert.reliability_score >= 70 ? 'text-green-700 bg-green-100' :
                                    alert.reliability_score >= 40 ? 'text-yellow-700 bg-yellow-100' :
                                    'text-red-700 bg-red-100'
                                }`}>
                                    {alert.reliability_score.toFixed(0)}% fiable
                                </span>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex space-x-3 pt-4 border-t border-gray-200">
                            <button
                                onClick={() => setShowHelpForm(true)}
                                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md"
                            >
                                Je peux aider
                            </button>
                            <button
                                onClick={() => onReport(alert.alert_id, 'confirmed')}
                                className="px-4 py-2 text-sm font-medium text-green-600 bg-green-100 hover:bg-green-200 rounded-md"
                            >
                                Confirmer
                            </button>
                            <button
                                onClick={() => onReport(alert.alert_id, 'false_alarm')}
                                className="px-4 py-2 text-sm font-medium text-red-600 bg-red-100 hover:bg-red-200 rounded-md"
                            >
                                Fausse alerte
                            </button>
                        </div>
                    </div>

                    {/* Formulaire d'offre d'aide */}
                    {showHelpForm && (
                        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                            <h4 className="font-medium text-gray-900 mb-3">Proposer votre aide</h4>
                            <div className="space-y-3">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Type d'aide</label>
                                    <select
                                        value={helpData.offer_type}
                                        onChange={(e) => setHelpData(prev => ({ ...prev, offer_type: e.target.value }))}
                                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                    >
                                        <option value="physical_help">Aide physique</option>
                                        <option value="information">Information</option>
                                        <option value="transport">Transport</option>
                                        <option value="medical">Aide médicale</option>
                                        <option value="technical">Aide technique</option>
                                        <option value="other">Autre</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Description</label>
                                    <textarea
                                        value={helpData.description}
                                        onChange={(e) => setHelpData(prev => ({ ...prev, description: e.target.value }))}
                                        rows={3}
                                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                        placeholder="Décrivez comment vous pouvez aider..."
                                    />
                                </div>
                                <div className="flex space-x-3">
                                    <button
                                        onClick={handleOfferHelp}
                                        className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md"
                                    >
                                        Envoyer
                                    </button>
                                    <button
                                        onClick={() => setShowHelpForm(false)}
                                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
                                    >
                                        Annuler
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CommunityAlerts; 
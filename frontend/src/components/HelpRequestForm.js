import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { 
    XMarkIcon, MapPinIcon, CameraIcon, ExclamationTriangleIcon,
    UserIcon, HeartIcon, ClockIcon, PhoneIcon, EnvelopeIcon,
    CalendarIcon, UsersIcon, HandRaisedIcon, TruckIcon,
    AcademicCapIcon, WrenchScrewdriverIcon, ShoppingBagIcon
} from '@heroicons/react/24/outline';




// Types de besoins avec icônes
const NEED_TYPES = {
    material: { 
        label: 'Matériel', 
        icon: '📦', 
        color: 'text-blue-600 bg-blue-100',
        heroIcon: TruckIcon,
        description: 'Prêt ou don de matériel'
    },
    presence: { 
        label: 'Présence/Accompagnement', 
        icon: '👥', 
        color: 'text-green-600 bg-green-100',
        heroIcon: UsersIcon,
        description: 'Accompagnement ou présence'
    },
    service: { 
        label: 'Service', 
        icon: '🛠️', 
        color: 'text-purple-600 bg-purple-100',
        heroIcon: HandRaisedIcon,
        description: 'Prestation de service'
    },
    transport: { 
        label: 'Transport', 
        icon: '🚗', 
        color: 'text-indigo-600 bg-indigo-100',
        heroIcon: TruckIcon,
        description: 'Transport ou livraison'
    },
    shopping: { 
        label: 'Courses', 
        icon: '🛒', 
        color: 'text-orange-600 bg-orange-100',
        heroIcon: ShoppingBagIcon,
        description: 'Courses ou achats'
    },
    technical: { 
        label: 'Aide technique', 
        icon: '🔧', 
        color: 'text-yellow-600 bg-yellow-100',
        heroIcon: WrenchScrewdriverIcon,
        description: 'Assistance technique'
    },
    education: { 
        label: 'Aide éducative', 
        icon: '📚', 
        color: 'text-teal-600 bg-teal-100',
        heroIcon: AcademicCapIcon,
        description: 'Soutien scolaire ou formation'
    },
    other: { 
        label: 'Autre', 
        icon: '🤝', 
        color: 'text-gray-600 bg-gray-100',
        heroIcon: HandRaisedIcon,
        description: 'Autre type d\'aide'
    },
};

// Durées estimées
const DURATION_OPTIONS = [
    { value: 'immediate', label: 'Immédiat', icon: '⚡', description: 'Besoin urgent' },
    { value: 'this_week', label: 'Cette semaine', icon: '📅', description: 'Dans les 7 jours' },
    { value: 'this_month', label: 'Ce mois', icon: '🗓️', description: 'Dans le mois' },
    { value: 'specific_date', label: 'Avant une date', icon: '📆', description: 'Date spécifique' },
    { value: 'ongoing', label: 'En continu', icon: '🔄', description: 'Besoin régulier' },
];

// Options pour "pour qui"
const FOR_WHO_OPTIONS = {
    myself: { label: 'Moi-même', icon: '👤', description: 'Aide personnelle' },
    family: { label: 'Ma famille', icon: '👨‍👩‍👧‍👦', description: 'Pour ma famille' },
    neighbor: { label: 'Mon voisin', icon: '🏠', description: 'Pour un voisin' },
    community: { label: 'La communauté', icon: '🌍', description: 'Pour la communauté' },
    other: { label: 'Autre', icon: '🤝', description: 'Autre personne' },
};

// Options de contact
const CONTACT_OPTIONS = [
    { value: 'message', label: 'Message privé', icon: '💬' },
    { value: 'phone', label: 'Téléphone', icon: '📞' },
    { value: 'email', label: 'Email', icon: '📧' },
    { value: 'any', label: 'N\'importe lequel', icon: '✅' },
];

const HelpRequestForm = ({ onClose, onSubmit, userLocation, needTypes = NEED_TYPES }) => {
    // États du formulaire
    const [formData, setFormData] = useState({
        request_type: 'request',
        need_type: '',
        for_who: 'myself',
        title: '',
        description: '',
        duration_type: 'this_week',
        specific_date: '',
        estimated_hours: '',
        proximity_zone: 'local',
        is_urgent: false,
        contact_preference: 'message',
        phone: '',
        email: '',
        custom_need_type: '',
        custom_for_who: '',
    });
    
    // États pour la géolocalisation
    const [location, setLocation] = useState({
        latitude: userLocation?.latitude || null,
        longitude: userLocation?.longitude || null,
        address: '',
        neighborhood: '',
        city: '',
        postal_code: '',
    });

    // Mettre à jour la location quand userLocation change
    useEffect(() => {
        if (userLocation?.latitude && userLocation?.longitude) {
            setLocation(prev => ({
                ...prev,
                latitude: userLocation.latitude,
                longitude: userLocation.longitude,
            }));
            // Géocodage inverse automatique
            reverseGeocode(userLocation.latitude, userLocation.longitude);
        }
    }, [userLocation]);
    
    // États pour l'interface
    const [loading, setLoading] = useState(false);

    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [currentStep, setCurrentStep] = useState(1);
    
    // Gérer les changements dans le formulaire
    const handleInputChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };
    
    // Gérer les changements de localisation
    const handleLocationChange = (field, value) => {
        setLocation(prev => ({
            ...prev,
            [field]: value
        }));
    };
    

    
    // Géocodage inverse
    const reverseGeocode = async (lat, lng) => {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
            );
            const data = await response.json();
            
            if (data.display_name) {
                const addressParts = data.display_name.split(', ');
                setLocation(prev => ({
                    ...prev,
                    address: data.display_name,
                    neighborhood: addressParts[1] || '',
                    city: addressParts[addressParts.length - 3] || '',
                    postal_code: addressParts[addressParts.length - 2] || '',
                }));
            }
        } catch (error) {
            console.error('Erreur géocodage:', error);
        }
    };
    
    // Gérer la sélection de fichier
    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        console.log('📁 handleFileSelect appelé');
        console.log('📁 file:', file);
        if (file) {
            console.log('📁 Fichier sélectionné:', file.name, file.type, file.size);
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onload = (e) => setPreviewUrl(e.target.result);
            reader.readAsDataURL(file);
        } else {
            console.log('📁 Aucun fichier sélectionné');
        }
    };
    
    // Validation du formulaire
    const validateForm = () => {
        console.log('🔍 Début validation');
        console.log('📋 formData.title:', formData.title);
        console.log('📋 formData.description:', formData.description);
        console.log('📋 formData.need_type:', formData.need_type);
        console.log('📍 location.latitude:', location.latitude);
        console.log('📍 location.longitude:', location.longitude);
        
        if (!formData.title || !formData.title.trim()) {
            console.log('❌ Titre manquant');
            toast.error('Veuillez saisir un titre pour votre demande d\'aide');
            return false;
        }
        
        if (!formData.description || !formData.description.trim()) {
            console.log('❌ Description manquante');
            toast.error('Veuillez saisir une description détaillée de votre besoin');
            return false;
        }
        
        if (!formData.need_type) {
            console.log('❌ Type de besoin manquant');
            toast.error('Veuillez sélectionner un type de besoin (étape 2)');
            return false;
        }
        
        if (formData.need_type === 'other' && !formData.custom_need_type.trim()) {
            console.log('❌ Type de besoin personnalisé manquant');
            toast.error('Veuillez spécifier le type de besoin personnalisé');
            return false;
        }
        
        if (formData.for_who === 'other' && !formData.custom_for_who.trim()) {
            console.log('❌ Pour qui personnalisé manquant');
            toast.error('Veuillez spécifier pour qui cette aide est destinée');
            return false;
        }
        
        if (formData.duration_type === 'specific_date' && !formData.specific_date) {
            console.log('❌ Date spécifique manquante');
            toast.error('Veuillez sélectionner une date spécifique');
            return false;
        }
        
        if (!location.latitude || !location.longitude) {
            console.log('❌ Localisation manquante');
            console.log('📍 latitude:', location.latitude);
            console.log('📍 longitude:', location.longitude);
            toast.error('Veuillez autoriser la géolocalisation ou sélectionner une localisation manuellement');
            return false;
        }
        
        console.log('✅ Validation réussie');
        return true;
    };
    
    // Soumettre le formulaire
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        console.log('🔍 Début handleSubmit');
        console.log('📋 formData:', formData);
        console.log('📍 location:', location);
        
        if (!validateForm()) {
            console.log('❌ Validation échouée');
            return;
        }
        
        console.log('✅ Validation réussie');
        setLoading(true);
        
        try {
            // Préparer les données
            const cleanedData = {
                ...formData,
                ...location,
                // Formater les coordonnées GPS à 6 décimales maximum
                latitude: location.latitude ? parseFloat(location.latitude.toFixed(6)) : null,
                longitude: location.longitude ? parseFloat(location.longitude.toFixed(6)) : null,
                expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(), // 7 jours
            };
            
            console.log('📤 Données à envoyer:', cleanedData);
            
            // Vérifier l'état de selectedFile
            console.log('📁 selectedFile:', selectedFile);
            console.log('📁 selectedFile existe:', !!selectedFile);
            
            // Envoyer les données
            if (selectedFile) {
                console.log('📷 Envoi avec photo');
                const formData = new FormData();
                
                // Ajouter tous les champs au FormData
                Object.keys(cleanedData).forEach(key => {
                    const value = cleanedData[key];
                    if (value !== null && value !== undefined && value !== '') {
                        formData.append(key, value);
                    }
                });
                
                // Ajouter la photo
                formData.append('photo', selectedFile);
                
                console.log('📋 FormData contenu:');
                for (let [key, value] of formData.entries()) {
                    console.log(key + ':', value);
                }
                
                await onSubmit(formData);
            } else {
                console.log('📤 Envoi sans photo');
                console.log('📋 Données JSON nettoyées:', cleanedData);
                await onSubmit(cleanedData);
            }
            
            console.log('✅ Soumission réussie');
            onClose();
        } catch (error) {
            console.error('❌ Erreur soumission:', error);
            toast.error('Erreur lors de la création de la demande d\'aide');
        } finally {
            setLoading(false);
        }
    };
    
    
    
    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-10 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    {/* En-tête */}
                    <div className="flex justify-between items-start mb-6">
                        <div>
                            <h3 className="text-2xl font-bold text-gray-900">
                                {formData.request_type === 'request' ? 'Demander de l\'aide' : 'Offrir de l\'aide'}
                            </h3>
                            <p className="text-sm text-gray-500 mt-1">
                                Partagez votre besoin ou votre disponibilité avec la communauté
                            </p>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <XMarkIcon className="w-6 h-6" />
                        </button>
                    </div>
                    
                    {/* Indicateur de progression */}
                    <div className="mb-6">
                        <div className="flex items-center justify-between text-sm text-gray-600">
                            <div className={`flex items-center ${formData.request_type ? 'text-blue-600' : ''}`}>
                                <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-2 ${
                                    formData.request_type ? 'bg-blue-600 text-white' : 'bg-gray-200'
                                }`}>
                                    {formData.request_type ? '✓' : '1'}
                                </div>
                                Type de demande
                            </div>
                            <div className={`flex items-center ${formData.need_type ? 'text-blue-600' : ''}`}>
                                <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-2 ${
                                    formData.need_type ? 'bg-blue-600 text-white' : 'bg-gray-200'
                                }`}>
                                    {formData.need_type ? '✓' : '2'}
                                </div>
                                Type de besoin
                            </div>
                            <div className={`flex items-center ${formData.title && formData.description ? 'text-blue-600' : ''}`}>
                                <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-2 ${
                                    formData.title && formData.description ? 'bg-blue-600 text-white' : 'bg-gray-200'
                                }`}>
                                    {formData.title && formData.description ? '✓' : '3'}
                                </div>
                                Détails
                            </div>
                        </div>
                    </div>

                    {/* Formulaire */}
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Type de demande */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Type de publication
                            </label>
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    type="button"
                                    onClick={() => handleInputChange('request_type', 'request')}
                                    className={`p-4 border-2 rounded-lg text-center transition-colors ${
                                        formData.request_type === 'request'
                                            ? 'border-blue-500 bg-blue-50 text-blue-700'
                                            : 'border-gray-300 hover:border-gray-400'
                                    }`}
                                >
                                    <HeartIcon className="w-8 h-8 mx-auto mb-2" />
                                    <div className="font-medium">Demander de l'aide</div>
                                    <div className="text-sm text-gray-500">J'ai besoin d'aide</div>
                                </button>
                                
                                <button
                                    type="button"
                                    onClick={() => handleInputChange('request_type', 'offer')}
                                    className={`p-4 border-2 rounded-lg text-center transition-colors ${
                                        formData.request_type === 'offer'
                                            ? 'border-green-500 bg-green-50 text-green-700'
                                            : 'border-gray-300 hover:border-gray-400'
                                    }`}
                                >
                                    <HandRaisedIcon className="w-8 h-8 mx-auto mb-2" />
                                    <div className="font-medium">Offrir de l'aide</div>
                                    <div className="text-sm text-gray-500">Je peux aider</div>
                                </button>
                            </div>
                        </div>
                        
                        {/* Type de besoin */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Type de besoin * <span className="text-red-500">(Obligatoire)</span>
                            </label>
                            
                            {/* Indicateur de sélection */}
                            {!formData.need_type && (
                                <div className="mb-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                                    <div className="flex items-center text-yellow-800">
                                        <ExclamationTriangleIcon className="w-4 h-4 mr-2" />
                                        <span className="text-sm font-medium">Veuillez sélectionner un type de besoin</span>
                                    </div>
                                </div>
                            )}
                            
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                {Object.entries(needTypes).map(([key, type]) => (
                                    <button
                                        key={key}
                                        type="button"
                                        onClick={() => handleInputChange('need_type', key)}
                                        className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                            formData.need_type === key
                                                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                                : 'border-gray-300 hover:border-gray-400'
                                        }`}
                                    >
                                        <div className="text-2xl mb-1">{type.icon}</div>
                                        <div className="text-xs font-medium">{type.label}</div>
                                        <div className="text-xs text-gray-500 mt-1">{type.description}</div>
                                    </button>
                                ))}
                            </div>
                            
                            {/* Type personnalisé */}
                            {formData.need_type === 'other' && (
                                <div className="mt-3">
                                    <input
                                        type="text"
                                        value={formData.custom_need_type}
                                        onChange={(e) => handleInputChange('custom_need_type', e.target.value)}
                                        placeholder="Précisez le type de besoin..."
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </div>
                            )}
                        </div>
                        
                        {/* Pour qui */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Pour qui cette aide est destinée ?
                            </label>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                {Object.entries(FOR_WHO_OPTIONS).map(([key, option]) => (
                                    <button
                                        key={key}
                                        type="button"
                                        onClick={() => handleInputChange('for_who', key)}
                                        className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                            formData.for_who === key
                                                ? 'border-blue-500 bg-blue-50'
                                                : 'border-gray-300 hover:border-gray-400'
                                        }`}
                                    >
                                        <div className="text-2xl mb-1">{option.icon}</div>
                                        <div className="text-sm font-medium">{option.label}</div>
                                        <div className="text-xs text-gray-500 mt-1">{option.description}</div>
                                    </button>
                                ))}
                            </div>
                            
                            {/* Autre option */}
                            {formData.for_who === 'other' && (
                                <div className="mt-3">
                                    <input
                                        type="text"
                                        value={formData.custom_for_who}
                                        onChange={(e) => handleInputChange('custom_for_who', e.target.value)}
                                        placeholder="Précisez pour qui..."
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </div>
                            )}
                        </div>
                        
                        {/* Titre et description */}
                        <div className="grid grid-cols-1 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Titre de votre demande *
                                </label>
                                <input
                                    type="text"
                                    value={formData.title}
                                    onChange={(e) => handleInputChange('title', e.target.value)}
                                    placeholder="Ex: Besoin d'aide pour déménager"
                                    className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500 ${
                                        formData.title ? 'border-green-300' : 'border-gray-300'
                                    }`}
                                    maxLength={200}
                                    required
                                />
                                {!formData.title && (
                                    <p className="mt-1 text-sm text-red-600">⚠️ Le titre est obligatoire</p>
                                )}
                            </div>
                            
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Description détaillée *
                                </label>
                                <textarea
                                    value={formData.description}
                                    onChange={(e) => handleInputChange('description', e.target.value)}
                                    placeholder="Décrivez votre besoin en détail..."
                                    rows={4}
                                    className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500 ${
                                        formData.description ? 'border-green-300' : 'border-gray-300'
                                    }`}
                                    maxLength={2000}
                                    required
                                />
                                {!formData.description && (
                                    <p className="mt-1 text-sm text-red-600">⚠️ La description est obligatoire</p>
                                )}
                            </div>
                        </div>
                        
                        {/* Durée et planning */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Quand avez-vous besoin de cette aide ?
                            </label>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                {DURATION_OPTIONS.map((option) => (
                                    <button
                                        key={option.value}
                                        type="button"
                                        onClick={() => handleInputChange('duration_type', option.value)}
                                        className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                            formData.duration_type === option.value
                                                ? 'border-blue-500 bg-blue-50'
                                                : 'border-gray-300 hover:border-gray-400'
                                        }`}
                                    >
                                        <div className="text-xl mb-1">{option.icon}</div>
                                        <div className="text-sm font-medium">{option.label}</div>
                                        <div className="text-xs text-gray-500 mt-1">{option.description}</div>
                                    </button>
                                ))}
                            </div>
                            
                            {/* Date spécifique */}
                            {formData.duration_type === 'specific_date' && (
                                <div className="mt-3">
                                    <input
                                        type="date"
                                        value={formData.specific_date}
                                        onChange={(e) => handleInputChange('specific_date', e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </div>
                            )}
                            
                            {/* Durée estimée */}
                            <div className="mt-3">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Durée estimée (en heures, optionnel)
                                </label>
                                <input
                                    type="number"
                                    value={formData.estimated_hours}
                                    onChange={(e) => handleInputChange('estimated_hours', e.target.value)}
                                    placeholder="Ex: 2"
                                    min="1"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                        </div>
                        
                        {/* Zone de proximité */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Zone de proximité
                            </label>
                            <div className="grid grid-cols-3 gap-3">
                                <button
                                    type="button"
                                    onClick={() => handleInputChange('proximity_zone', 'local')}
                                    className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                        formData.proximity_zone === 'local'
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-300 hover:border-gray-400'
                                    }`}
                                >
                                    <div className="text-lg mb-1">🏠</div>
                                    <div className="text-sm font-medium">Quartier</div>
                                </button>
                                
                                <button
                                    type="button"
                                    onClick={() => handleInputChange('proximity_zone', 'city')}
                                    className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                        formData.proximity_zone === 'city'
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-300 hover:border-gray-400'
                                    }`}
                                >
                                    <div className="text-lg mb-1">🏙️</div>
                                    <div className="text-sm font-medium">Ville</div>
                                </button>
                                
                                <button
                                    type="button"
                                    onClick={() => handleInputChange('proximity_zone', 'region')}
                                    className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                        formData.proximity_zone === 'region'
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-300 hover:border-gray-400'
                                    }`}
                                >
                                    <div className="text-lg mb-1">🌍</div>
                                    <div className="text-sm font-medium">Région</div>
                                </button>
                            </div>
                        </div>
                        
                        {/* Localisation */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-3">
                                Localisation *
                            </label>
                            
                            {/* Bouton pour afficher/masquer la carte */}
                            <div className="flex items-center justify-between mb-2">
                                <div className="text-sm text-gray-600">
                                    Entrez manuellement l'adresse ou utilisez votre position actuelle
                                </div>
                            <button
                                type="button"
                                    onClick={() => {
                                        if (navigator.geolocation) {
                                            navigator.geolocation.getCurrentPosition(
                                                (position) => {
                                                    const { latitude, longitude } = position.coords;
                                                    setLocation(prev => ({
                                                        ...prev,
                                                        latitude,
                                                        longitude
                                                    }));
                                                    reverseGeocode(latitude, longitude);
                                                    toast.success('Position actuelle récupérée');
                                                },
                                                (error) => {
                                                    console.error('Erreur géolocalisation:', error);
                                                    toast.error('Impossible d\'obtenir votre position');
                                                }
                                            );
                                        } else {
                                            toast.error('Géolocalisation non supportée');
                                        }
                                    }}
                                    className="flex items-center px-3 py-1 text-sm font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100"
                            >
                                    <MapPinIcon className="w-4 h-4 mr-1" />
                                    Utiliser ma position
                            </button>
                            </div>
                            
                            {/* Indicateur de localisation */}
                            <div className="mt-3 mb-2">
                                {location.latitude && location.longitude ? (
                                    <div className="flex items-center text-sm text-green-600 bg-green-50 px-3 py-2 rounded-md">
                                        <MapPinIcon className="w-4 h-4 mr-2" />
                                        Position définie: {location.latitude.toFixed(6)}, {location.longitude.toFixed(6)}
                                    </div>
                                ) : (
                                    <div className="flex items-center text-sm text-orange-600 bg-orange-50 px-3 py-2 rounded-md">
                                        <MapPinIcon className="w-4 h-4 mr-2" />
                                        Position non définie - Utilisez le bouton ci-dessus ou entrez manuellement
                                </div>
                            )}
                            </div>
                            
                            {/* Champs d'adresse */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            value={location.address}
                                            onChange={(e) => handleLocationChange('address', e.target.value)}
                                    placeholder="Adresse complète"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                        />
                                            <input
                                                type="text"
                                                value={location.neighborhood}
                                                onChange={(e) => handleLocationChange('neighborhood', e.target.value)}
                                    placeholder="Quartier"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                                            <input
                                                type="text"
                                                value={location.city}
                                                onChange={(e) => handleLocationChange('city', e.target.value)}
                                    placeholder="Ville"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                                        <input
                                            type="text"
                                            value={location.postal_code}
                                            onChange={(e) => handleLocationChange('postal_code', e.target.value)}
                                    placeholder="Code postal"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                        />
                            </div>
                        </div>
                        
                        {/* Options supplémentaires */}
                            <div className="space-y-4">
                            {/* Urgence */}
                            <div className="flex items-center">
                                        <input
                                            type="checkbox"
                                    id="is_urgent"
                                            checked={formData.is_urgent}
                                            onChange={(e) => handleInputChange('is_urgent', e.target.checked)}
                                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                        />
                                <label htmlFor="is_urgent" className="ml-2 text-sm text-gray-700">
                                    Marquer comme urgent
                                    </label>
                                </div>
                                
                            {/* Préférence de contact */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Préférence de contact
                                    </label>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                    {CONTACT_OPTIONS.map((option) => (
                                        <button
                                            key={option.value}
                                            type="button"
                                            onClick={() => handleInputChange('contact_preference', option.value)}
                                            className={`p-3 border-2 rounded-lg text-center transition-colors ${
                                                formData.contact_preference === option.value
                                                    ? 'border-blue-500 bg-blue-50'
                                                    : 'border-gray-300 hover:border-gray-400'
                                            }`}
                                        >
                                            <div className="text-lg mb-1">{option.icon}</div>
                                            <div className="text-sm font-medium">{option.label}</div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                            
                            {/* Contact info optionnel */}
                            {(formData.contact_preference === 'phone' || formData.contact_preference === 'any') && (
                                            <input
                                                type="tel"
                                                value={formData.phone}
                                                onChange={(e) => handleInputChange('phone', e.target.value)}
                                    placeholder="Numéro de téléphone (optionnel)"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                            )}
                                        
                            {(formData.contact_preference === 'email' || formData.contact_preference === 'any') && (
                                            <input
                                                type="email"
                                                value={formData.email}
                                                onChange={(e) => handleInputChange('email', e.target.value)}
                                    placeholder="Adresse email (optionnel)"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                            )}
                                
                            {/* Photo optionnelle */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Photo (optionnel)
                                    </label>
                                            <input
                                                type="file"
                                                accept="image/*"
                                                onChange={handleFileSelect}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                            />
                                        {previewUrl && (
                                    <div className="mt-2">
                                        <img src={previewUrl} alt="Aperçu" className="w-32 h-32 object-cover rounded-lg" />
                                    </div>
                                )}
                            </div>
                        </div>
                        
                        {/* Boutons d'action */}
                        <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
                            <button
                                type="button"
                                onClick={onClose}
                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                            >
                                Annuler
                            </button>
                            <button
                                type="submit"
                                disabled={loading || !formData.need_type}
                                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                                    loading || !formData.need_type
                                        ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                                        : 'bg-blue-600 text-white hover:bg-blue-700'
                                }`}
                            >
                                {loading ? 'Création...' : !formData.need_type ? 'Sélectionnez un type de besoin' : 'Créer la demande'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default HelpRequestForm; 
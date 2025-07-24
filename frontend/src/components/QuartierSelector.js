import React, { useState, useEffect } from 'react';
import { MapPin, Search, Loader } from 'lucide-react';

const QuartierSelector = ({ onQuartierSelect, userLocation }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedQuartier, setSelectedQuartier] = useState(null);
    const [quartiers, setQuartiers] = useState([]);

    // Charger les quartiers depuis l'API
    useEffect(() => {
        loadQuartiers();
    }, []);

    // Détecter automatiquement la position
    useEffect(() => {
        if (userLocation && !selectedQuartier) {
            detectQuartierFromCoordinates(userLocation.latitude, userLocation.longitude);
        }
    }, [userLocation]);

    const loadQuartiers = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/geography/quartiers/');
            if (response.ok) {
                const data = await response.json();
                setQuartiers(data.results || data);
            }
        } catch (error) {
            console.error('Erreur chargement quartiers:', error);
        }
    };

    const detectQuartierFromCoordinates = async (lat, lng) => {
        setIsLoading(true);
        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`);
            const data = await response.json();
            
            if (data.address) {
                // Chercher le quartier le plus proche dans notre base de données
                const detectedQuartier = findNearestQuartier(lat, lng, quartiers);
                if (detectedQuartier) {
                    setSelectedQuartier(detectedQuartier);
                    onQuartierSelect(detectedQuartier);
                }
            }
        } catch (error) {
            console.error('Erreur détection quartier:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const findNearestQuartier = (lat, lng, quartiers) => {
        // Logique simple pour trouver le quartier le plus proche
        // En production, on utiliserait une vraie logique de géolocalisation
        return quartiers.find(q => (q.nom || q.name) && (q.nom || q.name).toLowerCase().includes('centre')) || quartiers[0];
    };

    const searchQuartiers = async (query) => {
        if (query.length < 2) {
            setSuggestions([]);
            return;
        }

        setIsLoading(true);
        try {
            const filteredQuartiers = quartiers.filter(q => 
            (q.nom || q.name) && (q.nom || q.name).toLowerCase().includes(query.toLowerCase())
            );
            setSuggestions(filteredQuartiers.slice(0, 5));
        } catch (error) {
            console.error('Erreur recherche quartiers:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearchChange = (e) => {
        const query = e.target.value;
        setSearchQuery(query);
        searchQuartiers(query);
    };

    const selectQuartier = (quartier) => {
        setSelectedQuartier(quartier);
        setSearchQuery(quartier.nom || quartier.name);
        setSuggestions([]);
        // Envoyer le format attendu par Register.js
        onQuartierSelect({
            quartier_id: quartier.id,
            quartier_name: quartier.nom || quartier.name,
            commune_name: quartier.commune?.nom || quartier.commune?.name,
            prefecture_name: quartier.commune?.prefecture?.nom || quartier.commune?.prefecture?.name
        });
    };

    const useCurrentLocation = () => {
        if (navigator.geolocation) {
            setIsLoading(true);
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    detectQuartierFromCoordinates(position.coords.latitude, position.coords.longitude);
                },
                (error) => {
                    console.error('Erreur géolocalisation:', error);
                    setIsLoading(false);
                }
            );
        }
    };

    return (
        <div className="space-y-4">
            {/* Titre */}
            <div className="flex items-center space-x-2">
                <MapPin className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-medium text-gray-900">📍 Sélection de votre quartier</h3>
            </div>

            {/* Quartier sélectionné */}
            {selectedQuartier && (
                <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-green-800">
                Quartier sélectionné : {selectedQuartier.nom || selectedQuartier.name}
                            </p>
                            <p className="text-xs text-green-600">
                {selectedQuartier.commune?.nom || selectedQuartier.commune?.name}, {selectedQuartier.commune?.prefecture?.nom || selectedQuartier.commune?.prefecture?.name}
                            </p>
                        </div>
                        <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                            ✅ Sélectionné
                        </span>
                    </div>
                </div>
            )}

            {/* Recherche de quartier */}
            <div className="space-y-3">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <input
                        type="text"
                        value={searchQuery || ''}
                        onChange={handleSearchChange}
                        placeholder="Rechercher votre quartier..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    />
                    {isLoading && (
                        <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 animate-spin" />
                    )}
                </div>

                {/* Suggestions de recherche */}
                {suggestions.length > 0 && (
                    <div className="border border-gray-200 rounded-md max-h-40 overflow-y-auto">
                        {suggestions.map((quartier, index) => (
                            <button
                                key={quartier.id || index}
                                onClick={() => selectQuartier(quartier)}
                                className="w-full text-left px-3 py-2 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                            >
                                                            <div className="font-medium text-sm">{quartier.nom || quartier.name}</div>
                                <div className="text-xs text-gray-500">
                                {quartier.commune?.nom || quartier.commune?.name}, {quartier.commune?.prefecture?.nom || quartier.commune?.prefecture?.name}
                                </div>
                            </button>
                        ))}
                    </div>
                )}

                {/* Quartiers populaires */}
                <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">Quartiers populaires :</p>
                    <div className="grid grid-cols-2 gap-2">
                        {quartiers.slice(0, 6).map((quartier) => (
                            <button
                                key={quartier.id}
                                onClick={() => selectQuartier(quartier)}
                                className="text-left p-2 text-sm border border-gray-200 rounded hover:bg-blue-50 hover:border-blue-300"
                            >
                                <div className="font-medium">{quartier.nom || quartier.name}</div>
                                <div className="text-xs text-gray-500">{quartier.commune?.nom || quartier.commune?.name}</div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Bouton position actuelle */}
                <button
                    onClick={useCurrentLocation}
                    disabled={isLoading}
                    className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                    {isLoading ? (
                        <Loader className="h-4 w-4 animate-spin" />
                    ) : (
                        <MapPin className="h-4 w-4" />
                    )}
                    <span>Utiliser ma position actuelle</span>
                </button>
            </div>

            {/* Informations pour l'utilisateur */}
            <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                <p>💡 Conseil : Sélectionnez votre quartier de résidence pour une meilleure expérience communautaire.</p>
            </div>
        </div>
    );
};

export default QuartierSelector; 
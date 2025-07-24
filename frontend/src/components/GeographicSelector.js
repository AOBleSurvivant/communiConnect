import React, { useState, useEffect } from 'react';
import { MapPin, Search, Loader } from 'lucide-react';

const GeographicSelector = ({ onLocationSelect, userLocation }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedLocation, setSelectedLocation] = useState(null);

    // Quartiers populaires (à adapter selon votre région)
    const popularNeighborhoods = [
        { name: "Centre-ville", city: "Conakry", region: "Kaloum" },
        { name: "Hamdallaye", city: "Conakry", region: "Ratoma" },
        { name: "Almamya", city: "Conakry", region: "Kaloum" },
        { name: "Dixinn", city: "Conakry", region: "Dixinn" },
        { name: "Kankan", city: "Kankan", region: "Kankan" },
        { name: "Kindia", city: "Kindia", region: "Kindia" },
        { name: "N'Zérékoré", city: "N'Zérékoré", region: "N'Zérékoré" }
    ];

    // Détecter automatiquement la position
  useEffect(() => {
        if (userLocation && !selectedLocation) {
            detectAddressFromCoordinates(userLocation.latitude, userLocation.longitude);
        }
    }, [userLocation]);

    const detectAddressFromCoordinates = async (lat, lng) => {
        setIsLoading(true);
        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`);
            const data = await response.json();
            
            if (data.address) {
                const location = {
                    name: data.address.suburb || data.address.neighbourhood || data.address.city || 'Quartier',
                    city: data.address.city || data.address.town || data.address.village || 'Ville',
                    region: data.address.state || data.address.county || 'Région',
                    address: data.display_name,
                    latitude: lat,
                    longitude: lng
                };
                setSelectedLocation(location);
                onLocationSelect(location);
            }
        } catch (error) {
            console.error('Erreur détection adresse:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const searchLocations = async (query) => {
        if (query.length < 3) {
            setSuggestions([]);
            return;
        }

        setIsLoading(true);
        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}&countrycodes=gn&limit=5`);
            const data = await response.json();
            
            const formattedSuggestions = data.map(item => ({
                name: item.display_name.split(',')[0],
                city: item.address?.city || item.address?.town || '',
                region: item.address?.state || '',
                address: item.display_name,
                latitude: parseFloat(item.lat),
                longitude: parseFloat(item.lon)
            }));
            
            setSuggestions(formattedSuggestions);
        } catch (error) {
            console.error('Erreur recherche:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearchChange = (e) => {
        const query = e.target.value;
        setSearchQuery(query);
        searchLocations(query);
    };

    const selectLocation = (location) => {
        setSelectedLocation(location);
        setSearchQuery(location.name);
        setSuggestions([]);
        onLocationSelect(location);
    };

    const useCurrentLocation = () => {
        if (navigator.geolocation) {
            setIsLoading(true);
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    detectAddressFromCoordinates(position.coords.latitude, position.coords.longitude);
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
                <h3 className="text-lg font-medium text-gray-900">📍 Localisation de l'alerte</h3>
      </div>

            {/* Position actuelle automatique */}
            {selectedLocation && (
                <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                    <div className="flex items-center justify-between">
        <div>
                            <p className="text-sm font-medium text-green-800">
                                Position détectée : {selectedLocation.name}
                            </p>
                            <p className="text-xs text-green-600">
                                {selectedLocation.city}, {selectedLocation.region}
                            </p>
                        </div>
                        <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                            ✅ Détecté
                        </span>
          </div>
        </div>
            )}

            {/* Recherche manuelle */}
            <div className="space-y-3">
          <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={handleSearchChange}
                        placeholder="Rechercher un quartier, une ville..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    />
                    {isLoading && (
                        <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 animate-spin" />
                    )}
        </div>

                {/* Suggestions de recherche */}
                {suggestions.length > 0 && (
                    <div className="border border-gray-200 rounded-md max-h-40 overflow-y-auto">
                        {suggestions.map((suggestion, index) => (
                            <button
                                key={index}
                                onClick={() => selectLocation(suggestion)}
                                className="w-full text-left px-3 py-2 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                            >
                                <div className="font-medium text-sm">{suggestion.name}</div>
                                <div className="text-xs text-gray-500">{suggestion.city}, {suggestion.region}</div>
                            </button>
                        ))}
          </div>
                )}

                {/* Quartiers populaires */}
        <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">Quartiers populaires :</p>
                    <div className="grid grid-cols-2 gap-2">
                        {popularNeighborhoods.map((neighborhood, index) => (
                            <button
                                key={index}
                                onClick={() => selectLocation(neighborhood)}
                                className="text-left p-2 text-sm border border-gray-200 rounded hover:bg-blue-50 hover:border-blue-300"
                            >
                                <div className="font-medium">{neighborhood.name}</div>
                                <div className="text-xs text-gray-500">{neighborhood.city}</div>
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
                <p>💡 Conseil : Utilisez "Ma position actuelle" pour une détection automatique, ou recherchez votre quartier.</p>
          </div>
    </div>
  );
};

export default GeographicSelector; 
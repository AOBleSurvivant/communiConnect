import React, { useState, useEffect } from 'react';
import { geographyAPI } from '../services/api';
import { MapPin, ChevronDown } from 'lucide-react';

const GeographicSelector = ({ onSelectionChange, initialValues = {} }) => {
  const [selectedRegion, setSelectedRegion] = useState(initialValues.region_id || '');
  const [selectedPrefecture, setSelectedPrefecture] = useState(initialValues.prefecture_id || '');
  const [selectedCommune, setSelectedCommune] = useState(initialValues.commune_id || '');
  const [selectedQuartier, setSelectedQuartier] = useState(initialValues.quartier_id || '');
  const [geographicData, setGeographicData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Récupérer les données géographiques
  useEffect(() => {
    const fetchGeographicData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await geographyAPI.getGeographicData();
        setGeographicData(data);
      } catch (err) {
        setError('Erreur lors du chargement des données géographiques');
        console.error('Erreur API:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchGeographicData();
  }, []);

  // Filtrer les données basées sur les sélections
  const availablePrefectures = selectedRegion 
    ? geographicData?.regions?.find(r => r.id === parseInt(selectedRegion))?.prefectures || []
    : [];

  const availableCommunes = selectedPrefecture
    ? availablePrefectures.find(p => p.id === parseInt(selectedPrefecture))?.communes || []
    : [];

  const availableQuartiers = selectedCommune
    ? availableCommunes.find(c => c.id === parseInt(selectedCommune))?.quartiers || []
    : [];

  // Réinitialiser les sélections quand un niveau supérieur change
  useEffect(() => {
    if (selectedRegion !== initialValues.region_id) {
      setSelectedPrefecture('');
      setSelectedCommune('');
      setSelectedQuartier('');
    }
  }, [selectedRegion, initialValues.region_id]);

  useEffect(() => {
    if (selectedPrefecture !== initialValues.prefecture_id) {
      setSelectedCommune('');
      setSelectedQuartier('');
    }
  }, [selectedPrefecture, initialValues.prefecture_id]);

  useEffect(() => {
    if (selectedCommune !== initialValues.commune_id) {
      setSelectedQuartier('');
    }
  }, [selectedCommune, initialValues.commune_id]);

  // Notifier le parent des changements de sélection
  useEffect(() => {
    onSelectionChange({
      region_id: selectedRegion,
      prefecture_id: selectedPrefecture,
      commune_id: selectedCommune,
      quartier_id: selectedQuartier,
    });
  }, [selectedRegion, selectedPrefecture, selectedCommune, selectedQuartier, onSelectionChange]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        <span className="ml-2 text-gray-600">Chargement des données géographiques...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="text-red-600 mb-2">⚠️</div>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-2 text-sm text-green-600 hover:text-green-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center mb-4">
        <MapPin className="w-5 h-5 text-green-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">
          Sélectionnez votre localisation
        </h3>
      </div>

      <div className="space-y-4">
        {/* Sélection de la région */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Région <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <select
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              required
            >
              <option value="">Sélectionnez une région</option>
              {geographicData?.regions?.map((region) => (
                <option key={region.id} value={region.id}>
                  {region.nom}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>

        {/* Sélection de la préfecture */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Préfecture <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <select
              value={selectedPrefecture}
              onChange={(e) => setSelectedPrefecture(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              disabled={!selectedRegion}
              required
            >
              <option value="">
                {!selectedRegion ? 'Sélectionnez d\'abord une région' : 'Sélectionnez une préfecture'}
              </option>
              {availablePrefectures.map((prefecture) => (
                <option key={prefecture.id} value={prefecture.id}>
                  {prefecture.nom}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>

        {/* Sélection de la commune */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Commune <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <select
              value={selectedCommune}
              onChange={(e) => setSelectedCommune(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              disabled={!selectedPrefecture}
              required
            >
              <option value="">
                {!selectedPrefecture ? 'Sélectionnez d\'abord une préfecture' : 'Sélectionnez une commune'}
              </option>
              {availableCommunes.map((commune) => (
                <option key={commune.id} value={commune.id}>
                  {commune.nom} ({commune.type})
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>

        {/* Sélection du quartier */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quartier <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <select
              value={selectedQuartier}
              onChange={(e) => setSelectedQuartier(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              disabled={!selectedCommune}
              required
            >
              <option value="">
                {!selectedCommune ? 'Sélectionnez d\'abord une commune' : 'Sélectionnez un quartier'}
              </option>
              {availableQuartiers.map((quartier) => (
                <option key={quartier.id} value={quartier.id}>
                  {quartier.nom}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Affichage de la sélection complète */}
      {selectedQuartier && (
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <div className="flex items-center">
            <MapPin className="w-5 h-5 text-green-600 mr-2" />
            <div>
              <p className="text-sm font-medium text-green-800">
                Localisation sélectionnée :
              </p>
              <p className="text-sm text-green-700">
                {availableQuartiers.find(q => q.id === parseInt(selectedQuartier))?.nom}, {' '}
                {availableCommunes.find(c => c.id === parseInt(selectedCommune))?.nom}, {' '}
                {availablePrefectures.find(p => p.id === parseInt(selectedPrefecture))?.nom}, {' '}
                {geographicData?.regions?.find(r => r.id === parseInt(selectedRegion))?.nom}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GeographicSelector; 
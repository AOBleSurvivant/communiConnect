import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  MapPin, 
  Shield, 
  CheckCircle, 
  AlertCircle, 
  Globe, 
  Clock,
  ArrowRight
} from 'lucide-react';
import toast from 'react-hot-toast';

const GeographicVerification = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [verificationStatus, setVerificationStatus] = useState('pending');
  const [isLoading, setIsLoading] = useState(false);
  const [verificationData, setVerificationData] = useState(null);

  useEffect(() => {
    // Simuler la vérification géographique
    checkGeographicVerification();
  }, []);

  const checkGeographicVerification = async () => {
    setIsLoading(true);
    try {
      // Simulation d'une vérification géographique
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock data - à remplacer par un vrai appel API
      const mockVerificationData = {
        ip_address: '197.149.123.45',
        country_code: 'GN',
        country_name: 'Guinée',
        city: 'Conakry',
        latitude: 9.5370,
        longitude: -13.6785,
        is_guinea: true,
        verification_method: 'ip',
        timestamp: new Date().toISOString()
      };
      
      setVerificationData(mockVerificationData);
      
      if (mockVerificationData.is_guinea) {
        setVerificationStatus('success');
        toast.success('Vérification géographique réussie !');
      } else {
        setVerificationStatus('failed');
        toast.error('Accès refusé : Vous devez être en Guinée');
      }
    } catch (error) {
      setVerificationStatus('error');
      toast.error('Erreur lors de la vérification géographique');
    } finally {
      setIsLoading(false);
    }
  };

  const handleManualVerification = () => {
    toast('Vérification manuelle en cours de développement');
  };

  const handleContinue = () => {
    navigate('/dashboard');
  };

  const getStatusIcon = () => {
    switch (verificationStatus) {
      case 'success':
        return <CheckCircle className="w-12 h-12 text-green-600" />;
      case 'failed':
        return <AlertCircle className="w-12 h-12 text-red-600" />;
      case 'error':
        return <AlertCircle className="w-12 h-12 text-yellow-600" />;
      default:
        return <Clock className="w-12 h-12 text-blue-600 animate-pulse" />;
    }
  };

  const getStatusMessage = () => {
    switch (verificationStatus) {
      case 'success':
        return {
          title: 'Vérification réussie !',
          message: 'Votre localisation a été confirmée. Vous pouvez maintenant accéder à votre communauté.',
          color: 'text-green-600'
        };
      case 'failed':
        return {
          title: 'Accès refusé',
          message: 'Vous devez être en Guinée pour accéder à CommuniConnect.',
          color: 'text-red-600'
        };
      case 'error':
        return {
          title: 'Erreur de vérification',
          message: 'Une erreur est survenue lors de la vérification. Veuillez réessayer.',
          color: 'text-yellow-600'
        };
      default:
        return {
          title: 'Vérification en cours...',
          message: 'Nous vérifions votre localisation géographique.',
          color: 'text-blue-600'
        };
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-lg shadow-xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              {getStatusIcon()}
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Vérification Géographique
            </h1>
            <p className="text-gray-600">
              Confirmation de votre localisation pour CommuniConnect
            </p>
          </div>

          {/* Status Message */}
          <div className={`text-center mb-8 ${getStatusMessage().color}`}>
            <h2 className="text-xl font-semibold mb-2">
              {getStatusMessage().title}
            </h2>
            <p className="text-gray-700">
              {getStatusMessage().message}
            </p>
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Vérification en cours...</p>
            </div>
          )}

          {/* Verification Data */}
          {verificationData && verificationStatus === 'success' && (
            <div className="bg-green-50 rounded-lg p-6 mb-6">
              <h3 className="font-semibold text-green-800 mb-4 flex items-center">
                <Shield className="w-5 h-5 mr-2" />
                Informations de vérification
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Pays :</span>
                  <span className="ml-2 text-gray-600">{verificationData.country_name}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Ville :</span>
                  <span className="ml-2 text-gray-600">{verificationData.city}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Adresse IP :</span>
                  <span className="ml-2 text-gray-600">{verificationData.ip_address}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Méthode :</span>
                  <span className="ml-2 text-gray-600">
                    {verificationData.verification_method === 'ip' ? 'Géolocalisation IP' : 'Sélection manuelle'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* User Location Info */}
          {user?.location_info && (
            <div className="bg-blue-50 rounded-lg p-6 mb-6">
              <h3 className="font-semibold text-blue-800 mb-4 flex items-center">
                <MapPin className="w-5 h-5 mr-2" />
                Votre localisation enregistrée
              </h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Quartier :</span>
                  <span className="ml-2 text-gray-600">{user.location_info.quartier}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Commune :</span>
                  <span className="ml-2 text-gray-600">{user.location_info.commune}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Préfecture :</span>
                  <span className="ml-2 text-gray-600">{user.location_info.prefecture}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Région :</span>
                  <span className="ml-2 text-gray-600">{user.location_info.region}</span>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            {verificationStatus === 'success' ? (
              <button
                onClick={handleContinue}
                className="flex-1 bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors duration-200 flex items-center justify-center"
              >
                Continuer vers le tableau de bord
                <ArrowRight className="w-4 h-4 ml-2" />
              </button>
            ) : verificationStatus === 'failed' ? (
              <div className="w-full text-center">
                <p className="text-red-600 mb-4">
                  CommuniConnect est réservé aux habitants de Guinée
                </p>
                <button
                  onClick={handleManualVerification}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
                >
                  Vérification manuelle
                </button>
              </div>
            ) : verificationStatus === 'error' ? (
              <div className="w-full text-center space-y-4">
                <button
                  onClick={checkGeographicVerification}
                  className="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors duration-200"
                >
                  Réessayer
                </button>
                <button
                  onClick={handleManualVerification}
                  className="block w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
                >
                  Vérification manuelle
                </button>
              </div>
            ) : null}
          </div>

          {/* Information Box */}
          <div className="mt-8 bg-gray-50 rounded-lg p-4">
            <div className="flex items-start">
              <Globe className="w-5 h-5 text-gray-500 mr-3 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900 mb-2">
                  Pourquoi cette vérification ?
                </h4>
                <p className="text-sm text-gray-600">
                  CommuniConnect est une plateforme communautaire locale réservée aux habitants de Guinée. 
                  Cette vérification garantit que seuls les résidents locaux peuvent accéder à la plateforme 
                  et participer à leur communauté de quartier.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeographicVerification; 
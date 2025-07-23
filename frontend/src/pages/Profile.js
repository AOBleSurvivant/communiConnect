import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  User, 
  MapPin, 
  Mail, 
  Phone, 
  Calendar, 
  Edit, 
  Save, 
  X,
  Camera,
  Shield
} from 'lucide-react';
import toast from 'react-hot-toast';

const Profile = () => {
  const { user, updateProfile, uploadProfilePicture, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploadingPicture, setIsUploadingPicture] = useState(false);
  const [showPictureModal, setShowPictureModal] = useState(false);
  
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone_number: user?.phone_number || '',
    bio: user?.bio || '',
    date_of_birth: user?.date_of_birth ? new Date(user.date_of_birth).toISOString().split('T')[0] : ''
  });
  
  // Vérifier si l'utilisateur est connecté
  useEffect(() => {
    if (!isAuthenticated) {
      toast.error('Vous devez être connecté pour accéder à votre profil');
      navigate('/login');
      return;
    }
  }, [isAuthenticated, navigate]);

  // Si l'utilisateur n'est pas connecté, ne pas afficher le composant
  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      await updateProfile(formData);
      setIsEditing(false);
    } catch (error) {
      console.error('Erreur lors de la mise à jour du profil:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
      phone_number: user?.phone_number || '',
      bio: user?.bio || '',
      date_of_birth: user?.date_of_birth ? new Date(user.date_of_birth).toISOString().split('T')[0] : ''
    });
    setIsEditing(false);
  };

  // Fonctions pour l'upload de photo de profil
  const handlePictureUpload = () => {
    setShowPictureModal(true);
  };

  const handlePictureSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validation du fichier
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      toast.error('Type de fichier non supporté. Utilisez JPEG, PNG, GIF ou WebP.');
      return;
    }

    if (file.size > maxSize) {
      toast.error('Fichier trop volumineux. Taille maximale : 5MB.');
      return;
    }

    setIsUploadingPicture(true);
    try {
      const formData = new FormData();
      formData.append('profile_picture', file);

      // Utiliser la fonction du contexte d'authentification pour l'upload
      await uploadProfilePicture(formData);
      
      setShowPictureModal(false);
      toast.success('Photo de profil mise à jour avec succès !');
    } catch (error) {
      console.error('Erreur lors de l\'upload de la photo:', error);
      toast.error('Erreur lors de l\'upload de la photo de profil');
    } finally {
      setIsUploadingPicture(false);
    }
  };

  const handlePictureCancel = () => {
    setShowPictureModal(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Mon Profil</h1>
            <div className="flex space-x-3">
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
                >
                  <Edit className="w-4 h-4 mr-2" />
                  Modifier
                </button>
              ) : (
                <>
                  <button
                    onClick={handleCancel}
                    className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Annuler
                  </button>
                  <button
                    onClick={handleSave}
                    disabled={isLoading}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors duration-200"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Sauvegarde...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4 mr-2" />
                        Sauvegarder
                      </>
                    )}
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Profile Picture */}
          <div className="flex items-center space-x-6 mb-8">
            <div className="relative">
              <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center">
                {user?.profile_picture ? (
                  <img 
                    src={user.profile_picture} 
                    alt="Profil" 
                    className="w-24 h-24 rounded-full object-cover"
                  />
                ) : (
                  <User className="w-12 h-12 text-gray-400" />
                )}
              </div>
              {isEditing && (
                <button 
                  onClick={handlePictureUpload}
                  className="absolute bottom-0 right-0 bg-green-600 text-white p-2 rounded-full hover:bg-green-700 transition-colors duration-200"
                >
                  <Camera className="w-4 h-4" />
                </button>
              )}
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {user?.full_name || user?.username}
              </h2>
              <p className="text-gray-600">
                Membre depuis {user?.date_joined ? new Date(user.date_joined).toLocaleDateString('fr-FR') : 'récemment'}
              </p>
              <div className="flex items-center mt-2 text-sm text-gray-500">
                <MapPin className="w-4 h-4 mr-1" />
                {user?.location_info?.full_address}
              </div>
            </div>
          </div>
        </div>

        {/* Profile Information */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Informations personnelles</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* First Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prénom
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
              ) : (
                <p className="text-gray-900">{user?.first_name || 'Non renseigné'}</p>
              )}
            </div>

            {/* Last Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nom
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
              ) : (
                <p className="text-gray-900">{user?.last_name || 'Non renseigné'}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Mail className="w-4 h-4 inline mr-1" />
                Email
              </label>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
              ) : (
                <p className="text-gray-900">{user?.email}</p>
              )}
            </div>

            {/* Phone */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Phone className="w-4 h-4 inline mr-1" />
                Téléphone
              </label>
              {isEditing ? (
                <input
                  type="tel"
                  name="phone_number"
                  value={formData.phone_number}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder="+224 123 456 789"
                />
              ) : (
                <p className="text-gray-900">{user?.phone_number || 'Non renseigné'}</p>
              )}
            </div>

            {/* Date of Birth */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-1" />
                Date de naissance
              </label>
              {isEditing ? (
                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
              ) : (
                <p className="text-gray-900">
                  {user?.date_of_birth ? new Date(user.date_of_birth).toLocaleDateString('fr-FR') : 'Non renseigné'}
                </p>
              )}
            </div>

            {/* Role */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Shield className="w-4 h-4 inline mr-1" />
                Rôle
              </label>
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                user?.role === 'admin' ? 'bg-red-100 text-red-800' :
                user?.role === 'ambassador' ? 'bg-blue-100 text-blue-800' :
                'bg-green-100 text-green-800'
              }`}>
                {user?.role === 'admin' ? 'Administrateur' :
                 user?.role === 'ambassador' ? 'Ambassadeur' : 'Utilisateur'}
              </span>
            </div>
          </div>

          {/* Bio */}
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Bio
            </label>
            {isEditing ? (
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Parlez-nous un peu de vous..."
              />
            ) : (
              <p className="text-gray-900">{user?.bio || 'Aucune bio renseignée'}</p>
            )}
          </div>
        </div>

        {/* Location Information */}
        <div className="bg-white rounded-lg shadow-sm p-6 mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Localisation</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Région</label>
              <p className="text-gray-900">{user?.location_info?.region}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Préfecture</label>
              <p className="text-gray-900">{user?.location_info?.prefecture}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Commune</label>
              <p className="text-gray-900">{user?.location_info?.commune}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Quartier</label>
              <p className="text-gray-900">{user?.location_info?.quartier}</p>
            </div>
          </div>

          <div className="mt-4 p-4 bg-green-50 rounded-lg">
            <div className="flex items-center">
              <Shield className="w-5 h-5 text-green-600 mr-2" />
              <span className="text-sm text-green-800">
                Votre localisation a été vérifiée et confirmée
              </span>
            </div>
          </div>
        </div>

        {/* Account Settings */}
        <div className="bg-white rounded-lg shadow-sm p-6 mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Paramètres du compte</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-gray-900">Notifications</h4>
                <p className="text-sm text-gray-600">Recevoir les notifications par email</p>
              </div>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700 transition-colors duration-200">
                Configurer
              </button>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-gray-900">Confidentialité</h4>
                <p className="text-sm text-gray-600">Gérer la visibilité de votre profil</p>
              </div>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700 transition-colors duration-200">
                Configurer
              </button>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-gray-900">Sécurité</h4>
                <p className="text-sm text-gray-600">Changer votre mot de passe</p>
              </div>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700 transition-colors duration-200">
                Modifier
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal d'upload de photo de profil */}
      {showPictureModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Changer la photo de profil
              </h3>
              <button
                onClick={handlePictureCancel}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Informations */}
              <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
                <p className="text-sm text-blue-700">
                  Formats supportés : JPEG, PNG, GIF, WebP
                </p>
                <p className="text-sm text-blue-600 mt-1">
                  Taille maximale : 5MB
                </p>
              </div>
              
              {/* Zone de sélection de fichier */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handlePictureSelect}
                  className="hidden"
                  id="profile-picture-input"
                  disabled={isUploadingPicture}
                />
                <label
                  htmlFor="profile-picture-input"
                  className={`cursor-pointer flex flex-col items-center space-y-2 ${
                    isUploadingPicture ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  <Camera className="w-8 h-8 text-gray-400" />
                  <p className="text-sm text-gray-600">
                    {isUploadingPicture ? 'Upload en cours...' : 'Cliquez pour sélectionner une image'}
                  </p>
                  <p className="text-xs text-gray-400">
                    ou glissez-déposez votre fichier ici
                  </p>
                </label>
              </div>
              
              {/* Boutons */}
              <div className="flex space-x-3 pt-4">
                <button
                  onClick={handlePictureCancel}
                  disabled={isUploadingPicture}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  Annuler
                </button>
                <button
                  onClick={() => document.getElementById('profile-picture-input').click()}
                  disabled={isUploadingPicture}
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isUploadingPicture ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Upload...
                    </span>
                  ) : (
                    'Sélectionner'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile; 
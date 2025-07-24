import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import QuartierSelector from '../components/QuartierSelector';
import { Eye, EyeOff, User, Mail, Phone, Lock, MapPin, Shield } from 'lucide-react';

const Register = () => {
  const { register: registerUser, loading: registerLoading } = useAuth();
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [geographicSelection, setGeographicSelection] = useState({});

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const password = watch('password');

  const onSubmit = async (data) => {
    console.log('Geographic selection:', geographicSelection);
    console.log('Quartier ID:', geographicSelection.quartier_id);
    console.log('Type of quartier_id:', typeof geographicSelection.quartier_id);
    
    if (!geographicSelection.quartier_id) {
      alert('Veuillez sélectionner votre quartier de résidence.');
      return;
    }

    try {
      const userData = {
        ...data,
        quartier: parseInt(geographicSelection.quartier_id), // Changé de quartier_id à quartier
      };

      console.log('User data to send:', userData);
      await registerUser(userData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="flex items-center">
            <MapPin className="w-8 h-8 text-guinea-600 mr-2" />
            <h1 className="text-3xl font-bold text-gray-900">CommuniConnect</h1>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Créez votre compte
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Rejoignez la communauté locale de votre quartier
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Informations personnelles */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                Informations personnelles
              </h3>

              {/* Nom d'utilisateur */}
              <div>
                <label className="form-label">
                  Nom d'utilisateur <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    {...register('username', {
                      required: 'Le nom d\'utilisateur est requis',
                      minLength: {
                        value: 3,
                        message: 'Le nom d\'utilisateur doit contenir au moins 3 caractères',
                      },
                    })}
                    className="form-input pl-10"
                    placeholder="Votre nom d'utilisateur"
                  />
                </div>
                {errors.username && (
                  <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
                )}
              </div>

              {/* Prénom et nom */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">
                    Prénom <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    {...register('first_name', {
                      required: 'Le prénom est requis',
                    })}
                    className="form-input"
                    placeholder="Votre prénom"
                  />
                  {errors.first_name && (
                    <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
                  )}
                </div>

                <div>
                  <label className="form-label">
                    Nom <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    {...register('last_name', {
                      required: 'Le nom est requis',
                    })}
                    className="form-input"
                    placeholder="Votre nom"
                  />
                  {errors.last_name && (
                    <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
                  )}
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="form-label">
                  Adresse email <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="email"
                    {...register('email', {
                      required: 'L\'email est requis',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Adresse email invalide',
                      },
                    })}
                    className="form-input pl-10"
                    placeholder="votre.email@exemple.com"
                  />
                </div>
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                )}
              </div>

              {/* Téléphone */}
              <div>
                <label className="form-label">
                  Numéro de téléphone
                </label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="tel"
                    {...register('phone_number', {
                      pattern: {
                        value: /^\+?[1-9]\d{1,14}$/,
                        message: 'Numéro de téléphone invalide',
                      },
                    })}
                    className="form-input pl-10"
                    placeholder="+224 123 456 789"
                  />
                </div>
                {errors.phone_number && (
                  <p className="mt-1 text-sm text-red-600">{errors.phone_number.message}</p>
                )}
              </div>

              {/* Mot de passe */}
              <div>
                <label className="form-label">
                  Mot de passe <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    {...register('password', {
                      required: 'Le mot de passe est requis',
                      minLength: {
                        value: 8,
                        message: 'Le mot de passe doit contenir au moins 8 caractères',
                      },
                    })}
                    className="form-input pl-10 pr-10"
                    placeholder="Votre mot de passe"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
                )}
              </div>

              {/* Confirmation du mot de passe */}
              <div>
                <label className="form-label">
                  Confirmer le mot de passe <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    {...register('password_confirm', {
                      required: 'La confirmation du mot de passe est requise',
                      validate: (value) =>
                        value === password || 'Les mots de passe ne correspondent pas',
                    })}
                    className="form-input pl-10 pr-10"
                    placeholder="Confirmez votre mot de passe"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password_confirm && (
                  <p className="mt-1 text-sm text-red-600">{errors.password_confirm.message}</p>
                )}
              </div>
            </div>

            {/* Sélection géographique */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                Localisation en Guinée
              </h3>
              
              <QuartierSelector onQuartierSelect={setGeographicSelection} />
            </div>

            {/* Conditions d'utilisation */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                Conditions d'utilisation
              </h3>

              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                <div className="flex items-start">
                  <Shield className="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
                  <div className="text-sm text-yellow-800">
                    <p className="font-medium mb-2">Restrictions géographiques :</p>
                    <ul className="list-disc list-inside space-y-1">
                      <li>CommuniConnect est réservé aux résidents de la Guinée</li>
                      <li>Votre localisation sera vérifiée lors de l'inscription</li>
                      <li>L'accès peut être refusé si vous résidez hors de la Guinée</li>
                      <li>Vos données personnelles sont protégées et ne seront pas partagées</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <input
                  type="checkbox"
                  {...register('accept_terms', {
                    required: 'Vous devez accepter les conditions d\'utilisation',
                  })}
                  className="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">
                  J'accepte les{' '}
                  <Link to="/terms" className="text-primary-600 hover:text-primary-500">
                    conditions d'utilisation
                  </Link>{' '}
                  et la{' '}
                  <Link to="/privacy" className="text-primary-600 hover:text-primary-500">
                    politique de confidentialité
                  </Link>
                  <span className="text-red-500">*</span>
                </label>
              </div>
              {errors.accept_terms && (
                <p className="mt-1 text-sm text-red-600">{errors.accept_terms.message}</p>
              )}
            </div>

            {/* Bouton d'inscription */}
            <div>
              <button
                type="submit"
                disabled={registerLoading || !geographicSelection.quartier_id}
                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {registerLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="spinner mr-2"></div>
                    Création du compte...
                  </div>
                ) : (
                  'Créer mon compte'
                )}
              </button>
            </div>

            {/* Lien vers la connexion */}
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Déjà inscrit ?{' '}
                <Link to="/login" className="text-primary-600 hover:text-primary-500 font-medium">
                  Connectez-vous
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register; 
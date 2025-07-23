import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, userAPI } from '../services/api';
import { tokenService, userService, handleAPIError } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Vérifier l'authentification au chargement
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        const user = JSON.parse(userData);
        setUser(user);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Erreur parsing user data:', error);
        // Nettoyer les données corrompues
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []); // Dépendances vides car on ne veut exécuter qu'au montage


  const register = async (userData) => {
    try {
      setLoading(true);
      
      const response = await authAPI.register(userData);
      
      // Sauvegarder les tokens et les données utilisateur
      tokenService.saveTokens(response.tokens);
      userService.saveUser(response.user);
      
      setUser(response.user);
      setIsAuthenticated(true);
      
      toast.success(response.message || 'Inscription réussie !');
      
      return response;
    } catch (error) {
      const errorInfo = handleAPIError(error);
      
      if (errorInfo.type === 'geographic') {
        toast.error('Accès refusé. CommuniConnect est réservé aux habitants de Guinée.');
      } else if (errorInfo.type === 'validation') {
        // Afficher les erreurs de validation spécifiques
        if (errorInfo.details) {
          Object.keys(errorInfo.details).forEach(field => {
            if (Array.isArray(errorInfo.details[field])) {
              toast.error(errorInfo.details[field][0]);
            } else {
              toast.error(errorInfo.details[field]);
            }
          });
        } else {
          toast.error(errorInfo.message);
        }
      } else {
        toast.error(errorInfo.message);
      }
      
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      setLoading(true);
      
      const response = await authAPI.login(email, password);
      
      // La réponse de l'API contient directement user et tokens
      const { user, tokens, message } = response;
      
      // Sauvegarder les tokens et les données utilisateur
      tokenService.saveTokens(tokens);
      userService.saveUser(user);
      
      setUser(user);
      setIsAuthenticated(true);
      
      toast.success(message || 'Connexion réussie !');
      
      return response;
    } catch (error) {
      const errorInfo = handleAPIError(error);
      
      if (errorInfo.type === 'geographic') {
        toast.error('Accès refusé. Vous devez être en Guinée pour vous connecter.');
      } else if (errorInfo.type === 'auth') {
        toast.error('Email ou mot de passe incorrect.');
      } else {
        toast.error(errorInfo.message);
      }
      
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Appeler l'API de déconnexion si l'utilisateur est connecté
      if (isAuthenticated) {
        await authAPI.logout();
      }
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      // Nettoyer les données locales
      tokenService.clearTokens();
      userService.clearUser();
      
      setUser(null);
      setIsAuthenticated(false);
      
      toast.success('Déconnexion réussie');
    }
  };

  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      
      const response = await userAPI.updateProfile(profileData);
      
      // Mettre à jour les données utilisateur
      userService.saveUser(response.user || response);
      setUser(response.user || response);
      
      toast.success('Profil mis à jour avec succès !');
      
      return response;
    } catch (error) {
      const errorInfo = handleAPIError(error);
      
      // Si l'erreur est 401, déconnecter l'utilisateur
      if (error.response?.status === 401) {
        logout();
        toast.error('Session expirée. Veuillez vous reconnecter.');
      } else {
        toast.error(errorInfo.message);
      }
      
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const uploadProfilePicture = async (formData) => {
    try {
      setLoading(true);
      
      const response = await userAPI.uploadProfilePicture(formData);
      
      // Mettre à jour les données utilisateur avec la réponse de l'upload
      if (response.user) {
        userService.saveUser(response.user);
        setUser(response.user);
      }
      
      toast.success('Photo de profil mise à jour avec succès !');
      
      return response;
    } catch (error) {
      const errorInfo = handleAPIError(error);
      
      // Si l'erreur est 401, déconnecter l'utilisateur
      if (error.response?.status === 401) {
        logout();
        toast.error('Session expirée. Veuillez vous reconnecter.');
      } else {
        toast.error(errorInfo.message);
      }
      
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const refreshUserData = async () => {
    try {
      const response = await authAPI.getProfile();
      userService.saveUser(response);
      setUser(response);
      return response;
    } catch (error) {
      console.error('Erreur lors du rafraîchissement des données utilisateur:', error);
      // Si l'erreur est 401, déconnecter l'utilisateur
      if (error.response?.status === 401) {
        logout();
      }
      throw error;
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    register,
    login,
    logout,
    updateProfile,
    uploadProfilePicture,
    refreshUserData,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 
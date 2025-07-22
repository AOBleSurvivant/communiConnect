import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const TestNewUser = () => {
  const { register, login, isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [testResults, setTestResults] = useState([]);

  const addResult = (message, type = 'info') => {
    setTestResults(prev => [...prev, { message, type, timestamp: new Date().toISOString() }]);
  };

  const clearResults = () => {
    setTestResults([]);
  };

  const testNewUserFlow = async () => {
    clearResults();
    setIsLoading(true);
    
    try {
      // Générer des données uniques
      const timestamp = Date.now();
      const testEmail = `testuser${timestamp}@example.com`;
      const testUsername = `testuser${timestamp}`;
      
      addResult(`🧪 Début du test avec email: ${testEmail}`, 'info');
      
      // 1. Test d'inscription
      addResult('📝 Étape 1: Inscription...', 'info');
      
      const userData = {
        username: testUsername,
        email: testEmail,
        password: 'testpass123',
        password_confirm: 'testpass123',
        first_name: 'Test',
        last_name: 'Utilisateur',
        phone_number: '+224123456789',
        quartier: 676, // Quartier par défaut
        bio: 'Utilisateur de test pour vérifier l\'upload de photos'
      };
      
      await register(userData);
      addResult('✅ Inscription réussie', 'success');
      
      // 2. Test de connexion
      addResult('🔐 Étape 2: Connexion...', 'info');
      await login(testEmail, 'testpass123');
      addResult('✅ Connexion réussie', 'success');
      
      // 3. Vérifier l'état d'authentification
      addResult('🔍 Étape 3: Vérification de l\'authentification...', 'info');
      
      const token = localStorage.getItem('access_token');
      const storedUserData = localStorage.getItem('user');
      
      if (token && storedUserData) {
        addResult('✅ Token et données utilisateur présents', 'success');
        addResult(`📊 Token length: ${token.length}`, 'info');
      } else {
        addResult('❌ Token ou données utilisateur manquants', 'error');
      }
      
      // 4. Test de l'API profile
      addResult('🌐 Étape 4: Test de l\'API profile...', 'info');
      
      const response = await fetch('http://localhost:8000/api/users/my-profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        addResult('✅ API profile accessible', 'success');
        addResult(`👤 Utilisateur: ${data.first_name} ${data.last_name}`, 'info');
      } else {
        addResult(`❌ Erreur API profile: ${response.status}`, 'error');
      }
      
      // 5. Redirection vers le profil
      addResult('🎯 Étape 5: Redirection vers le profil...', 'info');
      addResult('✅ Test terminé avec succès !', 'success');
      addResult('📝 Vous pouvez maintenant tester l\'upload de photo sur la page de profil', 'info');
      
      // Rediriger vers le profil après un délai
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
      
    } catch (error) {
      addResult(`❌ Erreur lors du test: ${error.message}`, 'error');
      console.error('Erreur test:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const testExistingUser = async () => {
    clearResults();
    setIsLoading(true);
    
    try {
      addResult('🔐 Test avec utilisateur existant...', 'info');
      
      await login('testuser@example.com', 'testpass123');
      addResult('✅ Connexion réussie avec utilisateur existant', 'success');
      
      const token = localStorage.getItem('access_token');
      if (token) {
        addResult('✅ Token présent', 'success');
      } else {
        addResult('❌ Token manquant', 'error');
      }
      
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
      
    } catch (error) {
      addResult(`❌ Erreur: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const checkAuthStatus = () => {
    clearResults();
    
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    const refreshToken = localStorage.getItem('refresh_token');
    
    addResult('🔍 Vérification de l\'état d\'authentification...', 'info');
    addResult(`Token présent: ${token ? '✅' : '❌'}`, token ? 'success' : 'error');
    addResult(`Refresh token présent: ${refreshToken ? '✅' : '❌'}`, refreshToken ? 'success' : 'error');
    addResult(`Données utilisateur présentes: ${userData ? '✅' : '❌'}`, userData ? 'success' : 'error');
    addResult(`État isAuthenticated: ${isAuthenticated ? '✅' : '❌'}`, isAuthenticated ? 'success' : 'error');
    
    if (user) {
      addResult(`Utilisateur connecté: ${user.first_name} ${user.last_name}`, 'success');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            🧪 Test Utilisateur Nouveau
          </h1>
          
          <div className="mb-6">
            <p className="text-gray-600 mb-4">
              Ce composant permet de tester le processus complet d'inscription et de connexion 
              pour un nouvel utilisateur, puis de vérifier que l'upload de photo fonctionne.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <button
              onClick={testNewUserFlow}
              disabled={isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              {isLoading ? '⏳ Test en cours...' : '🧪 Test Nouvel Utilisateur'}
            </button>
            
            <button
              onClick={testExistingUser}
              disabled={isLoading}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              {isLoading ? '⏳ Test en cours...' : '🔐 Test Utilisateur Existant'}
            </button>
            
            <button
              onClick={checkAuthStatus}
              className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              🔍 Vérifier État Auth
            </button>
          </div>
          
          <div className="mb-4">
            <button
              onClick={clearResults}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              🗑️ Effacer les résultats
            </button>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <h3 className="font-semibold text-gray-900 mb-3">📊 Résultats des Tests</h3>
            
            {testResults.length === 0 ? (
              <p className="text-gray-500">Aucun test exécuté. Cliquez sur un bouton pour commencer.</p>
            ) : (
              <div className="space-y-2">
                {testResults.map((result, index) => (
                  <div
                    key={index}
                    className={`p-2 rounded text-sm ${
                      result.type === 'success' ? 'bg-green-100 text-green-800' :
                      result.type === 'error' ? 'bg-red-100 text-red-800' :
                      'bg-blue-100 text-blue-800'
                    }`}
                  >
                    <span className="font-mono text-xs text-gray-500">
                      {new Date(result.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="ml-2">{result.message}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <h4 className="font-semibold text-yellow-800 mb-2">💡 Instructions</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• <strong>Test Nouvel Utilisateur</strong> : Crée un compte et teste l'authentification</li>
              <li>• <strong>Test Utilisateur Existant</strong> : Se connecte avec un utilisateur de test</li>
              <li>• <strong>Vérifier État Auth</strong> : Affiche l'état actuel de l'authentification</li>
              <li>• Après un test réussi, vous serez redirigé vers la page de profil</li>
              <li>• Testez ensuite l'upload de photo sur la page de profil</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestNewUser; 
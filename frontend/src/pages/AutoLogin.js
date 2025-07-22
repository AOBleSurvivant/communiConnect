import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AutoLogin = () => {
  const [status, setStatus] = useState('Connexion en cours...');
  const navigate = useNavigate();

  useEffect(() => {
    const autoLogin = async () => {
      try {
        setStatus('Tentative de connexion...');
        
        const response = await fetch('http://localhost:8000/api/users/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: 'testuser@example.com',
            password: 'testpass123'
          })
        });

        if (response.ok) {
          const data = await response.json();
          
          // Sauvegarder les données
          localStorage.setItem('access_token', data.tokens.access);
          localStorage.setItem('refresh_token', data.tokens.refresh);
          localStorage.setItem('user', JSON.stringify(data.user));
          
          setStatus('✅ Connexion réussie ! Redirection...');
          
          // Rediriger vers le profil après 2 secondes
          setTimeout(() => {
            navigate('/profile');
          }, 2000);
          
        } else {
          const errorData = await response.json();
          setStatus(`❌ Erreur: ${JSON.stringify(errorData)}`);
        }
        
      } catch (error) {
        setStatus(`❌ Erreur réseau: ${error.message}`);
      }
    };

    autoLogin();
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h1 className="text-2xl font-bold text-center mb-6">
          🔐 Connexion Automatique
        </h1>
        
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{status}</p>
        </div>
        
        <div className="mt-6 text-sm text-gray-500">
          <p><strong>Email:</strong> testuser@example.com</p>
          <p><strong>Mot de passe:</strong> testpass123</p>
        </div>
      </div>
    </div>
  );
};

export default AutoLogin; 
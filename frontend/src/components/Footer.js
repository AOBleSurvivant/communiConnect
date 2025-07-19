import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Mail, Phone, Shield, Heart } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center mb-4">
              <h3 className="text-2xl font-bold">
                Communi<span className="text-green-400">Connect</span>
              </h3>
            </div>
            <p className="text-gray-300 mb-6 max-w-md">
              La plateforme communautaire qui connecte les Guinéens dans leurs quartiers. 
              Entraide, partage et solidarité locale.
            </p>
            <div className="flex items-center text-sm text-gray-400">
              <MapPin className="w-4 h-4 mr-2" />
              <span>République de Guinée</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Liens rapides</h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  to="/" 
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Accueil
                </Link>
              </li>
              <li>
                <Link 
                  to="/register" 
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  S'inscrire
                </Link>
              </li>
              <li>
                <Link 
                  to="/login" 
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Se connecter
                </Link>
              </li>
              <li>
                <Link 
                  to="/dashboard" 
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Tableau de bord
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact</h4>
            <ul className="space-y-3">
              <li className="flex items-center text-gray-300">
                <Mail className="w-4 h-4 mr-2" />
                <a 
                  href="mailto:contact@communiconnect.gn" 
                  className="hover:text-white transition-colors duration-200"
                >
                  contact@communiconnect.gn
                </a>
              </li>
              <li className="flex items-center text-gray-300">
                <Phone className="w-4 h-4 mr-2" />
                <a 
                  href="tel:+224123456789" 
                  className="hover:text-white transition-colors duration-200"
                >
                  +224 123 456 789
                </a>
              </li>
              <li className="flex items-center text-gray-300">
                <MapPin className="w-4 h-4 mr-2" />
                <span>Conakry, Guinée</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center text-sm text-gray-400 mb-4 md:mb-0">
              <Shield className="w-4 h-4 mr-2" />
              <span>Accès sécurisé et vérifié géographiquement</span>
            </div>
            
            <div className="flex items-center text-sm text-gray-400">
              <Heart className="w-4 h-4 mr-2 text-red-400" />
              <span>
                Fait avec amour pour la communauté guinéenne
              </span>
            </div>
          </div>
          
          <div className="flex flex-col md:flex-row justify-between items-center mt-4">
            <p className="text-sm text-gray-400">
              © {currentYear} CommuniConnect. Tous droits réservés.
            </p>
            
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link 
                to="/privacy" 
                className="text-sm text-gray-400 hover:text-white transition-colors duration-200"
              >
                Confidentialité
              </Link>
              <Link 
                to="/terms" 
                className="text-sm text-gray-400 hover:text-white transition-colors duration-200"
              >
                Conditions d'utilisation
              </Link>
              <Link 
                to="/about" 
                className="text-sm text-gray-400 hover:text-white transition-colors duration-200"
              >
                À propos
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
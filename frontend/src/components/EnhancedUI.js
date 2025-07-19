import React, { useState, useEffect } from 'react';
import { 
  Bell, 
  Search, 
  Filter, 
  Grid, 
  List, 
  Settings, 
  Moon, 
  Sun,
  Eye,
  EyeOff,
  Volume2,
  VolumeX,
  Smartphone,
  Monitor,
  Tablet
} from 'lucide-react';

const EnhancedUI = ({ children, onViewChange, onThemeChange, onNotificationChange }) => {
  const [viewMode, setViewMode] = useState('list'); // 'list' ou 'grid'
  const [theme, setTheme] = useState('light'); // 'light' ou 'dark'
  const [notifications, setNotifications] = useState(true);
  const [sound, setSound] = useState(true);
  const [deviceType, setDeviceType] = useState('desktop');

  // Détection automatique du type d'appareil
  useEffect(() => {
    const detectDevice = () => {
      const width = window.innerWidth;
      if (width < 768) {
        setDeviceType('mobile');
      } else if (width < 1024) {
        setDeviceType('tablet');
      } else {
        setDeviceType('desktop');
      }
    };

    detectDevice();
    window.addEventListener('resize', detectDevice);
    return () => window.removeEventListener('resize', detectDevice);
  }, []);

  // Gestion du thème
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark');
    onThemeChange?.(newTheme);
  };

  // Gestion des notifications
  const toggleNotifications = () => {
    setNotifications(!notifications);
    onNotificationChange?.(!notifications);
  };

  // Gestion du son
  const toggleSound = () => {
    setSound(!sound);
  };

  // Gestion du mode d'affichage
  const toggleViewMode = () => {
    const newMode = viewMode === 'list' ? 'grid' : 'list';
    setViewMode(newMode);
    onViewChange?.(newMode);
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'
    }`}>
      {/* Barre d'outils améliorée */}
      <div className={`sticky top-0 z-50 border-b ${
        theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo et titre */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">CC</span>
                </div>
                <span className={`font-bold text-lg ${
                  theme === 'dark' ? 'text-white' : 'text-gray-900'
                }`}>
                  CommuniConnect
                </span>
              </div>
              
              {/* Indicateur de type d'appareil */}
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                {deviceType === 'mobile' && <Smartphone className="w-3 h-3" />}
                {deviceType === 'tablet' && <Tablet className="w-3 h-3" />}
                {deviceType === 'desktop' && <Monitor className="w-3 h-3" />}
                <span className="capitalize">{deviceType}</span>
              </div>
            </div>

            {/* Contrôles */}
            <div className="flex items-center space-x-2">
              {/* Mode d'affichage */}
              <button
                onClick={toggleViewMode}
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700 text-gray-300' 
                    : 'hover:bg-gray-100 text-gray-600'
                }`}
                title={`Passer en mode ${viewMode === 'list' ? 'grille' : 'liste'}`}
              >
                {viewMode === 'list' ? <Grid className="w-4 h-4" /> : <List className="w-4 h-4" />}
              </button>

              {/* Notifications */}
              <button
                onClick={toggleNotifications}
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700 text-gray-300' 
                    : 'hover:bg-gray-100 text-gray-600'
                } ${notifications ? 'text-green-500' : 'text-gray-400'}`}
                title={notifications ? 'Désactiver les notifications' : 'Activer les notifications'}
              >
                <Bell className="w-4 h-4" />
              </button>

              {/* Son */}
              <button
                onClick={toggleSound}
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700 text-gray-300' 
                    : 'hover:bg-gray-100 text-gray-600'
                } ${sound ? 'text-blue-500' : 'text-gray-400'}`}
                title={sound ? 'Couper le son' : 'Activer le son'}
              >
                {sound ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
              </button>

              {/* Thème */}
              <button
                onClick={toggleTheme}
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700 text-gray-300' 
                    : 'hover:bg-gray-100 text-gray-600'
                }`}
                title={`Passer en mode ${theme === 'light' ? 'sombre' : 'clair'}`}
              >
                {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
              </button>

              {/* Paramètres */}
              <button
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700 text-gray-300' 
                    : 'hover:bg-gray-100 text-gray-600'
                }`}
                title="Paramètres"
              >
                <Settings className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal avec mode d'affichage */}
      <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 ${
        viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : ''
      }`}>
        {children}
      </div>

      {/* Indicateurs de performance */}
      <div className={`fixed bottom-4 right-4 flex flex-col space-y-2 ${
        theme === 'dark' ? 'text-white' : 'text-gray-600'
      }`}>
        <div className="text-xs opacity-75">
          Mode: {viewMode === 'list' ? 'Liste' : 'Grille'}
        </div>
        <div className="text-xs opacity-75">
          Thème: {theme === 'light' ? 'Clair' : 'Sombre'}
        </div>
        <div className="text-xs opacity-75">
          Notifications: {notifications ? 'On' : 'Off'}
        </div>
      </div>
    </div>
  );
};

export default EnhancedUI; 
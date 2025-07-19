import React, { createContext, useContext, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Sun, 
    Moon, 
    Palette, 
    Settings, 
    Eye, 
    EyeOff,
    Volume2,
    VolumeX,
    Smartphone,
    Monitor,
    Tablet
} from 'lucide-react';

// Contexte du thème
const ThemeContext = createContext();

// Thèmes disponibles
const themes = {
    light: {
        name: 'Clair',
        colors: {
            primary: '#3B82F6',
            secondary: '#10B981',
            accent: '#F59E0B',
            success: '#10B981',
            warning: '#F59E0B',
            error: '#EF4444',
            info: '#06B6D4',
            background: '#FFFFFF',
            surface: '#F8FAFC',
            text: '#1F2937',
            textSecondary: '#6B7280',
            border: '#E5E7EB',
            shadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            shadowHover: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        },
        gradients: {
            primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            secondary: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            success: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            warning: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        }
    },
    dark: {
        name: 'Sombre',
        colors: {
            primary: '#60A5FA',
            secondary: '#34D399',
            accent: '#FBBF24',
            success: '#34D399',
            warning: '#FBBF24',
            error: '#F87171',
            info: '#22D3EE',
            background: '#0F172A',
            surface: '#1E293B',
            text: '#F1F5F9',
            textSecondary: '#94A3B8',
            border: '#334155',
            shadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)',
            shadowHover: '0 10px 15px -3px rgba(0, 0, 0, 0.3)',
        },
        gradients: {
            primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            secondary: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            success: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            warning: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        }
    },
    guinean: {
        name: 'Guinéen',
        colors: {
            primary: '#059669',
            secondary: '#DC2626',
            accent: '#F59E0B',
            success: '#059669',
            warning: '#F59E0B',
            error: '#DC2626',
            info: '#0891B2',
            background: '#FFFFFF',
            surface: '#F0FDF4',
            text: '#064E3B',
            textSecondary: '#065F46',
            border: '#D1FAE5',
            shadow: '0 4px 6px -1px rgba(5, 150, 105, 0.1)',
            shadowHover: '0 10px 15px -3px rgba(5, 150, 105, 0.1)',
        },
        gradients: {
            primary: 'linear-gradient(135deg, #059669 0%, #10B981 100%)',
            secondary: 'linear-gradient(135deg, #DC2626 0%, #EF4444 100%)',
            success: 'linear-gradient(135deg, #059669 0%, #10B981 100%)',
            warning: 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
        }
    }
};

// Animations
const animations = {
    fadeIn: {
        initial: { opacity: 0 },
        animate: { opacity: 1 },
        exit: { opacity: 0 },
        transition: { duration: 0.3 }
    },
    slideUp: {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: -20 },
        transition: { duration: 0.4, ease: "easeOut" }
    },
    slideDown: {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: 20 },
        transition: { duration: 0.4, ease: "easeOut" }
    },
    scaleIn: {
        initial: { opacity: 0, scale: 0.9 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.9 },
        transition: { duration: 0.3, ease: "easeOut" }
    },
    rotateIn: {
        initial: { opacity: 0, rotate: -180 },
        animate: { opacity: 1, rotate: 0 },
        exit: { opacity: 0, rotate: 180 },
        transition: { duration: 0.5, ease: "easeOut" }
    },
    bounceIn: {
        initial: { opacity: 0, scale: 0.3 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.3 },
        transition: { 
            duration: 0.6, 
            ease: [0.68, -0.55, 0.265, 1.55] 
        }
    }
};

// Composants de base
export const Button = ({ 
    children, 
    variant = 'primary', 
    size = 'medium', 
    disabled = false,
    loading = false,
    icon,
    onClick,
    className = '',
    ...props 
}) => {
    const { theme } = useTheme();
    const currentTheme = themes[theme];
    
    const baseClasses = `
        inline-flex items-center justify-center font-medium rounded-lg
        transition-all duration-200 ease-in-out
        focus:outline-none focus:ring-2 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${className}
    `;
    
    const variants = {
        primary: `bg-gradient-to-r ${currentTheme.gradients.primary} text-white hover:shadow-lg`,
        secondary: `bg-gradient-to-r ${currentTheme.gradients.secondary} text-white hover:shadow-lg`,
        success: `bg-gradient-to-r ${currentTheme.gradients.success} text-white hover:shadow-lg`,
        warning: `bg-gradient-to-r ${currentTheme.gradients.warning} text-white hover:shadow-lg`,
        outline: `border-2 border-${currentTheme.colors.primary} text-${currentTheme.colors.primary} hover:bg-${currentTheme.colors.primary} hover:text-white`,
        ghost: `text-${currentTheme.colors.primary} hover:bg-${currentTheme.colors.primary} hover:bg-opacity-10`
    };
    
    const sizes = {
        small: 'px-3 py-1.5 text-sm',
        medium: 'px-4 py-2 text-base',
        large: 'px-6 py-3 text-lg'
    };
    
    return (
        <motion.button
            whileHover={{ scale: disabled ? 1 : 1.05 }}
            whileTap={{ scale: disabled ? 1 : 0.95 }}
            className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}
            disabled={disabled || loading}
            onClick={onClick}
            {...props}
        >
            {loading && (
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"
                />
            )}
            {icon && <span className="mr-2">{icon}</span>}
            {children}
        </motion.button>
    );
};

export const Card = ({ 
    children, 
    variant = 'default',
    hover = true,
    className = '',
    ...props 
}) => {
    const { theme } = useTheme();
    const currentTheme = themes[theme];
    
    const baseClasses = `
        rounded-xl border transition-all duration-200
        ${className}
    `;
    
    const variants = {
        default: `bg-${currentTheme.colors.surface} border-${currentTheme.colors.border}`,
        elevated: `bg-${currentTheme.colors.surface} border-${currentTheme.colors.border} shadow-lg`,
        gradient: `bg-gradient-to-r ${currentTheme.gradients.primary} text-white`
    };
    
    const hoverClasses = hover ? 'hover:shadow-xl hover:scale-105' : '';
    
    return (
        <motion.div
            whileHover={hover ? { y: -5 } : {}}
            className={`${baseClasses} ${variants[variant]} ${hoverClasses}`}
            {...props}
        >
            {children}
        </motion.div>
    );
};

export const Input = ({ 
    label,
    error,
    success,
    icon,
    className = '',
    ...props 
}) => {
    const { theme } = useTheme();
    const currentTheme = themes[theme];
    
    const baseClasses = `
        w-full px-4 py-3 border rounded-lg
        transition-all duration-200
        focus:outline-none focus:ring-2 focus:ring-offset-2
        ${className}
    `;
    
    const states = {
        default: `border-${currentTheme.colors.border} focus:ring-${currentTheme.colors.primary}`,
        error: `border-${currentTheme.colors.error} focus:ring-${currentTheme.colors.error}`,
        success: `border-${currentTheme.colors.success} focus:ring-${currentTheme.colors.success}`
    };
    
    const state = error ? 'error' : success ? 'success' : 'default';
    
    return (
        <div className="space-y-2">
            {label && (
                <label className="block text-sm font-medium text-gray-700">
                    {label}
                </label>
            )}
            <div className="relative">
                {icon && (
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        {icon}
                    </div>
                )}
                <input
                    className={`${baseClasses} ${states[state]} ${icon ? 'pl-10' : ''}`}
                    {...props}
                />
            </div>
            {error && (
                <motion.p
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-sm text-red-600"
                >
                    {error}
                </motion.p>
            )}
        </div>
    );
};

export const Modal = ({ 
    isOpen, 
    onClose, 
    title, 
    children, 
    size = 'medium',
    className = ''
}) => {
    const sizes = {
        small: 'max-w-md',
        medium: 'max-w-lg',
        large: 'max-w-2xl',
        xlarge: 'max-w-4xl'
    };
    
    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50"
                    onClick={onClose}
                >
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className={`bg-white rounded-xl shadow-2xl ${sizes[size]} w-full ${className}`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="flex items-center justify-between p-6 border-b">
                            <h2 className="text-xl font-semibold">{title}</h2>
                            <button
                                onClick={onClose}
                                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                            >
                                ×
                            </button>
                        </div>
                        <div className="p-6">
                            {children}
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export const Toast = ({ 
    message, 
    type = 'info', 
    duration = 3000,
    onClose 
}) => {
    const { theme } = useTheme();
    const currentTheme = themes[theme];
    
    const types = {
        success: { icon: '✓', color: currentTheme.colors.success },
        error: { icon: '✕', color: currentTheme.colors.error },
        warning: { icon: '⚠', color: currentTheme.colors.warning },
        info: { icon: 'ℹ', color: currentTheme.colors.info }
    };
    
    useEffect(() => {
        const timer = setTimeout(onClose, duration);
        return () => clearTimeout(timer);
    }, [duration, onClose]);
    
    return (
        <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white"
            style={{ backgroundColor: types[type].color }}
        >
            <div className="flex items-center space-x-2">
                <span className="text-lg">{types[type].icon}</span>
                <span>{message}</span>
            </div>
        </motion.div>
    );
};

export const Skeleton = ({ 
    width = 'w-full', 
    height = 'h-4', 
    className = '' 
}) => {
    return (
        <div className={`${width} ${height} bg-gray-200 rounded animate-pulse ${className}`} />
    );
};

export const Badge = ({ 
    children, 
    variant = 'default',
    size = 'medium',
    className = ''
}) => {
    const { theme } = useTheme();
    const currentTheme = themes[theme];
    
    const variants = {
        default: `bg-${currentTheme.colors.primary} text-white`,
        success: `bg-${currentTheme.colors.success} text-white`,
        warning: `bg-${currentTheme.colors.warning} text-white`,
        error: `bg-${currentTheme.colors.error} text-white`,
        info: `bg-${currentTheme.colors.info} text-white`
    };
    
    const sizes = {
        small: 'px-2 py-1 text-xs',
        medium: 'px-3 py-1 text-sm',
        large: 'px-4 py-2 text-base'
    };
    
    return (
        <span className={`inline-flex items-center rounded-full font-medium ${variants[variant]} ${sizes[size]} ${className}`}>
            {children}
        </span>
    );
};

// Hook personnalisé pour le thème
export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};

// Provider du thème
export const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState('light');
    const [animationsEnabled, setAnimationsEnabled] = useState(true);
    const [soundEnabled, setSoundEnabled] = useState(true);
    const [accessibilityMode, setAccessibilityMode] = useState(false);
    const [deviceType, setDeviceType] = useState('desktop');

    useEffect(() => {
        // Détecter le type d'appareil
        const detectDevice = () => {
            const width = window.innerWidth;
            if (width < 768) setDeviceType('mobile');
            else if (width < 1024) setDeviceType('tablet');
            else setDeviceType('desktop');
        };

        detectDevice();
        window.addEventListener('resize', detectDevice);
        return () => window.removeEventListener('resize', detectDevice);
    }, []);

    useEffect(() => {
        // Appliquer le thème au document
        document.documentElement.setAttribute('data-theme', theme);
        document.body.style.backgroundColor = themes[theme].colors.background;
        document.body.style.color = themes[theme].colors.text;
    }, [theme]);

    const value = {
        theme,
        setTheme,
        currentTheme: themes[theme],
        animationsEnabled,
        setAnimationsEnabled,
        soundEnabled,
        setSoundEnabled,
        accessibilityMode,
        setAccessibilityMode,
        deviceType
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

// Contrôles de thème
export const ThemeControls = () => {
    const { 
        theme, 
        setTheme, 
        animationsEnabled, 
        setAnimationsEnabled,
        soundEnabled,
        setSoundEnabled,
        accessibilityMode,
        setAccessibilityMode
    } = useTheme();

    return (
        <div className="fixed bottom-4 right-4 z-40">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-xl shadow-lg p-4 space-y-3"
            >
                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
                    </button>
                    <span className="text-sm font-medium">Thème</span>
                </div>

                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setAnimationsEnabled(!animationsEnabled)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        {animationsEnabled ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
                    </button>
                    <span className="text-sm font-medium">Animations</span>
                </div>

                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setSoundEnabled(!soundEnabled)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        {soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
                    </button>
                    <span className="text-sm font-medium">Son</span>
                </div>

                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setAccessibilityMode(!accessibilityMode)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <Settings className="w-5 h-5" />
                    </button>
                    <span className="text-sm font-medium">Accessibilité</span>
                </div>
            </motion.div>
        </div>
    );
};

export default {
    Button,
    Card,
    Input,
    Modal,
    Toast,
    Skeleton,
    Badge,
    ThemeProvider,
    ThemeControls,
    useTheme,
    animations,
    themes
}; 
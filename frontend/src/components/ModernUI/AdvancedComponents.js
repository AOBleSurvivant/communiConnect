import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useMotionValue, useTransform, useSpring } from 'framer-motion';
import { 
    Heart, 
    Share2, 
    MessageCircle, 
    Bookmark, 
    MoreHorizontal,
    Play,
    Pause,
    SkipBack,
    SkipForward,
    Volume2,
    Maximize,
    Minimize,
    Search,
    Filter,
    SortAsc,
    SortDesc,
    Calendar,
    Clock,
    MapPin,
    User,
    Users,
    Star,
    ThumbsUp,
    ThumbsDown,
    Flag,
    Edit,
    Trash2,
    Download,
    Upload,
    Copy,
    Link,
    Camera,
    Mic,
    Video,
    Image,
    File,
    Folder,
    Lock,
    Unlock,
    Eye,
    EyeOff,
    Check,
    X,
    Plus,
    Minus,
    ChevronUp,
    ChevronDown,
    ChevronLeft,
    ChevronRight,
    ArrowUp,
    ArrowDown,
    ArrowLeft,
    ArrowRight,
    RotateCcw,
    RefreshCw,
    Zap,
    Sparkles,
    Target,
    TrendingUp,
    TrendingDown,
    Activity,
    BarChart3,
    PieChart,
    LineChart,
    ScatterChart,
    AreaChart
} from 'lucide-react';

// Composant de carte interactive
export const InteractiveCard = ({ 
    children, 
    hoverEffect = true,
    clickEffect = true,
    dragEffect = false,
    className = '',
    onClick,
    ...props 
}) => {
    const [isHovered, setIsHovered] = useState(false);
    const [isPressed, setIsPressed] = useState(false);
    
    const scale = useSpring(1, { stiffness: 300, damping: 20 });
    const rotateX = useSpring(0, { stiffness: 300, damping: 20 });
    const rotateY = useSpring(0, { stiffness: 300, damping: 20 });
    
    useEffect(() => {
        if (hoverEffect) {
            scale.set(isHovered ? 1.05 : 1);
        }
    }, [isHovered, hoverEffect, scale]);
    
    const handleMouseMove = (e) => {
        if (hoverEffect && isHovered) {
            const rect = e.currentTarget.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateXValue = ((y - centerY) / centerY) * 10;
            const rotateYValue = ((x - centerX) / centerX) * 10;
            
            rotateX.set(rotateXValue);
            rotateY.set(rotateYValue);
        }
    };
    
    const handleMouseLeave = () => {
        setIsHovered(false);
        rotateX.set(0);
        rotateY.set(0);
    };
    
    return (
        <motion.div
            style={{
                scale,
                rotateX,
                rotateY,
                transformStyle: "preserve-3d"
            }}
            onHoverStart={() => setIsHovered(true)}
            onHoverEnd={handleMouseLeave}
            onMouseMove={handleMouseMove}
            onTapStart={() => setIsPressed(true)}
            onTapEnd={() => setIsPressed(false)}
            whileTap={clickEffect ? { scale: 0.95 } : {}}
            drag={dragEffect}
            dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
            dragElastic={0.1}
            className={`perspective-1000 ${className}`}
            onClick={onClick}
            {...props}
        >
            {children}
        </motion.div>
    );
};

// Composant de bouton avec effets sonores
export const SoundButton = ({ 
    children, 
    sound = 'click',
    onClick,
    className = '',
    ...props 
}) => {
    const audioRef = useRef(null);
    
    const playSound = () => {
        if (audioRef.current) {
            audioRef.current.currentTime = 0;
            audioRef.current.play();
        }
    };
    
    const handleClick = (e) => {
        playSound();
        if (onClick) onClick(e);
    };
    
    return (
        <>
            <audio ref={audioRef} src={`/sounds/${sound}.mp3`} preload="auto" />
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleClick}
                className={className}
                {...props}
            >
                {children}
            </motion.button>
        </>
    );
};

// Composant de carrousel moderne
export const ModernCarousel = ({ 
    items, 
    autoPlay = true,
    interval = 3000,
    showDots = true,
    showArrows = true,
    className = ''
}) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [direction, setDirection] = useState(0);
    
    useEffect(() => {
        if (autoPlay) {
            const timer = setInterval(() => {
                setDirection(1);
                setCurrentIndex((prev) => (prev + 1) % items.length);
            }, interval);
            
            return () => clearInterval(timer);
        }
    }, [autoPlay, interval, items.length]);
    
    const slideVariants = {
        enter: (direction) => ({
            x: direction > 0 ? 1000 : -1000,
            opacity: 0
        }),
        center: {
            zIndex: 1,
            x: 0,
            opacity: 1
        },
        exit: (direction) => ({
            zIndex: 0,
            x: direction < 0 ? 1000 : -1000,
            opacity: 0
        })
    };
    
    const swipeConfidenceThreshold = 10000;
    const swipePower = (offset, velocity) => {
        return Math.abs(offset) * velocity;
    };
    
    const paginate = (newDirection) => {
        setDirection(newDirection);
        setCurrentIndex((prev) => (prev + newDirection + items.length) % items.length);
    };
    
    return (
        <div className={`relative overflow-hidden rounded-xl ${className}`}>
            <AnimatePresence initial={false} custom={direction}>
                <motion.div
                    key={currentIndex}
                    custom={direction}
                    variants={slideVariants}
                    initial="enter"
                    animate="center"
                    exit="exit"
                    transition={{
                        x: { type: "spring", stiffness: 300, damping: 30 },
                        opacity: { duration: 0.2 }
                    }}
                    drag="x"
                    dragConstraints={{ left: 0, right: 0 }}
                    dragElastic={1}
                    onDragEnd={(e, { offset, velocity }) => {
                        const swipe = swipePower(offset.x, velocity.x);
                        
                        if (swipe < -swipeConfidenceThreshold) {
                            paginate(1);
                        } else if (swipe > swipeConfidenceThreshold) {
                            paginate(-1);
                        }
                    }}
                    className="absolute w-full h-full"
                >
                    {items[currentIndex]}
                </motion.div>
            </AnimatePresence>
            
            {showArrows && (
                <>
                    <button
                        className="absolute left-4 top-1/2 transform -translate-y-1/2 z-10 bg-white bg-opacity-80 rounded-full p-2 hover:bg-opacity-100 transition-all"
                        onClick={() => paginate(-1)}
                    >
                        <ChevronLeft className="w-6 h-6" />
                    </button>
                    <button
                        className="absolute right-4 top-1/2 transform -translate-y-1/2 z-10 bg-white bg-opacity-80 rounded-full p-2 hover:bg-opacity-100 transition-all"
                        onClick={() => paginate(1)}
                    >
                        <ChevronRight className="w-6 h-6" />
                    </button>
                </>
            )}
            
            {showDots && (
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2 z-10">
                    {items.map((_, index) => (
                        <button
                            key={index}
                            className={`w-3 h-3 rounded-full transition-all ${
                                index === currentIndex 
                                    ? 'bg-white scale-125' 
                                    : 'bg-white bg-opacity-50 hover:bg-opacity-75'
                            }`}
                            onClick={() => {
                                setDirection(index > currentIndex ? 1 : -1);
                                setCurrentIndex(index);
                            }}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

// Composant de notification moderne
export const ModernNotification = ({ 
    type = 'info',
    title,
    message,
    duration = 5000,
    onClose,
    actions = []
}) => {
    const [isVisible, setIsVisible] = useState(true);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(false);
            setTimeout(onClose, 300);
        }, duration);
        
        return () => clearTimeout(timer);
    }, [duration, onClose]);
    
    const types = {
        success: { icon: <Check className="w-5 h-5" />, color: 'bg-green-500' },
        error: { icon: <X className="w-5 h-5" />, color: 'bg-red-500' },
        warning: { icon: <AlertTriangle className="w-5 h-5" />, color: 'bg-yellow-500' },
        info: { icon: <Info className="w-5 h-5" />, color: 'bg-blue-500' }
    };
    
    return (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    initial={{ opacity: 0, x: 300, scale: 0.8 }}
                    animate={{ opacity: 1, x: 0, scale: 1 }}
                    exit={{ opacity: 0, x: 300, scale: 0.8 }}
                    className="fixed top-4 right-4 z-50 max-w-sm w-full bg-white rounded-xl shadow-2xl border"
                >
                    <div className="p-4">
                        <div className="flex items-start space-x-3">
                            <div className={`p-2 rounded-full ${types[type].color} text-white`}>
                                {types[type].icon}
                            </div>
                            <div className="flex-1 min-w-0">
                                <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
                                <p className="text-sm text-gray-600 mt-1">{message}</p>
                                {actions.length > 0 && (
                                    <div className="flex space-x-2 mt-3">
                                        {actions.map((action, index) => (
                                            <button
                                                key={index}
                                                onClick={action.onClick}
                                                className="text-xs px-3 py-1 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
                                            >
                                                {action.label}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                            <button
                                onClick={() => {
                                    setIsVisible(false);
                                    setTimeout(onClose, 300);
                                }}
                                className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
                            >
                                <X className="w-4 h-4 text-gray-400" />
                            </button>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

// Composant de menu contextuel moderne
export const ContextMenu = ({ 
    isOpen, 
    onClose, 
    x, 
    y, 
    items = [],
    className = ''
}) => {
    const menuRef = useRef(null);
    
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                onClose();
            }
        };
        
        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }
        
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isOpen, onClose]);
    
    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    ref={menuRef}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    style={{
                        position: 'fixed',
                        left: x,
                        top: y,
                        zIndex: 1000
                    }}
                    className={`bg-white rounded-lg shadow-2xl border py-2 min-w-48 ${className}`}
                >
                    {items.map((item, index) => (
                        <button
                            key={index}
                            onClick={() => {
                                item.onClick();
                                onClose();
                            }}
                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 transition-colors flex items-center space-x-2"
                        >
                            {item.icon && <span>{item.icon}</span>}
                            <span>{item.label}</span>
                        </button>
                    ))}
                </motion.div>
            )}
        </AnimatePresence>
    );
};

// Composant de tooltip moderne
export const ModernTooltip = ({ 
    children, 
    content, 
    position = 'top',
    className = ''
}) => {
    const [isVisible, setIsVisible] = useState(false);
    const [coords, setCoords] = useState({ x: 0, y: 0 });
    
    const positions = {
        top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
        bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
        left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
        right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
    };
    
    const arrows = {
        top: 'top-full left-1/2 transform -translate-x-1/2 border-t-gray-900',
        bottom: 'bottom-full left-1/2 transform -translate-x-1/2 border-b-gray-900',
        left: 'left-full top-1/2 transform -translate-y-1/2 border-l-gray-900',
        right: 'right-full top-1/2 transform -translate-y-1/2 border-r-gray-900'
    };
    
    return (
        <div
            className={`relative inline-block ${className}`}
            onMouseEnter={() => setIsVisible(true)}
            onMouseLeave={() => setIsVisible(false)}
        >
            {children}
            <AnimatePresence>
                {isVisible && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className={`absolute z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg ${positions[position]}`}
                    >
                        {content}
                        <div className={`absolute w-0 h-0 border-4 border-transparent ${arrows[position]}`} />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// Composant de skeleton loading moderne
export const ModernSkeleton = ({ 
    type = 'card',
    className = ''
}) => {
    const types = {
        card: (
            <div className={`bg-white rounded-xl p-6 shadow-lg ${className}`}>
                <div className="flex items-center space-x-4 mb-4">
                    <div className="w-12 h-12 bg-gray-200 rounded-full animate-pulse" />
                    <div className="flex-1">
                        <div className="h-4 bg-gray-200 rounded animate-pulse mb-2" />
                        <div className="h-3 bg-gray-200 rounded animate-pulse w-2/3" />
                    </div>
                </div>
                <div className="space-y-3">
                    <div className="h-4 bg-gray-200 rounded animate-pulse" />
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-5/6" />
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-4/6" />
                </div>
            </div>
        ),
        list: (
            <div className={`space-y-3 ${className}`}>
                {[...Array(5)].map((_, index) => (
                    <div key={index} className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <div className="w-10 h-10 bg-gray-200 rounded-full animate-pulse" />
                        <div className="flex-1">
                            <div className="h-4 bg-gray-200 rounded animate-pulse mb-2" />
                            <div className="h-3 bg-gray-200 rounded animate-pulse w-1/2" />
                        </div>
                    </div>
                ))}
            </div>
        ),
        table: (
            <div className={`bg-white rounded-lg shadow ${className}`}>
                <div className="p-4 border-b">
                    <div className="h-6 bg-gray-200 rounded animate-pulse w-1/3" />
                </div>
                <div className="p-4 space-y-3">
                    {[...Array(4)].map((_, index) => (
                        <div key={index} className="flex space-x-4">
                            <div className="h-4 bg-gray-200 rounded animate-pulse flex-1" />
                            <div className="h-4 bg-gray-200 rounded animate-pulse flex-1" />
                            <div className="h-4 bg-gray-200 rounded animate-pulse flex-1" />
                        </div>
                    ))}
                </div>
            </div>
        )
    };
    
    return types[type];
};

// Composant de progress bar moderne
export const ModernProgressBar = ({ 
    value, 
    max = 100,
    color = 'blue',
    showLabel = true,
    animated = true,
    className = ''
}) => {
    const percentage = (value / max) * 100;
    
    const colors = {
        blue: 'bg-blue-500',
        green: 'bg-green-500',
        red: 'bg-red-500',
        yellow: 'bg-yellow-500',
        purple: 'bg-purple-500',
        pink: 'bg-pink-500'
    };
    
    return (
        <div className={`w-full ${className}`}>
            {showLabel && (
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Progression</span>
                    <span>{Math.round(percentage)}%</span>
                </div>
            )}
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <motion.div
                    className={`h-full ${colors[color]} rounded-full`}
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: animated ? 0.8 : 0 }}
                />
            </div>
        </div>
    );
};

export default {
    InteractiveCard,
    SoundButton,
    ModernCarousel,
    ModernNotification,
    ContextMenu,
    ModernTooltip,
    ModernSkeleton,
    ModernProgressBar
}; 
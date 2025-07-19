import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useMotionValue, useTransform, useSpring, useAnimation } from 'framer-motion';
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
    AreaChart,
    Globe,
    Wifi,
    Bluetooth,
    Battery,
    Signal,
    Settings,
    Home,
    Search as SearchIcon,
    Bell,
    Mail,
    Phone,
    Map,
    Navigation,
    Compass,
    Location,
    Pin,
    Flag as FlagIcon,
    Award,
    Trophy,
    Medal,
    Crown,
    Diamond,
    Gem,
    Sparkle,
    Fire,
    Lightning,
    Thunder,
    Rain,
    Snow,
    Cloud,
    Sun,
    Moon,
    Star as StarIcon,
    Planet,
    Rocket,
    UFO,
    Alien,
    Ghost,
    Skull,
    Cross,
    Heart as HeartIcon,
    Pulse,
    Activity as ActivityIcon,
    Zap as ZapIcon,
    Target as TargetIcon,
    Bullseye,
    Darts,
    Basketball,
    Football,
    Tennis,
    Golf,
    Swimming,
    Running,
    Cycling,
    Hiking,
    Climbing,
    Surfing,
    Skiing,
    Snowboarding,
    Skateboarding,
    Rollerblading,
    Dancing,
    Yoga,
    Meditation,
    Prayer,
    Worship,
    Church,
    Mosque,
    Temple,
    Synagogue,
    Monastery,
    Shrine,
    Altar,
    Candle,
    Incense,
    Bell as BellIcon,
    Drum,
    Guitar,
    Piano,
    Violin,
    Trumpet,
    Saxophone,
    Flute,
    Clarinet,
    Trombone,
    Tuba,
    Harp,
    Accordion,
    Harmonica,
    Ukulele,
    Banjo,
    Mandolin,
    Sitar,
    Tabla,
    Djembe,
    Conga,
    Bongo,
    Maracas,
    Tambourine,
    Triangle,
    Xylophone,
    Vibraphone,
    Glockenspiel,
    Celesta,
    Organ,
    Synthesizer,
    DrumMachine,
    Turntable,
    Microphone,
    Speaker,
    Headphones,
    Earbuds,
    Radio,
    Television,
    Computer,
    Laptop,
    Tablet,
    Smartphone,
    Watch,
    Camera as CameraIcon,
    Video as VideoIcon,
    Photo,
    Film,
    Projector,
    Screen,
    Monitor,
    Keyboard,
    Mouse,
    Printer,
    Scanner,
    Fax,
    Router,
    Modem,
    Server,
    Database,
    Cloud,
    Internet,
    Website,
    App,
    Software,
    Hardware,
    Chip,
    Circuit,
    Battery as BatteryIcon,
    Power,
    Energy,
    Solar,
    Wind,
    Water,
    Nuclear,
    Fossil,
    Renewable,
    Green,
    Eco,
    Environment,
    Nature,
    Tree,
    Flower,
    Plant,
    Seed,
    Leaf,
    Root,
    Branch,
    Trunk,
    Bark,
    Wood,
    Forest,
    Jungle,
    Desert,
    Mountain,
    Valley,
    River,
    Lake,
    Ocean,
    Sea,
    Island,
    Beach,
    Coast,
    Cliff,
    Cave,
    Canyon,
    Volcano,
    Earthquake,
    Tsunami,
    Hurricane,
    Tornado,
    Storm,
    Lightning as LightningIcon,
    Thunder as ThunderIcon,
    Rain as RainIcon,
    Snow as SnowIcon,
    Cloud as CloudIcon,
    Fog,
    Mist,
    Haze,
    Smog,
    Pollution,
    Clean,
    Fresh,
    Pure,
    Natural,
    Organic,
    Healthy,
    Wellness,
    Fitness,
    Nutrition,
    Medicine,
    Doctor,
    Nurse,
    Hospital,
    Clinic,
    Pharmacy,
    Drug,
    Pill,
    Syringe,
    Bandage,
    Thermometer,
    Stethoscope,
    XRay,
    MRI,
    Ultrasound,
    Surgery,
    Operation,
    Treatment,
    Therapy,
    Rehabilitation,
    Recovery,
    Healing,
    Cure,
    Prevention,
    Vaccine,
    Immunity,
    Disease,
    Infection,
    Virus,
    Bacteria,
    Parasite,
    Fungus,
    Allergy,
    Asthma,
    Diabetes,
    Cancer,
    Heart,
    Brain,
    Lung,
    Liver,
    Kidney,
    Stomach,
    Intestine,
    Blood,
    Bone,
    Muscle,
    Skin,
    Hair,
    Nail,
    Tooth,
    Eye,
    Ear,
    Nose,
    Mouth,
    Tongue,
    Throat,
    Neck,
    Shoulder,
    Arm,
    Hand,
    Finger,
    Leg,
    Foot,
    Toe,
    Joint,
    Spine,
    Rib,
    Pelvis,
    Hip,
    Knee,
    Ankle,
    Wrist,
    Elbow,
    Shoulder as ShoulderIcon,
    Back,
    Chest,
    Abdomen,
    Waist,
    Hip as HipIcon,
    Buttock,
    Genital,
    Reproductive,
    Pregnancy,
    Birth,
    Baby,
    Child,
    Teen,
    Adult,
    Elder,
    Senior,
    Youth,
    Age,
    Gender,
    Male,
    Female,
    Transgender,
    NonBinary,
    Intersex,
    Queer,
    LGBT,
    Gay,
    Lesbian,
    Bisexual,
    Pansexual,
    Asexual,
    Demisexual,
    Polysexual,
    Omnisexual,
    Graysexual,
    Aromantic,
    Biromantic,
    Panromantic,
    Polyromantic,
    Omniromantic,
    Grayromantic,
    Demiromantic,
    Lithromantic,
    Recipromantic,
    Quoiromantic,
    Akoiromantic,
    Cupioromantic,
    Bellusromantic,
    Frayromantic,
    Idemromantic,
    Requiesromantic,
    Vultromantic,
    Apresromantic,
    Reciprosexual,
    Akoisexual,
    Cupiosexual,
    Bellusexual,
    Fraysexual,
    Idemsexual,
    Requiesexual,
    Vultsexual,
    Apresexual,
    Lithsexual,
    Quoisexual,
    Polysexual as PolysexualIcon,
    Omnisexual as OmnisexualIcon,
    Graysexual as GraysexualIcon,
    Aromantic as AromanticIcon,
    Biromantic as BiromanticIcon,
    Panromantic as PanromanticIcon,
    Polyromantic as PolyromanticIcon,
    Omniromantic as OmniromanticIcon,
    Grayromantic as GrayromanticIcon,
    Demiromantic as DemiromanticIcon,
    Lithromantic as LithromanticIcon,
    Recipromantic as RecipromanticIcon,
    Quoiromantic as QuoiromanticIcon,
    Akoiromantic as AkoiromanticIcon,
    Cupioromantic as CupioromanticIcon,
    Bellusromantic as BellusromanticIcon,
    Frayromantic as FrayromanticIcon,
    Idemromantic as IdemromanticIcon,
    Requiesromantic as RequiesromanticIcon,
    Vultromantic as VultromanticIcon,
    Apresromantic as ApresromanticIcon,
    Reciprosexual as ReciprosexualIcon,
    Akoisexual as AkoisexualIcon,
    Cupiosexual as CupiosexualIcon,
    Bellusexual as BellusexualIcon,
    Fraysexual as FraysexualIcon,
    Idemsexual as IdemsexualIcon,
    Requiesexual as RequiesexualIcon,
    Vultsexual as VultsexualIcon,
    Apresexual as ApresexualIcon,
    Lithsexual as LithsexualIcon,
    Quoisexual as QuoisexualIcon
} from 'lucide-react';

// Expérience de like avec animation de cœur
export const HeartLikeExperience = ({ 
    isLiked = false, 
    onToggle, 
    count = 0,
    size = 'medium',
    className = ''
}) => {
    const [isAnimating, setIsAnimating] = useState(false);
    const scale = useSpring(1, { stiffness: 300, damping: 20 });
    
    const sizes = {
        small: 'w-6 h-6',
        medium: 'w-8 h-8',
        large: 'w-12 h-12'
    };
    
    const handleClick = () => {
        setIsAnimating(true);
        scale.set(1.3);
        
        setTimeout(() => {
            scale.set(1);
            setIsAnimating(false);
        }, 200);
        
        if (onToggle) onToggle();
    };
    
    return (
        <div className={`flex items-center space-x-2 ${className}`}>
            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleClick}
                className={`relative ${sizes[size]} flex items-center justify-center`}
            >
                <motion.div
                    style={{ scale }}
                    className={`${sizes[size]} flex items-center justify-center`}
                >
                    <Heart
                        className={`${sizes[size]} transition-colors duration-200 ${
                            isLiked 
                                ? 'text-red-500 fill-current' 
                                : 'text-gray-400 hover:text-red-400'
                        }`}
                    />
                </motion.div>
                
                {isAnimating && (
                    <motion.div
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0, opacity: 0 }}
                        className="absolute inset-0 flex items-center justify-center"
                    >
                        <Heart className={`${sizes[size]} text-red-500 fill-current`} />
                    </motion.div>
                )}
            </motion.button>
            
            <motion.span
                key={count}
                initial={{ scale: 1.2, color: '#EF4444' }}
                animate={{ scale: 1, color: '#6B7280' }}
                transition={{ duration: 0.3 }}
                className="text-sm font-medium text-gray-600"
            >
                {count}
            </motion.span>
        </div>
    );
};

// Expérience de partage avec animation
export const ShareExperience = ({ 
    onShare, 
    platforms = ['facebook', 'twitter', 'whatsapp', 'email'],
    className = ''
}) => {
    const [isOpen, setIsOpen] = useState(false);
    
    const platformIcons = {
        facebook: '📘',
        twitter: '🐦',
        whatsapp: '💬',
        email: '📧',
        linkedin: '💼',
        instagram: '📷',
        telegram: '📡',
        discord: '🎮'
    };
    
    const handleShare = (platform) => {
        setIsOpen(false);
        if (onShare) onShare(platform);
    };
    
    return (
        <div className={`relative ${className}`}>
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsOpen(!isOpen)}
                className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            >
                <Share2 className="w-5 h-5 text-gray-600" />
            </motion.button>
            
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.8, y: 10 }}
                        className="absolute top-full right-0 mt-2 bg-white rounded-lg shadow-lg border p-2 z-50"
                    >
                        <div className="flex space-x-2">
                            {platforms.map((platform) => (
                                <motion.button
                                    key={platform}
                                    whileHover={{ scale: 1.1 }}
                                    whileTap={{ scale: 0.9 }}
                                    onClick={() => handleShare(platform)}
                                    className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
                                >
                                    <span className="text-lg">{platformIcons[platform]}</span>
                                </motion.button>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// Expérience de commentaire avec animation
export const CommentExperience = ({ 
    count = 0, 
    onComment,
    className = ''
}) => {
    const [isAnimating, setIsAnimating] = useState(false);
    
    const handleClick = () => {
        setIsAnimating(true);
        setTimeout(() => setIsAnimating(false), 300);
        if (onComment) onComment();
    };
    
    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleClick}
            className={`flex items-center space-x-2 p-2 rounded-full hover:bg-gray-100 transition-colors ${className}`}
        >
            <motion.div
                animate={isAnimating ? { rotate: [0, -10, 10, 0] } : {}}
                transition={{ duration: 0.3 }}
            >
                <MessageCircle className="w-5 h-5 text-gray-600" />
            </motion.div>
            <span className="text-sm font-medium text-gray-600">{count}</span>
        </motion.button>
    );
};

// Expérience de bookmark avec animation
export const BookmarkExperience = ({ 
    isBookmarked = false, 
    onToggle,
    className = ''
}) => {
    const [isAnimating, setIsAnimating] = useState(false);
    
    const handleClick = () => {
        setIsAnimating(true);
        setTimeout(() => setIsAnimating(false), 300);
        if (onToggle) onToggle();
    };
    
    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleClick}
            className={`p-2 rounded-full hover:bg-gray-100 transition-colors ${className}`}
        >
            <motion.div
                animate={isAnimating ? { y: [0, -5, 0] } : {}}
                transition={{ duration: 0.3 }}
            >
                <Bookmark
                    className={`w-5 h-5 transition-colors duration-200 ${
                        isBookmarked 
                            ? 'text-blue-500 fill-current' 
                            : 'text-gray-400 hover:text-blue-400'
                    }`}
                />
            </motion.div>
        </motion.button>
    );
};

// Expérience de recherche avec suggestions
export const SearchExperience = ({ 
    onSearch,
    placeholder = "Rechercher...",
    suggestions = [],
    className = ''
}) => {
    const [query, setQuery] = useState('');
    const [isFocused, setIsFocused] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(-1);
    
    const handleSearch = (searchQuery = query) => {
        if (onSearch) onSearch(searchQuery);
    };
    
    const handleKeyDown = (e) => {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setSelectedIndex(prev => 
                prev < suggestions.length - 1 ? prev + 1 : prev
            );
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (selectedIndex >= 0 && suggestions[selectedIndex]) {
                handleSearch(suggestions[selectedIndex]);
            } else {
                handleSearch();
            }
        }
    };
    
    return (
        <div className={`relative ${className}`}>
            <motion.div
                animate={{ scale: isFocused ? 1.02 : 1 }}
                className="relative"
            >
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setTimeout(() => setIsFocused(false), 200)}
                    onKeyDown={handleKeyDown}
                    placeholder={placeholder}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </motion.div>
            
            <AnimatePresence>
                {isFocused && suggestions.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-lg border max-h-60 overflow-y-auto z-50"
                    >
                        {suggestions.map((suggestion, index) => (
                            <motion.button
                                key={index}
                                whileHover={{ backgroundColor: '#F3F4F6' }}
                                onClick={() => handleSearch(suggestion)}
                                className={`w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors ${
                                    index === selectedIndex ? 'bg-blue-50' : ''
                                }`}
                            >
                                {suggestion}
                            </motion.button>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// Expérience de notification avec badge
export const NotificationExperience = ({ 
    count = 0,
    onNotification,
    className = ''
}) => {
    const [isAnimating, setIsAnimating] = useState(false);
    
    useEffect(() => {
        if (count > 0) {
            setIsAnimating(true);
            setTimeout(() => setIsAnimating(false), 1000);
        }
    }, [count]);
    
    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onNotification}
            className={`relative p-2 rounded-full hover:bg-gray-100 transition-colors ${className}`}
        >
            <Bell className="w-6 h-6 text-gray-600" />
            
            {count > 0 && (
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
                >
                    <motion.span
                        animate={isAnimating ? { scale: [1, 1.2, 1] } : {}}
                        transition={{ duration: 0.3 }}
                    >
                        {count > 99 ? '99+' : count}
                    </motion.span>
                </motion.div>
            )}
        </motion.button>
    );
};

// Expérience de navigation fluide
export const SmoothNavigation = ({ 
    children,
    className = ''
}) => {
    const [isNavigating, setIsNavigating] = useState(false);
    
    const handleNavigation = (callback) => {
        setIsNavigating(true);
        setTimeout(() => {
            if (callback) callback();
            setIsNavigating(false);
        }, 300);
    };
    
    return (
        <div className={`relative ${className}`}>
            {children}
            
            <AnimatePresence>
                {isNavigating && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
                    >
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            className="w-8 h-8 border-4 border-white border-t-transparent rounded-full"
                        />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// Expérience de feedback haptique
export const HapticFeedback = ({ 
    children,
    intensity = 'light',
    className = ''
}) => {
    const intensities = {
        light: 'vibrate(10ms)',
        medium: 'vibrate(20ms)',
        heavy: 'vibrate(50ms)'
    };
    
    const handleInteraction = () => {
        if ('vibrate' in navigator) {
            navigator.vibrate(intensities[intensity]);
        }
    };
    
    return (
        <div 
            onClick={handleInteraction}
            className={className}
        >
            {children}
        </div>
    );
};

// Expérience de parallax
export const ParallaxExperience = ({ 
    children,
    speed = 0.5,
    className = ''
}) => {
    const y = useMotionValue(0);
    const yTransform = useTransform(y, [0, 100], [0, 100 * speed]);
    
    return (
        <motion.div
            style={{ y: yTransform }}
            className={className}
        >
            {children}
        </motion.div>
    );
};

// Expérience de scroll infini
export const InfiniteScrollExperience = ({ 
    items = [],
    onLoadMore,
    hasMore = true,
    className = ''
}) => {
    const [isLoading, setIsLoading] = useState(false);
    
    const handleScroll = (e) => {
        const { scrollTop, scrollHeight, clientHeight } = e.target;
        
        if (scrollTop + clientHeight >= scrollHeight - 100 && hasMore && !isLoading) {
            setIsLoading(true);
            if (onLoadMore) {
                onLoadMore().finally(() => setIsLoading(false));
            }
        }
    };
    
    return (
        <div 
            onScroll={handleScroll}
            className={`overflow-y-auto ${className}`}
        >
            {items.map((item, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                >
                    {item}
                </motion.div>
            ))}
            
            {isLoading && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex justify-center p-4"
                >
                    <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-6 h-6 border-2 border-gray-300 border-t-blue-500 rounded-full"
                    />
                </motion.div>
            )}
        </div>
    );
};

export default {
    HeartLikeExperience,
    ShareExperience,
    CommentExperience,
    BookmarkExperience,
    SearchExperience,
    NotificationExperience,
    SmoothNavigation,
    HapticFeedback,
    ParallaxExperience,
    InfiniteScrollExperience
}; 
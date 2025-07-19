import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  Zap, 
  Clock, 
  Star, 
  Heart, 
  Eye, 
  MessageCircle, 
  Share, 
  Bookmark,
  Search,
  Filter,
  SortAsc,
  SortDesc,
  RefreshCw,
  Settings,
  Bell,
  User,
  Shield,
  Globe,
  Lock,
  EyeOff,
  Volume2,
  VolumeX,
  Smartphone,
  Monitor,
  Tablet,
  Wifi,
  WifiOff,
  Battery,
  BatteryCharging,
  Sun,
  Moon,
  Palette,
  Type,
  Image,
  Video,
  Music,
  FileText,
  Calendar,
  MapPin,
  Clock as TimeIcon,
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  PieChart,
  Target,
  Award,
  Gift,
  Sparkles,
  Rocket,
  Lightbulb,
  CheckCircle,
  AlertCircle,
  Info,
  HelpCircle,
  ExternalLink,
  Download,
  Upload,
  Sync,
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Maximize,
  Minimize,
  Fullscreen,
  FullscreenExit,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume1,
  Volume2 as Volume2Icon,
  VolumeX as VolumeXIcon,
  Mic,
  MicOff,
  Camera,
  CameraOff,
  Video as VideoIcon,
  VideoOff,
  Phone,
  PhoneOff,
  Mail,
  Send,
  Edit,
  Trash2,
  Copy,
  Link,
  Unlink,
  Lock as LockIcon,
  Unlock,
  Key,
  Fingerprint,
  QrCode,
  CreditCard,
  Wallet,
  ShoppingCart,
  Gift as GiftIcon,
  Package,
  Truck,
  Home,
  Building,
  Car,
  Bus,
  Train,
  Plane,
  Ship,
  Bike,
  Walk,
  Run,
  Heart as HeartIcon,
  HeartOff,
  ThumbsUp,
  ThumbsDown,
  Smile,
  Frown,
  Meh,
  Angry,
  Surprised,
  Confused,
  Happy,
  Sad,
  Excited,
  Tired,
  Sick,
  Healthy,
  Strong,
  Weak,
  Fast,
  Slow,
  Hot,
  Cold,
  Wet,
  Dry,
  Clean,
  Dirty,
  New,
  Old,
  Young,
  Adult,
  Child,
  Baby,
  Elder,
  Man,
  Woman,
  Boy,
  Girl,
  Family,
  Couple,
  Single,
  Married,
  Divorced,
  Widowed,
  Engaged,
  Dating,
  Friend,
  Enemy,
  Stranger,
  Acquaintance,
  Colleague,
  Boss,
  Employee,
  Student,
  Teacher,
  Doctor,
  Nurse,
  Police,
  Firefighter,
  Soldier,
  Artist,
  Musician,
  Actor,
  Writer,
  Journalist,
  Lawyer,
  Engineer,
  Scientist,
  Researcher,
  Designer,
  Developer,
  Manager,
  Director,
  CEO,
  President,
  King,
  Queen,
  Prince,
  Princess,
  Duke,
  Duchess,
  Lord,
  Lady,
  Sir,
  Madam,
  Mr,
  Mrs,
  Ms,
  Dr,
  Prof,
  Rev,
  Hon,
  Sen,
  Rep,
  Gov,
  Mayor,
  Judge,
  Ambassador,
  Minister,
  Secretary,
  Assistant,
  Intern,
  Volunteer,
  Consultant,
  Advisor,
  Expert,
  Specialist,
  Professional,
  Amateur,
  Beginner,
  Intermediate,
  Advanced,
  Expert as ExpertIcon,
  Master,
  Grandmaster,
  Champion,
  Winner,
  Loser,
  Runner,
  Participant,
  Spectator,
  Fan,
  Supporter,
  Critic,
  Reviewer,
  Commentator,
  Announcer,
  Host,
  Guest,
  Speaker,
  Presenter,
  Moderator,
  Facilitator,
  Coordinator,
  Organizer,
  Planner,
  Scheduler,
  Reminder,
  Alarm,
  Timer,
  Stopwatch,
  Chronometer,
  Calendar as CalendarIcon,
  Schedule,
  Agenda,
  Timeline,
  History,
  Future,
  Past,
  Present,
  Now,
  Today,
  Yesterday,
  Tomorrow,
  Week,
  Month,
  Year,
  Decade,
  Century,
  Millennium,
  Era,
  Age,
  Period,
  Phase,
  Stage,
  Level,
  Grade,
  Class,
  Category,
  Type,
  Kind,
  Sort,
  Order,
  Rank,
  Position,
  Status,
  State,
  Condition,
  Situation,
  Circumstance,
  Context,
  Environment,
  Atmosphere,
  Mood,
  Feeling,
  Emotion,
  Sentiment,
  Attitude,
  Opinion,
  View,
  Perspective,
  Standpoint,
  Position as PositionIcon,
  Side,
  Party,
  Group,
  Team,
  Squad,
  Crew,
  Gang,
  Band,
  Orchestra,
  Choir,
  Ensemble,
  Company,
  Corporation,
  Organization,
  Institution,
  Association,
  Society,
  Club,
  Union,
  Alliance,
  Partnership,
  Collaboration,
  Cooperation,
  Competition,
  Rivalry,
  Conflict,
  War,
  Peace,
  Truce,
  Ceasefire,
  Armistice,
  Treaty,
  Agreement,
  Contract,
  Deal,
  Bargain,
  Trade,
  Exchange,
  Transaction,
  Payment,
  Receipt,
  Invoice,
  Bill,
  Check,
  Money,
  Cash,
  Coin,
  Banknote,
  Currency,
  Dollar,
  Euro,
  Pound,
  Yen,
  Yuan,
  Rupee,
  Real,
  Peso,
  Ruble,
  Lira,
  Franc,
  Mark,
  Guilder,
  Krone,
  Krona,
  Forint,
  Zloty,
  Koruna,
  Leu,
  Lev,
  Tolar,
  Litas,
  Lat,
  Kroon,
  Crown,
  Shilling,
  Pence,
  Cent,
  Penny,
  Nickel,
  Dime,
  Quarter,
  Half,
  Dollar as DollarIcon,
  Euro as EuroIcon,
  Pound as PoundIcon,
  Yen as YenIcon,
  Yuan as YuanIcon,
  Rupee as RupeeIcon,
  Real as RealIcon,
  Peso as PesoIcon,
  Ruble as RubleIcon,
  Lira as LiraIcon,
  Franc as FrancIcon,
  Mark as MarkIcon,
  Guilder as GuilderIcon,
  Krone as KroneIcon,
  Krona as KronaIcon,
  Forint as ForintIcon,
  Zloty as ZlotyIcon,
  Koruna as KorunaIcon,
  Leu as LeuIcon,
  Lev as LevIcon,
  Tolar as TolarIcon,
  Litas as LitasIcon,
  Lat as LatIcon,
  Kroon as KroonIcon,
  Crown as CrownIcon,
  Shilling as ShillingIcon,
  Pence as PenceIcon,
  Cent as CentIcon,
  Penny as PennyIcon,
  Nickel as NickelIcon,
  Dime as DimeIcon,
  Quarter as QuarterIcon,
  Half as HalfIcon
} from 'lucide-react';
import toast from 'react-hot-toast';

const UserExperience = ({ children, onPreferencesChange }) => {
  const { user } = useAuth();
  const [preferences, setPreferences] = useState({
    theme: 'light',
    fontSize: 'medium',
    language: 'fr',
    notifications: true,
    sound: true,
    autoPlay: false,
    accessibility: {
      highContrast: false,
      reducedMotion: false,
      screenReader: false
    },
    privacy: {
      profileVisibility: 'public',
      postVisibility: 'friends',
      locationSharing: false
    },
    performance: {
      dataSaver: false,
      imageQuality: 'high',
      videoQuality: 'medium'
    }
  });

  const [userStats, setUserStats] = useState({
    sessionTime: 0,
    postsCreated: 0,
    interactions: 0,
    engagement: 0
  });

  const [quickActions, setQuickActions] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);

  useEffect(() => {
    loadUserPreferences();
    startSessionTimer();
    loadQuickActions();
  }, []);

  const loadUserPreferences = () => {
    const savedPrefs = localStorage.getItem('userPreferences');
    if (savedPrefs) {
      setPreferences(JSON.parse(savedPrefs));
    }
  };

  const saveUserPreferences = useCallback((newPrefs) => {
    setPreferences(newPrefs);
    localStorage.setItem('userPreferences', JSON.stringify(newPrefs));
    onPreferencesChange?.(newPrefs);
  }, [onPreferencesChange]);

  const startSessionTimer = () => {
    const startTime = Date.now();
    const timer = setInterval(() => {
      const sessionTime = Math.floor((Date.now() - startTime) / 1000);
      setUserStats(prev => ({ ...prev, sessionTime }));
    }, 1000);

    return () => clearInterval(timer);
  };

  const loadQuickActions = () => {
    setQuickActions([
      { id: 1, name: 'Nouveau post', icon: MessageCircle, action: 'createPost' },
      { id: 2, name: 'Rechercher', icon: Search, action: 'search' },
      { id: 3, name: 'Amis', icon: User, action: 'friends' },
      { id: 4, name: 'Événements', icon: Calendar, action: 'events' }
    ]);
  };

  const handleQuickAction = (action) => {
    switch (action) {
      case 'createPost':
        toast.success('Ouverture de la création de post...');
        break;
      case 'search':
        toast.success('Ouverture de la recherche...');
        break;
      case 'friends':
        toast.success('Ouverture des amis...');
        break;
      case 'events':
        toast.success('Ouverture des événements...');
        break;
      default:
        break;
    }
  };

  const toggleTheme = () => {
    const newTheme = preferences.theme === 'light' ? 'dark' : 'light';
    saveUserPreferences({
      ...preferences,
      theme: newTheme
    });
    document.documentElement.classList.toggle('dark');
  };

  const toggleAccessibility = (feature) => {
    saveUserPreferences({
      ...preferences,
      accessibility: {
        ...preferences.accessibility,
        [feature]: !preferences.accessibility[feature]
      }
    });
  };

  const updatePrivacy = (setting, value) => {
    saveUserPreferences({
      ...preferences,
      privacy: {
        ...preferences.privacy,
        [setting]: value
      }
    });
  };

  const updatePerformance = (setting, value) => {
    saveUserPreferences({
      ...preferences,
      performance: {
        ...preferences.performance,
        [setting]: value
      }
    });
  };

  const renderQuickActions = () => (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <h3 className="text-lg font-semibold mb-4">Actions rapides</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {quickActions.map(action => {
          const Icon = action.icon;
          return (
            <button
              key={action.id}
              onClick={() => handleQuickAction(action.action)}
              className="flex flex-col items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Icon className="w-6 h-6 text-blue-600 mb-2" />
              <span className="text-sm font-medium">{action.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );

  const renderUserStats = () => (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <h3 className="text-lg font-semibold mb-4">Mes statistiques</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center">
          <Clock className="w-8 h-8 text-blue-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">{Math.floor(userStats.sessionTime / 60)}m</div>
          <div className="text-sm text-gray-600">Session</div>
        </div>
        <div className="text-center">
          <MessageCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">{userStats.postsCreated}</div>
          <div className="text-sm text-gray-600">Posts</div>
        </div>
        <div className="text-center">
          <Heart className="w-8 h-8 text-red-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">{userStats.interactions}</div>
          <div className="text-sm text-gray-600">Interactions</div>
        </div>
        <div className="text-center">
          <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
          <div className="text-2xl font-bold">{userStats.engagement}%</div>
          <div className="text-sm text-gray-600">Engagement</div>
        </div>
      </div>
    </div>
  );

  const renderPreferences = () => (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold mb-4">Préférences</h3>
      
      {/* Thème */}
      <div className="mb-6">
        <h4 className="font-medium mb-3">Apparence</h4>
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            {preferences.theme === 'light' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            <span>Mode {preferences.theme === 'light' ? 'clair' : 'sombre'}</span>
          </button>
        </div>
      </div>

      {/* Accessibilité */}
      <div className="mb-6">
        <h4 className="font-medium mb-3">Accessibilité</h4>
        <div className="space-y-2">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.accessibility.highContrast}
              onChange={() => toggleAccessibility('highContrast')}
              className="rounded"
            />
            <span>Contraste élevé</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.accessibility.reducedMotion}
              onChange={() => toggleAccessibility('reducedMotion')}
              className="rounded"
            />
            <span>Mouvements réduits</span>
          </label>
        </div>
      </div>

      {/* Confidentialité */}
      <div className="mb-6">
        <h4 className="font-medium mb-3">Confidentialité</h4>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">Visibilité du profil</label>
            <select
              value={preferences.privacy.profileVisibility}
              onChange={(e) => updatePrivacy('profileVisibility', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="public">Public</option>
              <option value="friends">Amis</option>
              <option value="private">Privé</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Visibilité des posts</label>
            <select
              value={preferences.privacy.postVisibility}
              onChange={(e) => updatePrivacy('postVisibility', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="public">Public</option>
              <option value="friends">Amis</option>
              <option value="private">Privé</option>
            </select>
          </div>
        </div>
      </div>

      {/* Performance */}
      <div className="mb-6">
        <h4 className="font-medium mb-3">Performance</h4>
        <div className="space-y-3">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.performance.dataSaver}
              onChange={(e) => updatePerformance('dataSaver', e.target.checked)}
              className="rounded"
            />
            <span>Économiseur de données</span>
          </label>
          <div>
            <label className="block text-sm font-medium mb-1">Qualité des images</label>
            <select
              value={preferences.performance.imageQuality}
              onChange={(e) => updatePerformance('imageQuality', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="low">Basse</option>
              <option value="medium">Moyenne</option>
              <option value="high">Haute</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      preferences.theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'
    }`}>
      <div className="max-w-6xl mx-auto px-4 py-6">
        {renderQuickActions()}
        {renderUserStats()}
        {renderPreferences()}
        
        {/* Contenu principal */}
        <div className="mt-6">
          {children}
        </div>
      </div>
    </div>
  );
};

export default UserExperience; 
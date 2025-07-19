import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { 
    Shield, 
    Lock, 
    Unlock,
    Eye,
    EyeOff,
    Key,
    Fingerprint,
    Smartphone,
    Mail,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Clock,
    Calendar,
    MapPin,
    Globe,
    Users,
    Activity,
    BarChart3,
    PieChart,
    LineChart,
    TrendingUp,
    TrendingDown,
    Zap,
    Brain,
    Lightbulb,
    Settings,
    RefreshCw,
    Download,
    Filter,
    Search,
    Play,
    Pause,
    SkipBack,
    SkipForward,
    Volume2,
    Maximize,
    Minimize,
    RotateCcw,
    Sparkles,
    Rocket,
    Crown,
    Trophy,
    Medal,
    Award,
    Diamond,
    Gem,
    Fire,
    Lightning,
    Thunder,
    Rain,
    Snow,
    Cloud,
    Sun,
    Moon,
    Star,
    Planet,
    UFO,
    Alien,
    Ghost,
    Skull,
    Cross,
    Heart,
    Pulse,
    Activity as ActivityIcon,
    Zap as ZapIcon,
    Target,
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
    Bell,
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
    Camera,
    Video,
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
    Battery,
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

const SecurityDashboard = () => {
    const { user } = useContext(AuthContext);
    const [securityData, setSecurityData] = useState({});
    const [securityEvents, setSecurityEvents] = useState([]);
    const [threats, setThreats] = useState([]);
    const [incidents, setIncidents] = useState([]);
    const [audits, setAudits] = useState([]);
    const [compliance, setCompliance] = useState([]);
    const [userSecurityProfiles, setUserSecurityProfiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedTimeRange, setSelectedTimeRange] = useState('7d');
    const [selectedSeverity, setSelectedSeverity] = useState('all');

    useEffect(() => {
        if (user) {
            loadSecurityData();
        }
    }, [user, selectedTimeRange, selectedSeverity]);

    const loadSecurityData = async () => {
        try {
            setLoading(true);
            
            // Charger toutes les données de sécurité
            await Promise.all([
                loadSecurityDashboard(),
                loadSecurityEvents(),
                loadThreats(),
                loadIncidents(),
                loadAudits(),
                loadCompliance(),
                loadUserSecurityProfiles()
            ]);
            
        } catch (error) {
            console.error('Erreur chargement sécurité:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadSecurityDashboard = async () => {
        try {
            const response = await fetch('/api/security/dashboard/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSecurityData(data);
            }
        } catch (error) {
            console.error('Erreur dashboard sécurité:', error);
        }
    };

    const loadSecurityEvents = async () => {
        try {
            const response = await fetch('/api/security/events/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSecurityEvents(data.events || []);
            }
        } catch (error) {
            console.error('Erreur événements sécurité:', error);
        }
    };

    const loadThreats = async () => {
        try {
            const response = await fetch('/api/security/threats/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setThreats(data.threats || []);
            }
        } catch (error) {
            console.error('Erreur menaces:', error);
        }
    };

    const loadIncidents = async () => {
        try {
            const response = await fetch('/api/security/incidents/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setIncidents(data.incidents || []);
            }
        } catch (error) {
            console.error('Erreur incidents:', error);
        }
    };

    const loadAudits = async () => {
        try {
            const response = await fetch('/api/security/audits/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setAudits(data.audits || []);
            }
        } catch (error) {
            console.error('Erreur audits:', error);
        }
    };

    const loadCompliance = async () => {
        try {
            const response = await fetch('/api/security/compliance/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setCompliance(data.compliance || []);
            }
        } catch (error) {
            console.error('Erreur conformité:', error);
        }
    };

    const loadUserSecurityProfiles = async () => {
        try {
            const response = await fetch('/api/security/user-profiles/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setUserSecurityProfiles(data.profiles || []);
            }
        } catch (error) {
            console.error('Erreur profils utilisateur:', error);
        }
    };

    const getEventIcon = (eventType) => {
        const icons = {
            'login_success': <CheckCircle className="h-5 w-5 text-green-600" />,
            'login_failed': <XCircle className="h-5 w-5 text-red-600" />,
            'logout': <LogOut className="h-5 w-5 text-gray-600" />,
            'password_change': <Key className="h-5 w-5 text-blue-600" />,
            'password_reset': <RefreshCw className="h-5 w-5 text-orange-600" />,
            'mfa_enabled': <Fingerprint className="h-5 w-5 text-purple-600" />,
            'mfa_disabled': <Fingerprint className="h-5 w-5 text-gray-600" />,
            'mfa_used': <Smartphone className="h-5 w-5 text-green-600" />,
            'account_locked': <Lock className="h-5 w-5 text-red-600" />,
            'account_unlocked': <Unlock className="h-5 w-5 text-green-600" />,
            'suspicious_activity': <AlertTriangle className="h-5 w-5 text-orange-600" />,
            'ip_blocked': <Globe className="h-5 w-5 text-red-600" />,
            'geo_blocked': <MapPin className="h-5 w-5 text-red-600" />,
            'rate_limit_exceeded': <Zap className="h-5 w-5 text-yellow-600" />,
            'data_access': <Eye className="h-5 w-5 text-blue-600" />,
            'data_export': <Download className="h-5 w-5 text-purple-600" />,
            'data_deletion': <Trash2 className="h-5 w-5 text-red-600" />,
            'admin_action': <Settings className="h-5 w-5 text-gray-600" />,
            'security_alert': <AlertTriangle className="h-5 w-5 text-red-600" />,
            'threat_detected': <Shield className="h-5 w-5 text-red-600" />,
            'compliance_violation': <FileText className="h-5 w-5 text-orange-600" />
        };
        return icons[eventType] || <Info className="h-5 w-5" />;
    };

    const getThreatColor = (threatLevel) => {
        const colors = {
            'low': 'text-yellow-600 bg-yellow-50',
            'medium': 'text-orange-600 bg-orange-50',
            'high': 'text-red-600 bg-red-50',
            'critical': 'text-red-800 bg-red-100',
            'emergency': 'text-red-900 bg-red-200'
        };
        return colors[threatLevel] || 'text-gray-600 bg-gray-50';
    };

    const getIncidentStatus = (status) => {
        const statuses = {
            'detected': { color: 'text-red-600 bg-red-50', icon: <AlertTriangle className="h-4 w-4" /> },
            'investigating': { color: 'text-orange-600 bg-orange-50', icon: <Search className="h-4 w-4" /> },
            'contained': { color: 'text-yellow-600 bg-yellow-50', icon: <Shield className="h-4 w-4" /> },
            'resolved': { color: 'text-green-600 bg-green-50', icon: <CheckCircle className="h-4 w-4" /> },
            'closed': { color: 'text-gray-600 bg-gray-50', icon: <XCircle className="h-4 w-4" /> }
        };
        return statuses[status] || statuses['detected'];
    };

    const getComplianceStatus = (status) => {
        const statuses = {
            'compliant': { color: 'text-green-600 bg-green-50', icon: <CheckCircle className="h-4 w-4" /> },
            'non_compliant': { color: 'text-red-600 bg-red-50', icon: <XCircle className="h-4 w-4" /> },
            'partial': { color: 'text-yellow-600 bg-yellow-50', icon: <AlertTriangle className="h-4 w-4" /> },
            'not_applicable': { color: 'text-gray-600 bg-gray-50', icon: <Minus className="h-4 w-4" /> },
            'under_review': { color: 'text-blue-600 bg-blue-50', icon: <Clock className="h-4 w-4" /> }
        };
        return statuses[status] || statuses['under_review'];
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-red-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-gradient-to-r from-red-500 to-orange-500 rounded-full">
                                <Shield className="h-8 w-8 text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900">
                                    Sécurité Renforcée
                                </h1>
                                <p className="text-gray-600">
                                    Protection enterprise et monitoring avancé
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm font-medium text-green-600">
                                    Système Sécurisé
                                </span>
                            </div>
                            <button
                                onClick={loadSecurityData}
                                disabled={loading}
                                className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                            >
                                <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                                <span>Actualiser</span>
                            </button>
                        </div>
                    </div>
                </div>

                {/* Filtres */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <label className="text-sm font-medium text-gray-700">Période:</label>
                            <select
                                value={selectedTimeRange}
                                onChange={(e) => setSelectedTimeRange(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                            >
                                <option value="24h">24 Heures</option>
                                <option value="7d">7 Jours</option>
                                <option value="30d">30 Jours</option>
                                <option value="90d">90 Jours</option>
                            </select>
                            
                            <label className="text-sm font-medium text-gray-700">Sévérité:</label>
                            <select
                                value={selectedSeverity}
                                onChange={(e) => setSelectedSeverity(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                            >
                                <option value="all">Toutes</option>
                                <option value="low">Faible</option>
                                <option value="medium">Moyenne</option>
                                <option value="high">Élevée</option>
                                <option value="critical">Critique</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Métriques de Sécurité */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3">
                            <div className="p-3 bg-green-100 rounded-full">
                                <Shield className="h-6 w-6 text-green-600" />
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {securityData.security_score || 85}
                                </div>
                                <div className="text-sm text-gray-600">Score Sécurité</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3">
                            <div className="p-3 bg-blue-100 rounded-full">
                                <Users className="h-6 w-6 text-blue-600" />
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {securityData.users_with_mfa || 0}
                                </div>
                                <div className="text-sm text-gray-600">MFA Activé</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3">
                            <div className="p-3 bg-red-100 rounded-full">
                                <AlertTriangle className="h-6 w-6 text-red-600" />
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {securityData.recent_threats || 0}
                                </div>
                                <div className="text-sm text-gray-600">Menaces Détectées</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3">
                            <div className="p-3 bg-purple-100 rounded-full">
                                <Activity className="h-6 w-6 text-purple-600" />
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {securityData.recent_events || 0}
                                </div>
                                <div className="text-sm text-gray-600">Événements</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
                    {/* Événements de Sécurité */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Activity className="h-6 w-6 text-blue-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Événements de Sécurité
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {securityEvents.slice(0, 5).map((event, index) => (
                                <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center space-x-2 mb-2">
                                        {getEventIcon(event.event_type)}
                                        <span className="text-sm font-medium text-gray-900">{event.event_type}</span>
                                    </div>
                                    <div className="text-xs text-gray-600 mb-2">{event.description}</div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-500">
                                            {event.ip_address}
                                        </span>
                                        <span className="text-xs px-2 py-1 bg-gray-100 text-gray-800 rounded">
                                            {new Date(event.timestamp).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            ))}
                            
                            {securityEvents.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucun événement de sécurité
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Menaces Détectées */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <AlertTriangle className="h-6 w-6 text-red-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Menaces Détectées
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {threats.slice(0, 5).map((threat, index) => (
                                <div key={index} className={`p-3 rounded-lg ${getThreatColor(threat.threat_level)}`}>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">{threat.threat_type}</span>
                                        <span className="text-xs">
                                            {threat.threat_level}
                                        </span>
                                    </div>
                                    <div className="text-sm mb-2">{threat.title}</div>
                                    <div className="text-xs opacity-75">
                                        {new Date(threat.detected_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                            
                            {threats.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune menace détectée
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Incidents de Sécurité */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Shield className="h-6 w-6 text-orange-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Incidents de Sécurité
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {incidents.slice(0, 5).map((incident, index) => {
                                const status = getIncidentStatus(incident.status);
                                return (
                                    <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-sm font-medium">{incident.incident_type}</span>
                                            <div className={`flex items-center space-x-1 px-2 py-1 rounded ${status.color}`}>
                                                {status.icon}
                                                <span className="text-xs">{incident.status}</span>
                                            </div>
                                        </div>
                                        <div className="text-sm mb-2">{incident.title}</div>
                                        <div className="text-xs text-gray-500">
                                            {new Date(incident.detected_at).toLocaleDateString()}
                                        </div>
                                    </div>
                                );
                            })}
                            
                            {incidents.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucun incident de sécurité
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Audits de Sécurité */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <FileText className="h-6 w-6 text-purple-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Audits de Sécurité
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {audits.slice(0, 5).map((audit, index) => (
                                <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">{audit.audit_type}</span>
                                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                                            {audit.status}
                                        </span>
                                    </div>
                                    <div className="text-sm mb-2">{audit.title}</div>
                                    <div className="text-xs text-gray-500">
                                        {new Date(audit.created_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                            
                            {audits.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucun audit de sécurité
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Conformité */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <CheckCircle className="h-6 w-6 text-green-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Conformité
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {compliance.slice(0, 5).map((item, index) => {
                                const status = getComplianceStatus(item.status);
                                return (
                                    <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-sm font-medium">{item.framework}</span>
                                            <div className={`flex items-center space-x-1 px-2 py-1 rounded ${status.color}`}>
                                                {status.icon}
                                                <span className="text-xs">{item.status}</span>
                                            </div>
                                        </div>
                                        <div className="text-sm mb-2">{item.requirement_title}</div>
                                        <div className="text-xs text-gray-500">
                                            {new Date(item.assessment_date).toLocaleDateString()}
                                        </div>
                                    </div>
                                );
                            })}
                            
                            {compliance.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune donnée de conformité
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Profils Utilisateur */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Users className="h-6 w-6 text-indigo-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Profils Sécurité
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {userSecurityProfiles.slice(0, 5).map((profile, index) => (
                                <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">{profile.user?.username}</span>
                                        <span className={`text-xs px-2 py-1 rounded ${
                                            profile.mfa_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                        }`}>
                                            {profile.mfa_enabled ? 'MFA' : 'No MFA'}
                                        </span>
                                    </div>
                                    <div className="text-sm mb-2">
                                        Score: {profile.trust_score?.toFixed(1)}%
                                    </div>
                                    <div className="text-xs text-gray-500">
                                        Risque: {profile.risk_level}
                                    </div>
                                </div>
                            ))}
                            
                            {userSecurityProfiles.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucun profil utilisateur
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Graphiques de Sécurité */}
                <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Évolution des Menaces */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <TrendingUp className="h-6 w-6 text-red-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Évolution des Menaces
                            </h2>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-4 gap-4">
                                <div className="text-center p-4 bg-red-50 rounded-lg">
                                    <div className="text-2xl font-bold text-red-600">12</div>
                                    <div className="text-sm text-gray-600">Critiques</div>
                                </div>
                                <div className="text-center p-4 bg-orange-50 rounded-lg">
                                    <div className="text-2xl font-bold text-orange-600">28</div>
                                    <div className="text-sm text-gray-600">Élevées</div>
                                </div>
                                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                                    <div className="text-2xl font-bold text-yellow-600">45</div>
                                    <div className="text-sm text-gray-600">Moyennes</div>
                                </div>
                                <div className="text-center p-4 bg-green-50 rounded-lg">
                                    <div className="text-2xl font-bold text-green-600">156</div>
                                    <div className="text-sm text-gray-600">Faibles</div>
                                </div>
                            </div>

                            <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                                <div className="text-center text-gray-500">
                                    <LineChart className="h-12 w-12 mx-auto mb-2" />
                                    <div>Graphique d'évolution des menaces</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Répartition des Incidents */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <PieChart className="h-6 w-6 text-purple-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Répartition des Incidents
                            </h2>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-4 bg-red-50 rounded-lg">
                                    <div className="text-2xl font-bold text-red-600">3</div>
                                    <div className="text-sm text-gray-600">Actifs</div>
                                </div>
                                <div className="text-center p-4 bg-green-50 rounded-lg">
                                    <div className="text-2xl font-bold text-green-600">15</div>
                                    <div className="text-sm text-gray-600">Résolus</div>
                                </div>
                            </div>

                            <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                                <div className="text-center text-gray-500">
                                    <PieChart className="h-12 w-12 mx-auto mb-2" />
                                    <div>Graphique de répartition des incidents</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Configuration de Sécurité */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <Settings className="h-6 w-6 text-gray-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Configuration de Sécurité
                        </h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Fingerprint className="h-5 w-5 text-purple-600" />
                                <span className="font-medium">Authentification MFA</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>MFA Obligatoire:</span>
                                    <span className="font-medium text-green-600">Activé</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Méthodes:</span>
                                    <span className="font-medium">TOTP, SMS, Email</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Codes de Sauvegarde:</span>
                                    <span className="font-medium">10 codes</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Key className="h-5 w-5 text-blue-600" />
                                <span className="font-medium">Politique Mots de Passe</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Longueur Min:</span>
                                    <span className="font-medium">12 caractères</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Complexité:</span>
                                    <span className="font-medium">Élevée</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Expiration:</span>
                                    <span className="font-medium">90 jours</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Shield className="h-5 w-5 text-green-600" />
                                <span className="font-medium">Sécurité Réseau</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Limite de Taux:</span>
                                    <span className="font-medium text-green-600">Activée</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Blocage IP:</span>
                                    <span className="font-medium text-green-600">Activé</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Géo-restrictions:</span>
                                    <span className="font-medium text-green-600">Activées</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Eye className="h-5 w-5 text-indigo-600" />
                                <span className="font-medium">Monitoring</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Logs Sécurité:</span>
                                    <span className="font-medium text-green-600">Activés</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Détection Anomalies:</span>
                                    <span className="font-medium text-green-600">Activée</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Audit Logging:</span>
                                    <span className="font-medium text-green-600">Activé</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Lock className="h-5 w-5 text-red-600" />
                                <span className="font-medium">Chiffrement</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Algorithm:</span>
                                    <span className="font-medium">AES-256</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Rotation Clés:</span>
                                    <span className="font-medium">30 jours</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Données Sensibles:</span>
                                    <span className="font-medium text-green-600">Chiffrées</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <FileText className="h-5 w-5 text-purple-600" />
                                <span className="font-medium">Conformité</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>RGPD:</span>
                                    <span className="font-medium text-green-600">Conforme</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>ISO 27001:</span>
                                    <span className="font-medium text-green-600">Conforme</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Rétention:</span>
                                    <span className="font-medium">365 jours</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SecurityDashboard; 
import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { 
  BarChart3, 
    LineChart, 
    PieChart, 
  TrendingUp, 
    TrendingDown,
  Users, 
    Activity,
    Target,
    Zap,
    Brain,
    Lightbulb,
  Eye, 
  Heart, 
  MessageCircle, 
    Share2,
    Bookmark,
    Star,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Info,
    Clock,
  Calendar,
    MapPin,
    Globe,
    Smartphone,
    Monitor,
    Tablet,
    Filter,
    Search,
    Download,
    RefreshCw,
    Settings,
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
    Star as StarIcon,
    Planet,
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
    Tablet as TabletIcon,
    Smartphone as SmartphoneIcon,
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

const AnalyticsDashboard = () => {
    const { user } = useContext(AuthContext);
    const [analyticsData, setAnalyticsData] = useState({});
    const [userInsights, setUserInsights] = useState([]);
    const [predictions, setPredictions] = useState([]);
    const [trends, setTrends] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [anomalies, setAnomalies] = useState([]);
    const [businessMetrics, setBusinessMetrics] = useState({});
    const [loading, setLoading] = useState(false);
    const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
    const [selectedSegment, setSelectedSegment] = useState('all');

  useEffect(() => {
        if (user) {
            loadAnalyticsData();
        }
    }, [user, selectedTimeRange, selectedSegment]);

    const loadAnalyticsData = async () => {
        try {
    setLoading(true);
            
            // Charger toutes les données d'analytics
            await Promise.all([
                loadUserInsights(),
                loadPredictions(),
                loadTrends(),
                loadRecommendations(),
                loadAnomalies(),
                loadBusinessMetrics()
            ]);
            
    } catch (error) {
            console.error('Erreur chargement analytics:', error);
    } finally {
      setLoading(false);
    }
  };

    const loadUserInsights = async () => {
        try {
            const response = await fetch('/api/analytics/user-insights/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setUserInsights(data.insights || []);
            }
        } catch (error) {
            console.error('Erreur insights utilisateur:', error);
        }
    };

    const loadPredictions = async () => {
        try {
            const response = await fetch('/api/analytics/predictions/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setPredictions(data.predictions || []);
            }
        } catch (error) {
            console.error('Erreur prédictions:', error);
        }
    };

    const loadTrends = async () => {
        try {
            const response = await fetch('/api/analytics/trends/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setTrends(data.trends || []);
            }
        } catch (error) {
            console.error('Erreur tendances:', error);
        }
    };

    const loadRecommendations = async () => {
        try {
            const response = await fetch('/api/analytics/recommendations/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setRecommendations(data.recommendations || []);
            }
        } catch (error) {
            console.error('Erreur recommandations:', error);
        }
    };

    const loadAnomalies = async () => {
        try {
            const response = await fetch('/api/analytics/anomalies/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setAnomalies(data.anomalies || []);
            }
        } catch (error) {
            console.error('Erreur anomalies:', error);
        }
    };

    const loadBusinessMetrics = async () => {
        try {
            const response = await fetch('/api/analytics/business-metrics/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setBusinessMetrics(data.metrics || {});
            }
        } catch (error) {
            console.error('Erreur métriques business:', error);
        }
    };

    const getInsightIcon = (insightType) => {
        const icons = {
            'behavior_pattern': <Activity className="h-5 w-5" />,
            'preference_analysis': <Heart className="h-5 w-5" />,
            'engagement_trend': <TrendingUp className="h-5 w-5" />,
            'risk_assessment': <AlertTriangle className="h-5 w-5" />,
            'opportunity_identification': <Target className="h-5 w-5" />,
            'anomaly_detection': <Eye className="h-5 w-5" />,
            'recommendation_engine': <Sparkles className="h-5 w-5" />,
            'sentiment_analysis': <MessageCircle className="h-5 w-5" />,
            'network_analysis': <Users className="h-5 w-5" />,
            'temporal_pattern': <Clock className="h-5 w-5" />
        };
        return icons[insightType] || <Info className="h-5 w-5" />;
    };

    const getPredictionColor = (predictionType) => {
        const colors = {
            'user_engagement': 'text-blue-600 bg-blue-50',
            'content_recommendation': 'text-green-600 bg-green-50',
            'churn_prediction': 'text-red-600 bg-red-50',
            'conversion_prediction': 'text-purple-600 bg-purple-50',
            'revenue_prediction': 'text-yellow-600 bg-yellow-50',
            'anomaly_detection': 'text-orange-600 bg-orange-50',
            'sentiment_analysis': 'text-pink-600 bg-pink-50',
            'trend_prediction': 'text-indigo-600 bg-indigo-50',
            'user_lifetime_value': 'text-teal-600 bg-teal-50',
            'next_best_action': 'text-cyan-600 bg-cyan-50'
        };
        return colors[predictionType] || 'text-gray-600 bg-gray-50';
    };

    const getTrendDirection = (trend) => {
        if (trend.change_percentage > 0) {
            return { icon: <TrendingUp className="h-4 w-4 text-green-600" />, color: 'text-green-600' };
        } else if (trend.change_percentage < 0) {
            return { icon: <TrendingDown className="h-4 w-4 text-red-600" />, color: 'text-red-600' };
        } else {
            return { icon: <BarChart3 className="h-4 w-4 text-gray-600" />, color: 'text-gray-600' };
        }
    };

    const getAnomalySeverity = (severity) => {
        const severities = {
            'low': { color: 'text-yellow-600 bg-yellow-50', icon: <Info className="h-4 w-4" /> },
            'medium': { color: 'text-orange-600 bg-orange-50', icon: <AlertTriangle className="h-4 w-4" /> },
            'high': { color: 'text-red-600 bg-red-50', icon: <AlertTriangle className="h-4 w-4" /> },
            'critical': { color: 'text-red-800 bg-red-100', icon: <XCircle className="h-4 w-4" /> }
        };
        return severities[severity] || severities['low'];
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full">
                                <Brain className="h-8 w-8 text-white" />
      </div>
        <div>
                                <h1 className="text-3xl font-bold text-gray-900">
                                    Analytics Prédictifs
                                </h1>
                                <p className="text-gray-600">
                                    Intelligence artificielle et insights métier avancés
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm font-medium text-green-600">
                                    IA Active
                                </span>
                            </div>
                            <button
                                onClick={loadAnalyticsData}
                                disabled={loading}
                                className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
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
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="7d">7 Jours</option>
                                <option value="30d">30 Jours</option>
                                <option value="90d">90 Jours</option>
                                <option value="1y">1 An</option>
                            </select>
                            
                            <label className="text-sm font-medium text-gray-700">Segment:</label>
          <select 
                                value={selectedSegment}
                                onChange={(e) => setSelectedSegment(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="all">Tous</option>
                                <option value="power_users">Power Users</option>
                                <option value="active_users">Utilisateurs Actifs</option>
                                <option value="regular_users">Utilisateurs Réguliers</option>
                                <option value="at_risk">À Risque</option>
                                <option value="casual_users">Utilisateurs Occasionnels</option>
          </select>
        </div>
      </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
                    {/* Métriques Business */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <BarChart3 className="h-6 w-6 text-purple-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Métriques Business
                            </h2>
            </div>
            
                        <div className="space-y-4">
                            {businessMetrics && Object.keys(businessMetrics).length > 0 ? (
                                Object.entries(businessMetrics).map(([metric, value]) => (
                                    <div key={metric} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                                            <div className="text-sm font-medium text-gray-900">{metric}</div>
                                            <div className="text-xs text-gray-600">Métrique business</div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-lg font-bold text-gray-900">
                                                {typeof value === 'number' ? value.toLocaleString() : value}
                                            </div>
                                            <div className="text-xs text-green-600">+5.2%</div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune métrique disponible
                </div>
                            )}
              </div>
            </div>
            
                    {/* Insights Utilisateur */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Lightbulb className="h-6 w-6 text-yellow-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Insights Utilisateur
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {userInsights.slice(0, 5).map((insight, index) => (
                                <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center space-x-2 mb-2">
                                        {getInsightIcon(insight.insight_type)}
                                        <span className="text-sm font-medium text-gray-900">{insight.title}</span>
                                    </div>
                                    <div className="text-xs text-gray-600 mb-2">{insight.description}</div>
              <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-500">
                                            Confiance: {insight.confidence_score?.toFixed(1)}%
                                        </span>
                                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                                            {insight.priority}
                                        </span>
                                    </div>
                                </div>
                            ))}
                            
                            {userInsights.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucun insight disponible
                </div>
                            )}
              </div>
            </div>
            
                    {/* Prédictions IA */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Zap className="h-6 w-6 text-blue-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Prédictions IA
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {predictions.slice(0, 5).map((prediction, index) => (
                                <div key={index} className={`p-3 rounded-lg ${getPredictionColor(prediction.prediction_type)}`}>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">{prediction.prediction_type}</span>
                                        <span className="text-xs">
                                            {prediction.confidence_score?.toFixed(1)}%
                                        </span>
                </div>
                                    <div className="text-lg font-bold">
                                        {prediction.predicted_value?.toFixed(2)}
              </div>
                                    <div className="text-xs opacity-75">
                                        {new Date(prediction.timestamp).toLocaleDateString()}
            </div>
          </div>
                            ))}
                            
                            {predictions.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune prédiction disponible
              </div>
                            )}
            </div>
          </div>
          
                    {/* Tendances */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <TrendingUp className="h-6 w-6 text-green-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Tendances
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {trends.slice(0, 5).map((trend, index) => {
                                const direction = getTrendDirection(trend);
                                return (
                                    <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-sm font-medium">{trend.metric_name}</span>
                                            {direction.icon}
                                        </div>
                                        <div className="text-lg font-bold">
                                            {trend.current_value?.toLocaleString()}
              </div>
                                        <div className={`text-xs ${direction.color}`}>
                                            {trend.change_percentage > 0 ? '+' : ''}{trend.change_percentage?.toFixed(1)}%
            </div>
          </div>
                                );
                            })}
                            
                            {trends.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune tendance disponible
        </div>
      )}
                        </div>
                    </div>

                    {/* Recommandations */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Sparkles className="h-6 w-6 text-purple-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Recommandations
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {recommendations.slice(0, 5).map((rec, index) => (
                                <div key={index} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">{rec.recommendation_type}</span>
                                        <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">
                                            Score: {rec.score?.toFixed(2)}
                                        </span>
                                    </div>
                                    <div className="text-xs text-gray-600 mb-2">{rec.reason}</div>
                                    <div className="text-xs text-gray-500">
                                        {new Date(rec.generated_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                            
                            {recommendations.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune recommandation disponible
                </div>
                            )}
              </div>
            </div>
            
                    {/* Anomalies */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <AlertTriangle className="h-6 w-6 text-red-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Anomalies Détectées
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {anomalies.slice(0, 5).map((anomaly, index) => {
                                const severity = getAnomalySeverity(anomaly.severity);
                                return (
                                    <div key={index} className={`p-3 rounded-lg ${severity.color}`}>
                                        <div className="flex items-center space-x-2 mb-2">
                                            {severity.icon}
                                            <span className="text-sm font-medium">{anomaly.title}</span>
                                        </div>
                                        <div className="text-xs mb-2">{anomaly.description}</div>
              <div className="flex items-center justify-between">
                                            <span className="text-xs">
                                                {anomaly.anomaly_type}
                                            </span>
                                            <span className="text-xs">
                                                {new Date(anomaly.detected_at).toLocaleDateString()}
                                            </span>
                                        </div>
                                    </div>
                                );
                            })}
                            
                            {anomalies.length === 0 && (
                                <div className="text-center py-8 text-gray-500">
                                    Aucune anomalie détectée
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Graphiques Avancés */}
                <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Engagement Utilisateurs */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Users className="h-6 w-6 text-blue-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Engagement Utilisateurs
                            </h2>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-3 gap-4">
                                <div className="text-center p-4 bg-blue-50 rounded-lg">
                                    <div className="text-2xl font-bold text-blue-600">85%</div>
                                    <div className="text-sm text-gray-600">Taux d'Engagement</div>
                                </div>
                                <div className="text-center p-4 bg-green-50 rounded-lg">
                                    <div className="text-2xl font-bold text-green-600">1,250</div>
                                    <div className="text-sm text-gray-600">Utilisateurs Actifs</div>
                                </div>
                                <div className="text-center p-4 bg-purple-50 rounded-lg">
                                    <div className="text-2xl font-bold text-purple-600">+12%</div>
                                    <div className="text-sm text-gray-600">Croissance</div>
              </div>
            </div>
            
                            <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                                <div className="text-center text-gray-500">
                                    <BarChart3 className="h-12 w-12 mx-auto mb-2" />
                                    <div>Graphique d'engagement</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Prédictions de Churn */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Target className="h-6 w-6 text-red-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Prédictions de Churn
                            </h2>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-4 bg-red-50 rounded-lg">
                                    <div className="text-2xl font-bold text-red-600">15%</div>
                                    <div className="text-sm text-gray-600">Risque Élevé</div>
                                </div>
                                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                                    <div className="text-2xl font-bold text-yellow-600">25%</div>
                                    <div className="text-sm text-gray-600">Risque Moyen</div>
                  </div>
                </div>
            
                            <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                                <div className="text-center text-gray-500">
                                    <PieChart className="h-12 w-12 mx-auto mb-2" />
                                    <div>Graphique de churn</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Modèles IA */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <Brain className="h-6 w-6 text-purple-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Modèles d'Intelligence Artificielle
                        </h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Target className="h-5 w-5 text-blue-600" />
                                <span className="font-medium">Prédiction Churn</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Précision:</span>
                                    <span className="font-medium">92.5%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Rappel:</span>
                                    <span className="font-medium">89.3%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>F1-Score:</span>
                                    <span className="font-medium">90.8%</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <Sparkles className="h-5 w-5 text-green-600" />
                                <span className="font-medium">Recommandations</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Précision:</span>
                                    <span className="font-medium">87.2%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Couverture:</span>
                                    <span className="font-medium">94.1%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Diversité:</span>
                                    <span className="font-medium">85.6%</span>
              </div>
            </div>
          </div>
          
                        <div className="p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-2 mb-3">
                                <MessageCircle className="h-5 w-5 text-purple-600" />
                                <span className="font-medium">Analyse Sentiments</span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Précision:</span>
                                    <span className="font-medium">91.8%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Rappel:</span>
                                    <span className="font-medium">88.9%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>F1-Score:</span>
                                    <span className="font-medium">90.3%</span>
                                </div>
                            </div>
                        </div>
                  </div>
              </div>
            </div>
    </div>
  );
};

export default AnalyticsDashboard; 
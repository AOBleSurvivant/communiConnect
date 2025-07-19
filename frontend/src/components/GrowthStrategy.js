import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  TrendingUp, 
  Users, 
  Target, 
  Award, 
  Star, 
  Gift, 
  Share, 
  MessageCircle,
  Calendar,
  MapPin,
  Globe,
  Zap,
  Rocket,
  Lightbulb,
  CheckCircle,
  AlertCircle,
  Info,
  BarChart3,
  PieChart,
  Activity,
  Eye,
  Heart,
  Download,
  Upload,
  ExternalLink,
  Mail,
  Phone,
  Video,
  Camera,
  Mic,
  Settings,
  Bell,
  User,
  Shield,
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
  Music,
  FileText,
  Clock,
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
  Type as TypeIcon,
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
  Half
} from 'lucide-react';
import toast from 'react-hot-toast';

const GrowthStrategy = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('analytics');
  const [growthMetrics, setGrowthMetrics] = useState({});
  const [userEngagement, setUserEngagement] = useState({});
  const [contentPerformance, setContentPerformance] = useState({});
  const [communityGrowth, setCommunityGrowth] = useState({});
  const [monetizationData, setMonetizationData] = useState({});
  const [marketingCampaigns, setMarketingCampaigns] = useState([]);
  const [partnerships, setPartnerships] = useState([]);
  const [expansionPlans, setExpansionPlans] = useState([]);

  useEffect(() => {
    loadGrowthData();
  }, []);

  const loadGrowthData = async () => {
    try {
      // Simuler le chargement des données de croissance
      setGrowthMetrics({
        totalUsers: 15420,
        activeUsers: 8234,
        newUsers: 456,
        retentionRate: 78.5,
        growthRate: 12.3,
        targetUsers: 50000
      });

      setUserEngagement({
        dailyActive: 2341,
        weeklyActive: 5678,
        monthlyActive: 8234,
        averageSessionTime: 24.5,
        postsPerUser: 3.2,
        interactionsPerUser: 8.7
      });

      setContentPerformance({
        totalPosts: 45678,
        averageLikes: 23.4,
        averageComments: 5.6,
        averageShares: 2.1,
        viralPosts: 156,
        trendingTopics: 45
      });

      setCommunityGrowth({
        totalCommunities: 234,
        activeCommunities: 189,
        averageMembers: 45.6,
        communityEvents: 89,
        localPartnerships: 34
      });

      setMonetizationData({
        revenue: 45600,
        premiumUsers: 234,
        adRevenue: 12300,
        partnershipRevenue: 8900,
        targetRevenue: 100000
      });

      setMarketingCampaigns([
        { id: 1, name: 'Campagne Facebook', status: 'active', budget: 5000, reach: 45000, conversions: 234 },
        { id: 2, name: 'Influenceurs locaux', status: 'completed', budget: 3000, reach: 25000, conversions: 156 },
        { id: 3, name: 'Événements communautaires', status: 'planned', budget: 2000, reach: 15000, conversions: 89 }
      ]);

      setPartnerships([
        { id: 1, name: 'Mairie de Conakry', type: 'government', status: 'active', impact: 'high' },
        { id: 2, name: 'Université Gamal Abdel Nasser', type: 'education', status: 'active', impact: 'medium' },
        { id: 3, name: 'Chambre de Commerce', type: 'business', status: 'negotiating', impact: 'high' }
      ]);

      setExpansionPlans([
        { id: 1, city: 'Kankan', population: 200000, readiness: 85, timeline: 'Q2 2024' },
        { id: 2, city: 'Kindia', population: 150000, readiness: 72, timeline: 'Q3 2024' },
        { id: 3, city: 'Labé', population: 120000, readiness: 68, timeline: 'Q4 2024' }
      ]);
    } catch (error) {
      console.error('Erreur lors du chargement des données de croissance:', error);
      toast.error('Erreur lors du chargement des données de croissance');
    }
  };

  const renderAnalyticsTab = () => (
    <div className="space-y-6">
      {/* Métriques de croissance */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Métriques de croissance</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.totalUsers?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Utilisateurs totaux</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <Activity className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.activeUsers?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Utilisateurs actifs</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.growthRate}%</div>
            <div className="text-sm text-gray-600">Taux de croissance</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <Target className="w-8 h-8 text-orange-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.retentionRate}%</div>
            <div className="text-sm text-gray-600">Rétention</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <User className="w-8 h-8 text-red-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.newUsers}</div>
            <div className="text-sm text-gray-600">Nouveaux utilisateurs</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <Award className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{growthMetrics.targetUsers?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Objectif</div>
          </div>
        </div>
      </div>

      {/* Engagement utilisateur */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Engagement utilisateur</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium mb-2">Utilisateurs actifs</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Quotidien</span>
                <span className="font-semibold">{userEngagement.dailyActive?.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Hebdomadaire</span>
                <span className="font-semibold">{userEngagement.weeklyActive?.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Mensuel</span>
                <span className="font-semibold">{userEngagement.monthlyActive?.toLocaleString()}</span>
              </div>
            </div>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium mb-2">Activité</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Temps de session</span>
                <span className="font-semibold">{userEngagement.averageSessionTime} min</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Posts/utilisateur</span>
                <span className="font-semibold">{userEngagement.postsPerUser}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Interactions/utilisateur</span>
                <span className="font-semibold">{userEngagement.interactionsPerUser}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderMarketingTab = () => (
    <div className="space-y-6">
      {/* Campagnes marketing */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Campagnes marketing</h3>
        <div className="space-y-4">
          {marketingCampaigns.map(campaign => (
            <div key={campaign.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-semibold">{campaign.name}</h4>
                  <p className="text-sm text-gray-600">
                    Budget: ${campaign.budget?.toLocaleString()} • 
                    Portée: {campaign.reach?.toLocaleString()} • 
                    Conversions: {campaign.conversions}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs rounded-full ${
                  campaign.status === 'active' ? 'bg-green-100 text-green-800' :
                  campaign.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {campaign.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Partenariats */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Partenariats stratégiques</h3>
        <div className="space-y-4">
          {partnerships.map(partnership => (
            <div key={partnership.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Globe className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <h4 className="font-semibold">{partnership.name}</h4>
                  <p className="text-sm text-gray-600">
                    Type: {partnership.type} • 
                    Impact: {partnership.impact}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs rounded-full ${
                  partnership.status === 'active' ? 'bg-green-100 text-green-800' :
                  partnership.status === 'negotiating' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {partnership.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderExpansionTab = () => (
    <div className="space-y-6">
      {/* Plans d'expansion */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Plans d'expansion</h3>
        <div className="space-y-4">
          {expansionPlans.map(plan => (
            <div key={plan.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <MapPin className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h4 className="font-semibold">{plan.city}</h4>
                  <p className="text-sm text-gray-600">
                    Population: {plan.population?.toLocaleString()} • 
                    Préparation: {plan.readiness}% • 
                    Timeline: {plan.timeline}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-600 h-2 rounded-full" 
                    style={{ width: `${plan.readiness}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium">{plan.readiness}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderMonetizationTab = () => (
    <div className="space-y-6">
      {/* Données de monétisation */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Monétisation</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <Dollar className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">${monetizationData.revenue?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Revenus totaux</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <User className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">{monetizationData.premiumUsers}</div>
            <div className="text-sm text-gray-600">Utilisateurs premium</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <BarChart3 className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">${monetizationData.adRevenue?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Revenus publicitaires</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <Target className="w-8 h-8 text-orange-600 mx-auto mb-2" />
            <div className="text-2xl font-bold">${monetizationData.targetRevenue?.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Objectif revenus</div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Onglets */}
      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-6">
        {[
          { id: 'analytics', label: 'Analytics', icon: BarChart3 },
          { id: 'marketing', label: 'Marketing', icon: TrendingUp },
          { id: 'expansion', label: 'Expansion', icon: Globe },
          { id: 'monetization', label: 'Monétisation', icon: Dollar }
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                activeTab === tab.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'analytics' && renderAnalyticsTab()}
      {activeTab === 'marketing' && renderMarketingTab()}
      {activeTab === 'expansion' && renderExpansionTab()}
      {activeTab === 'monetization' && renderMonetizationTab()}
    </div>
  );
};

export default GrowthStrategy; 
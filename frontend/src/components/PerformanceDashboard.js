import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { 
    Activity, 
    Zap, 
    Database, 
    HardDrive, 
    Cpu, 
    Memory, 
    Network, 
    AlertTriangle,
    TrendingUp,
    TrendingDown,
    Clock,
    BarChart3,
    Settings,
    Play,
    Pause,
    RefreshCw,
    AlertCircle,
    CheckCircle,
    XCircle,
    Info,
    Gauge,
    Server,
    Globe,
    Shield,
    Rocket
} from 'lucide-react';

const PerformanceDashboard = () => {
    const { user } = useContext(AuthContext);
    const [performanceMetrics, setPerformanceMetrics] = useState({});
    const [systemResources, setSystemResources] = useState({});
    const [cachePerformance, setCachePerformance] = useState({});
    const [slowQueries, setSlowQueries] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [autoScalingStatus, setAutoScalingStatus] = useState({});
    const [reports, setReports] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [isMonitoring, setIsMonitoring] = useState(false);
    const [loading, setLoading] = useState(false);
    const [selectedTimeRange, setSelectedTimeRange] = useState('24h');

    useEffect(() => {
        if (user) {
            loadPerformanceData();
            startRealTimeUpdates();
        }
    }, [user, selectedTimeRange]);

    const loadPerformanceData = async () => {
        try {
            setLoading(true);
            
            // Charger toutes les données de performance
            await Promise.all([
                loadPerformanceMetrics(),
                loadSystemResources(),
                loadCachePerformance(),
                loadSlowQueries(),
                loadAlerts(),
                loadAutoScalingStatus(),
                loadReports(),
                loadRecommendations()
            ]);
            
        } catch (error) {
            console.error('Erreur chargement données performance:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadPerformanceMetrics = async () => {
        try {
            const response = await fetch(`/api/performance/metrics/?hours=${getHoursFromRange(selectedTimeRange)}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setPerformanceMetrics(data);
            }
        } catch (error) {
            console.error('Erreur métriques performance:', error);
        }
    };

    const loadSystemResources = async () => {
        try {
            const response = await fetch('/api/performance/system-resources/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSystemResources(data);
            }
        } catch (error) {
            console.error('Erreur ressources système:', error);
        }
    };

    const loadCachePerformance = async () => {
        try {
            const response = await fetch('/api/performance/cache-performance/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setCachePerformance(data);
            }
        } catch (error) {
            console.error('Erreur performance cache:', error);
        }
    };

    const loadSlowQueries = async () => {
        try {
            const response = await fetch('/api/performance/slow-queries/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSlowQueries(data.slow_queries || []);
            }
        } catch (error) {
            console.error('Erreur requêtes lentes:', error);
        }
    };

    const loadAlerts = async () => {
        try {
            const response = await fetch('/api/performance/alerts/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setAlerts(data.alerts || []);
            }
        } catch (error) {
            console.error('Erreur alertes:', error);
        }
    };

    const loadAutoScalingStatus = async () => {
        try {
            const response = await fetch('/api/performance/auto-scaling-status/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setAutoScalingStatus(data);
            }
        } catch (error) {
            console.error('Erreur statut auto-scaling:', error);
        }
    };

    const loadReports = async () => {
        try {
            const response = await fetch('/api/performance/reports/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setReports(data.reports || []);
            }
        } catch (error) {
            console.error('Erreur rapports:', error);
        }
    };

    const loadRecommendations = async () => {
        try {
            const response = await fetch('/api/performance/recommendations/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setRecommendations([
                    ...(data.database_recommendations || []),
                    ...(data.system_recommendations || [])
                ]);
            }
        } catch (error) {
            console.error('Erreur recommandations:', error);
        }
    };

    const startRealTimeUpdates = () => {
        // Mettre à jour les données toutes les 30 secondes
        const interval = setInterval(() => {
            if (isMonitoring) {
                loadPerformanceData();
            }
        }, 30000);

        return () => clearInterval(interval);
    };

    const getHoursFromRange = (range) => {
        switch (range) {
            case '1h': return 1;
            case '6h': return 6;
            case '12h': return 12;
            case '24h': return 24;
            case '7d': return 168;
            default: return 24;
        }
    };

    const startMonitoring = async () => {
        try {
            const response = await fetch('/api/performance/start-monitoring/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                setIsMonitoring(true);
            }
        } catch (error) {
            console.error('Erreur démarrage monitoring:', error);
        }
    };

    const stopMonitoring = async () => {
        try {
            const response = await fetch('/api/performance/stop-monitoring/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                setIsMonitoring(false);
            }
        } catch (error) {
            console.error('Erreur arrêt monitoring:', error);
        }
    };

    const resolveAlert = async (alertId) => {
        try {
            const response = await fetch('/api/performance/resolve-alert/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ alert_id: alertId })
            });
            
            if (response.ok) {
                // Recharger les alertes
                loadAlerts();
            }
        } catch (error) {
            console.error('Erreur résolution alerte:', error);
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'critical': return 'text-red-600 bg-red-50';
            case 'high': return 'text-orange-600 bg-orange-50';
            case 'medium': return 'text-yellow-600 bg-yellow-50';
            case 'low': return 'text-blue-600 bg-blue-50';
            default: return 'text-gray-600 bg-gray-50';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'success': return <CheckCircle className="h-5 w-5 text-green-600" />;
            case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
            case 'error': return <XCircle className="h-5 w-5 text-red-600" />;
            default: return <Info className="h-5 w-5 text-blue-600" />;
        }
    };

    const formatBytes = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const formatPercentage = (value) => {
        return `${value.toFixed(1)}%`;
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full">
                                <Activity className="h-8 w-8 text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900">
                                    Dashboard Performance
                                </h1>
                                <p className="text-gray-600">
                                    Monitoring et optimisations avancées de CommuniConnect
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                                <div className={`w-3 h-3 rounded-full ${isMonitoring ? 'bg-green-500' : 'bg-red-500'}`}></div>
                                <span className="text-sm font-medium">
                                    {isMonitoring ? 'Monitoring Actif' : 'Monitoring Inactif'}
                                </span>
                            </div>
                            <div className="flex space-x-2">
                                <button
                                    onClick={startMonitoring}
                                    disabled={isMonitoring}
                                    className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50"
                                >
                                    <Play className="h-4 w-4" />
                                    <span>Démarrer</span>
                                </button>
                                <button
                                    onClick={stopMonitoring}
                                    disabled={!isMonitoring}
                                    className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                                >
                                    <Pause className="h-4 w-4" />
                                    <span>Arrêter</span>
                                </button>
                            </div>
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
                                <option value="1h">1 Heure</option>
                                <option value="6h">6 Heures</option>
                                <option value="12h">12 Heures</option>
                                <option value="24h">24 Heures</option>
                                <option value="7d">7 Jours</option>
                            </select>
                        </div>
                        <button
                            onClick={loadPerformanceData}
                            disabled={loading}
                            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                        >
                            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                            <span>Actualiser</span>
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
                    {/* Métriques de Performance */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Zap className="h-6 w-6 text-yellow-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Métriques Performance
                            </h2>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-4 bg-blue-50 rounded-lg">
                                    <div className="text-2xl font-bold text-blue-600">
                                        {performanceMetrics.statistics?.average?.toFixed(1) || '0.0'}
                                    </div>
                                    <div className="text-sm text-gray-600">Temps Réponse (ms)</div>
                                </div>
                                <div className="text-center p-4 bg-green-50 rounded-lg">
                                    <div className="text-2xl font-bold text-green-600">
                                        {performanceMetrics.statistics?.count || '0'}
                                    </div>
                                    <div className="text-sm text-gray-600">Requêtes</div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-600">Métriques collectées:</span>
                                    <span className="font-medium">{performanceMetrics.metrics?.length || 0}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-600">Période:</span>
                                    <span className="font-medium">{selectedTimeRange}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Ressources Système */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Server className="h-6 w-6 text-purple-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Ressources Système
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {systemResources.real_time_metrics && (
                                <>
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            <Cpu className="h-4 w-4 text-blue-600" />
                                            <span className="text-sm text-gray-600">CPU</span>
                                        </div>
                                        <span className="font-semibold">
                                            {formatPercentage(systemResources.real_time_metrics.cpu.usage_percent)}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div 
                                            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                            style={{ width: `${systemResources.real_time_metrics.cpu.usage_percent}%` }}
                                        ></div>
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            <Memory className="h-4 w-4 text-green-600" />
                                            <span className="text-sm text-gray-600">Mémoire</span>
                                        </div>
                                        <span className="font-semibold">
                                            {formatPercentage(systemResources.real_time_metrics.memory.percent)}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div 
                                            className="bg-green-600 h-2 rounded-full transition-all duration-300"
                                            style={{ width: `${systemResources.real_time_metrics.memory.percent}%` }}
                                        ></div>
                                    </div>

                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            <HardDrive className="h-4 w-4 text-orange-600" />
                                            <span className="text-sm text-gray-600">Disque</span>
                                        </div>
                                        <span className="font-semibold">
                                            {formatPercentage(systemResources.real_time_metrics.disk.percent)}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div 
                                            className="bg-orange-600 h-2 rounded-full transition-all duration-300"
                                            style={{ width: `${systemResources.real_time_metrics.disk.percent}%` }}
                                        ></div>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Performance Cache */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Database className="h-6 w-6 text-indigo-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Performance Cache
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {cachePerformance.global_statistics && (
                                <>
                                    <div className="text-center p-4 bg-indigo-50 rounded-lg">
                                        <div className="text-3xl font-bold text-indigo-600">
                                            {cachePerformance.global_statistics.average_hit_rate?.toFixed(1) || '0.0'}%
                                        </div>
                                        <div className="text-sm text-gray-600">Taux de Réussite</div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="text-center">
                                            <div className="text-lg font-semibold text-green-600">
                                                {cachePerformance.global_statistics.total_hits || '0'}
                                            </div>
                                            <div className="text-xs text-gray-600">Hits</div>
                                        </div>
                                        <div className="text-center">
                                            <div className="text-lg font-semibold text-red-600">
                                                {cachePerformance.global_statistics.total_misses || '0'}
                                            </div>
                                            <div className="text-xs text-gray-600">Misses</div>
                                        </div>
                                    </div>

                                    <div className="text-center">
                                        <div className="text-sm text-gray-600">
                                            Temps de réponse moyen
                                        </div>
                                        <div className="text-lg font-semibold text-gray-900">
                                            {cachePerformance.global_statistics.average_response_time?.toFixed(2) || '0.00'} ms
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Alertes */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <AlertTriangle className="h-6 w-6 text-red-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Alertes Performance
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {alerts.slice(0, 5).map((alert) => (
                                <div key={alert.id} className={`p-3 rounded-lg border ${getSeverityColor(alert.severity)}`}>
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            {getStatusIcon(alert.alert_type)}
                                            <span className="text-sm font-medium">{alert.title}</span>
                                        </div>
                                        {!alert.is_resolved && (
                                            <button
                                                onClick={() => resolveAlert(alert.id)}
                                                className="text-xs px-2 py-1 bg-white rounded hover:bg-gray-50"
                                            >
                                                Résoudre
                                            </button>
                                        )}
                                    </div>
                                    <div className="text-xs text-gray-600 mt-1">
                                        {alert.description}
                                    </div>
                                </div>
                            ))}
                            
                            {alerts.length === 0 && (
                                <div className="text-center py-4 text-gray-500">
                                    Aucune alerte active
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Auto-Scaling */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Rocket className="h-6 w-6 text-green-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Auto-Scaling
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {autoScalingStatus.global_status && (
                                <>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="text-center p-3 bg-green-50 rounded-lg">
                                            <div className="text-xl font-bold text-green-600">
                                                {autoScalingStatus.global_status.active_configs || '0'}
                                            </div>
                                            <div className="text-xs text-gray-600">Configs Actives</div>
                                        </div>
                                        <div className="text-center p-3 bg-blue-50 rounded-lg">
                                            <div className="text-xl font-bold text-blue-600">
                                                {autoScalingStatus.global_status.scaling_actions_needed || '0'}
                                            </div>
                                            <div className="text-xs text-gray-600">Actions Nécessaires</div>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        {autoScalingStatus.global_status.scaling_needs?.slice(0, 3).map((need, index) => (
                                            <div key={index} className="flex items-center justify-between p-2 bg-yellow-50 rounded">
                                                <span className="text-sm text-yellow-800">{need.action}</span>
                                                <span className="text-xs text-yellow-600">{need.priority}</span>
                                            </div>
                                        ))}
                                    </div>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Recommandations */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Settings className="h-6 w-6 text-gray-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Recommandations
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {recommendations.slice(0, 5).map((rec, index) => (
                                <div key={index} className="p-3 bg-gray-50 rounded-lg">
                                    <div className="flex items-center space-x-2 mb-1">
                                        <Info className="h-4 w-4 text-blue-600" />
                                        <span className="text-sm font-medium text-gray-900">{rec.title}</span>
                                    </div>
                                    <div className="text-xs text-gray-600">{rec.description}</div>
                                    <div className="mt-2">
                                        <span className={`text-xs px-2 py-1 rounded ${
                                            rec.priority === 'critical' ? 'bg-red-100 text-red-800' :
                                            rec.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                                            'bg-blue-100 text-blue-800'
                                        }`}>
                                            {rec.priority}
                                        </span>
                                    </div>
                                </div>
                            ))}
                            
                            {recommendations.length === 0 && (
                                <div className="text-center py-4 text-gray-500">
                                    Aucune recommandation
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Requêtes Lentes */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <Clock className="h-6 w-6 text-orange-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Requêtes Lentes
                        </h2>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Type</th>
                                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Temps Moyen</th>
                                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Exécutions</th>
                                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Optimisé</th>
                                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Dernière Vue</th>
                                </tr>
                            </thead>
                            <tbody>
                                {slowQueries.map((query) => (
                                    <tr key={query.query_hash} className="border-b border-gray-100">
                                        <td className="py-3 px-4 text-sm text-gray-900">{query.query_type}</td>
                                        <td className="py-3 px-4 text-sm text-gray-900">
                                            {query.avg_execution_time.toFixed(2)} ms
                                        </td>
                                        <td className="py-3 px-4 text-sm text-gray-900">{query.execution_count}</td>
                                        <td className="py-3 px-4">
                                            {query.is_optimized ? (
                                                <CheckCircle className="h-4 w-4 text-green-600" />
                                            ) : (
                                                <XCircle className="h-4 w-4 text-red-600" />
                                            )}
                                        </td>
                                        <td className="py-3 px-4 text-sm text-gray-600">
                                            {new Date(query.last_seen).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        
                        {slowQueries.length === 0 && (
                            <div className="text-center py-8 text-gray-500">
                                Aucune requête lente détectée
                            </div>
                        )}
                    </div>
                </div>

                {/* Rapports */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <BarChart3 className="h-6 w-6 text-purple-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Rapports de Performance
                        </h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {reports.slice(0, 6).map((report) => (
                            <div key={report.id} className="p-4 border border-gray-200 rounded-lg">
                                <div className="flex items-center justify-between mb-2">
                                    <h3 className="font-semibold text-gray-900">{report.title}</h3>
                                    <span className="text-xs text-gray-500">{report.report_type}</span>
                                </div>
                                
                                <div className="space-y-2 text-sm">
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Temps réponse:</span>
                                        <span className="font-medium">{report.avg_response_time.toFixed(2)} ms</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Requêtes:</span>
                                        <span className="font-medium">{report.total_requests.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Taux erreur:</span>
                                        <span className="font-medium">{report.error_rate.toFixed(2)}%</span>
                                    </div>
                                </div>
                                
                                <div className="mt-3 pt-3 border-t border-gray-100">
                                    <div className="text-xs text-gray-500">
                                        {new Date(report.generated_at).toLocaleDateString()}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    
                    {reports.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            Aucun rapport disponible
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PerformanceDashboard; 
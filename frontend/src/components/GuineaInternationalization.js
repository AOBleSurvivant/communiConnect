import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { 
    Globe, 
    Languages, 
    MapPin, 
    Settings, 
    Translate, 
    Users, 
    BarChart3,
    Flag,
    DollarSign,
    Shield,
    Clock,
    Globe2,
    CheckCircle,
    AlertCircle,
    Info
} from 'lucide-react';

const GuineaInternationalization = () => {
    const { user } = useContext(AuthContext);
    const [selectedLanguage, setSelectedLanguage] = useState('fr');
    const [selectedRegion, setSelectedRegion] = useState('conakry');
    const [translationStats, setTranslationStats] = useState({});
    const [culturalAdaptations, setCulturalAdaptations] = useState({});
    const [paymentMethods, setPaymentMethods] = useState([]);
    const [legalCompliance, setLegalCompliance] = useState([]);
    const [loading, setLoading] = useState(false);

    // Langues supportées pour la Guinée
    const supportedLanguages = [
        { code: 'fr', name: 'Français', native_name: 'Français', flag: '🇫🇷' },
        { code: 'en', name: 'English', native_name: 'English', flag: '🇬🇧' },
        { code: 'ar', name: 'العربية', native_name: 'العربية', flag: '🇸🇦' }
    ];

    // Régions de la Guinée
    const guineaRegions = [
        { code: 'conakry', name: 'Conakry', name_ar: 'كوناكري', name_en: 'Conakry' },
        { code: 'kindia', name: 'Kindia', name_ar: 'كنديا', name_en: 'Kindia' },
        { code: 'kankan', name: 'Kankan', name_ar: 'كانكان', name_en: 'Kankan' },
        { code: 'nzerekore', name: 'Nzérékoré', name_ar: 'نزيريكوري', name_en: 'Nzérékoré' },
        { code: 'labe', name: 'Labé', name_ar: 'لابي', name_en: 'Labé' },
        { code: 'boke', name: 'Boké', name_ar: 'بوكي', name_en: 'Boké' },
        { code: 'faranah', name: 'Faranah', name_ar: 'فراناه', name_en: 'Faranah' },
        { code: 'kouroussa', name: 'Kouroussa', name_ar: 'كوروسا', name_en: 'Kouroussa' },
        { code: 'mamou', name: 'Mamou', name_ar: 'مامو', name_en: 'Mamou' },
        { code: 'siguiri', name: 'Siguiri', name_ar: 'سيغيري', name_en: 'Siguiri' },
        { code: 'telimele', name: 'Télimélé', name_ar: 'تليميلي', name_en: 'Télimélé' },
        { code: 'dabola', name: 'Dabola', name_ar: 'دابولا', name_en: 'Dabola' },
        { code: 'dinguiraye', name: 'Dinguiraye', name_ar: 'دينجيراي', name_en: 'Dinguiraye' },
        { code: 'fria', name: 'Fria', name_ar: 'فريا', name_en: 'Fria' },
        { code: 'gaoual', name: 'Gaoual', name_ar: 'جاوال', name_en: 'Gaoual' },
        { code: 'gueckedou', name: 'Guéckédou', name_ar: 'جيكيدو', name_en: 'Guéckédou' },
        { code: 'kissidougou', name: 'Kissidougou', name_ar: 'كيسيدوغو', name_en: 'Kissidougou' },
        { code: 'macenta', name: 'Macenta', name_ar: 'ماكنتا', name_en: 'Macenta' },
        { code: 'mandiana', name: 'Mandiana', name_ar: 'مانديانا', name_en: 'Mandiana' },
        { code: 'pita', name: 'Pita', name_ar: 'بيتا', name_en: 'Pita' },
        { code: 'tougue', name: 'Tougué', name_ar: 'توجي', name_en: 'Tougué' },
        { code: 'yomou', name: 'Yomou', name_ar: 'يومو', name_en: 'Yomou' }
    ];

    // Devises guinéennes
    const guineaCurrencies = [
        { code: 'GNF', name: 'Franc Guinéen', symbol: 'GNF', is_default: true },
        { code: 'USD', name: 'Dollar US', symbol: '$', is_default: false },
        { code: 'EUR', name: 'Euro', symbol: '€', is_default: false }
    ];

    useEffect(() => {
        if (user) {
            loadUserPreferences();
            loadTranslationStats();
            loadCulturalAdaptations();
            loadPaymentMethods();
            loadLegalCompliance();
        }
    }, [user, selectedRegion]);

    const loadUserPreferences = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/internationalization/user-preferences/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSelectedLanguage(data.primary_language?.code || 'fr');
                setSelectedRegion(data.region?.code || 'conakry');
            }
        } catch (error) {
            console.error('Erreur chargement préférences:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadTranslationStats = async () => {
        try {
            const response = await fetch('/api/internationalization/metrics/');
            if (response.ok) {
                const data = await response.json();
                setTranslationStats(data);
            }
        } catch (error) {
            console.error('Erreur chargement statistiques:', error);
        }
    };

    const loadCulturalAdaptations = async () => {
        try {
            const response = await fetch(`/api/internationalization/cultural-adaptations/?country=${selectedRegion}`);
            if (response.ok) {
                const data = await response.json();
                setCulturalAdaptations(data.adaptations || {});
            }
        } catch (error) {
            console.error('Erreur chargement adaptations culturelles:', error);
        }
    };

    const loadPaymentMethods = async () => {
        try {
            const response = await fetch(`/api/internationalization/payment-methods/?country=${selectedRegion}`);
            if (response.ok) {
                const data = await response.json();
                setPaymentMethods(data.payment_methods || []);
            }
        } catch (error) {
            console.error('Erreur chargement méthodes paiement:', error);
        }
    };

    const loadLegalCompliance = async () => {
        try {
            const response = await fetch(`/api/internationalization/legal-compliance/?country=${selectedRegion}`);
            if (response.ok) {
                const data = await response.json();
                setLegalCompliance(data.compliance_rules || []);
            }
        } catch (error) {
            console.error('Erreur chargement conformité légale:', error);
        }
    };

    const updateLanguagePreference = async (languageCode) => {
        try {
            setLoading(true);
            const response = await fetch('/api/internationalization/update-preferences/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    primary_language: languageCode
                })
            });

            if (response.ok) {
                setSelectedLanguage(languageCode);
                // Recharger les traductions
                window.location.reload();
            }
        } catch (error) {
            console.error('Erreur mise à jour langue:', error);
        } finally {
            setLoading(false);
        }
    };

    const updateRegionPreference = async (regionCode) => {
        try {
            setLoading(true);
            const response = await fetch('/api/internationalization/update-preferences/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    country: regionCode
                })
            });

            if (response.ok) {
                setSelectedRegion(regionCode);
                // Recharger les adaptations culturelles
                loadCulturalAdaptations();
                loadPaymentMethods();
                loadLegalCompliance();
            }
        } catch (error) {
            console.error('Erreur mise à jour région:', error);
        } finally {
            setLoading(false);
        }
    };

    const getRegionName = (regionCode, language = 'fr') => {
        const region = guineaRegions.find(r => r.code === regionCode);
        if (!region) return regionCode;
        
        switch (language) {
            case 'ar':
                return region.name_ar;
            case 'en':
                return region.name_en;
            default:
                return region.name;
        }
    };

    const getLanguageName = (languageCode) => {
        const language = supportedLanguages.find(l => l.code === languageCode);
        return language ? language.name : languageCode;
    };

    const formatCurrency = (amount, currencyCode = 'GNF') => {
        const currency = guineaCurrencies.find(c => c.code === currencyCode);
        if (!currency) return `${amount} GNF`;
        
        if (currency.symbol === 'GNF') {
            return `${amount.toLocaleString('fr-FR')} GNF`;
        } else {
            return `${currency.symbol}${amount.toLocaleString('fr-FR')}`;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-gradient-to-r from-green-500 to-blue-500 rounded-full">
                                <Globe className="h-8 w-8 text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900">
                                    Internationalisation Guinée
                                </h1>
                                <p className="text-gray-600">
                                    Gestion des langues et adaptations culturelles pour CommuniConnect
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Flag className="h-6 w-6 text-green-600" />
                            <span className="text-lg font-semibold text-green-600">Guinée</span>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Langues Supportées */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <Languages className="h-6 w-6 text-blue-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Langues Supportées
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {supportedLanguages.map((language) => (
                                <div
                                    key={language.code}
                                    className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                                        selectedLanguage === language.code
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-200 hover:border-gray-300'
                                    }`}
                                    onClick={() => updateLanguagePreference(language.code)}
                                >
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-3">
                                            <span className="text-2xl">{language.flag}</span>
                                            <div>
                                                <div className="font-semibold text-gray-900">
                                                    {language.name}
                                                </div>
                                                <div className="text-sm text-gray-600">
                                                    {language.native_name}
                                                </div>
                                            </div>
                                        </div>
                                        {selectedLanguage === language.code && (
                                            <CheckCircle className="h-5 w-5 text-blue-600" />
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Statistiques de traduction */}
                        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                            <h3 className="font-semibold text-gray-900 mb-3">Statistiques</h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="text-center">
                                    <div className="text-2xl font-bold text-blue-600">
                                        {translationStats.active_languages || 3}
                                    </div>
                                    <div className="text-sm text-gray-600">Langues actives</div>
                                </div>
                                <div className="text-center">
                                    <div className="text-2xl font-bold text-green-600">
                                        {translationStats.translation_coverage_avg 
                                            ? `${(translationStats.translation_coverage_avg * 100).toFixed(1)}%`
                                            : '85%'
                                        }
                                    </div>
                                    <div className="text-sm text-gray-600">Couverture</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Régions de la Guinée */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <MapPin className="h-6 w-6 text-green-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Régions de la Guinée
                            </h2>
                        </div>

                        <div className="mb-4">
                            <select
                                value={selectedRegion}
                                onChange={(e) => updateRegionPreference(e.target.value)}
                                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                            >
                                {guineaRegions.map((region) => (
                                    <option key={region.code} value={region.code}>
                                        {getRegionName(region.code, selectedLanguage)}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="space-y-3">
                            <div className="p-3 bg-green-50 rounded-lg">
                                <div className="font-semibold text-green-800">
                                    Région sélectionnée
                                </div>
                                <div className="text-green-600">
                                    {getRegionName(selectedRegion, selectedLanguage)}
                                </div>
                            </div>

                            {/* Adaptations culturelles */}
                            <div className="mt-4">
                                <h3 className="font-semibold text-gray-900 mb-3">
                                    Adaptations Culturelles
                                </h3>
                                <div className="space-y-2">
                                    {Object.keys(culturalAdaptations).map((adaptation) => (
                                        <div key={adaptation} className="flex items-center space-x-2">
                                            <CheckCircle className="h-4 w-4 text-green-600" />
                                            <span className="text-sm text-gray-700">
                                                {adaptation.replace('_', ' ')}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Méthodes de Paiement */}
                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <DollarSign className="h-6 w-6 text-yellow-600" />
                            <h2 className="text-xl font-semibold text-gray-900">
                                Méthodes de Paiement
                            </h2>
                        </div>

                        <div className="space-y-3">
                            {paymentMethods.map((method) => (
                                <div key={method.id} className="p-3 border border-gray-200 rounded-lg">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <div className="font-semibold text-gray-900">
                                                {method.provider_name}
                                            </div>
                                            <div className="text-sm text-gray-600">
                                                {method.payment_type.replace('_', ' ')}
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm text-gray-600">
                                                Frais: {method.transaction_fee_percentage}%
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {formatCurrency(method.min_amount)} - {formatCurrency(method.max_amount)}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Devises supportées */}
                        <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
                            <h3 className="font-semibold text-gray-900 mb-3">Devises Supportées</h3>
                            <div className="space-y-2">
                                {guineaCurrencies.map((currency) => (
                                    <div key={currency.code} className="flex items-center justify-between">
                                        <span className="text-sm text-gray-700">
                                            {currency.name}
                                        </span>
                                        <span className="text-sm font-semibold text-gray-900">
                                            {currency.symbol}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Conformité Légale */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <Shield className="h-6 w-6 text-red-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Conformité Légale Guinée
                        </h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {legalCompliance.map((compliance) => (
                            <div key={compliance.compliance_type} className="p-4 border border-gray-200 rounded-lg">
                                <div className="flex items-center space-x-2 mb-2">
                                    {compliance.is_implemented ? (
                                        <CheckCircle className="h-4 w-4 text-green-600" />
                                    ) : (
                                        <AlertCircle className="h-4 w-4 text-yellow-600" />
                                    )}
                                    <span className="font-semibold text-gray-900">
                                        {compliance.compliance_type.replace('_', ' ')}
                                    </span>
                                </div>
                                <div className="text-sm text-gray-600">
                                    {compliance.is_required ? 'Obligatoire' : 'Recommandé'}
                                </div>
                                {compliance.is_implemented && (
                                    <div className="text-xs text-green-600 mt-1">
                                        Implémenté
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Métriques Avancées */}
                <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-center space-x-3 mb-6">
                        <BarChart3 className="h-6 w-6 text-purple-600" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Métriques d'Internationalisation
                        </h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <div className="text-3xl font-bold text-blue-600">
                                {translationStats.total_translations || 1250}
                            </div>
                            <div className="text-sm text-gray-600">Traductions totales</div>
                        </div>

                        <div className="text-center p-4 bg-green-50 rounded-lg">
                            <div className="text-3xl font-bold text-green-600">
                                {translationStats.ai_translations || 980}
                            </div>
                            <div className="text-sm text-gray-600">Traductions IA</div>
                        </div>

                        <div className="text-center p-4 bg-yellow-50 rounded-lg">
                            <div className="text-3xl font-bold text-yellow-600">
                                {translationStats.manual_translations || 270}
                            </div>
                            <div className="text-sm text-gray-600">Traductions manuelles</div>
                        </div>

                        <div className="text-center p-4 bg-purple-50 rounded-lg">
                            <div className="text-3xl font-bold text-purple-600">
                                {translationStats.translation_accuracy 
                                    ? `${(translationStats.translation_accuracy * 100).toFixed(1)}%`
                                    : '92.5%'
                                }
                            </div>
                            <div className="text-sm text-gray-600">Précision</div>
                        </div>
                    </div>
                </div>

                {/* Informations supplémentaires */}
                <div className="mt-8 bg-gradient-to-r from-blue-500 to-green-500 rounded-xl shadow-lg p-6 text-white">
                    <div className="flex items-center space-x-3 mb-4">
                        <Info className="h-6 w-6" />
                        <h3 className="text-xl font-semibold">
                            À propos de l'Internationalisation Guinée
                        </h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 className="font-semibold mb-2">Langues Supportées</h4>
                            <p className="text-blue-100">
                                CommuniConnect supporte 3 langues principales adaptées au contexte guinéen : 
                                Français (langue officielle), Anglais (langue internationale) et Arabe 
                                (langue religieuse et culturelle).
                            </p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">Adaptations Régionales</h4>
                            <p className="text-blue-100">
                                Chaque région de la Guinée bénéficie d'adaptations culturelles spécifiques, 
                                incluant les méthodes de paiement locales, les considérations religieuses 
                                et les exigences légales régionales.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GuineaInternationalization; 
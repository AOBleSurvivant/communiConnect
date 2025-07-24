import React, { useState, useEffect, useRef } from 'react';
import { toast } from 'react-toastify';
import { 
    MapPinIcon, 
    ExclamationTriangleIcon,
    FireIcon,
    BoltIcon,
    ShieldExclamationIcon,
    HeartIcon,
    WrenchScrewdriverIcon,
    SpeakerWaveIcon,
    PaintBrushIcon,
    DocumentTextIcon
} from '@heroicons/react/24/solid';

const AlertMap = ({ alerts, userLocation, onAlertClick, className = "" }) => {
    const [map, setMap] = useState(null);
    const [mapContainer, setMapContainer] = useState(null);
    const [alertMarkers, setAlertMarkers] = useState([]);
    const [isMapLoaded, setIsMapLoaded] = useState(false);
    const mapRef = useRef(null);

    // Icônes personnalisées pour chaque catégorie
    const alertIcons = {
        fire: { icon: FireIcon, color: '#FF4444', bgColor: '#FFE6E6' },
        power_outage: { icon: BoltIcon, color: '#FFAA00', bgColor: '#FFF8E6' },
        road_blocked: { icon: ExclamationTriangleIcon, color: '#FF8800', bgColor: '#FFF2E6' },
        security: { icon: ShieldExclamationIcon, color: '#CC0000', bgColor: '#FFE6E6' },
        medical: { icon: HeartIcon, color: '#FF66CC', bgColor: '#FFE6F2' },
        flood: { icon: '🌊', color: '#0066CC', bgColor: '#E6F2FF' },
        gas_leak: { icon: '⛽', color: '#CC6600', bgColor: '#FFF2E6' },
        noise: { icon: SpeakerWaveIcon, color: '#9933CC', bgColor: '#F2E6FF' },
        vandalism: { icon: PaintBrushIcon, color: '#666666', bgColor: '#F2F2F2' },
        other: { icon: DocumentTextIcon, color: '#999999', bgColor: '#F8F8F8' }
    };

    // Charger Leaflet de manière dynamique
    useEffect(() => {
        const loadLeaflet = async () => {
            try {
                // Charger les scripts Leaflet
                if (!window.L) {
                    const link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
                    document.head.appendChild(link);

                    const script = document.createElement('script');
                    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
                    script.onload = () => {
                        initializeMap();
                    };
                    document.head.appendChild(script);
                } else {
                    initializeMap();
                }
            } catch (error) {
                console.error('Erreur chargement Leaflet:', error);
                toast.error('Erreur lors du chargement de la carte');
            }
        };

        loadLeaflet();
    }, []);

    const initializeMap = () => {
        if (!mapContainer || !window.L) return;

        try {
            // Créer la carte
            const mapInstance = window.L.map(mapContainer).setView(
                userLocation ? [userLocation.latitude, userLocation.longitude] : [0, 0],
                13
            );

            // Ajouter la couche de tuiles
            window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mapInstance);

            // Marqueur de l'utilisateur
            if (userLocation) {
                const userIcon = window.L.divIcon({
                    html: '📍',
                    className: 'user-location-marker',
                    iconSize: [30, 30],
                    iconAnchor: [15, 15]
                });

                window.L.marker([userLocation.latitude, userLocation.longitude], {
                    icon: userIcon
                }).addTo(mapInstance).bindPopup('Votre position');
            }

            // Cercle de proximité (5km)
            if (userLocation) {
                window.L.circle([userLocation.latitude, userLocation.longitude], {
                    color: '#2196F3',
                    fillColor: '#2196F3',
                    fillOpacity: 0.1,
                    radius: 5000
                }).addTo(mapInstance);
            }

            setMap(mapInstance);
            setIsMapLoaded(true);

        } catch (error) {
            console.error('Erreur initialisation carte:', error);
            toast.error('Erreur lors de l\'initialisation de la carte');
        }
    };

    // Mettre à jour les marqueurs quand les alertes changent
    useEffect(() => {
        if (!map || !alerts) return;

        // Supprimer les anciens marqueurs
        alertMarkers.forEach(marker => {
            map.removeLayer(marker);
        });

        const newMarkers = [];

        alerts.forEach(alert => {
            if (alert.latitude && alert.longitude) {
                const iconConfig = alertIcons[alert.category] || alertIcons.other;
                
                // Créer l'icône personnalisée
                const iconHtml = React.createElement(iconConfig.icon, {
                    className: 'w-6 h-6',
                    style: { color: iconConfig.color }
                });

                const customIcon = window.L.divIcon({
                    html: `<div style="
                        background-color: ${iconConfig.bgColor}; 
                        border: 2px solid ${iconConfig.color}; 
                        border-radius: 50%; 
                        width: 40px; 
                        height: 40px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    ">${iconConfig.icon === '🌊' ? '🌊' : iconConfig.icon === '⛽' ? '⛽' : ''}</div>`,
                    className: 'alert-marker',
                    iconSize: [40, 40],
                    iconAnchor: [20, 20]
                });

                const marker = window.L.marker([alert.latitude, alert.longitude], {
                    icon: customIcon
                }).addTo(map);

                // Popup avec informations détaillées
                const popupContent = `
                    <div class="alert-popup">
                        <h3 style="margin: 0 0 8px 0; color: ${iconConfig.color};">
                            ${alert.title}
                        </h3>
                        <p style="margin: 0 0 8px 0; font-size: 14px;">
                            ${alert.description}
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                            <span style="
                                background-color: ${iconConfig.bgColor}; 
                                color: ${iconConfig.color}; 
                                padding: 4px 8px; 
                                border-radius: 12px;
                            ">
                                ${alert.get_category_display()}
                            </span>
                            <span style="color: #666;">
                                ${alert.time_ago}
                            </span>
                        </div>
                        <div style="margin-top: 8px;">
                            <button onclick="window.alertMapClick('${alert.alert_id}')" 
                                    style="
                                        background-color: ${iconConfig.color}; 
                                        color: white; 
                                        border: none; 
                                        padding: 6px 12px; 
                                        border-radius: 4px; 
                                        cursor: pointer;
                                    ">
                                Voir détails
                            </button>
                        </div>
                    </div>
                `;

                marker.bindPopup(popupContent);
                newMarkers.push(marker);

                // Ajouter l'événement de clic
                marker.on('click', () => {
                    if (onAlertClick) {
                        onAlertClick(alert);
                    }
                });
            }
        });

        setAlertMarkers(newMarkers);

        // Ajuster la vue pour inclure tous les marqueurs
        if (newMarkers.length > 0) {
            const group = window.L.featureGroup(newMarkers);
            map.fitBounds(group.getBounds().pad(0.1));
        }

    }, [map, alerts, userLocation]);

    // Fonction globale pour les clics depuis les popups
    useEffect(() => {
        window.alertMapClick = (alertId) => {
            const alert = alerts.find(a => a.alert_id === alertId);
            if (alert && onAlertClick) {
                onAlertClick(alert);
            }
        };

        return () => {
            delete window.alertMapClick;
        };
    }, [alerts, onAlertClick]);

    return (
        <div className={`alert-map-container ${className}`}>
            <div 
                ref={setMapContainer}
                style={{ 
                    height: '500px', 
                    width: '100%',
                    borderRadius: '8px',
                    overflow: 'hidden',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                }}
            />
            
            {!isMapLoaded && (
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    background: 'white',
                    padding: '20px',
                    borderRadius: '8px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    zIndex: 1000
                }}>
                    <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <span className="ml-2">Chargement de la carte...</span>
                    </div>
                </div>
            )}
            
            {/* Légende */}
            <div className="mt-4 p-4 bg-white rounded-lg shadow-sm">
                <h4 className="font-semibold mb-3">Légende des alertes</h4>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {Object.entries(alertIcons).map(([category, config]) => (
                        <div key={category} className="flex items-center space-x-2">
                            <div style={{
                                backgroundColor: config.bgColor,
                                border: `2px solid ${config.color}`,
                                borderRadius: '50%',
                                width: '20px',
                                height: '20px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '12px'
                            }}>
                                {config.icon === '🌊' ? '🌊' : config.icon === '⛽' ? '⛽' : ''}
                            </div>
                            <span className="text-sm capitalize">
                                {category.replace('_', ' ')}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AlertMap; 
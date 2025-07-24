import { API_BASE_URL } from '../config';

class AlertService {
    constructor() {
        this.baseURL = `${API_BASE_URL}/notifications/alerts`;
    }

    // Récupérer le token d'authentification
    getAuthHeaders() {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    }

    // Récupérer toutes les alertes avec filtres
    async getAlerts(filters = {}) {
        try {
            const queryParams = new URLSearchParams();
            
            // Ajouter les filtres à l'URL
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== '' && value !== null && value !== undefined) {
                    queryParams.append(key, value);
                }
            });

            const url = queryParams.toString() 
                ? `${this.baseURL}/?${queryParams.toString()}`
                : this.baseURL;

            const response = await fetch(url, {
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des alertes:', error);
            throw error;
        }
    }

    // Récupérer une alerte spécifique
    async getAlert(alertId) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/`, {
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération de l\'alerte:', error);
            throw error;
        }
    }

    // Créer une nouvelle alerte
    async createAlert(alertData) {
        try {
            const response = await fetch(this.baseURL, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(alertData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de la création de l\'alerte');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la création de l\'alerte:', error);
            throw error;
        }
    }

    // Mettre à jour une alerte
    async updateAlert(alertId, alertData) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/`, {
                method: 'PUT',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(alertData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de la mise à jour de l\'alerte');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la mise à jour de l\'alerte:', error);
            throw error;
        }
    }

    // Supprimer une alerte
    async deleteAlert(alertId) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/`, {
                method: 'DELETE',
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return true;
        } catch (error) {
            console.error('Erreur lors de la suppression de l\'alerte:', error);
            throw error;
        }
    }

    // Rechercher des alertes
    async searchAlerts(searchData) {
        try {
            const response = await fetch(`${this.baseURL}/search/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(searchData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la recherche d\'alertes:', error);
            throw error;
        }
    }

    // Récupérer les alertes à proximité
    async getNearbyAlerts(locationData) {
        try {
            const response = await fetch(`${this.baseURL}/nearby/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(locationData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des alertes à proximité:', error);
            throw error;
        }
    }

    // Signaler une alerte
    async reportAlert(reportData) {
        try {
            const response = await fetch(`${this.baseURL}/report/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(reportData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de l\'envoi du rapport');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de l\'envoi du rapport:', error);
            throw error;
        }
    }

    // Offrir de l'aide
    async offerHelp(alertId, helpData) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/help/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(helpData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de l\'envoi de l\'offre d\'aide');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de l\'envoi de l\'offre d\'aide:', error);
            throw error;
        }
    }

    // Récupérer les offres d'aide pour une alerte
    async getHelpOffers(alertId) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/help/`, {
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des offres d\'aide:', error);
            throw error;
        }
    }

    // Récupérer les statistiques
    async getStatistics(period = 'monthly') {
        try {
            const response = await fetch(`${this.baseURL}/statistics/?period=${period}`, {
                headers: this.getAuthHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des statistiques:', error);
            throw error;
        }
    }

    // Marquer une alerte comme résolue
    async markAsResolved(alertId) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/`, {
                method: 'PATCH',
                headers: this.getAuthHeaders(),
                body: JSON.stringify({ status: 'resolved' })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de la résolution de l\'alerte');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la résolution de l\'alerte:', error);
            throw error;
        }
    }

    // Confirmer une alerte
    async confirmAlert(alertId) {
        try {
            const response = await fetch(`${this.baseURL}/${alertId}/`, {
                method: 'PATCH',
                headers: this.getAuthHeaders(),
                body: JSON.stringify({ status: 'confirmed' })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erreur lors de la confirmation de l\'alerte');
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la confirmation de l\'alerte:', error);
            throw error;
        }
    }

    // Obtenir la géolocalisation de l'utilisateur
    async getUserLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Géolocalisation non supportée'));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                },
                (error) => {
                    reject(error);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000 // 5 minutes
                }
            );
        });
    }

    // Calculer la distance entre deux points (formule de Haversine)
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Rayon de la Terre en km
        const dLat = this.toRadians(lat2 - lat1);
        const dLon = this.toRadians(lon2 - lon1);
        const a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * 
            Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    toRadians(degrees) {
        return degrees * (Math.PI/180);
    }

    // Formater la distance pour l'affichage
    formatDistance(distance) {
        if (distance < 1) {
            return `${Math.round(distance * 1000)} m`;
        } else if (distance < 10) {
            return `${distance.toFixed(1)} km`;
        } else {
            return `${Math.round(distance)} km`;
        }
    }

    // Formater le temps écoulé
    formatTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) {
            return 'à l\'instant';
        } else if (diffInSeconds < 3600) {
            const minutes = Math.floor(diffInSeconds / 60);
            return `il y a ${minutes} minute${minutes > 1 ? 's' : ''}`;
        } else if (diffInSeconds < 86400) {
            const hours = Math.floor(diffInSeconds / 3600);
            return `il y a ${hours} heure${hours > 1 ? 's' : ''}`;
        } else {
            const days = Math.floor(diffInSeconds / 86400);
            return `il y a ${days} jour${days > 1 ? 's' : ''}`;
        }
    }

    // Vérifier si une alerte est urgente
    isUrgent(category) {
        const urgentCategories = ['fire', 'medical', 'gas_leak', 'security'];
        return urgentCategories.includes(category);
    }

    // Vérifier si une alerte est fiable
    isReliable(reliabilityScore) {
        return reliabilityScore >= 70;
    }

    // Obtenir la couleur de fiabilité
    getReliabilityColor(reliabilityScore) {
        if (reliabilityScore >= 70) {
            return 'text-green-700 bg-green-100';
        } else if (reliabilityScore >= 40) {
            return 'text-yellow-700 bg-yellow-100';
        } else {
            return 'text-red-700 bg-red-100';
        }
    }

    // Obtenir les catégories d'alertes
    getAlertCategories() {
        return {
            fire: { icon: '🔥', label: 'Incendie', color: 'text-red-600 bg-red-100' },
            power_outage: { icon: '⚡', label: 'Coupure d\'électricité', color: 'text-yellow-600 bg-yellow-100' },
            road_blocked: { icon: '🚧', label: 'Route bloquée', color: 'text-orange-600 bg-orange-100' },
            security: { icon: '🚨', label: 'Agression ou sécurité', color: 'text-red-700 bg-red-200' },
            medical: { icon: '🏥', label: 'Urgence médicale', color: 'text-pink-600 bg-pink-100' },
            flood: { icon: '🌊', label: 'Inondation', color: 'text-blue-600 bg-blue-100' },
            gas_leak: { icon: '⛽', label: 'Fuite de gaz', color: 'text-orange-700 bg-orange-200' },
            noise: { icon: '🔊', label: 'Bruit excessif', color: 'text-purple-600 bg-purple-100' },
            vandalism: { icon: '🎨', label: 'Vandalisme', color: 'text-gray-600 bg-gray-100' },
            other: { icon: '📋', label: 'Autre', color: 'text-gray-500 bg-gray-50' }
        };
    }

    // Obtenir les statuts d'alertes
    getAlertStatuses() {
        return {
            pending: { label: 'En attente', color: 'text-yellow-600 bg-yellow-100' },
            confirmed: { label: 'Confirmée', color: 'text-green-600 bg-green-100' },
            in_progress: { label: 'En cours de traitement', color: 'text-blue-600 bg-blue-100' },
            resolved: { label: 'Résolue', color: 'text-green-700 bg-green-200' },
            false_alarm: { label: 'Fausse alerte', color: 'text-red-600 bg-red-100' }
        };
    }

    // Obtenir les types d'offres d'aide
    getHelpOfferTypes() {
        return {
            physical_help: { label: 'Aide physique', icon: '🤝' },
            information: { label: 'Information', icon: 'ℹ️' },
            transport: { label: 'Transport', icon: '🚗' },
            medical: { label: 'Aide médicale', icon: '🏥' },
            technical: { label: 'Aide technique', icon: '🔧' },
            other: { label: 'Autre', icon: '📋' }
        };
    }

    // Obtenir les types de rapports
    getReportTypes() {
        return {
            false_alarm: { label: 'Fausse alerte', icon: '❌' },
            confirmed: { label: 'Confirmée', icon: '✅' },
            inappropriate: { label: 'Inappropriée', icon: '🚫' },
            duplicate: { label: 'Doublon', icon: '🔄' },
            resolved: { label: 'Résolue', icon: '✅' }
        };
    }
}

// Instance singleton
const alertService = new AlertService();

export default alertService; 
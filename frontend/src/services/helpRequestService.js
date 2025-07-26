import api from './api';

/**
 * Service pour gérer les demandes d'aide
 * Inspiré de Nextdoor Help Map
 */
class HelpRequestService {
    
    /**
     * Récupérer toutes les demandes d'aide avec filtres
     */
    async getHelpRequests(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            // Ajouter les filtres
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== null && value !== undefined && value !== '') {
                    params.append(key, value);
                }
            });
            
            const response = await api.get(`/help-requests/api/requests/?${params}`);
            return response.data;
        } catch (error) {
            console.error('Erreur récupération demandes d\'aide:', error);
            throw error;
        }
    }
    
    /**
     * Récupérer une demande d'aide spécifique
     */
    async getHelpRequest(id) {
        try {
            const response = await api.get(`/help-requests/api/requests/${id}/`);
            return response.data;
        } catch (error) {
            console.error('Erreur récupération demande d\'aide:', error);
            throw error;
        }
    }
    
    /**
     * Créer une nouvelle demande d'aide
     */
    async createHelpRequest(requestData) {
        try {
            const response = await api.post('/help-requests/api/requests/', requestData, {
                headers: {
                    'Content-Type': requestData instanceof FormData ? 'multipart/form-data' : 'application/json'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Erreur création demande d\'aide:', error);
            throw error;
        }
    }
    
    /**
     * Mettre à jour une demande d'aide
     */
    async updateHelpRequest(id, requestData) {
        try {
            const response = await api.put(`/help-requests/api/requests/${id}/`, requestData, {
                headers: {
                    'Content-Type': requestData instanceof FormData ? 'multipart/form-data' : 'application/json'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Erreur mise à jour demande d\'aide:', error);
            throw error;
        }
    }
    
    /**
     * Supprimer une demande d'aide
     */
    async deleteHelpRequest(id) {
        try {
            await api.delete(`/help-requests/api/requests/${id}/`);
        } catch (error) {
            console.error('Erreur suppression demande d\'aide:', error);
            throw error;
        }
    }
    
    /**
     * Récupérer les données pour l'affichage sur la carte
     */
    async getMapData(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            // Ajouter les filtres pour la carte
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== null && value !== undefined && value !== '') {
                    params.append(key, value);
                }
            });
            
            const response = await api.get(`/help-requests/api/requests/map_data/?${params}`);
            return response.data;
        } catch (error) {
            console.error('Erreur récupération données carte:', error);
            throw error;
        }
    }
    
    /**
     * Récupérer les statistiques des demandes d'aide
     */
    async getStats() {
        try {
            const response = await api.get('/help-requests/api/requests/stats/');
            return response.data;
        } catch (error) {
            console.error('Erreur récupération statistiques:', error);
            throw error;
        }
    }
    
    /**
     * Répondre à une demande d'aide
     */
    async respondToRequest(requestId, responseData) {
        try {
            const response = await api.post(`/help-requests/api/requests/${requestId}/respond/`, responseData);
            return response.data;
        } catch (error) {
            console.error('Erreur réponse à la demande:', error);
            throw error;
        }
    }
    
    /**
     * Accepter une réponse
     */
    async acceptResponse(requestId, responseId) {
        try {
            const response = await api.post(`/help-requests/api/requests/${requestId}/accept-response/`, {
                response_id: responseId
            });
            return response.data;
        } catch (error) {
            console.error('Erreur acceptation réponse:', error);
            throw error;
        }
    }
    
    /**
     * Rejeter une réponse
     */
    async rejectResponse(requestId, responseId) {
        try {
            const response = await api.post(`/help-requests/api/requests/${requestId}/reject-response/`, {
                response_id: responseId
            });
            return response.data;
        } catch (error) {
            console.error('Erreur rejet réponse:', error);
            throw error;
        }
    }
    
    /**
     * Marquer une demande comme terminée
     */
    async markCompleted(requestId) {
        try {
            const response = await api.post(`/help-requests/api/requests/${requestId}/mark-completed/`);
            return response.data;
        } catch (error) {
            console.error('Erreur marquage terminé:', error);
            throw error;
        }
    }
    
    /**
     * Marquer une demande comme annulée
     */
    async markCancelled(requestId) {
        try {
            const response = await api.post(`/help-requests/api/requests/${requestId}/mark-cancelled/`);
            return response.data;
        } catch (error) {
            console.error('Erreur marquage annulé:', error);
            throw error;
        }
    }
    
    /**
     * Récupérer les réponses d'une demande d'aide
     */
    async getResponses(requestId) {
        try {
            const response = await api.get(`/help-requests/api/responses/?help_request=${requestId}`);
            return response.data;
        } catch (error) {
            console.error('Erreur récupération réponses:', error);
            throw error;
        }
    }
    
    /**
     * Récupérer les catégories d'aide
     */
    async getCategories() {
        try {
            const response = await api.get('/help-requests/api/categories/');
            return response.data;
        } catch (error) {
            console.error('Erreur récupération catégories:', error);
            throw error;
        }
    }
    
    /**
     * Géocodage inverse pour obtenir l'adresse à partir des coordonnées
     */
    async reverseGeocode(latitude, longitude) {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=18&addressdetails=1`
            );
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erreur géocodage inverse:', error);
            throw error;
        }
    }
    
    /**
     * Géocodage pour obtenir les coordonnées à partir d'une adresse
     */
    async geocode(address) {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`
            );
            const data = await response.json();
            return data[0] || null;
        } catch (error) {
            console.error('Erreur géocodage:', error);
            throw error;
        }
    }
    
    /**
     * Calculer la distance entre deux points (formule de Haversine)
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Rayon de la Terre en km
        const dLat = this.deg2rad(lat2 - lat1);
        const dLon = this.deg2rad(lon2 - lon1);
        const a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
            Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        const distance = R * c; // Distance en km
        return distance;
    }
    
    deg2rad(deg) {
        return deg * (Math.PI/180);
    }
    
    /**
     * Filtrer les demandes par distance
     */
    filterByDistance(requests, userLat, userLon, maxDistance) {
        return requests.filter(request => {
            if (!request.latitude || !request.longitude) return false;
            const distance = this.calculateDistance(
                userLat, userLon, 
                request.latitude, request.longitude
            );
            return distance <= maxDistance;
        });
    }
    
    /**
     * Trier les demandes par distance
     */
    sortByDistance(requests, userLat, userLon) {
        return requests.sort((a, b) => {
            if (!a.latitude || !a.longitude) return 1;
            if (!b.latitude || !b.longitude) return -1;
            
            const distanceA = this.calculateDistance(
                userLat, userLon, 
                a.latitude, a.longitude
            );
            const distanceB = this.calculateDistance(
                userLat, userLon, 
                b.latitude, b.longitude
            );
            
            return distanceA - distanceB;
        });
    }
    
    /**
     * Obtenir la position actuelle de l'utilisateur
     */
    async getCurrentPosition() {
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
                    maximumAge: 60000
                }
            );
        });
    }
}

export default new HelpRequestService(); 
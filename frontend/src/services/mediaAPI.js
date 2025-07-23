import api from './api';

// Service pour les médias
export const mediaAPI = {
  // Uploader un média avec barre de progression
  uploadMedia: async (formData, onProgress) => {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    };
    
    console.log('Uploading media with formData:', formData);
    const response = await api.post('/posts/media/upload/', formData, config);
    console.log('Media upload response:', response.data);
    return response.data;
  },

  // Récupérer tous les médias
  getMedia: async (params = {}) => {
    const response = await api.get('/posts/media/', { params });
    return response.data;
  },

  // Récupérer un média spécifique
  getMediaById: async (mediaId) => {
    const response = await api.get(`/posts/media/${mediaId}/`);
    return response.data;
  },

  // Supprimer un média
  deleteMedia: async (mediaId) => {
    const response = await api.delete(`/posts/media/${mediaId}/`);
    return response.data;
  },

  // Mettre à jour un média
  updateMedia: async (mediaId, mediaData) => {
    const response = await api.put(`/posts/media/${mediaId}/`, mediaData);
    return response.data;
  },

  // Démarrer un live
  startLive: async (liveData) => {
    const response = await api.post('/posts/live/start/', liveData);
    return response.data;
  },

  // Arrêter un live
  stopLive: async (liveId, videoData = null) => {
    const requestData = videoData ? { video_data: videoData } : {};
    const response = await api.put(`/posts/live/${liveId}/stop/`, requestData);
    return response.data;
  },

  // Uploader une vidéo de live enregistrée
  uploadLiveVideo: async (liveId, videoBlob, onProgress) => {
    const formData = new FormData();
    formData.append('video', videoBlob, `live_video_${liveId}.webm`);
    
    // Récupérer le token d'authentification
    const token = localStorage.getItem('access_token');
    
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`,
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    };
    
    console.log('Uploading live video with formData:', formData);
    console.log('Auth token:', token ? 'Present' : 'Missing');
    const response = await api.post(`/posts/live/${liveId}/upload-video/`, formData, config);
    console.log('Live video upload response:', response.data);
    return response.data;
  },

  // Sauvegarder une vidéo enregistrée pendant un live
  saveLiveVideo: async (liveId, videoData) => {
    const response = await api.put(`/posts/live/${liveId}/stop/`, {
      video_data: videoData
    });
    return response.data;
  },

  // Valider la durée d'une vidéo côté client
  validateVideoDuration: (file) => {
    return new Promise((resolve, reject) => {
      const video = document.createElement('video');
      video.preload = 'metadata';
      
      video.onloadedmetadata = () => {
        window.URL.revokeObjectURL(video.src);
        const duration = video.duration;
        
        if (duration > 60) {
          reject(new Error('La vidéo ne peut pas dépasser 60 secondes'));
        } else {
          resolve(duration);
        }
      };
      
      video.onerror = () => {
        reject(new Error('Impossible de lire la vidéo'));
      };
      
      video.src = URL.createObjectURL(file);
    });
  },

  // Valider le type et la taille d'un fichier
  validateFile: (file) => {
    const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const allowedVideoTypes = ['video/mp4', 'video/webm', 'video/quicktime', 'video/avi'];
    
    const maxImageSize = 10 * 1024 * 1024; // 10MB
    const maxVideoSize = 50 * 1024 * 1024; // 50MB
    
    if (file.type.startsWith('image/')) {
      if (!allowedImageTypes.includes(file.type)) {
        throw new Error('Type d\'image non supporté');
      }
      if (file.size > maxImageSize) {
        throw new Error('Image trop volumineuse (max 10MB)');
      }
    } else if (file.type.startsWith('video/')) {
      if (!allowedVideoTypes.includes(file.type)) {
        throw new Error('Type de vidéo non supporté');
      }
      if (file.size > maxVideoSize) {
        throw new Error('Vidéo trop volumineuse (max 50MB)');
      }
    } else {
      throw new Error('Type de fichier non supporté');
    }
    
    return true;
  },

  // Créer une miniature pour une vidéo
  createVideoThumbnail: (videoFile) => {
    return new Promise((resolve, reject) => {
      const video = document.createElement('video');
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      video.onloadedmetadata = () => {
        // Prendre une capture à 1 seconde
        video.currentTime = 1;
      };
      
      video.onseeked = () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        canvas.toBlob((blob) => {
          resolve(blob);
        }, 'image/jpeg', 0.8);
      };
      
      video.onerror = () => {
        reject(new Error('Impossible de créer la miniature'));
      };
      
      video.src = URL.createObjectURL(videoFile);
    });
  },

  // Compresser une image
  compressImage: (file, maxWidth = 1920, maxHeight = 1080, quality = 0.8) => {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.onload = () => {
        // Calculer les nouvelles dimensions
        let { width, height } = img;
        
        if (width > maxWidth) {
          height = (height * maxWidth) / width;
          width = maxWidth;
        }
        
        if (height > maxHeight) {
          width = (width * maxHeight) / height;
          height = maxHeight;
        }
        
        canvas.width = width;
        canvas.height = height;
        
        // Dessiner l'image redimensionnée
        ctx.drawImage(img, 0, 0, width, height);
        
        // Convertir en blob
        canvas.toBlob((blob) => {
          resolve(new File([blob], file.name, {
            type: file.type,
            lastModified: Date.now(),
          }));
        }, file.type, quality);
      };
      
      img.onerror = () => {
        reject(new Error('Impossible de charger l\'image'));
      };
      
      img.src = URL.createObjectURL(file);
    });
  },

  // Obtenir les informations d'un fichier
  getFileInfo: (file) => {
    return {
      name: file.name,
      size: file.size,
      type: file.type,
      lastModified: file.lastModified,
      sizeInMB: (file.size / 1024 / 1024).toFixed(2),
    };
  },
}; 
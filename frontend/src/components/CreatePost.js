import React, { useState, useRef, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { postsAPI } from '../services/postsAPI';
import { mediaAPI } from '../services/mediaAPI';
import { 
  MessageCircle, 
  Calendar, 
  HelpCircle, 
  AlertCircle, 
  Users,
  Send,
  X,
  Image,
  Trash2,
  Video as VideoIcon,
  Video,
  Camera,
  Smile,
  MapPin,
  Globe,
  Users as UsersIcon,
  Lock,
  Upload,
  Play,
  Pause,
  Volume2,
  VolumeX
} from 'lucide-react';
import toast from 'react-hot-toast';

const MAX_IMAGE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_VIDEO_SIZE = 50 * 1024 * 1024; // 50MB
const MAX_VIDEO_DURATION = 60; // 60 secondes
const MAX_FILES_PER_POST = 5; // Maximum 5 fichiers par post
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
const ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/quicktime', 'video/avi'];

const CreatePost = ({ isOpen, onClose, onPostCreated }) => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const dropZoneRef = useRef(null);
  
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    post_type: 'info',
    is_anonymous: false,
    privacy: 'public' // public, friends, private
  });

  const postTypes = [
    { value: 'info', label: 'Information', icon: AlertCircle, color: 'text-blue-600' },
    { value: 'event', label: 'Événement', icon: Calendar, color: 'text-green-600' },
    { value: 'help', label: 'Demande d\'aide', icon: HelpCircle, color: 'text-red-600' },
    { value: 'announcement', label: 'Annonce', icon: Users, color: 'text-purple-600' },
    { value: 'discussion', label: 'Discussion', icon: MessageCircle, color: 'text-orange-600' }
  ];

  const privacyOptions = [
    { value: 'public', label: 'Public', icon: Globe, description: 'Tout le monde peut voir' },
    { value: 'friends', label: 'Amis', icon: UsersIcon, description: 'Seuls vos amis peuvent voir' },
    { value: 'private', label: 'Privé', icon: Lock, description: 'Seulement vous' }
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const validateFile = (file) => {
    // Vérifier le type
    if (file.type.startsWith('image/')) {
      if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
        throw new Error('Type d\'image non supporté');
      }
      if (file.size > MAX_IMAGE_SIZE) {
        throw new Error('Image trop volumineuse (max 10MB)');
      }
    } else if (file.type.startsWith('video/')) {
      if (!ALLOWED_VIDEO_TYPES.includes(file.type)) {
        throw new Error('Type de vidéo non supporté');
      }
      if (file.size > MAX_VIDEO_SIZE) {
        throw new Error('Vidéo trop volumineuse (max 50MB)');
      }
    } else {
      throw new Error('Type de fichier non supporté');
    }
  };

  const handleFileSelect = useCallback((files) => {
    const newFiles = Array.from(files);
    const validFiles = [];
    const errors = [];

    // Vérifier la limite du nombre de fichiers
    const totalFiles = selectedFiles.length + newFiles.length;
    if (totalFiles > MAX_FILES_PER_POST) {
      toast.error(`Vous ne pouvez pas sélectionner plus de ${MAX_FILES_PER_POST} fichiers au total`);
      return;
    }

    newFiles.forEach(file => {
      try {
        validateFile(file);
        validFiles.push(file);
      } catch (error) {
        errors.push(`${file.name}: ${error.message}`);
      }
    });

    if (errors.length > 0) {
      errors.forEach(error => toast.error(error));
    }

    if (validFiles.length > 0) {
      setSelectedFiles(prev => [...prev, ...validFiles]);
    }
  }, [selectedFiles.length]);

  const handleFileInput = (e) => {
    handleFileSelect(e.target.files);
    e.target.value = ''; // Reset input
  };

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files);
    }
  }, [handleFileSelect]);

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const uploadFiles = async () => {
    if (selectedFiles.length === 0) return [];

    setIsUploading(true);
    setUploadProgress(0);
    const uploadedMedia = [];

    try {
      for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', file.name);
        
        console.log(`Uploading file ${i + 1}/${selectedFiles.length}: ${file.name}`);
        console.log('File size:', file.size, 'bytes');
        console.log('File type:', file.type);
        
        const response = await mediaAPI.uploadMedia(formData, (progress) => {
          const totalProgress = ((i + progress) / selectedFiles.length) * 100;
          setUploadProgress(totalProgress);
        });
        
        console.log(`File uploaded successfully:`, response);
        uploadedMedia.push(response);
      }
      
      console.log(`All files uploaded:`, uploadedMedia);
      toast.success(`${uploadedMedia.length} fichier(s) uploadé(s) avec succès`);
      return uploadedMedia;
    } catch (error) {
      console.error('Erreur upload:', error);
      
      // Afficher plus de détails sur l'erreur d'upload
      if (error.response) {
        console.error('Upload response data:', error.response.data);
        console.error('Upload response status:', error.response.status);
        
        if (error.response.data && typeof error.response.data === 'object') {
          const errorMessages = [];
          Object.keys(error.response.data).forEach(key => {
            if (Array.isArray(error.response.data[key])) {
              errorMessages.push(...error.response.data[key]);
            } else {
              errorMessages.push(error.response.data[key]);
            }
          });
          
          if (errorMessages.length > 0) {
            toast.error(`Erreur upload: ${errorMessages.join(', ')}`);
            throw error;
          }
        }
      }
      
      toast.error('Erreur lors de l\'upload des fichiers');
      throw error;
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.content.trim() && selectedFiles.length === 0) {
      toast.error('Veuillez ajouter du contenu ou des médias');
      return;
    }

    setIsLoading(true);
    try {
      // Upload des fichiers d'abord
      console.log('Starting file upload...');
      const uploadedMedia = await uploadFiles();
      console.log('Upload completed, media:', uploadedMedia);
      
      // Créer le post avec les médias
      const postData = {
        ...formData,
        media_files: uploadedMedia.map(media => media.id)
      };

      console.log('Creating post with data:', postData);
      console.log('Media IDs:', uploadedMedia.map(media => media.id));

      const response = await postsAPI.createPost(postData);
      
      console.log('Post created successfully:', response);
      toast.success('Publication créée avec succès !');
      onPostCreated(response);
      handleClose();
    } catch (error) {
      console.error('Erreur création post:', error);
      
      // Afficher plus de détails sur l'erreur
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        
        // Afficher les erreurs de validation si disponibles
        if (error.response.data && typeof error.response.data === 'object') {
          const errorMessages = [];
          Object.keys(error.response.data).forEach(key => {
            if (Array.isArray(error.response.data[key])) {
              errorMessages.push(...error.response.data[key]);
            } else {
              errorMessages.push(error.response.data[key]);
            }
          });
          
          if (errorMessages.length > 0) {
            toast.error(`Erreur: ${errorMessages.join(', ')}`);
            return;
          }
        }
      }
      
      toast.error('Erreur lors de la création de la publication');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      title: '',
      content: '',
      post_type: 'info',
      is_anonymous: false,
      privacy: 'public'
    });
    setSelectedFiles([]);
    setUploadProgress(0);
    onClose();
  };

  const renderFilePreview = (file, index) => {
    const isVideo = file.type.startsWith('video/');
    const isImage = file.type.startsWith('image/');
    
    return (
      <div key={index} className="relative group">
        <div className="relative rounded-lg overflow-hidden bg-gray-100">
          {isImage ? (
            <img
              src={URL.createObjectURL(file)}
              alt={file.name}
              className="w-full h-32 object-cover"
            />
          ) : isVideo ? (
            <video
              src={URL.createObjectURL(file)}
              className="w-full h-32 object-cover"
              controls
            />
          ) : null}
          
          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-200 flex items-center justify-center">
            <button
              onClick={() => removeFile(index)}
              className="opacity-0 group-hover:opacity-100 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-all duration-200"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="mt-2 text-xs text-gray-500">
          {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
        </div>
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">Créer une publication</h3>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4">
          {/* Zone de texte */}
          <div className="mb-4">
            <textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              placeholder={`Quoi de neuf, ${user?.first_name || 'utilisateur'} ?`}
              className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={4}
            />
          </div>

          {/* Zone de drag & drop */}
          <div
            ref={dropZoneRef}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-6 text-center transition-all duration-200 ${
              dragActive 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept="image/*,video/*"
              onChange={handleFileInput}
              className="hidden"
            />
            
            <div className="space-y-2">
              <div className="flex justify-center space-x-4">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Image className="w-4 h-4" />
                  <span>Photo/Vidéo</span>
                </button>
              </div>
              
              <p className="text-sm text-gray-500">
                Glissez-déposez vos fichiers ici ou cliquez pour sélectionner
              </p>
              <p className="text-xs text-gray-400">
                Images: max 10MB • Vidéos: max 50MB, 60s max
              </p>
            </div>
          </div>

          {/* Aperçu des fichiers */}
          {selectedFiles.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                Fichiers sélectionnés ({selectedFiles.length})
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {selectedFiles.map((file, index) => renderFilePreview(file, index))}
              </div>
            </div>
          )}

          {/* Barre de progression */}
          {isUploading && (
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                <span>Upload en cours...</span>
                <span>{Math.round(uploadProgress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}

          {/* Options de publication */}
          <div className="mt-6 space-y-4">
            {/* Type de publication */}
          <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type de publication
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {postTypes.map((type) => {
                const Icon = type.icon;
                return (
                  <button
                    key={type.value}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, post_type: type.value }))}
                      className={`flex items-center space-x-2 p-3 rounded-lg border transition-colors ${
                        formData.post_type === type.value
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${type.color}`} />
                      <span className="text-sm">{type.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

            {/* Confidentialité */}
          <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confidentialité
                  </label>
              <div className="space-y-2">
                {privacyOptions.map((option) => {
                  const Icon = option.icon;
                  return (
                    <button
                      key={option.value}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, privacy: option.value }))}
                      className={`flex items-center space-x-3 w-full p-3 rounded-lg border transition-colors ${
                        formData.privacy === option.value
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      <Icon className="w-4 h-4 text-gray-600" />
                      <div className="text-left">
                        <div className="text-sm font-medium">{option.label}</div>
                        <div className="text-xs text-gray-500">{option.description}</div>
              </div>
                </button>
                  );
                })}
              </div>
              </div>

            {/* Options supplémentaires */}
          <div className="flex items-center space-x-4">
            <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="is_anonymous"
                  checked={formData.is_anonymous}
                  onChange={handleChange}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Publication anonyme</span>
            </label>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3 mt-6 pt-4 border-t">
            <button
              type="button"
              onClick={handleClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={isLoading || isUploading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? 'Publication...' : 'Publier'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreatePost; 
import React, { useState } from 'react';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  X, 
  ChevronLeft, 
  ChevronRight,
  Maximize2
} from 'lucide-react';
import LiveTimer from './LiveTimer';

const MediaGallery = ({ media, className = '' }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [showFullscreen, setShowFullscreen] = useState(false);


  if (!media || media.length === 0) return null;

  const currentMedia = media[currentIndex];
  const isVideo = currentMedia.media_type === 'video';
  const isLive = currentMedia.is_live;

  const nextMedia = () => {
    setCurrentIndex((prev) => (prev + 1) % media.length);
  };

  const prevMedia = () => {
    setCurrentIndex((prev) => (prev - 1 + media.length) % media.length);
  };





  const togglePlayPause = () => {
    if (isVideo) {
      const video = document.getElementById(`video-${currentMedia.id}`);
      if (video) {
        if (isPlaying) {
          video.pause();
        } else {
          video.play();
        }
        setIsPlaying(!isPlaying);
      }
    }
  };

  const toggleMute = () => {
    if (isVideo) {
      const video = document.getElementById(`video-${currentMedia.id}`);
      if (video) {
        video.muted = !isMuted;
        setIsMuted(!isMuted);
      }
    }
  };

  const handleVideoPlay = () => setIsPlaying(true);
  const handleVideoPause = () => setIsPlaying(false);

  const renderMediaContent = () => {
    if (isLive) {
      // Construire l'URL de la vidéo avec fallback
      const videoUrl = currentMedia.file_url || currentMedia.file || '';
      
      // Détecter le type MIME basé sur l'extension
      const getVideoType = (url) => {
        if (url.includes('.webm')) return 'video/webm';
        if (url.includes('.mp4')) return 'video/mp4';
        if (url.includes('.mov')) return 'video/quicktime';
        return 'video/mp4'; // fallback
      };
      
      const videoType = getVideoType(videoUrl);
      
      return (
        <div className="relative bg-black rounded-lg overflow-hidden">
          <video
            id={`video-${currentMedia.id}`}
            className="w-full h-full object-cover"
            autoPlay
            muted
            onPlay={handleVideoPlay}
            onPause={handleVideoPause}
            onError={(e) => {
              console.error('Erreur chargement vidéo live:', videoUrl, e);
            }}
          >
            <source src={videoUrl} type={videoType} />
          </video>
          
          {/* Badge Live avec chronomètre */}
          <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
            <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
            <span>EN DIRECT</span>
            <LiveTimer 
              startTime={currentMedia.live_started_at}
              isActive={isLive}
              variant="compact"
              className="ml-2"
            />
          </div>
          
          {/* Spectateurs */}
          <div className="absolute top-4 right-4 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
            {currentMedia.live_viewers_count} spectateurs
          </div>
        </div>
      );
    }

    if (isVideo) {
      // Construire l'URL de la vidéo avec fallback
      const videoUrl = currentMedia.file_url || currentMedia.file || '';
      
      // Détecter le type MIME basé sur l'extension
      const getVideoType = (url) => {
        if (url.includes('.webm')) return 'video/webm';
        if (url.includes('.mp4')) return 'video/mp4';
        if (url.includes('.mov')) return 'video/quicktime';
        return 'video/mp4'; // fallback
      };
      
      const videoType = getVideoType(videoUrl);
      
      return (
        <div className="relative bg-black rounded-lg overflow-hidden">
          <video
            id={`video-${currentMedia.id}`}
            className="w-full h-full object-cover"
            controls
            preload="metadata"
            onPlay={handleVideoPlay}
            onPause={handleVideoPause}
            onError={(e) => {
              console.error('Erreur chargement vidéo:', videoUrl, e);
              // Essayer de détecter le type de fichier et proposer une solution
              if (videoUrl.includes('.webm')) {
                console.warn('Format WebM détecté - compatibilité limitée sur certains navigateurs');
                console.warn('Format vidéo non supporté par votre navigateur. Essayez Chrome ou Firefox.');
              }
            }}
          >
            <source src={videoUrl} type={videoType} />
            <source src={videoUrl} type="video/mp4" />
            <source src={videoUrl} type="video/webm" />
            <div className="flex flex-col items-center justify-center h-full text-white bg-gray-800 p-4">
              <p className="mb-4">Votre navigateur ne supporte pas la lecture de cette vidéo.</p>
              {videoUrl.includes('.webm') && (
                <a 
                  href={videoUrl} 
                  download 
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  📥 Télécharger la vidéo
                </a>
              )}
            </div>
          </video>
          
          {/* Contrôles personnalisés */}
          <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between bg-black bg-opacity-50 rounded-lg p-2">
            <button
              onClick={togglePlayPause}
              className="text-white hover:text-gray-300 transition-colors"
            >
              {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
            </button>
            
            <button
              onClick={toggleMute}
              className="text-white hover:text-gray-300 transition-colors"
            >
              {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
            </button>
            
            <button
              onClick={() => setShowFullscreen(true)}
              className="text-white hover:text-gray-300 transition-colors"
            >
              <Maximize2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      );
    }

    // Image - Utiliser l'URL complète si disponible, sinon construire l'URL
    const imageUrl = currentMedia.file || currentMedia.file_url || '';
    
    return (
      <div className="relative">
        <img
          src={imageUrl}
          alt={currentMedia.title || 'Image'}
          className="w-full h-full object-cover rounded-lg"
          onError={(e) => {
            console.error('Erreur chargement image:', imageUrl);
            e.target.style.display = 'none';
          }}
        />
        
        {/* Bouton plein écran */}
        <button
          onClick={() => setShowFullscreen(true)}
          className="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70 transition-colors"
        >
          <Maximize2 className="w-5 h-5" />
        </button>
      </div>
    );
  };

  const renderThumbnails = () => {
    if (media.length <= 1) return null;

    return (
      <div className="flex space-x-2 mt-3 overflow-x-auto">
        {media.map((item, index) => {
          // Utiliser l'URL complète si disponible
          const imageUrl = item.file || item.file_url || '';
          const thumbnailUrl = item.thumbnail_url || imageUrl;
          
          return (
            <button
              key={item.id}
              onClick={() => setCurrentIndex(index)}
              className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all ${
                index === currentIndex
                  ? 'border-blue-500'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              {item.media_type === 'video' ? (
                <div className="relative w-full h-full">
                  <img
                    src={thumbnailUrl}
                    alt={item.title || 'Vidéo'}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      console.error('Erreur chargement thumbnail vidéo:', thumbnailUrl);
                      e.target.style.display = 'none';
                    }}
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                    <Play className="w-4 h-4 text-white" />
                  </div>
                </div>
              ) : (
                <img
                  src={imageUrl}
                  alt={item.title || 'Image'}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    console.error('Erreur chargement thumbnail image:', imageUrl);
                    e.target.style.display = 'none';
                  }}
                />
              )}
            </button>
          );
        })}
      </div>
    );
  };

  const renderFullscreenModal = () => {
    if (!showFullscreen) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
        <div className="relative w-full h-full flex items-center justify-center">
          {/* Fermer */}
          <button
            onClick={() => setShowFullscreen(false)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors z-10"
          >
            <X className="w-8 h-8" />
          </button>

          {/* Navigation */}
          {media.length > 1 && (
            <>
              <button
                onClick={prevMedia}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-10"
              >
                <ChevronLeft className="w-8 h-8" />
              </button>
              <button
                onClick={nextMedia}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-10"
              >
                <ChevronRight className="w-8 h-8" />
              </button>
            </>
          )}

          {/* Contenu */}
          <div className="max-w-4xl max-h-full p-4">
            {isVideo ? (
              <video
                src={currentMedia.file_url}
                className="max-w-full max-h-full object-contain"
                controls
                autoPlay
              />
            ) : (
              <img
                src={currentMedia.file || currentMedia.file_url}
                alt={currentMedia.title || 'Image'}
                className="max-w-full max-h-full object-contain"
                onError={(e) => {
                  console.error('Erreur chargement image plein écran:', currentMedia.file || currentMedia.file_url);
                }}
              />
            )}
          </div>

          {/* Indicateurs */}
          {media.length > 1 && (
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
              {media.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentIndex(index)}
                  className={`w-3 h-3 rounded-full transition-colors ${
                    index === currentIndex ? 'bg-white' : 'bg-white bg-opacity-50'
                  }`}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className={className}>
      <div className="relative">
        {renderMediaContent()}
        
        {/* Navigation pour plusieurs médias */}
        {media.length > 1 && (
          <>
            <button
              onClick={prevMedia}
              className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70 transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button
              onClick={nextMedia}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70 transition-colors"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </>
        )}
      </div>

      {renderThumbnails()}
      {renderFullscreenModal()}
    </div>
  );
};

export default MediaGallery; 
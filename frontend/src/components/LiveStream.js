import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { mediaAPI } from '../services/mediaAPI';
import { 
  Mic, 
  MicOff, 
  Camera, 
  CameraOff,
  Play,
  Square,
  MessageCircle,
  Send,
  X,
  Volume2,
  Sliders,
  Monitor,
  Wifi,
  Activity
} from 'lucide-react';
import toast from 'react-hot-toast';
import { formatTime } from '../utils/timeUtils';
import LiveTimer from './LiveTimer';

const LiveStream = ({ isOpen, onClose, onLiveStarted }) => {
  const { user } = useAuth();
  const [isStarting, setIsStarting] = useState(false);
  const [isLive, setIsLive] = useState(false);
  const [stream, setStream] = useState(null);
  const [liveData, setLiveData] = useState(null);
  const [showChat, setShowChat] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoEnabled, setIsVideoEnabled] = useState(true);
  const [viewersCount] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  
  // Nouveaux états pour les contrôles de niveau live
  const [streamVolume, setStreamVolume] = useState(100);
  const [videoQuality, setVideoQuality] = useState('720p');
  const [showAdvancedControls, setShowAdvancedControls] = useState(false);
  const [streamLatency, setStreamLatency] = useState('low');
  const [bitrate, setBitrate] = useState(2500);
  const [fps, setFps] = useState(30);
  
  // États pour la vidéo enregistrée
  const [recordedVideo, setRecordedVideo] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [videoDuration, setVideoDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  
  // États pour le chronomètre du live
  const [liveStartTime, setLiveStartTime] = useState(null);
  const [liveDuration, setLiveDuration] = useState(0);
  
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    content: ''
  });

  useEffect(() => {
    if (isOpen && !stream) {
      startCamera();
    }
    
    return () => {
      stopCamera();
      // Nettoyer l'URL de la vidéo enregistrée
      if (recordedVideo) {
        URL.revokeObjectURL(recordedVideo);
      }
    };
  }, [isOpen, recordedVideo, stream]);



  const startCamera = async () => {
    // Vérifier que l'API getUserMedia est disponible
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast.error('Votre navigateur ne supporte pas l\'accès à la caméra');
      return;
    }

    try {
      // Première tentative avec des contraintes optimales
      const constraints = {
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          frameRate: { ideal: 30 }
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      };

      // Créer une promesse avec timeout plus long
      const getUserMediaPromise = navigator.mediaDevices.getUserMedia(constraints);
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Timeout: Impossible d\'accéder à la caméra dans le délai imparti')), 30000);
      });

      const mediaStream = await Promise.race([getUserMediaPromise, timeoutPromise]);
      
      setStream(mediaStream);
      streamRef.current = mediaStream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error('Première tentative échouée, essai avec des contraintes simplifiées:', error);
      
      // Deuxième tentative avec des contraintes plus simples
      try {
        const simpleConstraints = {
          video: true,
          audio: true
        };

        const mediaStream = await navigator.mediaDevices.getUserMedia(simpleConstraints);
        
        setStream(mediaStream);
        streamRef.current = mediaStream;
        
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
        
        toast.success('Caméra démarrée avec des paramètres de base');
      } catch (secondError) {
        console.error('Erreur accès caméra (tentative finale):', secondError);
        
        // Messages d'erreur plus spécifiques
        if (secondError.name === 'NotAllowedError') {
          toast.error('Accès à la caméra refusé. Veuillez autoriser l\'accès dans les paramètres du navigateur.');
        } else if (secondError.name === 'NotFoundError') {
          toast.error('Aucune caméra trouvée. Veuillez connecter une caméra.');
        } else if (secondError.message.includes('Timeout')) {
          toast.error('Délai d\'attente dépassé. Vérifiez que votre caméra n\'est pas utilisée par une autre application.');
        } else {
          toast.error('Impossible d\'accéder à la caméra/microphone. Vérifiez vos permissions.');
        }
      }
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      setStream(null);
      streamRef.current = null;
    }
  };

  const toggleMute = () => {
    if (stream) {
      const audioTrack = stream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        setIsMuted(!isMuted);
      }
    }
  };

  const toggleVideo = () => {
    if (stream) {
      const videoTrack = stream.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled;
        setIsVideoEnabled(!isVideoEnabled);
      }
    }
  };

  const startLive = async () => {
    // Si pas de titre, utiliser un titre par défaut
    const liveData = {
      title: formData.title.trim() || `Live de ${user?.first_name || 'Utilisateur'}`,
      description: formData.description.trim() || 'Live en cours...',
      content: formData.content.trim() || 'Live démarré !'
    };

    setIsStarting(true);
    try {
      const response = await mediaAPI.startLive(liveData);
      setLiveData(response);
      setIsLive(true);
      setLiveStartTime(Date.now()); // Démarrer le chronomètre
      
      // Démarrer l'enregistrement de la vidéo
      if (stream && !mediaRecorderRef.current) {
        const mediaRecorder = new MediaRecorder(stream, {
          mimeType: 'video/webm;codecs=vp8,opus'
        });
        
        mediaRecorderRef.current = mediaRecorder;
        mediaRecorderRef.current.recordedChunks = [];
        
        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            mediaRecorderRef.current.recordedChunks.push(event.data);
          }
        };
        
        mediaRecorderRef.current.start(1000); // Enregistrer par segments de 1 seconde
      }
      
      toast.success('Live démarré avec succès !');
      onLiveStarted?.(response);
      
    } catch (error) {
      console.error('Erreur démarrage live:', error);
      toast.error('Erreur lors du démarrage du live');
    } finally {
      setIsStarting(false);
    }
  };

  const stopLive = async () => {
    if (!liveData) return;

    try {
      // Arrêter l'enregistrement si actif
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
      }

      await mediaAPI.stopLive(liveData.live_id);
      setIsLive(false);
      setLiveData(null);
      setLiveStartTime(null); // Arrêter le chronomètre
      setLiveDuration(0);
      
      // Créer une URL pour la vidéo enregistrée
      if (mediaRecorderRef.current && mediaRecorderRef.current.recordedChunks && mediaRecorderRef.current.recordedChunks.length > 0) {
        const blob = new Blob(mediaRecorderRef.current.recordedChunks, { type: 'video/webm' });
        const videoUrl = URL.createObjectURL(blob);
        setRecordedVideo(videoUrl);
        
        // Configurer la vidéo pour la lecture avec un délai pour s'assurer que le DOM est mis à jour
        setTimeout(() => {
          if (videoRef.current) {
            videoRef.current.src = videoUrl;
            videoRef.current.load();
            videoRef.current.addEventListener('loadedmetadata', () => {
              setVideoDuration(videoRef.current.duration);
              setCurrentTime(0);
              setIsPlaying(false);
            });
          }
        }, 100);
        
        toast.success('Live arrêté - Vidéo disponible pour lecture');
      } else {
        toast.warning('Aucune vidéo enregistrée disponible');
      }
    } catch (error) {
      console.error('Erreur arrêt live:', error);
      toast.error('Erreur lors de l\'arrêt du live');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    startLive();
  };

  const sendChatMessage = () => {
    if (!newMessage.trim()) return;
    
    const message = {
      id: Date.now(),
      author: user,
      content: newMessage,
      timestamp: new Date().toISOString()
    };
    
    setChatMessages(prev => [...prev, message]);
    setNewMessage('');
  };

  // Nouvelles fonctions pour les contrôles de niveau live
  const handleVolumeChange = (newVolume) => {
    setStreamVolume(newVolume);
    if (stream) {
      const audioTrack = stream.getAudioTracks()[0];
      if (audioTrack) {
        // Ajuster le volume du stream audio
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        const gainNode = audioContext.createGain();
        gainNode.gain.value = newVolume / 100;
        source.connect(gainNode);
      }
    }
  };

  const handleQualityChange = (quality) => {
    setVideoQuality(quality);
    // Dans un vrai projet, vous ajusteriez la qualité du stream ici
    toast.success(`Qualité vidéo changée vers ${quality}`);
  };

  const handleLatencyChange = (latency) => {
    setStreamLatency(latency);
    // Dans un vrai projet, vous ajusteriez la latence du stream ici
    toast.success(`Latence changée vers ${latency}`);
  };

  const handleBitrateChange = (newBitrate) => {
    setBitrate(newBitrate);
    // Dans un vrai projet, vous ajusteriez le bitrate du stream ici
    toast.success(`Bitrate changé vers ${newBitrate} kbps`);
  };

  const handleFpsChange = (newFps) => {
    setFps(newFps);
    // Dans un vrai projet, vous ajusteriez le FPS du stream ici
    toast.success(`FPS changé vers ${newFps}`);
  };

  // Fonctions pour la lecture de la vidéo enregistrée
  const togglePlayPause = () => {
    if (videoRef.current && recordedVideo) {
      if (isPlaying) {
        videoRef.current.pause();
        setIsPlaying(false);
      } else {
        const playPromise = videoRef.current.play();
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              setIsPlaying(true);
            })
            .catch(error => {
              console.error('Erreur lors de la lecture:', error);
              toast.error('Erreur lors de la lecture de la vidéo');
            });
        }
      }
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setVideoDuration(videoRef.current.duration);
    }
  };

  const handleSeek = (e) => {
    if (videoRef.current) {
      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const width = rect.width;
      const seekTime = (clickX / width) * videoDuration;
      videoRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
  };



  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">
            {isLive ? 'Live en cours' : recordedVideo ? 'Vidéo enregistrée' : 'Démarrer un live'}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex h-[calc(90vh-120px)]">
          {/* Zone principale */}
          <div className="flex-1 flex flex-col">
            {/* Prévisualisation vidéo */}
            <div className="flex-1 bg-black relative">
              <video
                ref={videoRef}
                autoPlay={!recordedVideo}
                muted={!recordedVideo}
                playsInline
                className="w-full h-full object-cover transform scale-x-[-1]"
                style={{ transform: recordedVideo ? 'none' : 'scaleX(-1)' }}
                onTimeUpdate={handleTimeUpdate}
                onLoadedMetadata={handleLoadedMetadata}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
              />
              
              {/* Badge Live avec chronomètre */}
              {isLive && (
                <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  <span>EN DIRECT</span>
                  <LiveTimer 
                    startTime={liveStartTime} 
                    isActive={isLive}
                    variant="compact"
                    className="ml-2"
                  />
                </div>
              )}
              
              {/* Spectateurs */}
              {isLive && (
                <div className="absolute top-4 right-4 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
                  {viewersCount} spectateurs
                </div>
              )}
              
              {/* Bouton démarrer le live - visible quand pas en live */}
              {!isLive && stream && !recordedVideo && (
                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30">
                  <div className="text-center">
                    <div className="bg-white rounded-lg p-6 shadow-2xl max-w-md mx-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Prêt à démarrer votre live ?
                      </h3>
                      <p className="text-gray-600 mb-6">
                        Votre caméra est active. Cliquez sur "Démarrer le live" pour commencer à diffuser.
                      </p>
                      <div className="flex space-x-3">
                        <button
                          onClick={onClose}
                          className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          Annuler
                        </button>
                        <button
                          onClick={startLive}
                          disabled={isStarting}
                          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {isStarting ? (
                            <>
                              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                              <span>Démarrage...</span>
                            </>
                          ) : (
                            <>
                              <Play className="w-4 h-4" />
                              <span>Démarrer le live</span>
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Message si pas de caméra */}
              {!stream && !isLive && !recordedVideo && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
                  <div className="text-center text-white">
                    <Camera className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                    <h3 className="text-lg font-semibold mb-2">Accès à la caméra</h3>
                    <p className="text-gray-400 mb-4">
                      Autorisez l'accès à votre caméra pour commencer le live
                    </p>
                    <button
                      onClick={startCamera}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Autoriser la caméra
                    </button>
                  </div>
                </div>
              )}

              {/* Message pour vidéo enregistrée en cours de chargement */}
              {recordedVideo && !isLive && videoDuration === 0 && (
                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                  <div className="text-center text-white">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-white mb-4"></div>
                    <h3 className="text-lg font-semibold mb-2">Préparation de la vidéo</h3>
                    <p className="text-gray-300">
                      Votre vidéo enregistrée est en cours de préparation...
                    </p>
                  </div>
                </div>
              )}
              
              {/* Contrôles de live */}
              {isLive && (
                <div className="absolute bottom-6 left-6 right-6 flex items-center justify-between bg-gradient-to-t from-black/80 to-transparent p-4 rounded-lg">
                <div className="flex items-center space-x-3">
                  {/* Chronomètre du live */}
                  <LiveTimer 
                    startTime={liveStartTime}
                    isActive={isLive}
                    variant="detailed"
                    className="mr-4"
                  />
                  <button
                    onClick={toggleMute}
                    className={`p-3 rounded-full transition-all duration-200 shadow-lg ${
                      isMuted ? 'bg-red-500 text-white hover:bg-red-600' : 'bg-black/70 text-white hover:bg-black/90'
                    }`}
                    title={isMuted ? 'Activer le micro' : 'Désactiver le micro'}
                  >
                    {isMuted ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                  </button>
                  
                  <button
                    onClick={toggleVideo}
                    className={`p-3 rounded-full transition-all duration-200 shadow-lg ${
                      !isVideoEnabled ? 'bg-red-500 text-white hover:bg-red-600' : 'bg-black/70 text-white hover:bg-black/90'
                    }`}
                    title={isVideoEnabled ? 'Désactiver la caméra' : 'Activer la caméra'}
                  >
                    {isVideoEnabled ? <Camera className="w-5 h-5" /> : <CameraOff className="w-5 h-5" />}
                  </button>

                  {/* Contrôles de niveau live */}
                  {isLive && (
                    <>
                      {/* Contrôle du volume */}
                      <div className="flex items-center space-x-2 bg-black/70 rounded-lg px-3 py-2 backdrop-blur-sm">
                        <Volume2 className="w-4 h-4 text-white" />
                        <input
                          type="range"
                          min="0"
                          max="100"
                          value={streamVolume}
                          onChange={(e) => handleVolumeChange(parseInt(e.target.value))}
                          className="w-20 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
                        />
                        <span className="text-white text-xs font-medium">{streamVolume}%</span>
                      </div>

                      {/* Contrôle de la qualité */}
                      <div className="flex items-center space-x-2 bg-black/70 rounded-lg px-3 py-2 backdrop-blur-sm">
                        <Monitor className="w-4 h-4 text-white" />
                        <select
                          value={videoQuality}
                          onChange={(e) => handleQualityChange(e.target.value)}
                          className="bg-transparent text-white text-xs border-none outline-none font-medium"
                        >
                          <option value="480p">480p</option>
                          <option value="720p">720p</option>
                          <option value="1080p">1080p</option>
                        </select>
                      </div>

                      {/* Bouton paramètres avancés */}
                      <button
                        onClick={() => setShowAdvancedControls(!showAdvancedControls)}
                        className="p-3 rounded-full transition-all duration-200 bg-black/70 text-white hover:bg-black/90 shadow-lg"
                        title="Paramètres avancés"
                      >
                        <Sliders className="w-5 h-5" />
                      </button>
                    </>
                  )}
                </div>
                
                {isLive && (
                  <button
                    onClick={stopLive}
                    className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-all duration-200 flex items-center space-x-2 shadow-lg font-medium"
                  >
                    <Square className="w-4 h-4" />
                    <span>Arrêter le live</span>
                  </button>
                )}
              </div>
              )}

              {/* Contrôles de lecture pour la vidéo enregistrée */}
              {recordedVideo && !isLive && (
                <div className="absolute bottom-6 left-6 right-6 bg-gradient-to-t from-black/80 to-transparent p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <button
                        onClick={togglePlayPause}
                        className="p-3 rounded-full bg-black/70 text-white hover:bg-black/90 transition-all duration-200 shadow-lg"
                        title={isPlaying ? 'Pause' : 'Lecture'}
                      >
                        {isPlaying ? (
                          <div className="w-5 h-5 flex items-center justify-center">
                            <div className="w-1 h-4 bg-white mx-0.5"></div>
                            <div className="w-1 h-4 bg-white mx-0.5"></div>
                          </div>
                        ) : (
                          <Play className="w-5 h-5" />
                        )}
                      </button>
                      
                      <div className="text-white text-sm font-medium">
                        {videoDuration > 0 ? `${formatTime(currentTime)} / ${formatTime(videoDuration)}` : 'Chargement...'}
                      </div>
                    </div>
                    
                    <button
                      onClick={onClose}
                      className="text-white hover:text-gray-300 transition-colors"
                      title="Fermer"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  
                  {/* Barre de progression */}
                  <div 
                    className="w-full h-2 bg-gray-600 rounded-full cursor-pointer relative"
                    onClick={handleSeek}
                  >
                    <div 
                      className="h-full bg-red-600 rounded-full transition-all duration-200"
                      style={{ width: `${videoDuration > 0 ? (currentTime / videoDuration) * 100 : 0}%` }}
                ></div>
              </div>
                  
                  {/* Message d'information */}
                  {videoDuration === 0 && (
                    <div className="text-center text-white text-sm mt-2">
                      <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Préparation de la vidéo...
                    </div>
                  )}
                </div>
              )}

              {/* Panneau de contrôles avancés */}
              {isLive && showAdvancedControls && (
                <div className="absolute bottom-32 left-6 bg-black/95 text-white rounded-lg p-6 space-y-4 min-w-80 live-controls-panel backdrop-blur-sm shadow-2xl border border-white/10">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">Paramètres avancés</h4>
                    <button
                      onClick={() => setShowAdvancedControls(false)}
                      className="text-gray-400 hover:text-white"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="space-y-3">
                    {/* Latence */}
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Latence</label>
                      <select
                        value={streamLatency}
                        onChange={(e) => handleLatencyChange(e.target.value)}
                        className="w-full bg-gray-800 text-white text-sm rounded px-2 py-1"
                      >
                        <option value="ultra-low">Ultra-faible</option>
                        <option value="low">Faible</option>
                        <option value="medium">Moyenne</option>
                        <option value="high">Élevée</option>
                      </select>
                    </div>

                    {/* Bitrate */}
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Bitrate (kbps)</label>
                      <input
                        type="range"
                        min="1000"
                        max="6000"
                        step="500"
                        value={bitrate}
                        onChange={(e) => handleBitrateChange(parseInt(e.target.value))}
                        className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
                      />
                      <div className="flex justify-between text-xs text-gray-300">
                        <span>1000</span>
                        <span>{bitrate}</span>
                        <span>6000</span>
                      </div>
                    </div>

                    {/* FPS */}
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">FPS</label>
                      <select
                        value={fps}
                        onChange={(e) => handleFpsChange(parseInt(e.target.value))}
                        className="w-full bg-gray-800 text-white text-sm rounded px-2 py-1"
                      >
                        <option value={24}>24 FPS</option>
                        <option value={30}>30 FPS</option>
                        <option value={60}>60 FPS</option>
                      </select>
                    </div>

                    {/* Statistiques de streaming */}
                    <div className="pt-2 border-t border-gray-700">
                      <div className="flex items-center space-x-2 text-xs">
                        <Wifi className="w-3 h-3" />
                        <span>Connexion stable</span>
                      </div>
                      <div className="flex items-center space-x-2 text-xs mt-1">
                        <Activity className="w-3 h-3" />
                        <span>Latence: {streamLatency === 'ultra-low' ? '< 1s' : streamLatency === 'low' ? '1-2s' : '2-3s'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Message pour la vidéo enregistrée */}
              {recordedVideo && !isLive && (
                <div className="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                  <span>VIDÉO ENREGISTRÉE</span>
                </div>
              )}
            </div>

            {/* Formulaire de configuration */}
            {!isLive && (
              <div className="p-4 border-t">
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Titre du live *
                    </label>
                    <input
                      type="text"
                      name="title"
                      value={formData.title}
                      onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                      placeholder="Titre de votre live..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description (optionnel)
                    </label>
                    <textarea
                      name="description"
                      value={formData.description}
                      onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                      placeholder="Description de votre live..."
                      rows={2}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Message de publication
                    </label>
                    <textarea
                      name="content"
                      value={formData.content}
                      onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                      placeholder="Message accompagnant votre live..."
                      rows={2}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    />
                  </div>
                  
                  <div className="flex justify-end space-x-3">
                    <button
                      type="button"
                      onClick={onClose}
                      className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                    >
                      Annuler
                    </button>
                    <button
                      type="submit"
                      disabled={isStarting}
                      className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                    >
                      {isStarting ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Démarrage...</span>
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4" />
                          <span>Démarrer le live</span>
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>

          {/* Chat */}
          {isLive && (
            <div className="w-80 border-l border-gray-200 flex flex-col">
              <div className="p-4 border-b">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium text-gray-900">Chat en direct</h4>
                  <button
                    onClick={() => setShowChat(!showChat)}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <MessageCircle className="w-5 h-5" />
                  </button>
                </div>
              </div>
              
              {showChat && (
                <>
                  <div className="flex-1 p-4 overflow-y-auto space-y-3">
                    {chatMessages.map((message) => (
                      <div key={message.id} className="flex space-x-2">
                        <img
                          src={message.author?.profile_picture || '/default-avatar.svg'}
                          alt={message.author?.first_name || 'Utilisateur'}
                          className="w-6 h-6 rounded-full object-cover flex-shrink-0"
                          onError={(e) => {
                            e.target.src = '/default-avatar.svg';
                          }}
                        />
                        <div className="flex-1">
                          <div className="bg-gray-50 rounded-lg px-3 py-2">
                            <div className="flex items-center space-x-2">
                              <span className="text-sm font-medium text-gray-900">
                                {message.author?.first_name || 'Utilisateur'} {message.author?.last_name || ''}
                              </span>
                              <span className="text-xs text-gray-500">
                                {new Date(message.timestamp).toLocaleTimeString('fr-FR', { 
                                  hour: '2-digit', 
                                  minute: '2-digit' 
                                })}
                              </span>
                            </div>
                            <p className="text-sm text-gray-700 mt-1">{message.content}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="p-4 border-t">
                    <form onSubmit={(e) => { e.preventDefault(); sendChatMessage(); }} className="flex space-x-2">
                      <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Tapez votre message..."
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                      />
                      <button
                        type="submit"
                        disabled={!newMessage.trim()}
                        className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      >
                        <Send className="w-4 h-4" />
                      </button>
                    </form>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LiveStream; 
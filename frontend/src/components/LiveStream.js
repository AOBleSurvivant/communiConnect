import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { mediaAPI } from '../services/mediaAPI';
import { liveChatAPI } from '../services/liveChatAPI';
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
  Activity,
  Check,
  Info
} from 'lucide-react';
import toast from 'react-hot-toast';
import { formatTime } from '../utils/timeUtils';
import LiveTimer from './LiveTimer';

const LiveStream = ({ isOpen, onClose, onLiveStarted, onLiveStopped }) => {
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
  
  // Informations sur l'origine live de la vidéo
  const [liveInfo] = useState(null);
  const [showLiveDetails, setShowLiveDetails] = useState(false);
  
  // États pour le chronomètre du live
  const [liveStartTime, setLiveStartTime] = useState(null);
  
  const [isStopping, setIsStopping] = useState(false);
  const [showStopConfirmation, setShowStopConfirmation] = useState(false);
  
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
    };
  }, [isOpen]); // Supprimé stream comme dépendance pour éviter la boucle infinie

  useEffect(() => {
    // Nettoyer l'URL de la vidéo enregistrée quand le composant se démonte
    return () => {
      if (recordedVideo) {
        URL.revokeObjectURL(recordedVideo);
      }
    };
  }, [recordedVideo]);

  // Debug: Surveiller les changements d'état (réduit pour éviter le spam)
  useEffect(() => {
    console.log('🔄 État recordedVideo changé:', recordedVideo);
    console.log('🔄 État isLive:', isLive);
    console.log('🔄 État videoDuration:', videoDuration);
  }, [recordedVideo, isLive]); // Supprimé videoDuration pour éviter les logs excessifs



  const startCamera = async () => {
    // Éviter de redémarrer si un stream existe déjà
    if (stream || streamRef.current) {
      console.log('🎥 Caméra déjà active, pas de redémarrage nécessaire');
      return;
    }

    // Vérifier que l'API getUserMedia est disponible
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast.error('Votre navigateur ne supporte pas l\'accès à la caméra');
      return;
    }

    try {
      // Commencer avec des contraintes très simples
      const simpleConstraints = {
        video: true,
        audio: true
      };

      console.log('🎥 Tentative d\'accès à la caméra avec contraintes simples...');
      const mediaStream = await navigator.mediaDevices.getUserMedia(simpleConstraints);
      
      setStream(mediaStream);
      streamRef.current = mediaStream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        // Attendre que la vidéo soit chargée
        videoRef.current.onloadedmetadata = () => {
          console.log('✅ Caméra démarrée avec succès');
          toast.success('Caméra démarrée !');
        };
      }
      
    } catch (error) {
      console.error('❌ Erreur accès caméra:', error);
      
      // Messages d'erreur spécifiques
      if (error.name === 'NotAllowedError') {
        toast.error('Accès à la caméra refusé. Veuillez autoriser l\'accès dans les paramètres du navigateur.');
      } else if (error.name === 'NotFoundError') {
        toast.error('Aucune caméra trouvée. Veuillez connecter une caméra.');
      } else if (error.name === 'NotReadableError') {
        toast.error('Caméra déjà utilisée par une autre application.');
      } else if (error.name === 'OverconstrainedError') {
        toast.error('Contraintes de caméra non supportées.');
      } else if (error.message.includes('Timeout')) {
        toast.error('Délai d\'attente dépassé. Vérifiez que votre caméra n\'est pas utilisée par une autre application.');
      } else {
        toast.error(`Impossible d'accéder à la caméra: ${error.message}`);
      }
      
      // Essayer avec seulement la vidéo si l'audio échoue
      try {
        console.log('🎥 Tentative avec vidéo seulement...');
        const videoOnlyConstraints = {
          video: true,
          audio: false
        };
        
        const mediaStream = await navigator.mediaDevices.getUserMedia(videoOnlyConstraints);
        
        setStream(mediaStream);
        streamRef.current = mediaStream;
        
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
          videoRef.current.onloadedmetadata = () => {
            console.log('✅ Caméra démarrée (vidéo seulement)');
            toast.success('Caméra démarrée (sans audio) !');
          };
        }
        
      } catch (secondError) {
        console.error('❌ Échec de la deuxième tentative:', secondError);
        toast.error('Impossible de démarrer la caméra. Vérifiez vos permissions et votre matériel.');
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
      
      // Charger les messages existants du live
      if (response.post_id) {
        await loadChatMessages(response.post_id);
      }
      
      // Démarrer l'enregistrement de la vidéo
      if (stream && !mediaRecorderRef.current) {
        // Debug: Vérifier les types MIME supportés
        console.log('🔍 Types MIME supportés:');
        console.log('- video/mp4:', MediaRecorder.isTypeSupported('video/mp4'));
        console.log('- video/mp4;codecs=h264:', MediaRecorder.isTypeSupported('video/mp4;codecs=h264'));
        console.log('- video/webm:', MediaRecorder.isTypeSupported('video/webm'));
        console.log('- video/webm;codecs=vp8,opus:', MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus'));
        
        // Essayer différents formats MP4, sinon fallback vers WebM
        let mimeType = 'video/mp4';
        if (!MediaRecorder.isTypeSupported('video/mp4')) {
          if (MediaRecorder.isTypeSupported('video/mp4;codecs=h264')) {
            mimeType = 'video/mp4;codecs=h264';
          } else if (MediaRecorder.isTypeSupported('video/webm')) {
            mimeType = 'video/webm';
          } else {
            mimeType = 'video/webm;codecs=vp8,opus';
          }
        }
        
        console.log('🎬 Type MIME choisi:', mimeType);
        
        const mediaRecorder = new MediaRecorder(stream, {
          mimeType: mimeType
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
    // Afficher la confirmation d'arrêt
    setShowStopConfirmation(true);
  };

  const confirmStopLive = async () => {
    console.log('🛑 Tentative d\'arrêt du live...');
    console.log('📊 État actuel:', { isLive, liveData, mediaRecorderRef: mediaRecorderRef.current?.state });
    
    setIsStopping(true);
    setShowStopConfirmation(false);
    
    if (!liveData) {
      console.log('❌ Pas de liveData, arrêt direct');
      setIsLive(false);
      setLiveData(null);
      setLiveStartTime(null);
      setIsStopping(false);
      toast.success('Live arrêté');
      return;
    }

    // Étape 1: Afficher le message d'arrêt en cours
    toast.success('🔄 Arrêt du live en cours...', { autoClose: 2000 });
    
    try {
      // Étape 2: Arrêter l'enregistrement média avec transition
      console.log('🎥 Arrêt de l\'enregistrement média...');
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        console.log('⏹️ Arrêt du MediaRecorder...');
        
        // Attendre que l'enregistrement se termine proprement
        return new Promise((resolve) => {
          mediaRecorderRef.current.addEventListener('stop', async () => {
            console.log('✅ MediaRecorder arrêté, traitement de la vidéo...');
            
            // Étape 3: Appel API pour arrêter le live
            try {
              // Créer une URL pour la vidéo enregistrée
              if (mediaRecorderRef.current && mediaRecorderRef.current.recordedChunks && mediaRecorderRef.current.recordedChunks.length > 0) {
                console.log('🎬 Création du blob vidéo...');
                // Utiliser le même type MIME que celui détecté pour le MediaRecorder
                const mimeType = mediaRecorderRef.current.mimeType || 'video/mp4';
                const blob = new Blob(mediaRecorderRef.current.recordedChunks, { type: mimeType });
                
                // Uploader la vidéo vers le serveur
                console.log('📤 Upload de la vidéo vers le serveur...');
                console.log('🔍 liveData actuel:', liveData);
                console.log('🔍 live_id utilisé:', liveData.live_id);
                const uploadResponse = await mediaAPI.uploadLiveVideo(
                  liveData.live_id, 
                  blob,
                  (progress) => {
                    console.log(`📤 Upload progress: ${progress}%`);
                    toast.success(`📤 Upload vidéo: ${progress}%`, { autoClose: 1000 });
                  }
                );
                
                console.log('✅ Réponse upload vidéo:', uploadResponse);
                
                // Maintenant arrêter le live
                console.log('🌐 Appel API stopLive...');
                const response = await mediaAPI.stopLive(liveData.live_id);
                console.log('✅ Réponse API stopLive:', response);
                
                if (uploadResponse.media_id) {
                  console.log('✅ Vidéo uploadée et sauvegardée dans la base de données');
                  toast.success('🎬 Vidéo enregistrée et sauvegardée !');
                } else {
                  console.log('⚠️ Vidéo uploadée mais non sauvegardée');
                  toast.error('⚠️ Vidéo enregistrée localement seulement');
                }
                
                // Étape 4: Mise à jour des états avec transition
                setTimeout(() => {
                  setIsLive(false);
                  setLiveData(null);
                  setLiveStartTime(null);
                  setIsStopping(false);
                  
                  console.log('📹 Traitement de la vidéo enregistrée...');
                  // Utiliser l'URL du serveur si disponible
                  const videoUrl = uploadResponse.file_url || URL.createObjectURL(blob);
                  forceVideoDisplay(videoUrl);
                  
                  // Notifier le parent que le live est arrêté
                  onLiveStopped?.({ video_saved: true, video_url: videoUrl, media_id: uploadResponse.media_id });
                  
                  toast.success('🎬 Live terminé - Votre vidéo est prête !', { autoClose: 4000 });
                }, 500); // Délai pour une transition plus douce
                
              } else {
                console.log('⚠️ Aucune vidéo enregistrée trouvée');
                toast.error('⚠️ Aucune vidéo enregistrée disponible');
              }
              
              resolve();
            } catch (apiError) {
              console.error('❌ Erreur API arrêt live:', apiError);
              toast.error('❌ Erreur serveur - Live arrêté localement');
              
              // Arrêt local en cas d'erreur API
              setIsLive(false);
              setLiveData(null);
              setLiveStartTime(null);
              setIsStopping(false);
              
              // Notifier le parent que le live est arrêté
              onLiveStopped?.({ video_saved: false, error: 'API error' });
              
              resolve();
            }
          });
          
          mediaRecorderRef.current.stop();
        });
      } else {
        // Si pas d'enregistrement actif, arrêt direct
        console.log('🌐 Appel API stopLive avec live_id:', liveData.live_id);
        const response = await mediaAPI.stopLive(liveData.live_id);
        console.log('✅ Réponse API stopLive:', response);
        
        setTimeout(() => {
          setIsLive(false);
          setLiveData(null);
          setLiveStartTime(null);
          setIsStopping(false);
          
          // Notifier le parent que le live est arrêté
          onLiveStopped?.({ video_saved: false });
          
          toast.success('✅ Live arrêté avec succès');
        }, 300);
      }
      
    } catch (error) {
      console.error('❌ Erreur arrêt live:', error);
      
      // En cas d'erreur, on arrête quand même le live côté frontend
      console.log('🔄 Arrêt forcé côté frontend...');
      setTimeout(() => {
        setIsLive(false);
        setLiveData(null);
        setLiveStartTime(null);
        setIsStopping(false);
        
        // Notifier le parent que le live est arrêté
        onLiveStopped?.({ video_saved: false, error: 'network_error' });
        
        if (error.response) {
          console.log('📊 Détails erreur:', error.response.data);
          toast.error(`❌ Erreur serveur: ${error.response.data.message || 'Erreur lors de l\'arrêt du live'}`);
        } else if (error.request) {
          console.log('🌐 Erreur réseau');
          toast.error('🌐 Erreur de connexion - Live arrêté localement');
        } else {
          toast.error(`❌ Erreur: ${error.message}`);
        }
      }, 200);
    }
  };

  // Fonction d'arrêt forcé (urgence)
  const forceStopLive = () => {
    console.log('🚨 ARRÊT FORCÉ DU LIVE');
    
    // Arrêter l'enregistrement
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    
    // Arrêter la caméra
    stopCamera();
    
    // Réinitialiser tous les états
    setIsLive(false);
    setLiveData(null);
    setLiveStartTime(null);
    setRecordedVideo(null);
    
    // Notifier le parent que le live est arrêté
    onLiveStopped?.({ video_saved: false, error: 'force_stop' });
    
    toast.success('Live arrêté de force');
    console.log('✅ Live arrêté de force');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    startLive();
  };

  // Charger les messages existants du live
  const loadChatMessages = async (postId) => {
    try {
      console.log('📨 Chargement des messages du live...');
      const messages = await liveChatAPI.getMessages(postId);
      setChatMessages(messages);
      console.log(`✅ ${messages.length} messages chargés`);
    } catch (error) {
      console.error('❌ Erreur chargement messages:', error);
      toast.error('Erreur lors du chargement des messages');
    }
  };

  const sendChatMessage = async () => {
    if (!newMessage.trim() || !liveData) return;
    
    try {
      // Envoyer le message au backend
      const savedMessage = await liveChatAPI.sendMessage(liveData.post_id, {
        content: newMessage.trim(),
        type: 'text'
      });
      
      // Ajouter le message à la liste locale
      setChatMessages(prev => [...prev, savedMessage]);
      setNewMessage('');
      
      console.log('✅ Message envoyé et sauvegardé:', savedMessage);
    } catch (error) {
      console.error('❌ Erreur envoi message:', error);
      toast.error('Erreur lors de l\'envoi du message');
    }
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
      const duration = videoRef.current.duration;
      console.log('📊 Durée vidéo détectée:', duration);
      
      // Vérifier que la durée est valide et éviter les corrections en boucle
      if (isFinite(duration) && duration > 0 && duration !== Infinity) {
        setVideoDuration(duration);
        console.log('✅ Durée vidéo définie:', duration);
      } else if (videoDuration === 0 || videoDuration === Infinity) {
        // Seulement corriger si la durée actuelle est invalide
        console.log('⚠️ Durée vidéo invalide, correction nécessaire');
        setVideoDuration(1); // 1 seconde par défaut
        console.log('🔄 Durée forcée à 1 seconde');
      }
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

  // Fonction pour forcer l'affichage de la vidéo
  const forceVideoDisplay = (videoUrl) => {
    console.log('🔄 Force video display avec URL:', videoUrl);
    
    // Forcer la mise à jour des états
    setRecordedVideo(videoUrl);
    setIsLive(false);
    setLiveData(null);
    setLiveStartTime(null);
    
    // Configurer la vidéo après un délai
    setTimeout(() => {
      if (videoRef.current) {
        videoRef.current.src = videoUrl;
        videoRef.current.load();
        
        videoRef.current.addEventListener('loadedmetadata', () => {
          console.log('✅ Vidéo chargée avec succès');
          const duration = videoRef.current.duration;
          
          // Gérer la durée invalide de manière plus robuste
          if (isFinite(duration) && duration > 0 && duration !== Infinity) {
            setVideoDuration(duration);
            console.log('✅ Durée vidéo définie:', duration);
          } else {
            // Seulement définir la durée par défaut si elle n'est pas déjà correcte
            if (videoDuration === 0 || videoDuration === Infinity) {
              setVideoDuration(1); // Durée par défaut
              console.log('🔄 Durée forcée à 1 seconde');
            }
          }
          
          setCurrentTime(0);
          setIsPlaying(false);
          
          // Forcer le re-rendu
          setTimeout(() => {
            console.log('🔄 Re-rendu forcé de l\'interface');
            setRecordedVideo(videoUrl); // Forcer la mise à jour
            toast.success('🎬 Vidéo enregistrée prête pour la lecture !');
          }, 100);
        });
        
        videoRef.current.addEventListener('error', (e) => {
          console.error('❌ Erreur vidéo:', e);
          toast.error('Erreur lors du chargement de la vidéo');
        });
        
        // Forcer le chargement si pas d'événement (avec délai plus long)
        setTimeout(() => {
          if (videoDuration === 0 || videoDuration === Infinity) {
            console.log('🔄 Forçage du chargement vidéo après timeout');
            setVideoDuration(1);
            setCurrentTime(0);
            setIsPlaying(false);
          }
        }, 2000); // Délai plus long pour éviter les corrections prématurées
      }
    }, 300);
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

              {/* Message de confirmation vidéo prête */}
              {recordedVideo && !isLive && videoDuration > 0 && (
                <div className="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                  <span>VIDÉO PRÊTE</span>
                </div>
              )}

              {/* Informations sur l'origine live de la vidéo */}
              {recordedVideo && !isLive && liveInfo && (
                <div className="absolute top-4 right-4 bg-black bg-opacity-75 text-white p-3 rounded-lg backdrop-blur-sm max-w-xs">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-semibold">ENREGISTRÉ EN DIRECT</span>
                  </div>
                  
                  <div className="space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-gray-300">Titre:</span>
                      <span className="font-medium">{liveInfo.title}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-300">Auteur:</span>
                      <span className="font-medium">{liveInfo.author}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-300">Durée:</span>
                      <span className="font-medium">{formatTime(liveInfo.duration)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-300">Messages:</span>
                      <span className="font-medium">{liveInfo.chatMessages}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-300">Spectateurs:</span>
                      <span className="font-medium">{liveInfo.viewersCount}</span>
                    </div>
                  </div>
                  
                  <div className="mt-2 pt-2 border-t border-gray-600">
                    <div className="text-xs text-gray-400">
                      Enregistré le {new Date(liveInfo.endTime).toLocaleDateString('fr-FR')} à {new Date(liveInfo.endTime).toLocaleTimeString('fr-FR', {hour: '2-digit', minute:'2-digit'})}
                    </div>
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
                  <div className="flex space-x-3">
                    {!showStopConfirmation ? (
                      <button
                        onClick={stopLive}
                        disabled={isStopping}
                        className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-all duration-200 flex items-center space-x-2 shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isStopping ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Arrêt en cours...</span>
                          </>
                        ) : (
                          <>
                            <Square className="w-4 h-4" />
                            <span>Arrêter le live</span>
                          </>
                        )}
                      </button>
                    ) : (
                      <div className="flex space-x-2">
                        <button
                          onClick={confirmStopLive}
                          className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 transition-all duration-200 flex items-center space-x-2 shadow-lg font-medium"
                        >
                          <Check className="w-4 h-4" />
                          <span>Confirmer</span>
                        </button>
                        <button
                          onClick={() => setShowStopConfirmation(false)}
                          className="bg-gray-600 text-white px-4 py-3 rounded-lg hover:bg-gray-700 transition-all duration-200 flex items-center space-x-2 shadow-lg font-medium"
                        >
                          <X className="w-4 h-4" />
                          <span>Annuler</span>
                        </button>
                      </div>
                    )}
                    
                    <button
                      onClick={forceStopLive}
                      className="bg-red-800 text-white px-4 py-3 rounded-lg hover:bg-red-900 transition-all duration-200 flex items-center space-x-2 shadow-lg font-medium border-2 border-red-400"
                      title="Arrêt d'urgence - Force l'arrêt complet"
                    >
                      <X className="w-4 h-4" />
                      <span>Arrêt forcé</span>
                    </button>
                  </div>
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
                        className="bg-white/20 hover:bg-white/30 text-white p-3 rounded-full transition-all duration-200 shadow-lg"
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
                        {videoDuration > 0 && isFinite(videoDuration) ? `${formatTime(currentTime)} / ${formatTime(videoDuration)}` : 'Chargement...'}
                      </div>

                      {/* Badge "LIVE" pour indiquer l'origine */}
                      {liveInfo && (
                        <div className="bg-red-600 text-white px-2 py-1 rounded text-xs font-medium flex items-center space-x-1">
                          <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
                          <span>LIVE</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex space-x-2">
                      <button
                        onClick={onClose}
                        className="text-white hover:text-gray-300 transition-colors"
                        title="Fermer"
                      >
                        <X className="w-5 h-5" />
                      </button>

                      {/* Bouton détails du live */}
                      {liveInfo && (
                        <button
                          onClick={() => setShowLiveDetails(!showLiveDetails)}
                          className="text-white hover:text-gray-300 transition-colors"
                          title="Détails du live"
                        >
                          <Info className="w-5 h-5" />
                        </button>
                      )}
                    </div>
                  </div>
                  
                  {/* Barre de progression */}
                  <div 
                    className="w-full h-2 bg-gray-600 rounded-full cursor-pointer relative"
                    onClick={handleSeek}
                  >
                    <div 
                      className="h-full bg-red-600 rounded-full transition-all duration-200"
                      style={{ width: `${videoDuration > 0 && isFinite(videoDuration) ? (currentTime / videoDuration) * 100 : 0}%` }}
                    ></div>
                  </div>
                  
                  {/* Message d'information */}
                  {(videoDuration === 0 || !isFinite(videoDuration)) && (
                    <div className="text-center text-white text-sm mt-2">
                      <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Préparation de la vidéo...
                    </div>
                  )}
                </div>
              )}

              {/* Message de confirmation vidéo prête */}
              {recordedVideo && !isLive && videoDuration > 0 && (
                <div className="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                  <span>VIDÉO PRÊTE</span>
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
      {/* Message de confirmation d'arrêt */}
      {showStopConfirmation && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 shadow-2xl max-w-md mx-4 text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Square className="w-8 h-8 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Arrêter le live ?
            </h3>
            <p className="text-gray-600 mb-6">
              Votre vidéo sera automatiquement enregistrée et disponible pour lecture après l'arrêt.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => setShowStopConfirmation(false)}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Continuer le live
              </button>
              <button
                onClick={confirmStopLive}
                className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
              >
                <Square className="w-4 h-4" />
                <span>Arrêter le live</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Message d'arrêt en cours */}
      {isStopping && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 shadow-2xl max-w-md mx-4 text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Arrêt du live en cours...
            </h3>
            <p className="text-gray-600">
              Veuillez patienter pendant que nous finalisons l'enregistrement de votre vidéo.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveStream; 
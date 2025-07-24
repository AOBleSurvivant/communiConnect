import React, { useState, useRef, useEffect } from 'react';
import { Camera, Mic, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'react-hot-toast';

const CameraTest = ({ isOpen, onClose }) => {
  const [hasCamera, setHasCamera] = useState(false);
  const [hasMicrophone, setHasMicrophone] = useState(false);
  const [cameraPermission, setCameraPermission] = useState('unknown');
  const [microphonePermission, setMicrophonePermission] = useState('unknown');
  const [isTesting, setIsTesting] = useState(false);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      checkPermissions();
    }
  }, [isOpen]);

  const checkPermissions = async () => {
    setIsTesting(true);
    
    try {
      // Vérifier si l'API est disponible
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        toast.error('Votre navigateur ne supporte pas l\'accès aux médias');
        return;
      }

      // Vérifier les permissions
      if (navigator.permissions) {
        try {
          const cameraPermission = await navigator.permissions.query({ name: 'camera' });
          setCameraPermission(cameraPermission.state);
          
          const microphonePermission = await navigator.permissions.query({ name: 'microphone' });
          setMicrophonePermission(microphonePermission.state);
        } catch (error) {
          console.log('Permissions API non supportée, test direct...');
        }
      }

      // Tester l'accès à la caméra
      try {
        const videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        setHasCamera(true);
        setCameraPermission('granted');
        
        if (videoRef.current) {
          videoRef.current.srcObject = videoStream;
          streamRef.current = videoStream;
        }
        
        toast.success('Caméra détectée et accessible !');
      } catch (error) {
        setHasCamera(false);
        setCameraPermission('denied');
        console.error('Erreur caméra:', error);
      }

      // Tester l'accès au microphone
      try {
        const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        setHasMicrophone(true);
        setMicrophonePermission('granted');
        
        // Arrêter le stream audio de test
        audioStream.getTracks().forEach(track => track.stop());
        
        toast.success('Microphone détecté et accessible !');
      } catch (error) {
        setHasMicrophone(false);
        setMicrophonePermission('denied');
        console.error('Erreur microphone:', error);
      }

    } catch (error) {
      console.error('Erreur lors du test:', error);
      toast.error('Erreur lors du test des permissions');
    } finally {
      setIsTesting(false);
    }
  };

  const requestPermissions = async () => {
    setIsTesting(true);
    
    try {
      // Demander les permissions
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true, 
        audio: true 
      });
      
      setHasCamera(true);
      setHasMicrophone(true);
      setCameraPermission('granted');
      setMicrophonePermission('granted');
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
      
      toast.success('Permissions accordées !');
      
    } catch (error) {
      console.error('Erreur demande permissions:', error);
      
      if (error.name === 'NotAllowedError') {
        toast.error('Permissions refusées. Veuillez les autoriser manuellement.');
      } else {
        toast.error(`Erreur: ${error.message}`);
      }
    } finally {
      setIsTesting(false);
    }
  };

  const stopTest = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  useEffect(() => {
    return () => {
      stopTest();
    };
  }, []);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Test de la Caméra</h2>
          <button
            onClick={() => {
              stopTest();
              onClose();
            }}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        {/* Statut des permissions */}
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div className="flex items-center space-x-2">
              <Camera className="w-5 h-5" />
              <span>Caméra</span>
            </div>
            <div className="flex items-center space-x-2">
              {hasCamera ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
              <span className={`text-sm ${cameraPermission === 'granted' ? 'text-green-600' : 'text-red-600'}`}>
                {cameraPermission === 'granted' ? 'Autorisé' : 'Non autorisé'}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div className="flex items-center space-x-2">
              <Mic className="w-5 h-5" />
              <span>Microphone</span>
            </div>
            <div className="flex items-center space-x-2">
              {hasMicrophone ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
              <span className={`text-sm ${microphonePermission === 'granted' ? 'text-green-600' : 'text-red-600'}`}>
                {microphonePermission === 'granted' ? 'Autorisé' : 'Non autorisé'}
              </span>
            </div>
          </div>
        </div>

        {/* Prévisualisation vidéo */}
        {hasCamera && (
          <div className="mb-4">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-48 bg-gray-900 rounded"
            />
          </div>
        )}

        {/* Actions */}
        <div className="flex space-x-3">
          <button
            onClick={checkPermissions}
            disabled={isTesting}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {isTesting ? 'Test en cours...' : 'Tester'}
          </button>
          
          <button
            onClick={requestPermissions}
            disabled={isTesting}
            className="flex-1 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
          >
            Demander Permissions
          </button>
        </div>

        {/* Instructions */}
        <div className="mt-4 p-3 bg-blue-50 rounded text-sm">
          <h3 className="font-semibold mb-2">Instructions :</h3>
          <ul className="space-y-1 text-gray-600">
            <li>• Cliquez sur "Tester" pour vérifier l'état actuel</li>
            <li>• Cliquez sur "Demander Permissions" pour autoriser l'accès</li>
            <li>• Si les permissions sont refusées, autorisez-les manuellement dans les paramètres du navigateur</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CameraTest; 
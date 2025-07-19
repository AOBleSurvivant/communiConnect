import React, { useState, useEffect } from 'react';
import { formatTime } from '../utils/timeUtils';

/**
 * Composant de chronomètre pour les lives
 */
const LiveTimer = ({ 
  startTime, 
  isActive = true, 
  className = '', 
  showLabel = true,
  variant = 'default' // 'default', 'compact', 'detailed'
}) => {
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    if (!isActive || !startTime) {
      setDuration(0);
      return;
    }

    const interval = setInterval(() => {
      const start = new Date(startTime).getTime();
      const now = Date.now();
      const elapsed = Math.floor((now - start) / 1000);
      setDuration(elapsed);
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime, isActive]);

  if (!isActive || !startTime) {
    return null;
  }

  const renderTimer = () => {
    switch (variant) {
      case 'compact':
        return (
          <div className={`inline-flex items-center space-x-1 ${className}`}>
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            <span className="font-mono text-sm">{formatTime(duration)}</span>
          </div>
        );
      
      case 'detailed':
        return (
          <div className={`bg-black/70 text-white px-3 py-2 rounded-lg backdrop-blur-sm ${className}`}>
            {showLabel && <div className="text-xs text-gray-300">Durée</div>}
            <div className="font-mono font-bold text-lg">{formatTime(duration)}</div>
          </div>
        );
      
      default:
        return (
          <div className={`inline-flex items-center space-x-1 ${className}`}>
            <span className="font-mono text-sm">• {formatTime(duration)}</span>
          </div>
        );
    }
  };

  return renderTimer();
};

export default LiveTimer; 
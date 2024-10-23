import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Radio } from 'lucide-react';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [isPTTActive, setIsPTTActive] = useState(false);
  const [studentName, setStudentName] = useState('');
  const [isNameSubmitted, setIsNameSubmitted] = useState(false);
  const [status, setStatus] = useState('Disconnected');
  const audioContextRef = useRef<AudioContext | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    return () => {
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (studentName.trim()) {
      setIsNameSubmitted(true);
      initializeAudioContext();
    }
  };

  const initializeAudioContext = async () => {
    try {
      audioContextRef.current = new AudioContext();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;
      setIsConnected(true);
      setStatus('Ready to talk');
    } catch (error) {
      console.error('Error accessing microphone:', error);
      setStatus('Error: Microphone access denied');
    }
  };

  const startPTT = () => {
    if (isConnected) {
      setIsPTTActive(true);
      setStatus('Broadcasting...');
      // TCP connection and audio streaming logic will be implemented here
    }
  };

  const stopPTT = () => {
    setIsPTTActive(false);
    setStatus('Ready to talk');
    // Stop TCP streaming logic will be implemented here
  };

  if (!isNameSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
          <div className="flex items-center justify-center mb-8">
            <Radio className="w-12 h-12 text-blue-600" />
          </div>
          <h1 className="text-2xl font-bold text-center mb-6">Push-to-Talk</h1>
          <form onSubmit={handleNameSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Enter your name
              </label>
              <input
                type="text"
                id="name"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Your name"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              Join Class
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold mb-2">Welcome, {studentName}</h1>
          <p className="text-gray-600">{status}</p>
        </div>

        <div className="flex flex-col items-center space-y-6">
          <div className="relative">
            <div
              className={`w-32 h-32 rounded-full flex items-center justify-center transition-all ${
                isPTTActive
                  ? 'bg-red-500 scale-95'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
              onMouseDown={startPTT}
              onMouseUp={stopPTT}
              onTouchStart={startPTT}
              onTouchEnd={stopPTT}
            >
              {isPTTActive ? (
                <Mic className="w-16 h-16 text-white" />
              ) : (
                <MicOff className="w-16 h-16 text-white" />
              )}
            </div>
            <div
              className={`absolute -inset-2 rounded-full bg-blue-500 opacity-20 transition-transform ${
                isPTTActive ? 'animate-ping' : 'scale-0'
              }`}
            />
          </div>
          
          <p className="text-sm text-gray-600 text-center">
            {isPTTActive ? 'Release to stop talking' : 'Press and hold to talk'}
          </p>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Connection Status:</span>
            <span className={`font-medium ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
import React from 'react';
import { Mic, MicOff } from 'lucide-react';

interface PTTButtonProps {
  isTalking: boolean;
  isConnected: boolean;
  onStart: () => void;
  onStop: () => void;
}

export function PTTButton({ isTalking, isConnected, onStart, onStop }: PTTButtonProps) {
  return (
    <button
      onMouseDown={onStart}
      onMouseUp={onStop}
      onMouseLeave={onStop}
      disabled={!isConnected}
      className={`w-32 h-32 rounded-full flex items-center justify-center focus:outline-none transition-colors ${
        isTalking
          ? 'bg-red-500 hover:bg-red-600'
          : 'bg-blue-500 hover:bg-blue-600'
      } ${!isConnected && 'opacity-50 cursor-not-allowed'}`}
    >
      {isTalking ? (
        <Mic className="w-16 h-16 text-white" />
      ) : (
        <MicOff className="w-16 h-16 text-white" />
      )}
    </button>
  );
}
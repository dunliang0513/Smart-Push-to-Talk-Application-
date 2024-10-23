import React from 'react';

interface LoginFormProps {
  studentName: string;
  onNameChange: (name: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function LoginForm({ studentName, onNameChange, onSubmit }: LoginFormProps) {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <form onSubmit={onSubmit} className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Join Class Discussion</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Your Name
            </label>
            <input
              id="name"
              type="text"
              value={studentName}
              onChange={(e) => onNameChange(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your name"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Join Class
          </button>
        </div>
      </form>
    </div>
  );
}
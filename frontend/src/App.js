import React from 'react';
import ClaimsPredictor from './components/ClaimsPredictor';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Claims Reporting Automation System
          </h1>
          <p className="text-gray-600 mt-2">
            ML-Powered Claims Prediction Dashboard
          </p>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-8">
        <ClaimsPredictor />
      </main>
    </div>
  );
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/tailwind.css';
import reportWebVitals from './reportWebVitals';
import ErrorBoundary from './components/ErrorBoundary';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      {/* Removed <Router> here since it's already being used inside App.js */}
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);

// For measuring performance (optional but recommended for enterprise apps)
reportWebVitals(console.log);

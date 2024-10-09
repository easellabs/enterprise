import React from 'react';

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
      <p className="ml-4 text-blue-500">Loading...</p>
    </div>
  );
}

export default LoadingSpinner;

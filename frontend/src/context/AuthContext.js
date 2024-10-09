// AuthProvider.js
import React, { createContext, useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { getAuthTokens, setAuthTokens as saveAuthTokens } from '../services/tokenService';

export const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(getAuthTokens());
  const navigate = useNavigate();

  // Effect to synchronize tokens in storage
  useEffect(() => {
    if (authTokens) {
      saveAuthTokens(authTokens);
    } else {
      sessionStorage.removeItem('authTokens');
    }
  }, [authTokens]);

  // Logout function
  const logout = useCallback(() => {
    setAuthTokens(null);
    sessionStorage.removeItem('authTokens');
    navigate('/login'); // Redirect to login after logout
  }, [navigate]);

  // Effect to manage user inactivity and logout after an idle timeout
  useEffect(() => {
    let idleTimer;

    const resetIdleTimer = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        logout();
      }, 15 * 60 * 1000); // Idle timeout set to 15 minutes
    };

    window.addEventListener('mousemove', resetIdleTimer);
    window.addEventListener('keydown', resetIdleTimer);

    resetIdleTimer(); // Initialize the timer on component mount

    return () => {
      clearTimeout(idleTimer);
      window.removeEventListener('mousemove', resetIdleTimer);
      window.removeEventListener('keydown', resetIdleTimer);
    };
  }, [logout]);

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthProvider;

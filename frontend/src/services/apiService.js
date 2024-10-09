import axios from 'axios';
import CryptoJS from 'crypto-js';
import Cookies from 'js-cookie';

const secretKey = process.env.REACT_APP_SECRET_KEY || 'your-very-secret-key'; // Use environment variables
const baseURL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/auth/'; // Base URL from env vars

// Axios instance configuration
const api = axios.create({
  baseURL,
  timeout: 20000, // Increased timeout to avoid false errors due to latency
});

// Encrypt and store auth tokens securely
export const setAuthTokens = (tokens) => {
  if (!tokens) return;
  const encryptedTokens = CryptoJS.AES.encrypt(JSON.stringify(tokens), secretKey).toString();
  sessionStorage.setItem('authTokens', encryptedTokens); // Use sessionStorage for better security
};

// Retrieve and decrypt auth tokens
export const getAuthTokens = () => {
  const encryptedTokens = sessionStorage.getItem('authTokens');
  if (!encryptedTokens) {
    return null;
  }
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedTokens, secretKey);
    return JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
  } catch (e) {
    console.error('Failed to decrypt tokens:', e);
    return null;
  }
};

// Function to register a new user
export const registerUser = async (username, password, role = 'User') => {
  try {
    const response = await api.post('register/', { username, password, role });
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Registration failed:', error.response.data);
    } else {
      console.error('Registration failed:', error.message);
    }
    throw error;
  }
};

// Function to log in the user
export const loginUser = async (username, password) => {
  try {
    const response = await api.post('api/token/', { username, password });
    setAuthTokens(response.data);
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Login failed:', error.response.data);
    } else {
      console.error('Login failed:', error.message);
    }
    throw error;
  }
};

// Function to refresh the JWT access token
export const refreshToken = async () => {
  const tokens = getAuthTokens();
  if (tokens && tokens.refresh) {
    try {
      const response = await api.post('api/token/refresh/', { refresh: tokens.refresh });
      setAuthTokens(response.data);
      return response.data.access;
    } catch (error) {
      if (error.response) {
        console.error('Token refresh failed:', error.response.data);
      } else {
        console.error('Token refresh failed:', error.message);
      }
      throw error;
    }
  }
  return null;
};

// // Attach Authorization header with access token to every request
// api.interceptors.request.use(
//   (config) => {
//     const tokens = getAuthTokens();
//     if (tokens && tokens.access) {
//       config.headers.Authorization = `Bearer ${tokens.access}`;
//     }

//     // Get CSRF token from the cookies
//     const csrfToken = Cookies.get('csrftoken');
//     if (csrfToken) {
//       config.headers['X-CSRFToken'] = csrfToken;
//     }

//     return config;
//   },
//   (error) => {
//     console.error('Request error:', error);
//     return Promise.reject(error);
//   }
// );

api.interceptors.request.use(
  (config) => {
    const csrftoken = Cookies.get('csrftoken'); // Get CSRF token from cookie
    if (csrftoken) {
      config.headers['X-CSRFToken'] = csrftoken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors globally
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle token expiration and retry with refreshed token
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newAccessToken = await refreshToken();
        if (newAccessToken) {
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        }
      } catch (err) {
        console.error('Retry after token refresh failed:', err);
        // Optional: Implement logic to handle token refresh failure (e.g., logout the user)
      }
    }

    // Global error handling for different status codes
    if (error.response) {
      switch (error.response.status) {
        case 403:
          console.error('Access forbidden:', error.response.data);
          alert('Access forbidden. Please check your permissions or login again.');
          break;
        case 404:
          console.error('Resource not found:', error.response.data);
          break;
        default:
          console.error('Request error:', error.response.data);
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Unexpected error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default api;

import axios from 'axios';

// Use environment variable for base URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // To allow sending cookies if needed, particularly useful for session-based auth
});

// Add request interceptor (optional, for logging or modifying requests before sending)
apiClient.interceptors.request.use(
  (config) => {
    // Optionally log or modify requests here
    console.log(`[Request] ${config.method.toUpperCase()} - ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor (optional, for handling common response errors)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors such as 401 Unauthorized
    if (error.response && error.response.status === 401) {
      console.error("Unauthorized - Redirect to login.");
      // Optional: Add logic to redirect the user to login if unauthorized
    }
    return Promise.reject(error);
  }
);

export default apiClient;

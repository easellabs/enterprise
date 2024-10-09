import axios from 'axios';

// BASE_URL can be extracted from a configuration file
const BASE_URL = process.env.REACT_APP_BASE_URL || '/api/auth';

// Axios instance for authentication
const axiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // For cookies to work
});

// Request Interceptor
axiosInstance.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem('accessToken');
        if (accessToken) {
            config.headers['Authorization'] = `Bearer ${accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor for handling 401 errors and refreshing token
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const response = await refreshTokens();
                if (response.status === 200) {
                    return axiosInstance(originalRequest);
                }
            } catch (e) {
                console.error('Token refresh failed.');
            }
        }
        return Promise.reject(error);
    }
);

// Register a new user
export const registerUser = async (formData) => {
    try {
        const response = await axiosInstance.post('/register/', formData);
        return response;
    } catch (error) {
        handleApiError(error);
    }
};

// Login a user
export const loginUser = async (formData) => {
    try {
        const response = await axiosInstance.post('/login/', formData);
        // Store tokens in secure HTTP-only cookies
        return response.data;
    } catch (error) {
        handleApiError(error);
    }
};

// Enable Two-Factor Authentication
export const enableTwoFactor = async () => {
    try {
        const response = await axiosInstance.post('/enable-2fa/');
        return response.data; // Contains QR code URL
    } catch (error) {
        handleApiError(error);
    }
};

// Verify OTP for 2FA
export const verifyTwoFactor = async (otp) => {
    try {
        const response = await axiosInstance.post('/verify-2fa/', { otp });
        return response.data; // Contains access and refresh tokens
    } catch (error) {
        handleApiError(error);
    }
};

// Refresh tokens
export const refreshTokens = async () => {
    try {
        const refreshToken = getRefreshToken(); // Should use secure storage
        if (refreshToken) {
            const response = await axios.post(`${BASE_URL}/token/refresh/`, {
                refresh: refreshToken,
            });
            setAccessToken(response.data.access); // Store in secure cookie
            return response;
        } else {
            throw new Error('No refresh token available.');
        }
    } catch (error) {
        handleApiError(error);
    }
};

// Logout a user
export const logoutUser = () => {
    clearTokens();
};

// Utility functions
const handleApiError = (error) => {
    const response = error.response;
    if (response) {
        switch (response.status) {
            case 400:
                console.error('Validation error:', response.data);
                break;
            case 401:
                console.error('Unauthorized access. Please log in again.');
                break;
            default:
                console.error('An error occurred:', response.data);
        }
    } else {
        console.error('Network error occurred.');
    }
};

const getRefreshToken = () => {
    // Logic to get refresh token from secure cookies
};

const setAccessToken = (token) => {
    // Logic to set access token in secure cookie
};

const clearTokens = () => {
    // Logic to clear tokens from secure storage
};


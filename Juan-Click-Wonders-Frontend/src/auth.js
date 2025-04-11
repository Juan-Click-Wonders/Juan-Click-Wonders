import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // Required for cookies to be sent
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    
    // If token exists, add it to the Authorization header
    if (token) {
      // Ensure the token is properly formatted
      const formattedToken = token.trim();
      
      // Set the token in the request headers
      config.headers['Authorization'] = `Bearer ${formattedToken}`;
      
    } else {
      // No token found in localStorage
    }
    
    return config;
  },
  (error) => {
    console.error("Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    // Detailed error logging
    console.error("API Error:", {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      headers: error.config?.headers,
      token: localStorage.getItem('access_token'),
      fullUrl: `${error.config?.baseURL}${error.config?.url}`
    });

    if (error.response?.status === 401) {
      // Don't redirect immediately, let the component handle it
    }
    return Promise.reject(error);
  }
);

// Helper function to check if user is authenticated
export const isAuthenticated = () => {
  // Check for access token in localStorage or JWT cookie
  return localStorage.getItem('access_token') || 
         document.cookie.includes('jwt=') || 
         document.cookie.includes('access_token=');
};

// Helper function to get CSRF token from cookies
export const getCsrfToken = () => {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

export default api;
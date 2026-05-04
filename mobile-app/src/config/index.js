/**
 * Configuration settings for the mobile app
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: __DEV__
    ? 'http://192.168.1.191:5000' // Backend server IP for local testing
    : 'https://your-production-api.com',
  TIMEOUT: 30000, // 30 seconds
};

// App Configuration
export const APP_CONFIG = {
  NAME: 'Plant Disease Detection',
  VERSION: '1.0.0',
};

// Image Configuration
export const IMAGE_CONFIG = {
  MAX_SIZE: 5 * 1024 * 1024, // 5MB
  QUALITY: 0.8,
};

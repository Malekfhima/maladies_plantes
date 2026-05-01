/**
 * API Service for Plant Disease Detection
 * Handles communication with the backend API
 */

import axios from 'axios';
import { API_CONFIG } from '../config';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * Check if the backend API is healthy
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Unable to connect to server');
  }
};

/**
 * Predict plant disease from image
 * @param {string} imageUri - URI of the image to analyze
 * @returns {object} Prediction result with disease, confidence, description, treatment
 */
export const predictDisease = async (imageUri) => {
  try {
    // Create FormData
    const formData = new FormData();
    
    // Get file info
    const uri = imageUri;
    const fileType = uri.substring(uri.lastIndexOf('.') + 1);
    const fileName = uri.substring(uri.lastIndexOf('/') + 1);
    
    // Append image to form data
    formData.append('image', {
      uri: uri,
      name: fileName,
      type: `image/${fileType}`,
    });
    
    // Make API call
    const response = await api.post('/predict', formData);
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.message || 'Prediction failed');
    } else if (error.request) {
      // Request made but no response received
      throw new Error('No response from server. Check your connection.');
    } else {
      // Error in request setup
      throw new Error(error.message || 'Prediction failed');
    }
  }
};

/**
 * Get all available disease classes
 */
export const getClasses = async () => {
  try {
    const response = await api.get('/classes');
    return response.data;
  } catch (error) {
    throw new Error('Failed to retrieve disease classes');
  }
};

export default api;

/**
 * Network Utility
 * Checks network connectivity before API calls
 */

import NetInfo from '@react-native-community/netinfo';

/**
 * Check if device has network connection
 * @returns {Promise<boolean>} True if connected, false otherwise
 */
export const checkNetworkConnection = async () => {
  try {
    const state = await NetInfo.fetch();
    return state.isConnected;
  } catch (error) {
    console.error('Network check failed:', error);
    return false;
  }
};

/**
 * Get network type
 * @returns {Promise<string>} Network type (wifi, cellular, etc.)
 */
export const getNetworkType = async () => {
  try {
    const state = await NetInfo.fetch();
    return state.type;
  } catch (error) {
    console.error('Network type check failed:', error);
    return 'unknown';
  }
};

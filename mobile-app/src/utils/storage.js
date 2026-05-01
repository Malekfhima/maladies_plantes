/**
 * Storage Utility
 * Handles AsyncStorage operations for scan history
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

const HISTORY_KEY = '@plant_disease_history';
const MAX_HISTORY_SIZE = 50;

/**
 * Save scan result to history
 * @param {object} scanData - Scan data to save
 * @returns {Promise<void>}
 */
export const saveScanToHistory = async (scanData) => {
  try {
    const history = await getScanHistory();
    
    // Add new scan at the beginning
    const newHistory = [
      {
        ...scanData,
        timestamp: new Date().toISOString(),
        id: Date.now().toString(),
      },
      ...history,
    ];

    // Keep only the last MAX_HISTORY_SIZE scans
    const trimmedHistory = newHistory.slice(0, MAX_HISTORY_SIZE);
    
    await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(trimmedHistory));
  } catch (error) {
    console.error('Failed to save scan to history:', error);
  }
};

/**
 * Get scan history
 * @returns {Promise<Array>} Array of scan history
 */
export const getScanHistory = async () => {
  try {
    const historyJson = await AsyncStorage.getItem(HISTORY_KEY);
    return historyJson ? JSON.parse(historyJson) : [];
  } catch (error) {
    console.error('Failed to get scan history:', error);
    return [];
  }
};

/**
 * Clear scan history
 * @returns {Promise<void>}
 */
export const clearScanHistory = async () => {
  try {
    await AsyncStorage.removeItem(HISTORY_KEY);
  } catch (error) {
    console.error('Failed to clear scan history:', error);
  }
};

/**
 * Delete specific scan from history
 * @param {string} scanId - ID of the scan to delete
 * @returns {Promise<void>}
 */
export const deleteScanFromHistory = async (scanId) => {
  try {
    const history = await getScanHistory();
    const filteredHistory = history.filter(scan => scan.id !== scanId);
    await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(filteredHistory));
  } catch (error) {
    console.error('Failed to delete scan from history:', error);
  }
};

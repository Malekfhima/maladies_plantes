/**
 * Image Utility
 * Handles image compression and manipulation
 */

import * as ImageManipulator from 'expo-image-manipulator';

/**
 * Compress image to reduce file size
 * @param {string} uri - Image URI
 * @param {number} quality - Compression quality (0-1)
 * @param {number} maxWidth - Maximum width in pixels
 * @returns {Promise<string>} Compressed image URI
 */
export const compressImage = async (uri, quality = 0.7, maxWidth = 1024) => {
  try {
    const result = await ImageManipulator.manipulateAsync(
      uri,
      [{ resize: { width: maxWidth } }],
      {
        compress: quality,
        format: ImageManipulator.SaveFormat.JPEG,
      }
    );
    return result.uri;
  } catch (error) {
    console.error('Image compression failed:', error);
    return uri; // Return original if compression fails
  }
};

/**
 * Get image file info
 * @param {string} uri - Image URI
 * @returns {Promise<object>} Image info with width, height, size
 */
export const getImageInfo = async (uri) => {
  try {
    const result = await ImageManipulator.manipulateAsync(uri, []);
    return {
      width: result.width,
      height: result.height,
      uri: result.uri,
    };
  } catch (error) {
    console.error('Get image info failed:', error);
    return null;
  }
};

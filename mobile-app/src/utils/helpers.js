/**
 * Utility helper functions
 */

/**
 * Format confidence percentage
 */
export const formatConfidence = (confidence) => {
  return `${confidence.toFixed(2)}%`;
};

/**
 * Validate image file
 */
export const validateImage = (file) => {
  if (!file) return false;
  
  const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  
  if (!validTypes.includes(file.type)) {
    return { valid: false, error: 'Invalid file type. Please select JPEG or PNG.' };
  }
  
  if (file.size > maxSize) {
    return { valid: false, error: 'File too large. Maximum size is 5MB.' };
  }
  
  return { valid: true };
};

/**
 * Get disease severity based on confidence
 */
export const getSeverity = (confidence) => {
  if (confidence >= 80) return 'high';
  if (confidence >= 50) return 'medium';
  return 'low';
};

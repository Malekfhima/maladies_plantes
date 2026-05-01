"""
Image processing service for preprocessing images
"""
import numpy as np
from PIL import Image, UnidentifiedImageError
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import IMG_SIZE

class ImageProcessor:
    """Service for preprocessing images for model prediction"""
    
    @staticmethod
    def preprocess_image(image_file):
        """
        Preprocess uploaded image for prediction
        
        Args:
            image_file: Uploaded image file object
            
        Returns:
            numpy.ndarray: Preprocessed image array ready for prediction
            
        Raises:
            ValueError: If image file is invalid or corrupted
            UnidentifiedImageError: If file is not a valid image
        """
        try:
            # Open image
            img = Image.open(image_file)
            
            # Verify image is valid
            img.verify()
            
            # Reopen after verify (verify closes the file)
            image_file.seek(0)
            img = Image.open(image_file)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image
            img = img.resize((IMG_SIZE, IMG_SIZE))
            
            # Convert to numpy array and normalize
            img_array = np.array(img) / 255.0
            
            # Expand dimensions for batch
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except UnidentifiedImageError:
            raise ValueError("Invalid image file. Please upload a valid image (JPEG, PNG).")
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")

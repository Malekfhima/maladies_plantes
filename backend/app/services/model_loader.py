"""
Model loader service for loading and managing ML models
"""
import json
import tensorflow as tf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import MODEL_PATH, CLASS_LABELS_PATH

class ModelLoader:
    """Service for loading and managing the ML model and class labels"""
    
    def __init__(self):
        self.model = None
        self.class_labels = None
    
    def load_model_and_labels(self):
        """
        Load the trained model and class labels
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load model
            self.model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully!")
            
            # Load class labels
            with open(CLASS_LABELS_PATH, 'r') as f:
                self.class_labels = json.load(f)
            print("Class labels loaded successfully!")
            
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def get_model(self):
        """Get the loaded model"""
        return self.model
    
    def get_class_labels(self):
        """Get the loaded class labels"""
        return self.class_labels
    
    def is_loaded(self):
        """Check if model and labels are loaded"""
        return self.model is not None and self.class_labels is not None

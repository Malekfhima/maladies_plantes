"""
Prediction service for making disease predictions
"""
import numpy as np

class Predictor:
    """Service for making plant disease predictions"""
    
    def __init__(self, model, class_labels):
        """
        Initialize predictor with model and class labels
        
        Args:
            model: Loaded TensorFlow model
            class_labels: Dictionary of class labels
            
        Raises:
            ValueError: If model or class labels are None
        """
        if model is None:
            raise ValueError("Model cannot be None")
        if class_labels is None:
            raise ValueError("Class labels cannot be None")
            
        self.model = model
        self.class_labels = class_labels
    
    def predict_disease(self, img_array):
        """
        Predict disease from preprocessed image
        
        Args:
            img_array: Preprocessed image array
            
        Returns:
            dict: Prediction result with disease info
            
        Raises:
            ValueError: If prediction fails or returns invalid results
        """
        try:
            # Validate input array
            if img_array is None or img_array.size == 0:
                raise ValueError("Invalid image array provided")
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            
            # Validate predictions
            if predictions is None or len(predictions) == 0:
                raise ValueError("Model returned no predictions")
                
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class] * 100)
            
            # Get class info
            class_info = self.class_labels.get(str(predicted_class), {})
            
            result = {
                "disease": class_info.get("name", "Unknown"),
                "confidence": round(confidence, 2),
                "description": class_info.get("description", "Description not available"),
                "treatment": class_info.get("treatment", "Treatment not available"),
                "class_id": int(predicted_class),
                "status": "success"
            }
            
            return result
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            raise ValueError(f"Prediction failed: {str(e)}")

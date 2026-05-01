"""
Prediction endpoints
"""
from flask import request, jsonify
import sys
import os
import logging
from werkzeug.utils import secure_filename
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_predict_routes(app, model_loader):
    """Register prediction endpoints"""
    
    image_processor = ImageProcessor()
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """
        Predict plant disease from uploaded image
        Expects: multipart/form-data with 'image' field
        Returns: JSON with prediction results
        """
        try:
            # Check if file is in request
            if 'image' not in request.files:
                logger.warning("Prediction request without image file")
                return jsonify({
                    "status": "error",
                    "message": "No image file provided"
                }), 400
            
            file = request.files['image']
            
            # Check if file is selected
            if file.filename == '':
                logger.warning("Prediction request with empty filename")
                return jsonify({
                    "status": "error",
                    "message": "No file selected"
                }), 400
            
            # Secure filename
            filename = secure_filename(file.filename)
            
            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
            if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                logger.warning(f"Invalid file type attempted: {filename}")
                return jsonify({
                    "status": "error",
                    "message": "Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, BMP, WEBP)."
                }), 400
            
            # Check file size (max 10MB)
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            max_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_size:
                logger.warning(f"File too large: {file_size} bytes")
                return jsonify({
                    "status": "error",
                    "message": f"File too large. Maximum size is 10MB. Your file is {file_size / (1024*1024):.2f}MB."
                }), 413
            
            # Check if model is loaded
            if not model_loader.is_loaded():
                logger.error("Model not loaded during prediction request")
                return jsonify({
                    "status": "error",
                    "message": "Model not loaded. Please check server configuration."
                }), 500
            
            # Preprocess image
            try:
                img_array = image_processor.preprocess_image(file)
                logger.info(f"Image preprocessed successfully: {filename}")
            except ValueError as e:
                logger.error(f"Image preprocessing failed: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400
            except Exception as e:
                logger.error(f"Unexpected error during preprocessing: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": "Failed to process image. Please ensure the image is valid."
                }), 400
            
            # Make prediction
            try:
                predictor = Predictor(model_loader.get_model(), model_loader.get_class_labels())
                result = predictor.predict_disease(img_array)
                logger.info(f"Prediction successful: {result.get('disease', 'unknown')} with {result.get('confidence', 0)}% confidence")
            except ValueError as e:
                logger.error(f"Prediction failed: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500
            except Exception as e:
                logger.error(f"Unexpected error during prediction: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": "Prediction failed due to an unexpected error."
                }), 500
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Unexpected error in predict endpoint: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "An unexpected error occurred. Please try again."
            }), 500
    
    @app.route('/classes', methods=['GET'])
    def get_classes():
        """
        Get all available disease classes
        """
        try:
            class_labels = model_loader.get_class_labels()
            if class_labels is None:
                logger.error("Class labels not loaded")
                return jsonify({
                    "status": "error",
                    "message": "Class labels not loaded"
                }), 500
            
            classes = []
            for class_id, info in class_labels.items():
                classes.append({
                    "id": int(class_id),
                    "name": info.get("name", "Unknown"),
                    "description": info.get("description", "")
                })
            
            logger.info(f"Retrieved {len(classes)} disease classes")
            return jsonify({
                "status": "success",
                "classes": classes,
                "total": len(classes)
            }), 200
            
        except Exception as e:
            logger.error(f"Failed to retrieve classes: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve disease classes"
            }), 500

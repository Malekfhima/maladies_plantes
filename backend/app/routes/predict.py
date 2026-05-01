"""
Prediction endpoints
"""
from flask import request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor

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
                return jsonify({
                    "status": "error",
                    "message": "No image file provided"
                }), 400
            
            file = request.files['image']
            
            # Check if file is selected
            if file.filename == '':
                return jsonify({
                    "status": "error",
                    "message": "No file selected"
                }), 400
            
            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
            if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                return jsonify({
                    "status": "error",
                    "message": "Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, BMP)."
                }), 400
            
            # Check if model is loaded
            if not model_loader.is_loaded():
                return jsonify({
                    "status": "error",
                    "message": "Model not loaded. Please check server configuration."
                }), 500
            
            # Preprocess image
            try:
                img_array = image_processor.preprocess_image(file)
            except ValueError as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400
            
            # Make prediction
            try:
                predictor = Predictor(model_loader.get_model(), model_loader.get_class_labels())
                result = predictor.predict_disease(img_array)
            except ValueError as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Prediction failed: {str(e)}"
            }), 500
    
    @app.route('/classes', methods=['GET'])
    def get_classes():
        """
        Get all available disease classes
        """
        try:
            class_labels = model_loader.get_class_labels()
            if class_labels is None:
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
            
            return jsonify({
                "status": "success",
                "classes": classes,
                "total": len(classes)
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Failed to retrieve classes: {str(e)}"
            }), 500

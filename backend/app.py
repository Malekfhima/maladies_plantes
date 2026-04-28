"""
Plant Disease Detection Backend API
Flask REST API for plant disease prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Configuration
IMG_SIZE = 224
MODEL_PATH = '../ml-model/models/plant_disease_model.h5'
CLASS_LABELS_PATH = '../ml-model/models/class_labels.json'

# Global variables for model and labels
model = None
class_labels = None

def load_model_and_labels():
    """
    Load the trained model and class labels
    """
    global model, class_labels
    
    try:
        # Load model
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
        
        # Load class labels
        with open(CLASS_LABELS_PATH, 'r') as f:
            class_labels = json.load(f)
        print("Class labels loaded successfully!")
        
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def preprocess_image(image_file):
    """
    Preprocess uploaded image for prediction
    """
    try:
        # Open image
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
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        raise

def predict_disease(img_array):
    """
    Predict disease from preprocessed image
    """
    try:
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class] * 100)
        
        # Get class info
        class_info = class_labels.get(str(predicted_class), {})
        
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
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "labels_loaded": class_labels is not None
    })

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
        
        # Check if model is loaded
        if model is None:
            return jsonify({
                "status": "error",
                "message": "Model not loaded. Please check server configuration."
            }), 500
        
        # Preprocess image
        img_array = preprocess_image(file)
        
        # Make prediction
        result = predict_disease(img_array)
        
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Load model on startup
    print("Starting Plant Disease Detection API...")
    if load_model_and_labels():
        print("Model and labels loaded successfully!")
        print("API is ready to accept requests.")
    else:
        print("Warning: Model or labels failed to load. API may not function correctly.")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

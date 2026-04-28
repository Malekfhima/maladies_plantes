"""
Plant Disease Detection Backend API - Demo Mode
Flask REST API for plant disease prediction (demo mode without ML model)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Demo disease information
DEMO_DISEASES = [
    {
        "name": "healthy",
        "description": "The plant appears healthy with no visible signs of disease. Leaves are green and vibrant.",
        "treatment": "Continue regular watering, fertilization, and monitoring practices. Maintain proper spacing and sunlight."
    },
    {
        "name": "late_blight",
        "description": "Late blight is caused by the fungus-like organism Phytophthora infestans. It causes dark, water-soaked lesions on leaves that quickly spread.",
        "treatment": "Apply fungicides containing copper or chlorothalonil. Remove infected plant parts immediately. Improve air circulation and avoid overhead watering."
    },
    {
        "name": "early_blight",
        "description": "Early blight is caused by the fungus Alternaria solani. It causes dark concentric rings on leaves, often starting on older leaves.",
        "treatment": "Apply fungicides, remove infected leaves, avoid overhead watering, and rotate crops. Use disease-resistant varieties when possible."
    },
    {
        "name": "leaf_spot",
        "description": "Leaf spot diseases cause circular spots on leaves, often with dark borders. Can be caused by fungi or bacteria.",
        "treatment": "Remove infected leaves, apply fungicides, ensure proper spacing for air circulation, avoid overhead irrigation."
    },
    {
        "name": "powdery_mildew",
        "description": "Powdery mildew appears as white powdery coating on leaves, stems, and flowers. Thrives in humid conditions.",
        "treatment": "Apply sulfur-based fungicides, improve air circulation, avoid overhead watering, and reduce humidity around plants."
    }
]

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "mode": "demo",
        "model_loaded": False,
        "labels_loaded": True
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict plant disease from uploaded image (demo mode)
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
        
        # Demo mode: return random prediction
        disease = random.choice(DEMO_DISEASES)
        confidence = round(random.uniform(70, 98), 2)
        
        result = {
            "disease": disease["name"],
            "confidence": confidence,
            "description": disease["description"],
            "treatment": disease["treatment"],
            "class_id": DEMO_DISEASES.index(disease),
            "status": "success",
            "mode": "demo"
        }
        
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
        classes = []
        for idx, disease in enumerate(DEMO_DISEASES):
            classes.append({
                "id": idx,
                "name": disease["name"],
                "description": disease["description"]
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
    print("Starting Plant Disease Detection API (DEMO MODE)...")
    print("Note: This is a demo mode without actual ML model.")
    print("For production, train the model and use app.py instead.")
    print("API is ready to accept requests on http://0.0.0.0:5000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

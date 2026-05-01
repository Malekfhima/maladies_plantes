"""
Health check endpoint
"""
from flask import jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.model_loader import ModelLoader

def register_health_route(app, model_loader: ModelLoader):
    """Register health check endpoint"""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint
        """
        return jsonify({
            "status": "healthy",
            "model_loaded": model_loader.is_loaded(),
            "labels_loaded": model_loader.get_class_labels() is not None
        })

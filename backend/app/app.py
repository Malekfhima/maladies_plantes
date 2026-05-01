"""
Plant Disease Detection Backend API
Flask REST API for plant disease prediction
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.settings import API_HOST, API_PORT, DEBUG, CORS_ORIGINS, MAX_CONTENT_LENGTH
from app.services.model_loader import ModelLoader
from app.routes.health import register_health_route
from app.routes.predict import register_predict_routes

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure max upload size
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    # Enable CORS
    CORS(app, origins=CORS_ORIGINS)
    
    # Initialize model loader
    model_loader = ModelLoader()
    
    # Register routes
    register_health_route(app, model_loader)
    register_predict_routes(app, model_loader)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "message": "Method not allowed"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "status": "error",
            "message": "File too large. Maximum size is 10MB."
        }), 413
    
    return app, model_loader

if __name__ == '__main__':
    # Create app and load model
    print("Starting Plant Disease Detection API...")
    app, model_loader = create_app()
    
    if model_loader.load_model_and_labels():
        print("Model and labels loaded successfully!")
        print("API is ready to accept requests.")
    else:
        print("Warning: Model or labels failed to load. API may not function correctly.")
    
    # Run Flask app
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)

"""
Entry point for the Flask application
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from app.app import create_app

app, model_loader = create_app()

if __name__ == '__main__':
    print("Starting Plant Disease Detection API...")
    
    if model_loader.load_model_and_labels():
        print("Model and labels loaded successfully!")
        print("API is ready to accept requests.")
    else:
        print("Warning: Model or labels failed to load. API may not function correctly.")
    
    from config.settings import API_HOST, API_PORT, DEBUG
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)

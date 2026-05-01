"""
Configuration settings for the Plant Disease Detection API
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Model configuration
IMG_SIZE = 224
MODEL_PATH = os.path.join(BASE_DIR, 'ml-model', 'models', 'plant_disease_model.h5')
CLASS_LABELS_PATH = os.path.join(BASE_DIR, 'ml-model', 'models', 'class_labels.json')

# API configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# CORS configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

# File upload configuration
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

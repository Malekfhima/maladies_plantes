"""
Configuration settings for ML model training and inference
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data paths
DATASET_PATH = os.path.join(BASE_DIR, 'ml-model', 'data', 'dataset')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'ml-model', 'data', 'processed')

# Model paths
MODELS_DIR = os.path.join(BASE_DIR, 'ml-model', 'models')
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, 'plant_disease_model.h5')
TFLITE_MODEL_PATH = os.path.join(MODELS_DIR, 'plant_disease_model.tflite')
CLASS_LABELS_PATH = os.path.join(MODELS_DIR, 'class_labels.json')

# Training parameters
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2

# Data augmentation
DATA_AUGMENTATION = {
    'rotation_range': 20,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'shear_range': 0.2,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    'fill_mode': 'nearest'
}

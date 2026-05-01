"""
Utility functions for ML model training and inference
"""
import json
import os
from pathlib import Path
from config import CLASS_LABELS_PATH

def save_class_labels(class_names, label_mapping):
    """
    Save class labels to JSON file
    
    Args:
        class_names: List of class names
        label_mapping: Dictionary mapping class indices to names
    """
    labels = {}
    for idx, name in enumerate(class_names):
        labels[str(idx)] = {
            "name": name,
            "description": f"Disease: {name}",
            "treatment": "Consult agricultural expert for specific treatment"
        }
    
    # Ensure models directory exists
    os.makedirs(os.path.dirname(CLASS_LABELS_PATH), exist_ok=True)
    
    with open(CLASS_LABELS_PATH, 'w') as f:
        json.dump(labels, f, indent=2)
    
    print(f"Class labels saved to {CLASS_LABELS_PATH}")

def load_class_labels():
    """
    Load class labels from JSON file
    
    Returns:
        dict: Class labels dictionary
    """
    if os.path.exists(CLASS_LABELS_PATH):
        with open(CLASS_LABELS_PATH, 'r') as f:
            return json.load(f)
    return None

def create_directory_structure():
    """Create necessary directory structure for the project"""
    directories = [
        'ml-model/data/dataset',
        'ml-model/data/processed',
        'ml-model/models',
        'ml-model/notebooks'
    ]
    
    for dir_path in directories:
        full_path = os.path.join(BASE_DIR, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")

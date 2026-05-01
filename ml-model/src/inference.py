"""
Plant Disease Detection - Model Inference
Script to test the trained model on individual images
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os
from config import IMG_SIZE, MODEL_SAVE_PATH, CLASS_LABELS_PATH

def load_model_and_labels():
    """
    Load the trained model and class labels
    """
    # Check if model exists
    if not os.path.exists(MODEL_SAVE_PATH):
        print(f"Model not found at {MODEL_SAVE_PATH}")
        return None, None
    
    # Load model
    model = tf.keras.models.load_model(MODEL_SAVE_PATH)
    
    # Load class labels
    if not os.path.exists(CLASS_LABELS_PATH):
        print(f"Class labels not found at {CLASS_LABELS_PATH}")
        return model, None
    
    with open(CLASS_LABELS_PATH, 'r') as f:
        class_labels = json.load(f)
    
    return model, class_labels

def preprocess_image(img_path):
    """
    Preprocess image for prediction
    """
    # Load and resize image
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    
    # Expand dimensions and normalize
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    return img_array

def predict_disease(model, class_labels, img_path):
    """
    Predict disease from image
    """
    # Preprocess image
    img_array = preprocess_image(img_path)
    
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
        "class_id": int(predicted_class)
    }
    
    return result

def main():
    """
    Main inference function
    """
    # Load model and labels
    print("Loading model and labels...")
    model, class_labels = load_model_and_labels()
    
    if model is None:
        print("Failed to load model. Please train the model first using train.py")
        return
    
    if class_labels is None:
        print("Failed to load class labels. Please train the model first using train.py")
        return
    
    print("Model and labels loaded successfully!")
    
    # Test image path (update with your test image)
    test_image = "test_image.jpg"
    
    if not os.path.exists(test_image):
        print(f"Test image not found: {test_image}")
        print("Please provide a valid image path")
        return
    
    # Make prediction
    print(f"\nAnalyzing image: {test_image}")
    result = predict_disease(model, class_labels, test_image)
    
    # Display results
    print("\n" + "="*50)
    print("PREDICTION RESULTS")
    print("="*50)
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"\nDescription: {result['description']}")
    print(f"\nTreatment: {result['treatment']}")
    print("="*50)

if __name__ == "__main__":
    main()

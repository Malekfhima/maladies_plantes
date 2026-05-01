"""
Plant Disease Detection - CNN Model Training
Uses PlantVillage dataset to train a CNN for plant disease classification
"""

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import os
import json
from config import (
    IMG_SIZE, BATCH_SIZE, EPOCHS, LEARNING_RATE,
    DATASET_PATH, MODEL_SAVE_PATH, TFLITE_MODEL_PATH, CLASS_LABELS_PATH
)

def create_data_generators():
    """
    Create data generators for training, validation, and testing
    with data augmentation for training
    """
    # Ensure dataset path exists
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset path not found: {DATASET_PATH}")
        print("Please download and organize the PlantVillage dataset in ml-model/data/dataset/")
        return None, None
    
    # Training data with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Validation and test data (only rescaling)
    test_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    validation_generator = test_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, validation_generator

def build_cnn_model(num_classes):
    """
    Build a CNN model for plant disease classification
    """
    model = models.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def compile_model(model):
    """
    Compile the model with optimizer, loss function, and metrics
    """
    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return model

def train_model(model, train_generator, validation_generator):
    """
    Train the model with callbacks for early stopping and learning rate reduction
    """
    # Create directories for saving models
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train the model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def evaluate_model(model, validation_generator):
    """
    Evaluate the model on validation data
    """
    results = model.evaluate(validation_generator, verbose=1)
    print(f"\nValidation Loss: {results[0]:.4f}")
    print(f"Validation Accuracy: {results[1]:.4f}")
    print(f"Validation Precision: {results[2]:.4f}")
    print(f"Validation Recall: {results[3]:.4f}")
    
    return results

def save_class_labels(train_generator):
    """
    Save class labels mapping for inference
    """
    class_labels = {v: k for k, v in train_generator.class_indices.items()}
    
    # Disease information (expand based on your dataset)
    disease_info = {
        "healthy": {
            "description": "The plant appears healthy with no visible signs of disease.",
            "treatment": "Continue regular watering, fertilization, and monitoring practices."
        },
        "late_blight": {
            "description": "Late blight is caused by the fungus-like organism Phytophthora infestans. It causes dark, water-soaked lesions on leaves.",
            "treatment": "Apply fungicides containing copper or chlorothalonil. Remove infected plant parts. Improve air circulation."
        },
        "early_blight": {
            "description": "Early blight is caused by the fungus Alternaria solani. It causes dark concentric rings on leaves.",
            "treatment": "Apply fungicides, remove infected leaves, avoid overhead watering, and rotate crops."
        },
        "leaf_spot": {
            "description": "Leaf spot diseases cause circular spots on leaves, often with dark borders.",
            "treatment": "Remove infected leaves, apply fungicides, ensure proper spacing for air circulation."
        },
        "powdery_mildew": {
            "description": "Powdery mildew appears as white powdery coating on leaves, stems, and flowers.",
            "treatment": "Apply sulfur-based fungicides, improve air circulation, avoid overhead watering."
        },
        "rust": {
            "description": "Rust diseases cause orange-brown pustules on leaf undersides.",
            "treatment": "Apply fungicides, remove infected plant material, practice crop rotation."
        },
        "bacterial_spot": {
            "description": "Bacterial spot causes water-soaked spots that turn brown or black.",
            "treatment": "Use copper-based bactericides, avoid working with plants when wet, remove infected plants."
        },
        "mosaic_virus": {
            "description": "Mosaic virus causes mottled patterns on leaves, stunted growth, and distorted foliage.",
            "treatment": "No cure exists. Remove infected plants, control aphids which spread the virus."
        },
        "septoria_leaf_spot": {
            "description": "Septoria leaf spot causes small circular spots with dark borders and gray centers.",
            "treatment": "Apply fungicides, remove infected leaves, mulch to prevent soil splash."
        },
        "target_spot": {
            "description": "Target spot causes concentric ring patterns on leaves similar to early blight.",
            "treatment": "Apply fungicides, improve air circulation, remove infected plant debris."
        },
        "yellow_leaf_curl_virus": {
            "description": "Yellow leaf curl virus causes leaves to curl and turn yellow, stunting plant growth.",
            "treatment": "No chemical cure. Remove infected plants, control whiteflies which spread the virus."
        },
        "bacterial_blight": {
            "description": "Bacterial blight causes water-soaked lesions that turn brown and papery.",
            "treatment": "Use copper-based bactericides, avoid overhead irrigation, practice crop rotation."
        },
        "alternaria_leaf_spot": {
            "description": "Alternaria leaf spot causes dark spots with concentric rings on leaves.",
            "treatment": "Apply fungicides, remove infected leaves, improve air circulation."
        },
        "downy_mildew": {
            "description": "Downy mildew causes yellow patches on leaf tops with gray fuzzy growth underneath.",
            "treatment": "Apply fungicides, improve air circulation, reduce humidity around plants."
        },
        "anthracnose": {
            "description": "Anthracnose causes dark sunken lesions on leaves, stems, and fruits.",
            "treatment": "Apply fungicides, remove infected plant parts, avoid overhead watering."
        }
    }
    
    # Merge class labels with disease info
    class_mapping = {}
    for class_id, class_name in class_labels.items():
        class_mapping[str(class_id)] = {
            "name": class_name,
            "description": disease_info.get(class_name, {}).get("description", "Disease description not available."),
            "treatment": disease_info.get(class_name, {}).get("treatment", "Consult agricultural expert for treatment.")
        }
    
    # Save to JSON
    with open(CLASS_LABELS_PATH, 'w') as f:
        json.dump(class_mapping, f, indent=2)
    
    print(f"Class labels saved to {CLASS_LABELS_PATH}")

def convert_to_tflite(model):
    """
    Convert the trained model to TensorFlow Lite format for mobile deployment
    """
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    with open(TFLITE_MODEL_PATH, 'wb') as f:
        f.write(tflite_model)
    
    print(f"TensorFlow Lite model saved to {TFLITE_MODEL_PATH}")

def main():
    """
    Main training pipeline
    """
    print("Starting Plant Disease Detection Model Training...")
    print(f"Image size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Epochs: {EPOCHS}")
    print(f"Dataset path: {DATASET_PATH}")
    print("-" * 50)
    
    # Create data generators
    print("Loading and preprocessing data...")
    train_generator, validation_generator = create_data_generators()
    
    if train_generator is None or validation_generator is None:
        print("Failed to create data generators. Exiting.")
        return
    
    NUM_CLASSES = len(train_generator.class_indices)
    print(f"Number of classes: {NUM_CLASSES}")
    print(f"Class names: {list(train_generator.class_indices.keys())}")
    print("-" * 50)
    
    # Build model
    print("Building CNN model...")
    model = build_cnn_model(NUM_CLASSES)
    model.summary()
    print("-" * 50)
    
    # Compile model
    print("Compiling model...")
    model = compile_model(model)
    print("-" * 50)
    
    # Train model
    print("Training model...")
    history = train_model(model, train_generator, validation_generator)
    print("-" * 50)
    
    # Evaluate model
    print("Evaluating model...")
    evaluate_model(model, validation_generator)
    print("-" * 50)
    
    # Save class labels
    print("Saving class labels...")
    save_class_labels(train_generator)
    print("-" * 50)
    
    # Convert to TFLite
    print("Converting model to TensorFlow Lite...")
    convert_to_tflite(model)
    print("-" * 50)
    
    print("Training complete! Models saved successfully.")

if __name__ == "__main__":
    main()

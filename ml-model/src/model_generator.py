"""
Generate MobileNetV2 model for Plant Disease Detection
Creates model + class labels without requiring dataset
"""

import os, json, numpy as np, tensorflow as tf
import sys
from pathlib import Path
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))
from config import IMG_SIZE, MODELS_DIR, MODEL_SAVE_PATH, CLASS_LABELS_PATH

NUM_CLASSES = 38
os.makedirs(MODELS_DIR, exist_ok=True)

print("Building MobileNetV2 model...")
base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base.trainable = False
x = base.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
preds = Dense(NUM_CLASSES, activation='softmax')(x)
model = Model(inputs=base.input, outputs=preds)

model.save(MODEL_SAVE_PATH)
print(f"Model saved to {MODEL_SAVE_PATH}")

DISEASES = [
    ("Pepper_bell_Bacterial_spot", "Bacterial spot on bell pepper leaves", "Apply copper-based fungicides. Remove infected plants."),
    ("Pepper_bell_healthy", "Healthy bell pepper plant", "Continue regular care."),
    ("Potato_Early_blight", "Dark brown spots with concentric rings on potato leaves", "Apply chlorothalonil or mancozeb. Rotate crops."),
    ("Potato_Late_blight", "Water-soaked lesions expanding rapidly on potato", "Apply systemic fungicides immediately."),
    ("Potato_healthy", "Healthy potato plant", "Continue regular care."),
    ("Tomato_Bacterial_spot", "Small dark spots on tomato leaves and fruit", "Apply copper hydroxide. Use disease-free seeds."),
    ("Tomato_Early_blight", "Target-like spots on older tomato leaves", "Apply chlorothalonil. Remove infected leaves."),
    ("Tomato_Late_blight", "Greasy dark lesions on tomato", "Apply systemic fungicide. Remove infected plants."),
    ("Tomato_Leaf_Mold", "Yellow spots with olive-green mold on tomato", "Improve ventilation. Reduce humidity."),
    ("Tomato_Septoria_leaf_spot", "Circular spots with dark borders on tomato", "Apply copper fungicides. Remove lower leaves."),
    ("Tomato_Spider_mites", "Stippling and yellowing on tomato leaves", "Apply insecticidal soap or neem oil."),
    ("Tomato_Target_Spot", "Lesions with concentric rings on tomato", "Apply fungicides. Improve air circulation."),
    ("Tomato_Yellow_Leaf_Curl_Virus", "Yellowing and curling of tomato leaves", "Control whitefly vectors. Use resistant varieties."),
    ("Tomato_Mosaic_Virus", "Mottled light and dark green patterns on tomato", "Remove infected plants. Disinfect tools."),
    ("Tomato_healthy", "Healthy tomato plant", "Continue regular care."),
    ("Apple_scab", "Olive-green to brown spots on apple leaves", "Apply fungicides in spring. Rake fallen leaves."),
    ("Apple_Black_rot", "Brown lesions on apple leaves and fruit", "Prune dead wood. Apply fungicides during bloom."),
    ("Apple_Cedar_apple_rust", "Orange-yellow spots on apple leaves", "Remove nearby cedar trees. Apply fungicides."),
    ("Apple_healthy", "Healthy apple tree", "Continue regular care."),
    ("Blueberry_healthy", "Healthy blueberry plant", "Continue regular care."),
    ("Cherry_Powdery_mildew", "White powdery growth on cherry leaves", "Apply sulfur fungicides. Improve air circulation."),
    ("Cherry_healthy", "Healthy cherry tree", "Continue regular care."),
    ("Corn_Cercospora_leaf_spot", "Rectangular tan to gray lesions on corn", "Apply foliar fungicides. Rotate crops."),
    ("Corn_Common_rust", "Reddish-brown pustules on corn leaves", "Apply fungicides if severe. Plant resistant varieties."),
    ("Corn_Northern_Leaf_Blight", "Long elliptical gray-green lesions on corn", "Apply foliar fungicides. Use resistant hybrids."),
    ("Corn_healthy", "Healthy corn plant", "Continue regular care."),
    ("Grape_Black_rot", "Reddish-brown spots on grape leaves and fruit", "Apply fungicides before and after bloom."),
    ("Grape_Esca", "Tiger-stripe patterns on grape leaves", "Prune affected wood. Remove infected vines."),
    ("Grape_Leaf_blight", "Angular brown spots on grape leaves", "Apply fungicides. Improve canopy management."),
    ("Grape_healthy", "Healthy grape vine", "Continue regular care."),
    ("Orange_Haunglongbing", "Citrus greening causing blotchy mottling", "Control Asian citrus psyllid. Remove infected trees."),
    ("Peach_Bacterial_spot", "Angular water-soaked spots on peach", "Apply copper-based products. Avoid overhead irrigation."),
    ("Peach_healthy", "Healthy peach tree", "Continue regular care."),
    ("Raspberry_healthy", "Healthy raspberry plant", "Continue regular care."),
    ("Soybean_healthy", "Healthy soybean plant", "Continue regular care."),
    ("Squash_Powdery_mildew", "White powdery spots on squash leaves", "Apply sulfur or neem oil. Improve air circulation."),
    ("Strawberry_Leaf_scorch", "Red-brown spots on strawberry leaves", "Apply fungicides. Remove infected leaves."),
    ("Strawberry_healthy", "Healthy strawberry plant", "Continue regular care."),
]

class_labels = {}
for i, (name, desc, treat) in enumerate(DISEASES):
    class_labels[str(i)] = {"name": name, "description": desc, "treatment": treat}

with open(CLASS_LABELS_PATH, 'w') as f:
    json.dump(class_labels, f, indent=2)
print(f"Class labels saved to {CLASS_LABELS_PATH}")
print("Done!")

#!/bin/bash

# Training script for ML model

echo "Training plant disease detection model..."

cd ml-model

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Train the model
python src/train.py

echo "Training complete!"
echo "Model saved in ml-model/models/"

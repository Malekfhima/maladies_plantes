#!/bin/bash

# Setup script for Plant Disease Detection project

echo "Setting up Plant Disease Detection project..."

# Create virtual environment for backend
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Create virtual environment for ML model
echo "Setting up ML model..."
cd ml-model
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install mobile app dependencies
echo "Setting up mobile app..."
cd mobile-app
npm install
cd ..

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Download and organize dataset in ml-model/data/dataset/"
echo "2. Train the model: cd ml-model && python src/train.py"
echo "3. Start the backend: cd backend && python run.py"
echo "4. Start the mobile app: cd mobile-app && npm start"

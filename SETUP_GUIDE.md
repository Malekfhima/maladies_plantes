# Setup Guide

## Python Environment Setup

Since TensorFlow doesn't support Python 3.14 yet, you need to use Python 3.10, 3.11, or 3.12.

### Option 1: Using pyenv (Recommended for macOS/Linux)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11.9

# Set local Python version for this project
cd /run/media/malek/Nouveau\ nom/ML
pyenv local 3.11.9

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### Option 2: Using conda

```bash
# Create environment with Python 3.11
conda create -n plant-disease python=3.11

# Activate environment
conda activate plant-disease

# Navigate to project
cd /run/media/malek/Nouveau\ nom/ML/plant-disease-detection
```

### Option 3: Using system Python 3.10-3.12

If you have Python 3.10, 3.11, or 3.12 installed:

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

## Install Dependencies

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### ML Model

```bash
cd ml-model
pip install -r requirements.txt
```

### Mobile App

```bash
cd mobile-app
npm install
```

## Quick Start with Existing Model

The project already has a trained model in `ml-model/models/`. You can start the backend immediately:

```bash
cd backend
python run.py
```

The API will be available at `http://localhost:5000`

### Test the Backend

In a new terminal:

```bash
cd plant-disease-detection
python scripts/test_backend.py
```

## Training a New Model (Optional)

If you want to train your own model:

1. Download the PlantVillage dataset from [Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)
2. Extract and organize it in `ml-model/data/dataset/`
3. Run the training script:

```bash
cd ml-model
python src/train.py
```

Or use the provided script:

```bash
./scripts/train.sh
```

## Running the Mobile App

```bash
cd mobile-app
npm start
```

Update the API URL in `mobile-app/src/config/index.js` to point to your backend.

## Troubleshooting

### TensorFlow Installation Error

If you get "No matching distribution found for tensorflow", you're using an unsupported Python version. Use Python 3.10, 3.11, or 3.12.

### Model Not Loading

Ensure the model files exist in `ml-model/models/`:
- `plant_disease_model.h5`
- `class_labels.json`

### Backend Connection Error

Check that:
1. The backend is running (`python backend/run.py`)
2. The mobile app config has the correct IP address
3. Firewall is not blocking port 5000

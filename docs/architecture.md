# Architecture Documentation

## System Architecture

The Plant Disease Detection system consists of three main components:

1. **ML Model** - CNN model for disease classification
2. **Backend API** - Flask REST API for model inference
3. **Mobile App** - React Native app for user interaction

## Component Architecture

### ML Model

```
ml-model/
├── src/
│   ├── train.py           # Model training script
│   ├── inference.py       # Model inference script
│   ├── model_generator.py # Model architecture definition
│   ├── config.py          # Configuration settings
│   └── utils.py           # Utility functions
├── data/
│   ├── dataset/           # Raw training data
│   └── processed/        # Processed data
├── models/               # Trained models
└── notebooks/            # Jupyter notebooks for experimentation
```

### Backend API

```
backend/
├── config/
│   └── settings.py       # Configuration management
├── app/
│   ├── app.py           # Flask application factory
│   ├── routes/          # API endpoints
│   │   ├── health.py    # Health check endpoint
│   │   └── predict.py   # Prediction endpoints
│   └── services/        # Business logic
│       ├── model_loader.py      # Model loading service
│       ├── image_processor.py  # Image preprocessing
│       └── predictor.py        # Prediction service
├── tests/               # Unit tests
└── run.py               # Application entry point
```

### Mobile App

```
mobile-app/
├── src/
│   ├── api/            # API communication
│   ├── components/     # Reusable components
│   ├── config/         # App configuration
│   ├── constants/      # App constants
│   ├── i18n/          # Internationalization
│   ├── navigation/    # Navigation configuration
│   ├── screens/       # Screen components
│   └── utils/         # Utility functions
├── assets/            # Images, fonts, etc.
└── App.js             # Main entry point
```

## Data Flow

1. User captures/selects image in mobile app
2. Mobile app sends image to backend API via `/predict` endpoint
3. Backend preprocesses image
4. Backend loads model and makes prediction
5. Backend returns prediction results to mobile app
6. Mobile app displays results to user

## Model Architecture

The CNN model consists of:
- 4 Convolutional blocks with Batch Normalization and Dropout
- Max Pooling layers for dimensionality reduction
- Dense layers with Batch Normalization and Dropout
- Softmax output layer for multi-class classification

## Technology Stack

- **ML Model**: TensorFlow/Keras
- **Backend**: Flask, Flask-CORS
- **Mobile**: React Native (Expo)
- **Deployment**: Docker, Gunicorn

# Plant Disease Detection App

A complete smart agriculture mobile application that detects plant diseases using computer vision and deep learning.

## 📱 Features

- **Camera Integration**: Capture plant images directly from your phone camera
- **Gallery Selection**: Upload images from your photo gallery
- **AI-Powered Detection**: Uses a trained CNN model to identify plant diseases
- **Detailed Results**: Displays disease name, confidence percentage, description, and treatment recommendations
- **Modern UI**: Clean, intuitive interface with loading indicators and error handling
- **Cross-Platform**: Built with React Native (Expo) for iOS and Android

## 🏗️ Project Structure

```
plant-disease-detection/
├── ml-model/              # Machine Learning Model
│   ├── train_model.py     # CNN training script
│   ├── inference.py       # Model inference script
│   ├── requirements.txt  # ML dependencies
│   ├── dataset/           # Training dataset (PlantVillage)
│   └── models/            # Saved models (created after training)
│       ├── plant_disease_model.h5
│       ├── plant_disease_model.tflite
│       └── class_labels.json
│
├── backend/               # Flask Backend API
│   ├── app.py            # Flask application with REST API
│   └── requirements.txt  # Backend dependencies
│
└── mobile-app/           # React Native Mobile App
    ├── App.js            # Main entry point
    ├── app.json          # Expo configuration
    ├── package.json      # Node dependencies
    ├── src/
    │   ├── api/
    │   │   └── api.js    # API service for backend communication
    │   ├── screens/
    │   │   └── HomeScreen.js  # Main screen with camera/gallery
    │   └── components/
    │       └── ResultCard.js  # Result display component
    └── assets/           # App icons and splash screens
```

## 🧠 Machine Learning Model

### Model Architecture

The model uses a Convolutional Neural Network (CNN) with the following architecture:

- 4 Convolutional blocks with Batch Normalization and Dropout
- Max Pooling layers for dimensionality reduction
- Dense layers with Batch Normalization and Dropout
- Softmax output layer for multi-class classification

### Training Details

- **Image Size**: 224x224 pixels
- **Batch Size**: 32
- **Epochs**: 50 (with early stopping)
- **Optimizer**: Adam (learning rate: 0.001)
- **Loss Function**: Categorical Crossentropy
- **Data Augmentation**: Rotation, shift, shear, zoom, horizontal flip

### Supported Diseases

The model can detect various plant diseases including:
- Late Blight
- Early Blight
- Leaf Spot
- Powdery Mildew
- Rust
- Bacterial Spot
- Mosaic Virus
- Septoria Leaf Spot
- And more...

## 🌐 Backend API

### Endpoints

#### `GET /health`
Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "labels_loaded": true
}
```

#### `POST /predict`
Predict plant disease from uploaded image.

**Request:** `multipart/form-data` with `image` field

**Response:**
```json
{
  "disease": "late_blight",
  "confidence": 95.5,
  "description": "Late blight is caused by the fungus-like organism...",
  "treatment": "Apply fungicides containing copper...",
  "class_id": 1,
  "status": "success"
}
```

#### `GET /classes`
Get all available disease classes.

**Response:**
```json
{
  "status": "success",
  "classes": [...],
  "total": 15
}
```

## 📲 Mobile App

### Tech Stack

- **Framework**: React Native with Expo
- **Navigation**: React Navigation
- **HTTP Client**: Axios
- **Icons**: @expo/vector-icons
- **Camera**: expo-camera
- **Image Picker**: expo-image-picker

### Features

- Camera permission handling
- Gallery permission handling
- Image preview
- Loading indicators during prediction
- Error handling with user-friendly messages
- Modern card-based result display
- Responsive design

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Expo CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

### 1. ML Model Setup

#### Install Dependencies

```bash
cd ml-model
pip install -r requirements.txt
```

#### Prepare Dataset

1. Download the PlantVillage dataset from [Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)
2. Extract and organize the dataset:
   ```
   dataset/plantvillage/
   ├── Pepper__bell___Bacterial_spot/
   ├── Pepper__bell___healthy/
   ├── Potato___Early_blight/
   ├── Potato___Late_blight/
   ├── Potato___healthy/
   ├── Tomato___Bacterial_spot/
   ├── Tomato___Early_blight/
   ├── Tomato___Late_blight/
   ├── Tomato___healthy/
   └── ...
   ```

#### Train the Model

```bash
python train_model.py
```

This will:
- Train the CNN model
- Save the model as `plant_disease_model.h5`
- Convert to TensorFlow Lite format `plant_disease_model.tflite`
- Save class labels as `class_labels.json`

#### Test the Model

```bash
python inference.py
```

### 2. Backend API Setup

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Update API Configuration

Edit `backend/app.py` and update the model paths if needed:
```python
MODEL_PATH = '../ml-model/models/plant_disease_model.h5'
CLASS_LABELS_PATH = '../ml-model/models/class_labels.json'
```

#### Run the Backend

```bash
python app.py
```

The API will start on `http://0.0.0.0:5000`

#### Test the API

```bash
curl http://localhost:5000/health
```

### 3. Mobile App Setup

#### Install Dependencies

```bash
cd mobile-app
npm install
```

#### Update API URL

Edit `mobile-app/src/api/api.js` and update the backend URL:

```javascript
// For local testing, use your computer's IP address
const API_BASE_URL = 'http://YOUR_COMPUTER_IP:5000';
```

To find your computer's IP:
- **Windows**: Run `ipconfig` in command prompt
- **Mac/Linux**: Run `ifconfig` or `ip a` in terminal

#### Run the App

**Development Mode:**
```bash
npm start
```

Then:
- Press `a` to run on Android emulator/device
- Press `i` to run on iOS simulator (macOS only)
- Scan the QR code with Expo Go app on your phone

**Production Build:**

For Android:
```bash
npm run android
```

For iOS:
```bash
npm run ios
```

## 📦 Deployment

### Backend Deployment

#### Option 1: Cloud VM (AWS, GCP, Azure)

1. Deploy the backend to a cloud VM
2. Install Python and dependencies
3. Run the Flask app with a production server (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
4. Use Nginx as a reverse proxy
5. Configure SSL with Let's Encrypt

#### Option 2: Docker

Create a `Dockerfile` in the backend directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t plant-disease-api .
docker run -p 5000:5000 plant-disease-api
```

### Mobile App Deployment

#### Option 1: Expo Application Services (EAS)

```bash
npm install -g eas-cli
eas build:configure
eas build --platform android
eas build --platform ios
```

#### Option 2: Google Play Store (Android)

1. Build the APK/AAB:
   ```bash
   eas build --platform android --profile production
   ```
2. Upload to Google Play Console

#### Option 3: Apple App Store (iOS)

1. Build the IPA:
   ```bash
   eas build --platform ios --profile production
   ```
2. Upload to App Store Connect

## 🔧 Configuration

### Model Training Parameters

Edit `ml-model/train_model.py` to adjust:

```python
IMG_SIZE = 224          # Image dimensions
BATCH_SIZE = 32         # Training batch size
EPOCHS = 50            # Number of training epochs
LEARNING_RATE = 0.001  # Learning rate
```

### Backend Configuration

Edit `backend/app.py` to adjust:

```python
MODEL_PATH = '../ml-model/models/plant_disease_model.h5'
CLASS_LABELS_PATH = '../ml-model/models/class_labels.json'
```

### Mobile App Configuration

Edit `mobile-app/src/api/api.js` to change the backend URL.

Edit `mobile-app/app.json` to change app name, icons, and permissions.

## 🐛 Troubleshooting

### Model Training Issues

**Issue**: Out of memory during training
**Solution**: Reduce `BATCH_SIZE` in `train_model.py`

**Issue**: Poor accuracy
**Solution**: 
- Increase training epochs
- Add more data augmentation
- Use a larger dataset
- Try transfer learning with pre-trained models (ResNet, MobileNet)

### Backend Issues

**Issue**: Model not loading
**Solution**: Ensure the model files exist in the correct path

**Issue**: CORS errors
**Solution**: Flask CORS is already enabled. If issues persist, check the CORS configuration

**Issue**: Connection timeout
**Solution**: Increase the timeout in `mobile-app/src/api/api.js`

### Mobile App Issues

**Issue**: Camera not working
**Solution**: 
- Ensure camera permissions are granted
- Check `app.json` permissions configuration

**Issue**: Cannot connect to backend
**Solution**: 
- Ensure backend is running
- Check the API URL in `api.js`
- Ensure your phone and computer are on the same network
- Check firewall settings

**Issue**: Build fails
**Solution**: 
- Clear cache: `expo start -c`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Update Expo dependencies

## 📊 Performance Optimization

### Model Optimization

- Use TensorFlow Lite for mobile inference
- Apply quantization to reduce model size
- Consider using MobileNetV2 or EfficientNet for better mobile performance

### Backend Optimization

- Use Gunicorn with multiple workers
- Implement caching for repeated predictions
- Use CDN for serving static assets
- Implement rate limiting

### Mobile App Optimization

- Compress images before sending to API
- Implement offline mode with TensorFlow Lite
- Add request caching
- Optimize image quality/size tradeoff

## 🔒 Security Considerations

- Implement API authentication (JWT tokens)
- Add rate limiting to prevent abuse
- Validate and sanitize all inputs
- Use HTTPS in production
- Implement proper error handling (don't expose sensitive information)
- Add CORS restrictions in production

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- PlantVillage dataset for the training images
- TensorFlow/Keras for the deep learning framework
- React Native/Expo for the mobile framework
- Flask for the backend API

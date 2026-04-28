# Quick Start Guide

Get the Plant Disease Detection app up and running in minutes!

## 🚀 Fast Setup (5 minutes)

### Option 1: Use Pre-trained Model (Recommended)

If you have a pre-trained model, skip the training step and go directly to backend setup.

### Option 2: Train Your Own Model (1-2 hours)

1. **Download Dataset**
   ```bash
   cd ml-model
   # Download PlantVillage dataset from Kaggle
   # Extract to dataset/plantvillage/
   ```

2. **Train Model**
   ```bash
   pip install -r requirements.txt
   python train_model.py
   ```

3. **Model files will be saved in `models/` directory**

## 🌐 Backend Setup (2 minutes)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend will run on `http://localhost:5000`

Test it:
```bash
curl http://localhost:5000/health
```

## 📱 Mobile App Setup (3 minutes)

```bash
cd mobile-app
npm install
```

**Important**: Update the API URL in `src/api/api.js`:
```javascript
const API_BASE_URL = 'http://YOUR_COMPUTER_IP:5000';
```

Find your IP:
- **Windows**: `ipconfig`
- **Mac/Linux**: `ifconfig` or `ip a`

Run the app:
```bash
npm start
```

Scan the QR code with Expo Go app on your phone.

## 🎯 That's It!

You now have a fully functional plant disease detection app:
- Open the app on your phone
- Take a photo or select from gallery
- Get instant disease prediction with treatment recommendations

## 🐛 Common Issues

### "Cannot connect to server"
- Ensure backend is running (`python app.py`)
- Check your phone and computer are on the same Wi-Fi
- Verify the IP address in `api.js`

### "Camera permission denied"
- Grant camera permission in phone settings
- Check `app.json` permissions configuration

### "Model not found"
- Ensure you've trained the model or have pre-trained model files
- Check that `models/plant_disease_model.h5` exists

## 📚 For Detailed Instructions

See the main [README.md](README.md) for:
- Detailed setup instructions
- Deployment guides
- Troubleshooting
- Configuration options

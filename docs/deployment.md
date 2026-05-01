# Deployment Guide

## Backend Deployment

### Option 1: Cloud VM (AWS, GCP, Azure)

1. Deploy the backend to a cloud VM
2. Install Python and dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run with Gunicorn (production server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
4. Use Nginx as a reverse proxy
5. Configure SSL with Let's Encrypt

### Option 2: Docker

Build and run with Docker:
```bash
cd backend
docker build -t plant-disease-api .
docker run -p 5000:5000 plant-disease-api
```

Or use docker-compose:
```bash
docker-compose up -d
```

## Mobile App Deployment

### Option 1: Expo Application Services (EAS)

```bash
npm install -g eas-cli
eas build:configure
eas build --platform android
eas build --platform ios
```

### Option 2: Google Play Store (Android)

1. Build the APK/AAB:
   ```bash
   eas build --platform android --profile production
   ```
2. Upload to Google Play Console

### Option 3: Apple App Store (iOS)

1. Build the IPA:
   ```bash
   eas build --platform ios --profile production
   ```
2. Upload to App Store Connect

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with your production settings.

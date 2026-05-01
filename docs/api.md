# API Documentation

## Overview

The Plant Disease Detection API provides endpoints for predicting plant diseases from images.

## Base URL

```
http://localhost:5000
```

## Endpoints

### Health Check

Check if the API is running and model is loaded.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "labels_loaded": true
}
```

### Predict Disease

Predict plant disease from an uploaded image.

**Endpoint:** `POST /predict`

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

**Error Response:**
```json
{
  "status": "error",
  "message": "No image file provided"
}
```

### Get Classes

Get all available disease classes.

**Endpoint:** `GET /classes`

**Response:**
```json
{
  "status": "success",
  "classes": [
    {
      "id": 0,
      "name": "healthy",
      "description": "Plant is healthy"
    }
  ],
  "total": 15
}
```

## Error Codes

- `400` - Bad Request (missing or invalid parameters)
- `404` - Not Found (endpoint doesn't exist)
- `500` - Internal Server Error (server-side error)

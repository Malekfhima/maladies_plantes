/**
 * Home Screen
 * Main screen of the app with options to capture or select image
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { MaterialIcons } from '@expo/vector-icons';
import { useTranslation } from 'react-i18next';
import { predictDisease } from '../api/api';
import ResultCard from '../components/ResultCard';
import LanguageSelector from '../components/LanguageSelector';

const HomeScreen = () => {
  const { t } = useTranslation();
  const [imageUri, setImageUri] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Request camera permissions
   */
  const requestCameraPermission = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(
        t('errors.cameraPermission'),
        ''
      );
      return false;
    }
    return true;
  };

  /**
   * Request gallery permissions
   */
  const requestGalleryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(
        t('errors.galleryPermission'),
        ''
      );
      return false;
    }
    return true;
  };

  /**
   * Open camera to capture photo
   */
  const openCamera = async () => {
    try {
      const hasPermission = await requestCameraPermission();
      if (!hasPermission) return;

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setImageUri(result.assets[0].uri);
        setPrediction(null);
        setError(null);
        // Automatically predict after capturing
        await analyzeImage(result.assets[0].uri);
      }
    } catch (err) {
      setError(t('errors.cameraError'));
      Alert.alert('Error', t('errors.cameraError'));
    }
  };

  /**
   * Open gallery to select photo
   */
  const openGallery = async () => {
    try {
      const hasPermission = await requestGalleryPermission();
      if (!hasPermission) return;

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setImageUri(result.assets[0].uri);
        setPrediction(null);
        setError(null);
        // Automatically predict after selecting
        await analyzeImage(result.assets[0].uri);
      }
    } catch (err) {
      setError(t('errors.galleryError'));
      Alert.alert('Error', t('errors.galleryError'));
    }
  };

  /**
   * Analyze image using backend API
   */
  const analyzeImage = async (uri) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await predictDisease(uri);
      setPrediction(result);
    } catch (err) {
      setError(err.message || t('errors.predictionError'));
      Alert.alert('Error', err.message || t('errors.predictionError'));
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reset the app state
   */
  const resetState = () => {
    setImageUri(null);
    setPrediction(null);
    setError(null);
    setLoading(false);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Language Selector */}
      <LanguageSelector />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>{t('app.title')}</Text>
        <Text style={styles.subtitle}>
          {t('app.subtitle')}
        </Text>
      </View>

      {/* Image Preview */}
      {imageUri ? (
        <View style={styles.imagePreviewContainer}>
          <Image source={{ uri: imageUri }} style={styles.previewImage} />
          <TouchableOpacity style={styles.resetButton} onPress={resetState}>
            <Text style={styles.resetButtonText}>{t('home.newImage')}</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.placeholderContainer}>
          <MaterialIcons name="image-not-supported" size={64} color="#A0A0A0" />
          <Text style={styles.placeholderText}>
            {t('home.noImage')}
          </Text>
        </View>
      )}

      {/* Loading Indicator */}
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>{t('home.analyzing')}</Text>
        </View>
      )}

      {/* Error Message */}
      {error && !loading && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      {/* Prediction Result */}
      {prediction && !loading && (
        <ResultCard prediction={prediction} />
      )}

      {/* Action Buttons */}
      {!loading && (
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.cameraButton]}
            onPress={openCamera}
          >
            <MaterialIcons name="camera-alt" size={24} color="#FFFFFF" />
            <Text style={styles.buttonText}>{t('home.takePhoto')}</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.galleryButton]}
            onPress={openGallery}
          >
            <MaterialIcons name="photo-library" size={24} color="#FFFFFF" />
            <Text style={styles.buttonText}>{t('home.selectGallery')}</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Info Section */}
      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>{t('home.howItWorks')}</Text>
        <View style={styles.stepContainer}>
          <View style={styles.stepIconContainer}>
            <MaterialIcons name="camera-alt" size={24} color="#4CAF50" />
          </View>
          <Text style={styles.infoText}>
            {t('home.step1')}
          </Text>
        </View>
        <View style={styles.stepContainer}>
          <View style={styles.stepIconContainer}>
            <MaterialIcons name="psychology" size={24} color="#2196F3" />
          </View>
          <Text style={styles.infoText}>
            {t('home.step2')}
          </Text>
        </View>
        <View style={styles.stepContainer}>
          <View style={styles.stepIconContainer}>
            <MaterialIcons name="assignment-turned-in" size={24} color="#FF9800" />
          </View>
          <Text style={styles.infoText}>
            {t('home.step3')}
          </Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#757575',
    textAlign: 'center',
  },
  imagePreviewContainer: {
    marginBottom: 20,
    alignItems: 'center',
  },
  previewImage: {
    width: '100%',
    height: 300,
    borderRadius: 12,
    resizeMode: 'cover',
  },
  resetButton: {
    marginTop: 10,
    paddingHorizontal: 20,
    paddingVertical: 8,
    backgroundColor: '#757575',
    borderRadius: 20,
  },
  resetButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  placeholderContainer: {
    width: '100%',
    height: 300,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#E0E0E0',
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
  },
  placeholderText: {
    marginTop: 16,
    fontSize: 16,
    color: '#9E9E9E',
    fontWeight: '500',
  },
  loadingContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666666',
  },
  errorContainer: {
    backgroundColor: '#FFEBEE',
    padding: 16,
    borderRadius: 8,
    marginBottom: 20,
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  errorText: {
    color: '#D32F2F',
    fontSize: 14,
  },
  buttonContainer: {
    marginTop: 20,
    gap: 12,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 18,
    borderRadius: 16,
    gap: 12,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
  },
  cameraButton: {
    backgroundColor: '#4CAF50',
  },
  galleryButton: {
    backgroundColor: '#2196F3',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
  infoContainer: {
    marginTop: 40,
    padding: 24,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  infoTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 16,
    textAlign: 'center',
  },
  infoText: {
    fontSize: 15,
    color: '#424242',
    marginBottom: 12,
    lineHeight: 22,
    paddingLeft: 8,
    flex: 1,
  },
  stepContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  stepIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
});

export default HomeScreen;

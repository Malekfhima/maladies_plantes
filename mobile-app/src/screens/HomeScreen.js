/**
 * Home Screen
 * Main screen of the app with options to capture or select image
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  ActivityIndicator,
  Alert,
  Animated,
  StatusBar,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { MaterialIcons } from '@expo/vector-icons';
import { useTranslation } from 'react-i18next';
import { predictDisease } from '../api/api';
import ResultCard from '../components/ResultCard';
import LanguageSelector from '../components/LanguageSelector';
import { LinearGradient } from 'expo-linear-gradient';
import { checkNetworkConnection } from '../utils/network';
import { compressImage } from '../utils/imageUtils';
import { saveScanToHistory, getScanHistory } from '../utils/storage';
import theme from '../constants/theme';

const HomeScreen = () => {
  const { t } = useTranslation();
  const [imageUri, setImageUri] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [history, setHistory] = useState([]);
  
  const currentTheme = isDarkMode ? theme.COLORS.dark : theme.COLORS.light;
  
  // Animation values
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 800,
        useNativeDriver: true,
      }),
    ]).start();

    loadHistory();
  }, []);

  const loadHistory = async () => {
    const scanHistory = await getScanHistory();
    setHistory(scanHistory);
  };

  const requestCameraPermission = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(t('errors.cameraPermission'), '');
      return false;
    }
    return true;
  };

  const requestGalleryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(t('errors.galleryPermission'), '');
      return false;
    }
    return true;
  };

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
        await analyzeImage(result.assets[0].uri);
      }
    } catch (err) {
      setError(t('errors.cameraError'));
      Alert.alert('Error', t('errors.cameraError'));
    }
  };

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
        await analyzeImage(result.assets[0].uri);
      }
    } catch (err) {
      setError(t('errors.galleryError'));
      Alert.alert('Error', t('errors.galleryError'));
    }
  };

  const analyzeImage = async (uri) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const isConnected = await checkNetworkConnection();
      if (!isConnected) {
        throw new Error(t('errors.noConnection'));
      }

      const compressedUri = await compressImage(uri, 0.7, 1024);
      const result = await predictDisease(compressedUri);
      
      setPrediction(result);
      await saveScanToHistory({ imageUri: uri, prediction: result });
      await loadHistory();
    } catch (err) {
      setError(err.message || t('errors.predictionError'));
      Alert.alert('Error', err.message || t('errors.predictionError'));
    } finally {
      setLoading(false);
    }
  };

  const resetState = () => {
    setImageUri(null);
    setPrediction(null);
    setError(null);
    setLoading(false);
  };

  const styles = getStyles(currentTheme, isDarkMode);

  return (
    <View style={styles.container}>
      <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} />
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.contentContainer} showsVerticalScrollIndicator={false}>
        
        {/* Header with gradient */}
        <LinearGradient
          colors={[currentTheme.primary, currentTheme.primaryDark]}
          style={styles.headerGradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.topBar}>
            <LanguageSelector isDarkMode={isDarkMode} currentTheme={currentTheme} />
            <TouchableOpacity style={styles.darkModeToggle} onPress={() => setIsDarkMode(!isDarkMode)}>
              <MaterialIcons name={isDarkMode ? 'light-mode' : 'dark-mode'} size={24} color="#FFFFFF" />
            </TouchableOpacity>
          </View>

          <Animated.View style={[styles.header, { opacity: fadeAnim }]}>
            <Text style={styles.title}>{t('app.title')}</Text>
            <Text style={styles.subtitle}>{t('app.subtitle')}</Text>
          </Animated.View>
        </LinearGradient>

        <View style={styles.mainContent}>
          {/* Image Preview */}
          {imageUri ? (
            <View style={styles.imagePreviewContainer}>
              <Image source={{ uri: imageUri }} style={styles.previewImage} />
              <TouchableOpacity style={styles.resetButton} onPress={resetState}>
                <MaterialIcons name="refresh" size={20} color={currentTheme.primary} style={{marginRight: 6}} />
                <Text style={styles.resetButtonText}>{t('home.newImage')}</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.placeholderContainer} onPress={openGallery} activeOpacity={0.8}>
              <View style={styles.placeholderIconWrapper}>
                <MaterialIcons name="add-photo-alternate" size={48} color={currentTheme.primary} />
              </View>
              <Text style={styles.placeholderText}>{t('home.noImage')}</Text>
              <Text style={styles.placeholderSubtext}>Tap to browse gallery</Text>
            </TouchableOpacity>
          )}

          {/* Loading Indicator */}
          {loading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color={currentTheme.primary} />
              <Text style={styles.loadingText}>{t('home.analyzing')}</Text>
            </View>
          )}

          {/* Error Message */}
          {error && !loading && (
            <View style={styles.errorContainer}>
              <MaterialIcons name="error-outline" size={24} color={currentTheme.error} style={{marginRight: 10}}/>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Prediction Result */}
          {prediction && !loading && (
            <ResultCard prediction={prediction} currentTheme={currentTheme} isDarkMode={isDarkMode} />
          )}

          {/* Action Buttons */}
          {!loading && (
            <View style={styles.buttonContainer}>
              <TouchableOpacity style={[styles.button, styles.cameraButton]} onPress={openCamera} activeOpacity={0.8}>
                <MaterialIcons name="photo-camera" size={24} color="#FFFFFF" />
                <Text style={styles.buttonText}>{t('home.takePhoto')}</Text>
              </TouchableOpacity>

              <TouchableOpacity style={[styles.button, styles.galleryButton]} onPress={openGallery} activeOpacity={0.8}>
                <MaterialIcons name="collections" size={24} color="#FFFFFF" />
                <Text style={styles.buttonText}>{t('home.selectGallery')}</Text>
              </TouchableOpacity>
            </View>
          )}

          {/* Info Section */}
          {!imageUri && !loading && (
            <View style={styles.infoContainer}>
              <Text style={styles.infoTitle}>{t('home.howItWorks')}</Text>
              
              <View style={styles.stepContainer}>
                <View style={[styles.stepIconContainer, {backgroundColor: currentTheme.primary + '20'}]}>
                  <MaterialIcons name="camera-alt" size={22} color={currentTheme.primary} />
                </View>
                <Text style={styles.infoText}>{t('home.step1')}</Text>
              </View>
              
              <View style={styles.stepContainer}>
                <View style={[styles.stepIconContainer, {backgroundColor: currentTheme.secondary + '20'}]}>
                  <MaterialIcons name="psychology" size={22} color={currentTheme.secondary} />
                </View>
                <Text style={styles.infoText}>{t('home.step2')}</Text>
              </View>
              
              <View style={styles.stepContainer}>
                <View style={[styles.stepIconContainer, {backgroundColor: currentTheme.warning + '20'}]}>
                  <MaterialIcons name="assignment-turned-in" size={22} color={currentTheme.warning} />
                </View>
                <Text style={styles.infoText}>{t('home.step3')}</Text>
              </View>
            </View>
          )}
        </View>
      </ScrollView>
    </View>
  );
};

const getStyles = (currentTheme, isDarkMode) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: currentTheme.background,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    paddingBottom: 40,
  },
  headerGradient: {
    paddingTop: 60,
    paddingBottom: 40,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 40,
    borderBottomRightRadius: 40,
    elevation: 8,
    shadowColor: currentTheme.primaryDark,
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  darkModeToggle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    alignItems: 'center',
  },
  title: {
    ...theme.FONTS.h1,
    color: '#FFFFFF',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    ...theme.FONTS.body2,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
  },
  mainContent: {
    paddingHorizontal: 24,
    marginTop: -20,
  },
  imagePreviewContainer: {
    marginBottom: 24,
    alignItems: 'center',
    backgroundColor: currentTheme.cardBackground,
    borderRadius: theme.SIZES.radiusLg,
    padding: 12,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'medium'],
  },
  previewImage: {
    width: '100%',
    height: 320,
    borderRadius: theme.SIZES.radius,
    resizeMode: 'cover',
  },
  resetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 8,
    paddingHorizontal: 24,
    paddingVertical: 12,
    backgroundColor: currentTheme.primary + '15',
    borderRadius: 24,
  },
  resetButtonText: {
    color: currentTheme.primary,
    ...theme.FONTS.h4,
  },
  placeholderContainer: {
    width: '100%',
    height: 280,
    backgroundColor: currentTheme.cardBackground,
    borderRadius: theme.SIZES.radiusLg,
    borderWidth: 2,
    borderColor: currentTheme.primary + '40',
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'light'],
  },
  placeholderIconWrapper: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: currentTheme.primary + '15',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  placeholderText: {
    ...theme.FONTS.h3,
    color: currentTheme.text,
  },
  placeholderSubtext: {
    ...theme.FONTS.body3,
    color: currentTheme.textMuted,
    marginTop: 8,
  },
  loadingContainer: {
    alignItems: 'center',
    marginVertical: 32,
    backgroundColor: currentTheme.cardBackground,
    padding: 32,
    borderRadius: theme.SIZES.radiusLg,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'light'],
  },
  loadingText: {
    marginTop: 16,
    ...theme.FONTS.body1,
    color: currentTheme.textSecondary,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: currentTheme.errorBackground,
    padding: 16,
    borderRadius: theme.SIZES.radius,
    marginBottom: 24,
    borderLeftWidth: 4,
    borderLeftColor: currentTheme.error,
  },
  errorText: {
    color: currentTheme.error,
    ...theme.FONTS.body3,
    flex: 1,
  },
  buttonContainer: {
    marginTop: 8,
    gap: 16,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    borderRadius: theme.SIZES.radius,
    gap: 12,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'medium'],
  },
  cameraButton: {
    backgroundColor: currentTheme.primary,
  },
  galleryButton: {
    backgroundColor: currentTheme.secondary,
  },
  buttonText: {
    color: '#FFFFFF',
    ...theme.FONTS.h4,
  },
  infoContainer: {
    marginTop: 32,
    padding: 24,
    backgroundColor: currentTheme.cardBackground,
    borderRadius: theme.SIZES.radiusLg,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'light'],
  },
  infoTitle: {
    ...theme.FONTS.h3,
    color: currentTheme.text,
    marginBottom: 20,
  },
  infoText: {
    ...theme.FONTS.body2,
    color: currentTheme.textSecondary,
    lineHeight: 24,
    flex: 1,
  },
  stepContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  stepIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
});

export default HomeScreen;

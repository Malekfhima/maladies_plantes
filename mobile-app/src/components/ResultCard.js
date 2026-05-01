/**
 * Result Card Component
 * Displays the prediction results in a modern card layout
 */

import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Share, Alert } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useTranslation } from 'react-i18next';
import theme from '../constants/theme';

const ResultCard = ({ prediction, currentTheme, isDarkMode }) => {
  const { t, i18n } = useTranslation();
  const { disease, confidence, description, treatment } = prediction;

  const lang = i18n.language || 'en';
  
  // Handle case where backend returns object or string
  const diseaseName = typeof disease === 'object' ? (disease[lang] || disease['en']) : disease;
  const descText = typeof description === 'object' ? (description[lang] || description['en']) : description;
  const treatText = typeof treatment === 'object' ? (treatment[lang] || treatment['en']) : treatment;

  const handleShare = async () => {
    try {
      const message = `Plant Disease Detection Result:\n\nDisease: ${diseaseName}\nConfidence: ${confidence}%\n\nDescription: ${descText}\n\nTreatment: ${treatText}`;
      await Share.share({ message });
    } catch (error) {
      Alert.alert('Error', 'Failed to share result');
    }
  };

  const isHealthy = typeof disease === 'object' 
    ? (disease['en'] && disease['en'].toLowerCase().includes('healthy'))
    : (typeof disease === 'string' && (disease.toLowerCase().includes('healthy') || disease.toLowerCase().includes('sain')));

  const getStatusColor = () => {
    if (isHealthy) return currentTheme.success;
    return currentTheme.error;
  };

  const statusColor = getStatusColor();
  const diseaseIcon = isHealthy ? 'check-circle' : 'warning';
  
  const styles = getStyles(currentTheme, isDarkMode);

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.card}>
        {/* Header Section */}
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <View style={[styles.iconContainer, { backgroundColor: statusColor + '20' }]}>
              <MaterialIcons name={diseaseIcon} size={36} color={statusColor} />
            </View>
            <View style={styles.headerText}>
              <Text style={styles.diseaseName}>{diseaseName}</Text>
              <View style={styles.confidenceContainer}>
                <View style={styles.progressBarBackground}>
                  <View style={[styles.progressBarFill, { width: `${confidence}%`, backgroundColor: statusColor }]} />
                </View>
                <Text style={[styles.confidenceValue, { color: statusColor }]}>
                  {confidence}%
                </Text>
              </View>
            </View>
          </View>
          
          <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
            <MaterialIcons name="ios-share" size={22} color={currentTheme.primary} />
          </TouchableOpacity>
        </View>

        <View style={styles.divider} />

        {/* Description Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <View style={[styles.sectionIconBg, { backgroundColor: currentTheme.secondary + '15' }]}>
              <MaterialIcons name="info-outline" size={20} color={currentTheme.secondary} />
            </View>
            <Text style={styles.sectionTitle}>{t('result.description')}</Text>
          </View>
          <Text style={styles.sectionText}>{descText}</Text>
        </View>

        {/* Treatment Section (Only show if not healthy) */}
        {!isHealthy && (
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <View style={[styles.sectionIconBg, { backgroundColor: currentTheme.error + '15' }]}>
                <MaterialIcons name="medical-services" size={20} color={currentTheme.error} />
              </View>
              <Text style={styles.sectionTitle}>{t('result.treatment')}</Text>
            </View>
            <Text style={styles.sectionText}>{treatText}</Text>
          </View>
        )}

      </View>
    </ScrollView>
  );
};

const getStyles = (currentTheme, isDarkMode) => StyleSheet.create({
  container: {
    width: '100%',
    marginBottom: 24,
  },
  card: {
    backgroundColor: currentTheme.cardBackground,
    borderRadius: theme.SIZES.radiusLg,
    padding: 24,
    ...theme.SHADOWS[isDarkMode ? 'dark' : 'medium'],
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerText: {
    marginLeft: 16,
    flex: 1,
  },
  diseaseName: {
    ...theme.FONTS.h2,
    color: currentTheme.text,
    marginBottom: 8,
    textTransform: 'capitalize',
  },
  confidenceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressBarBackground: {
    flex: 1,
    height: 6,
    backgroundColor: currentTheme.border,
    borderRadius: 3,
    marginRight: 12,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 3,
  },
  confidenceValue: {
    ...theme.FONTS.h4,
  },
  shareButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: currentTheme.primary + '15',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 12,
  },
  divider: {
    height: 1,
    backgroundColor: currentTheme.border,
    marginBottom: 24,
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionIconBg: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  sectionTitle: {
    ...theme.FONTS.h3,
    color: currentTheme.text,
  },
  sectionText: {
    ...theme.FONTS.body2,
    color: currentTheme.textSecondary,
    lineHeight: 24,
  },
});

export default ResultCard;

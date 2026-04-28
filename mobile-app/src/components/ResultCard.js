/**
 * Result Card Component
 * Displays the prediction results in a modern card layout
 */

import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useTranslation } from 'react-i18next';

const ResultCard = ({ prediction }) => {
  const { t } = useTranslation();
  const { disease, confidence, description, treatment } = prediction;

  // Determine confidence color
  const getConfidenceColor = (conf) => {
    if (conf >= 80) return '#4CAF50'; // Green
    if (conf >= 60) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  // Get disease icon based on result
  const getDiseaseIcon = (diseaseName) => {
    if (diseaseName.toLowerCase().includes('healthy')) {
      return 'check-circle';
    }
    return 'warning';
  };

  const confidenceColor = getConfidenceColor(confidence);
  const diseaseIcon = getDiseaseIcon(disease);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.card}>
        {/* Disease Name */}
        <View style={styles.header}>
          <MaterialIcons 
            name={diseaseIcon} 
            size={32} 
            color={confidenceColor} 
          />
          <View style={styles.headerText}>
            <Text style={styles.diseaseName}>{disease}</Text>
            <View style={styles.confidenceContainer}>
              <Text style={styles.confidenceLabel}>{t('result.confidence')}:</Text>
              <Text 
                style={[styles.confidenceValue, { color: confidenceColor }]}
              >
                {confidence}%
              </Text>
            </View>
          </View>
        </View>

        {/* Description */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <MaterialIcons name="info" size={20} color="#2196F3" />
            <Text style={styles.sectionTitle}>{t('result.description')}</Text>
          </View>
          <Text style={styles.sectionText}>{description}</Text>
        </View>

        {/* Treatment */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <MaterialIcons name="medical-services" size={20} color="#4CAF50" />
            <Text style={styles.sectionTitle}>{t('result.treatment')}</Text>
          </View>
          <Text style={styles.sectionText}>{treatment}</Text>
        </View>

        {/* Disclaimer */}
        <View style={styles.disclaimer}>
          <MaterialIcons name="info-outline" size={16} color="#757575" />
          <Text style={styles.disclaimerText}>
            {t('result.disclaimer')}
          </Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 24,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
    paddingBottom: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E8E8E8',
  },
  headerText: {
    flex: 1,
    marginLeft: 16,
  },
  diseaseName: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 10,
    textTransform: 'capitalize',
  },
  confidenceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  confidenceLabel: {
    fontSize: 14,
    color: '#757575',
    marginRight: 8,
  },
  confidenceValue: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#212121',
    marginLeft: 10,
  },
  sectionText: {
    fontSize: 15,
    color: '#424242',
    lineHeight: 24,
    paddingLeft: 34,
  },
  disclaimer: {
    flexDirection: 'row',
    backgroundColor: '#FFF8E1',
    padding: 16,
    borderRadius: 12,
    marginTop: 12,
    borderWidth: 1,
    borderColor: '#FFE082',
  },
  disclaimerText: {
    flex: 1,
    fontSize: 13,
    color: '#757575',
    marginLeft: 10,
    lineHeight: 18,
  },
});

export default ResultCard;

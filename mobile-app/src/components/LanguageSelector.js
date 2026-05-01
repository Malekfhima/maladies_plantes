/**
 * Language Selector Component
 * Allows users to switch between English, French, and German
 */

import React, { useRef, useEffect } from 'react';
import { View, StyleSheet, TouchableOpacity, Text, Animated } from 'react-native';
import { useTranslation } from 'react-i18next';
import { changeLanguage } from '../i18n/i18n';
import theme from '../constants/theme';

const LanguageSelector = ({ isDarkMode, currentTheme }) => {
  const { t, i18n } = useTranslation();

  const languages = [
    { code: 'en', name: 'EN' },
    { code: 'fr', name: 'FR' },
    { code: 'de', name: 'DE' },
  ];

  const handleLanguageChange = async (langCode) => {
    await changeLanguage(langCode);
  };

  const styles = getStyles(currentTheme, isDarkMode);

  return (
    <View style={styles.container}>
      <View style={styles.segmentControl}>
        {languages.map((lang, index) => {
          const isActive = i18n.language === lang.code;
          return (
            <TouchableOpacity
              key={lang.code}
              style={[
                styles.segmentButton,
                isActive && styles.activeButton,
              ]}
              onPress={() => handleLanguageChange(lang.code)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.languageText,
                  isActive && styles.activeText,
                ]}
              >
                {lang.name}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

const getStyles = (currentTheme, isDarkMode) => StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  segmentControl: {
    flexDirection: 'row',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 24,
    padding: 4,
  },
  segmentButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  activeButton: {
    backgroundColor: '#FFFFFF',
    ...theme.SHADOWS.light,
  },
  languageText: {
    ...theme.FONTS.body3,
    fontWeight: '600',
    color: 'rgba(255, 255, 255, 0.8)',
  },
  activeText: {
    color: theme.COLORS.light.primary,
    fontWeight: 'bold',
  },
});

export default LanguageSelector;

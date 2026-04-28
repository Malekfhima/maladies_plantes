/**
 * i18n Configuration
 * Internationalization setup for English, French, and German
 */

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import AsyncStorage from '@react-native-async-storage/async-storage';

import en from './locales/en.json';
import fr from './locales/fr.json';
import de from './locales/de.json';

const LANGUAGE_KEY = '@plant_disease_app_language';

const resources = {
  en: { translation: en },
  fr: { translation: fr },
  de: { translation: de },
};

const initI18n = async () => {
  // Get saved language or use device language
  const savedLanguage = await AsyncStorage.getItem(LANGUAGE_KEY);
  
  await i18n.use(initReactI18next).init({
    resources,
    lng: savedLanguage || 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });
};

initI18n();

// Function to change language
export const changeLanguage = async (language) => {
  await i18n.changeLanguage(language);
  await AsyncStorage.setItem(LANGUAGE_KEY, language);
};

// Function to get current language
export const getCurrentLanguage = () => i18n.language;

export default i18n;

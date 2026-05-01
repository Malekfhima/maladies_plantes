export const COLORS = {
  // Light Mode Colors
  light: {
    background: '#F8F9FA',
    surface: '#FFFFFF',
    primary: '#10B981', // Emerald green
    primaryDark: '#059669',
    secondary: '#3B82F6', // Blue
    text: '#1F2937', // Gray 800
    textSecondary: '#6B7280', // Gray 500
    textMuted: '#9CA3AF', // Gray 400
    border: '#E5E7EB', // Gray 200
    error: '#EF4444', // Red 500
    errorBackground: '#FEF2F2',
    success: '#22C55E', // Green 500
    warning: '#F59E0B', // Amber 500
    iconPrimary: '#10B981',
    iconSecondary: '#3B82F6',
    cardBackground: '#FFFFFF',
  },
  // Dark Mode Colors
  dark: {
    background: '#0F172A', // Slate 900
    surface: '#1E293B', // Slate 800
    primary: '#10B981', // Emerald green
    primaryDark: '#059669',
    secondary: '#3B82F6', // Blue
    text: '#F9FAFB', // Gray 50
    textSecondary: '#D1D5DB', // Gray 300
    textMuted: '#9CA3AF', // Gray 400
    border: '#334155', // Slate 700
    error: '#F87171', // Red 400
    errorBackground: '#451A1A',
    success: '#4ADE80', // Green 400
    warning: '#FBBF24', // Amber 400
    iconPrimary: '#34D399',
    iconSecondary: '#60A5FA',
    cardBackground: '#1E293B',
  }
};

export const SIZES = {
  // Global sizes
  base: 8,
  font: 14,
  radius: 16,
  radiusLg: 24,
  padding: 24,

  // Font sizes
  h1: 32,
  h2: 26,
  h3: 20,
  h4: 18,
  body1: 16,
  body2: 15,
  body3: 14,
  body4: 13,
};

export const FONTS = {
  h1: { fontSize: SIZES.h1, fontWeight: '700' },
  h2: { fontSize: SIZES.h2, fontWeight: '700' },
  h3: { fontSize: SIZES.h3, fontWeight: '600' },
  h4: { fontSize: SIZES.h4, fontWeight: '600' },
  body1: { fontSize: SIZES.body1, fontWeight: '400' },
  body2: { fontSize: SIZES.body2, fontWeight: '400' },
  body3: { fontSize: SIZES.body3, fontWeight: '400' },
  body4: { fontSize: SIZES.body4, fontWeight: '400' },
};

export const SHADOWS = {
  light: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 4,
  },
  medium: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.12,
    shadowRadius: 16,
    elevation: 8,
  },
  dark: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  }
};

export default { COLORS, SIZES, FONTS, SHADOWS };

import { StyleSheet, Text, View, Pressable } from 'react-native';

import { useTranslation } from '../hooks/useTranslation';
import { colors, radii, spacing } from '../theme/tokens';

export const LanguageToggle = () => {
  const { language, setLanguage } = useTranslation();

  return (
    <View style={styles.container}>
      {(['en', 'np'] as const).map((lang, index) => (
        <Pressable
          key={lang}
          style={[styles.button, language === lang && styles.buttonActive, index === 0 && styles.left, index === 1 && styles.right]}
          onPress={() => setLanguage(lang)}
        >
          <Text style={[styles.label, language === lang && styles.labelActive]}>{lang === 'en' ? 'EN' : 'नेपाली'}</Text>
        </Pressable>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    borderRadius: radii.pill,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
    backgroundColor: colors.surface,
  },
  button: {
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.lg,
  },
  buttonActive: {
    backgroundColor: colors.accent,
  },
  left: {
    borderTopLeftRadius: radii.pill,
    borderBottomLeftRadius: radii.pill,
  },
  right: {
    borderTopRightRadius: radii.pill,
    borderBottomRightRadius: radii.pill,
  },
  label: {
    fontWeight: '600',
    color: colors.mutedText,
  },
  labelActive: {
    color: '#fff',
  },
});

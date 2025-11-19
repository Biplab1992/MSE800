import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import { TranslationStrings } from '../i18n/translations';
import { Meal, MealType } from '../types/meals';
import { colors, radii, spacing } from '../theme/tokens';

export type MealCardProps = {
  mealType: MealType;
  meal?: Meal;
  isActive?: boolean;
  onAdd: (mealType: MealType) => void;
  onEdit: (meal: Meal) => void;
  t: TranslationStrings;
};

export const MealCard = ({ mealType, meal, isActive = false, onAdd, onEdit, t }: MealCardProps) => {
  return (
    <View style={[styles.card, isActive && styles.cardActive]}>
      <View style={styles.headerRow}>
        <Text style={styles.typeLabel}>{t.mealTypeLabel[mealType]}</Text>
      </View>
      {meal ? (
        <>
          <Text style={styles.title}>{meal.title}</Text>
          {meal.imageUrl ? <Image source={{ uri: meal.imageUrl }} style={styles.image} /> : null}
          {meal.description ? <Text style={styles.description}>{meal.description}</Text> : null}
          {meal.createdBy ? (
            <Text style={styles.meta}>
              {t.addedByPrefix}: <Text style={styles.metaStrong}>{meal.createdBy}</Text>
            </Text>
          ) : null}
          <View style={styles.actions}>
            <TouchableOpacity style={styles.secondaryButton} onPress={() => onEdit(meal)}>
              <Text style={styles.secondaryLabel}>{t.editMeal}</Text>
            </TouchableOpacity>
          </View>
        </>
      ) : (
        <>
          <Text style={styles.empty}>{t.noMeal}</Text>
          <TouchableOpacity style={styles.primaryButton} onPress={() => onAdd(mealType)}>
            <Text style={styles.primaryLabel}>{t.addMeal}</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    backgroundColor: '#f8fafc',
    padding: spacing.md,
    flex: 1,
  },
  cardActive: {
    borderColor: colors.accent,
    backgroundColor: colors.accentMuted,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  typeLabel: {
    textTransform: 'uppercase',
    letterSpacing: 1,
    fontSize: 12,
    color: colors.mutedText,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    marginBottom: spacing.xs,
  },
  image: {
    height: 120,
    borderRadius: radii.md,
    marginBottom: spacing.sm,
  },
  description: {
    color: colors.mutedText,
    marginBottom: spacing.sm,
  },
  meta: {
    color: colors.mutedText,
    marginBottom: spacing.sm,
  },
  metaStrong: {
    fontWeight: '600',
    color: colors.text,
  },
  actions: {
    marginTop: 'auto',
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  primaryButton: {
    backgroundColor: colors.accent,
    paddingVertical: spacing.sm,
    borderRadius: radii.md,
    marginTop: 'auto',
    alignItems: 'center',
  },
  primaryLabel: {
    color: '#fff',
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: colors.border,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    borderRadius: radii.md,
  },
  secondaryLabel: {
    fontWeight: '600',
    color: colors.text,
  },
  empty: {
    color: colors.mutedText,
    marginBottom: spacing.md,
  },
});
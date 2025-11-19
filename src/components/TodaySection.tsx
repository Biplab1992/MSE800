import { StyleSheet, Text, View } from 'react-native';

import { TranslationStrings } from '../i18n/translations';
import { Meal, MealType } from '../types/meals';
import { colors, radii, spacing } from '../theme/tokens';
import { MealCard } from './MealCard';

export type TodaySectionProps = {
  dateLabel: string;
  mealsByType: Record<MealType, Meal | undefined>;
  focusMeal: MealType;
  onAddMeal: (mealType: MealType) => void;
  onEditMeal: (meal: Meal) => void;
  t: TranslationStrings;
};

export const TodaySection = ({ dateLabel, mealsByType, focusMeal, onAddMeal, onEditMeal, t }: TodaySectionProps) => {
  const mealTypes: MealType[] = ['breakfast', 'lunch', 'dinner'];
  return (
    <View style={styles.panel}>
      <View style={styles.headerRow}>
        <View>
          <Text style={styles.eyebrow}>{t.todayDatePrefix}</Text>
          <Text style={styles.heading}>{dateLabel}</Text>
        </View>
      </View>
      <View style={styles.grid}>
        {mealTypes.map((mealType) => (
          <MealCard
            key={mealType}
            mealType={mealType}
            meal={mealsByType[mealType]}
            isActive={mealType === focusMeal}
            onAdd={onAddMeal}
            onEdit={onEditMeal}
            t={t}
          />
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  panel: {
    backgroundColor: colors.surface,
    borderRadius: radii.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  eyebrow: {
    textTransform: 'uppercase',
    fontSize: 12,
    color: colors.mutedText,
    letterSpacing: 1,
  },
  heading: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.text,
  },
  grid: {
    gap: spacing.md,
  },
});

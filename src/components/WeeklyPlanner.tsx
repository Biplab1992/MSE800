import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import { TranslationStrings } from '../i18n/translations';
import { Meal, MealType } from '../types/meals';
import { colors, radii, spacing } from '../theme/tokens';

export type WeeklyPlannerProps = {
  weekDates: string[];
  meals: Meal[];
  onSlotSelect: (payload: { date: string; mealType: MealType; meal?: Meal }) => void;
  t: TranslationStrings;
};

export const WeeklyPlanner = ({ weekDates, meals, onSlotSelect, t }: WeeklyPlannerProps) => {
  const lookup = weekDates.reduce<Record<string, Record<MealType, Meal | undefined>>>(
    (acc, date) => ({ ...acc, [date]: { breakfast: undefined, lunch: undefined, dinner: undefined } }),
    {}
  );
  meals.forEach((meal) => {
    if (!lookup[meal.date]) {
      lookup[meal.date] = { breakfast: undefined, lunch: undefined, dinner: undefined };
    }
    lookup[meal.date][meal.mealType] = meal;
  });

  const dayFormatter = new Intl.DateTimeFormat('en-US', { weekday: 'long' });
  const mealTypes: MealType[] = ['breakfast', 'lunch', 'dinner'];

  return (
    <View style={styles.panel}>
      <View style={styles.headerRow}>
        <View>
          <Text style={styles.eyebrow}>{t.thisWeek}</Text>
          <Text style={styles.heading}>{t.weeklyPlan}</Text>
        </View>
        <Text style={styles.helper}>{t.weeklyLeadCopy}</Text>
      </View>
      <View style={styles.weekGrid}>
        {weekDates.map((date) => {
          const dayMeals = lookup[date];
          const weekday = dayFormatter.format(new Date(date));
          return (
            <View style={styles.weekCard} key={date}>
              <View style={styles.weekCardHeader}>
                <Text style={styles.weekday}>{weekday}</Text>
                <Text style={styles.dateLabel}>{date}</Text>
              </View>
              <View style={styles.slotList}>
                {mealTypes.map((mealType) => {
                  const slotMeal = dayMeals?.[mealType];
                  return (
                    <TouchableOpacity
                      key={`${date}-${mealType}`}
                      style={[styles.slot, slotMeal && styles.slotFilled]}
                      onPress={() => onSlotSelect({ date, mealType, meal: slotMeal })}
                    >
                      <Text style={styles.slotLabel}>{t.mealTypeLabel[mealType]}</Text>
                      {slotMeal ? (
                        <Text style={styles.slotTitle}>{slotMeal.title}</Text>
                      ) : (
                        <Text style={styles.slotEmpty}>{t.addMeal}</Text>
                      )}
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>
          );
        })}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  panel: {
    backgroundColor: colors.surface,
    borderRadius: radii.lg,
    padding: spacing.lg,
  },
  headerRow: {
    marginBottom: spacing.lg,
    gap: spacing.sm,
  },
  eyebrow: {
    textTransform: 'uppercase',
    fontSize: 12,
    color: colors.mutedText,
    letterSpacing: 1,
  },
  heading: {
    fontSize: 22,
    fontWeight: '700',
    color: colors.text,
  },
  helper: {
    color: colors.mutedText,
  },
  weekGrid: {
    gap: spacing.md,
  },
  weekCard: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.sm,
    backgroundColor: '#f8fafc',
  },
  weekCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  weekday: {
    fontWeight: '600',
    color: colors.text,
  },
  dateLabel: {
    color: colors.mutedText,
  },
  slotList: {
    gap: spacing.sm,
  },
  slot: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    padding: spacing.sm,
  },
  slotFilled: {
    borderColor: colors.accent,
  },
  slotLabel: {
    fontSize: 12,
    textTransform: 'uppercase',
    color: colors.mutedText,
  },
  slotTitle: {
    marginTop: 2,
    fontWeight: '600',
    color: colors.text,
  },
  slotEmpty: {
    marginTop: 2,
    color: colors.accent,
  },
});

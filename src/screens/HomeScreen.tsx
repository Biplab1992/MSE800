import { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { formatDisplayDate } from '../utils/nepaliDate';
import { AlertBar } from '../components/AlertBar';
import { LanguageToggle } from '../components/LanguageToggle';
import { MealFormModal } from '../components/MealFormModal';
import { TodaySection } from '../components/TodaySection';
import { WeeklyPlanner } from '../components/WeeklyPlanner';
import { useTranslation } from '../hooks/useTranslation';
import { createMeal, deleteMeal, fetchTodayMeals, fetchWeekMeals, updateMeal } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Meal, MealFormData, MealType } from '../types/meals';
import { colors, radii, spacing } from '../theme/tokens';

const getFocusMeal = (): MealType => {
  const hour = new Date().getHours();
  if (hour < 11) return 'breakfast';
  if (hour < 17) return 'lunch';
  return 'dinner';
};

const defaultFormValues: MealFormData = {
  date: new Date().toISOString().split('T')[0],
  mealType: 'breakfast',
  title: '',
  description: '',
  imageUrl: '',
  createdBy: '',
};

export const HomeScreen = () => {
  const { t, language } = useTranslation();
  const { user, logout } = useAuth();
  const [view, setView] = useState<'today' | 'week'>('today');
  const [todayMeals, setTodayMeals] = useState<Meal[]>([]);
  const [weekMeals, setWeekMeals] = useState<Meal[]>([]);
  const [weekDates, setWeekDates] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formVisible, setFormVisible] = useState(false);
  const [formMode, setFormMode] = useState<'add' | 'edit'>('add');
  const [formValues, setFormValues] = useState<MealFormData>(defaultFormValues);
  const [editingMealId, setEditingMealId] = useState<string | null>(null);
  const [focusMeal, setFocusMeal] = useState<MealType>(getFocusMeal());

  const loadData = async () => {
    if (!user?.home) return;
    try {
      setLoading(true);
      const [today, week] = await Promise.all([fetchTodayMeals(), fetchWeekMeals()]);
      setTodayMeals(today);
      setWeekDates(week.weekDates);
      setWeekMeals(week.meals);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user?.home?._id]);

  useEffect(() => {
    const timer = setInterval(() => setFocusMeal(getFocusMeal()), 60 * 1000);
    return () => clearInterval(timer);
  }, []);

  const mealsByType = useMemo(() => {
    return todayMeals.reduce<Record<MealType, Meal | undefined>>(
      (acc, meal) => ({ ...acc, [meal.mealType]: meal }),
      { breakfast: undefined, lunch: undefined, dinner: undefined }
    );
  }, [todayMeals]);

  const openAddForm = (mealType: MealType, date?: string) => {
    setFormMode('add');
    setEditingMealId(null);
    setFormValues({ ...defaultFormValues, mealType, date: date ?? defaultFormValues.date });
    setFormVisible(true);
  };

  const openEditForm = (meal: Meal) => {
    setFormMode('edit');
    setEditingMealId(meal._id);
    setFormValues({
      date: meal.date,
      mealType: meal.mealType,
      title: meal.title,
      description: meal.description ?? '',
      imageUrl: meal.imageUrl ?? '',
      createdBy: meal.createdBy ?? '',
    });
    setFormVisible(true);
  };

  const closeForm = () => {
    setFormVisible(false);
    setError(null);
  };

  const handleSubmit = async (values: MealFormData) => {
    try {
      setSaving(true);
      if (formMode === 'edit' && editingMealId) {
        await updateMeal(editingMealId, values);
      } else {
        await createMeal(values);
      }
      closeForm();
      await loadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!editingMealId) return;
    try {
      setSaving(true);
      await deleteMeal(editingMealId);
      closeForm();
      await loadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  const handleSlotSelect = ({ date, mealType, meal }: { date: string; mealType: MealType; meal?: Meal }) => {
    if (meal) {
      openEditForm(meal);
    } else {
      openAddForm(mealType, date);
    }
  };

  const todayLabel = useMemo(() => formatDisplayDate(new Date(), language), [language]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.toggleRow}>
          <LanguageToggle />
        </View>
        <View style={styles.headerRow}>
          <View>
            <Text style={styles.title}>{t.headingToday}</Text>
            {user?.home ? (
              <Text style={styles.eyebrow}>
                {user.home.name} � {t.homeSetup.codeLabel}: {user.home.code}
              </Text>
            ) : null}
          </View>
        </View>
        <View style={styles.viewSwitch}>
          {(
            [
              { key: 'today', label: t.today },
              { key: 'week', label: t.thisWeek },
            ] as const
          ).map((tab) => (
            <TouchableOpacity
              key={tab.key}
              style={[styles.viewButton, view === tab.key && styles.viewButtonActive]}
              onPress={() => setView(tab.key)}
            >
              <Text style={[styles.viewButtonLabel, view === tab.key && styles.viewButtonLabelActive]}>{tab.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
        {error ? <AlertBar message={error} /> : null}
        {loading ? (
          <ActivityIndicator size="large" color={colors.accent} />
        ) : view === 'today' ? (
          <TodaySection
            dateLabel={todayLabel}
            mealsByType={mealsByType}
            focusMeal={focusMeal}
            onAddMeal={openAddForm}
            onEditMeal={openEditForm}
            t={t}
          />
        ) : (
          <WeeklyPlanner weekDates={weekDates} meals={weekMeals} onSlotSelect={handleSlotSelect} t={t} />
        )}
        <View style={{ height: spacing.lg }} />
      </ScrollView>
      <View style={styles.logoutBar}>
        <TouchableOpacity onPress={logout} style={styles.logoutButtonWide}>
          <Text style={styles.logoutLabel}>{t.logout}</Text>
        </TouchableOpacity>
      </View>
      <MealFormModal
        visible={formVisible}
        initialValues={formValues}
        mode={formMode}
        onSubmit={handleSubmit}
        onCancel={closeForm}
        onDelete={formMode === 'edit' ? handleDelete : undefined}
        isSubmitting={saving}
        t={t}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },
  container: {
    padding: spacing.lg,
    gap: spacing.md,
  },
  toggleRow: {
    alignItems: 'center',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: colors.text,
  },
  eyebrow: {
    textTransform: 'uppercase',
    fontSize: 12,
    color: colors.mutedText,
    letterSpacing: 1,
  },
  viewSwitch: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: radii.pill,
    padding: spacing.xs,
    gap: spacing.xs,
  },
  viewButton: {
    flex: 1,
    paddingVertical: spacing.sm,
    borderRadius: radii.pill,
    alignItems: 'center',
  },
  viewButtonActive: {
    backgroundColor: colors.accent,
  },
  viewButtonLabel: {
    fontWeight: '600',
    color: colors.mutedText,
  },
  viewButtonLabelActive: {
    color: '#fff',
  },
  logoutBar: {
    padding: spacing.md,
    borderTopWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
  },
  logoutButtonWide: {
    backgroundColor: colors.border,
    paddingVertical: spacing.sm,
    borderRadius: radii.md,
    alignItems: 'center',
  },
  logoutLabel: {
    fontWeight: '600',
    color: colors.text,
  },
});

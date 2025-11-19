import { useEffect, useState } from 'react';
import { Modal, StyleSheet, Text, TextInput, TouchableOpacity, View, ScrollView } from 'react-native';

import { TranslationStrings } from '../i18n/translations';
import { MealFormData, MealType } from '../types/meals';
import { colors, radii, spacing } from '../theme/tokens';

export type MealFormModalProps = {
  visible: boolean;
  mode: 'add' | 'edit';
  initialValues: MealFormData;
  onSubmit: (values: MealFormData) => void;
  onCancel: () => void;
  onDelete?: () => void;
  isSubmitting?: boolean;
  t: TranslationStrings;
};

const mealTypes: MealType[] = ['breakfast', 'lunch', 'dinner'];

export const MealFormModal = ({ visible, mode, initialValues, onSubmit, onCancel, onDelete, isSubmitting = false, t }: MealFormModalProps) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues, visible]);

  const validate = () => {
    const next: Record<string, string> = {};
    if (!values.mealType) next.mealType = t.formErrors.mealType;
    if (!values.date) next.date = t.formErrors.date;
    if (!values.title.trim()) next.title = t.formErrors.title;
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = () => {
    if (!validate()) return;
    onSubmit({ ...values, title: values.title.trim() });
  };

  const updateField = (field: keyof MealFormData, value: string) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View style={styles.backdrop}>
        <ScrollView contentContainerStyle={styles.form} style={styles.formWrapper}>
          <View style={styles.headerRow}>
            <Text style={styles.formTitle}>{mode === 'add' ? t.addMeal : t.editMeal}</Text>
            <TouchableOpacity onPress={onCancel} accessibilityLabel={t.cancel}>
              <Text style={styles.close}>×</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>{t.fieldLabels.mealType}</Text>
            <View style={styles.segmented}>
              {mealTypes.map((type) => (
                <TouchableOpacity
                  key={type}
                  style={[styles.segment, values.mealType === type && styles.segmentActive]}
                  onPress={() => updateField('mealType', type)}
                >
                  <Text style={[styles.segmentLabel, values.mealType === type && styles.segmentLabelActive]}>
                    {t.mealTypeLabel[type]}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
            {errors.mealType ? <Text style={styles.error}>{errors.mealType}</Text> : null}
          </View>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>{t.fieldLabels.date}</Text>
            <TextInput value={values.date} onChangeText={(text) => updateField('date', text)} placeholder="YYYY-MM-DD" style={styles.input} />
            {errors.date ? <Text style={styles.error}>{errors.date}</Text> : null}
          </View>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>{t.fieldLabels.title}</Text>
            <TextInput value={values.title} onChangeText={(text) => updateField('title', text)} placeholder="Veg Dal Bhat" style={styles.input} />
            {errors.title ? <Text style={styles.error}>{errors.title}</Text> : null}
          </View>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>{t.fieldLabels.description}</Text>
            <TextInput value={values.description ?? ''} onChangeText={(text) => updateField('description', text)} style={[styles.input, styles.multiline]} multiline numberOfLines={3} />
          </View>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>{t.fieldLabels.imageUrl}</Text>
            <TextInput value={values.imageUrl ?? ''} onChangeText={(text) => updateField('imageUrl', text)} placeholder="https://" style={styles.input} autoCapitalize="none" />
          </View>
          <View style={styles.actions}>
            {mode === 'edit' && onDelete ? (
              <TouchableOpacity style={[styles.button, styles.danger]} onPress={onDelete} disabled={isSubmitting}>
                <Text style={styles.buttonLabel}>{t.deleteMeal}</Text>
              </TouchableOpacity>
            ) : (
              <View />
            )}
            <View style={styles.actionRight}>
              <TouchableOpacity style={[styles.button, styles.secondary]} onPress={onCancel}>
                <Text style={[styles.buttonLabel, styles.secondaryLabel]}>{t.cancel}</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.button, styles.primary]} onPress={handleSubmit} disabled={isSubmitting}>
                <Text style={styles.buttonLabel}>{isSubmitting ? '…' : t.save}</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(15,23,42,0.5)',
    justifyContent: 'center',
    padding: spacing.lg,
  },
  formWrapper: {
    maxHeight: '90%',
    borderRadius: radii.lg,
  },
  form: {
    backgroundColor: colors.surface,
    borderRadius: radii.lg,
    padding: spacing.lg,
    gap: spacing.md,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  formTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: colors.text,
  },
  close: {
    fontSize: 28,
    color: colors.mutedText,
    fontWeight: '600',
  },
  fieldGroup: {
    gap: spacing.xs,
  },
  label: {
    fontWeight: '600',
    color: colors.text,
  },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    fontSize: 16,
  },
  multiline: {
    height: 100,
    textAlignVertical: 'top',
  },
  segmented: {
    flexDirection: 'row',
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.pill,
    overflow: 'hidden',
  },
  segment: {
    flex: 1,
    paddingVertical: spacing.sm,
    alignItems: 'center',
  },
  segmentActive: {
    backgroundColor: colors.accent,
  },
  segmentLabel: {
    fontWeight: '600',
    color: colors.mutedText,
  },
  segmentLabelActive: {
    color: '#fff',
  },
  error: {
    color: colors.danger,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: spacing.sm,
    flexWrap: 'wrap',
  },
  actionRight: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  button: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    borderRadius: radii.md,
  },
  primary: {
    backgroundColor: colors.accent,
  },
  secondary: {
    backgroundColor: colors.border,
  },
  secondaryLabel: {
    color: colors.text,
  },
  danger: {
    backgroundColor: colors.danger,
  },
  buttonLabel: {
    color: '#fff',
    fontWeight: '600',
  },
});

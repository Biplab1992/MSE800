import { useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

import { useAuth } from '../context/AuthContext';
import { useTranslation } from '../hooks/useTranslation';
import { colors, radii, spacing } from '../theme/tokens';
import { LanguageToggle } from '../components/LanguageToggle';

export const AuthScreen = () => {
  const { login, register } = useAuth();
  const { t } = useTranslation();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      if (mode === 'register') {
        await register({ name: form.name.trim(), email: form.email.trim(), password: form.password });
      } else {
        await login({ email: form.email.trim(), password: form.password });
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.wrapper}>
      <View style={styles.toggleRow}>
        <LanguageToggle />
      </View>
      <Text style={styles.title}>{t.auth.welcome}</Text>
      {mode === 'register' && (
        <TextInput
          style={styles.input}
          placeholder={t.auth.name}
          value={form.name}
          onChangeText={(text) => setForm((prev) => ({ ...prev, name: text }))}
        />
      )}
      <TextInput
        style={styles.input}
        placeholder={t.auth.email}
        keyboardType="email-address"
        autoCapitalize="none"
        value={form.email}
        onChangeText={(text) => setForm((prev) => ({ ...prev, email: text }))}
      />
      <TextInput
        style={styles.input}
        placeholder={t.auth.password}
        secureTextEntry
        value={form.password}
        onChangeText={(text) => setForm((prev) => ({ ...prev, password: text }))}
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <TouchableOpacity style={styles.primaryButton} onPress={handleSubmit} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.primaryLabel}>{mode === 'register' ? t.auth.register : t.auth.login}</Text>}
      </TouchableOpacity>
      <TouchableOpacity style={styles.linkButton} onPress={() => setMode(mode === 'login' ? 'register' : 'login')}>
        <Text style={styles.linkText}>{mode === 'login' ? t.auth.switchToRegister : t.auth.switchToLogin}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    justifyContent: 'center',
    padding: spacing.lg,
    gap: spacing.sm,
    backgroundColor: colors.background,
  },
  toggleRow: {
    alignItems: 'flex-end',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: spacing.sm,
    color: colors.text,
  },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    padding: spacing.md,
    backgroundColor: '#fff',
  },
  primaryButton: {
    backgroundColor: colors.accent,
    padding: spacing.md,
    borderRadius: radii.md,
    alignItems: 'center',
  },
  primaryLabel: {
    color: '#fff',
    fontWeight: '600',
  },
  linkButton: {
    alignItems: 'center',
  },
  linkText: {
    color: colors.accent,
    fontWeight: '600',
  },
  error: {
    color: colors.danger,
  },
});

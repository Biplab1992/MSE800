import { useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

import { useAuth } from '../context/AuthContext';
import { useTranslation } from '../hooks/useTranslation';
import { colors, radii, spacing } from '../theme/tokens';

export const HomeSetupScreen = () => {
  const { createHome, joinHome, user } = useAuth();
  const { t } = useTranslation();
  const [homeName, setHomeName] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCreate = async () => {
    setLoading(true);
    setError(null);
    try {
      const home = await createHome({ name: homeName.trim() });
      setMessage(`${t.homeSetup.codeLabel}: ${home.code}`);
      setHomeName('');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async () => {
    setLoading(true);
    setError(null);
    try {
      const home = await joinHome({ code: code.trim() });
      setMessage(`${t.homeSetup.codeLabel}: ${home.code}`);
      setCode('');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.wrapper}>
      <Text style={styles.heading}>{t.homeSetup.heading}</Text>
      {user?.home && <Text style={styles.helper}>{user.home.name}</Text>}
      {message ? <Text style={styles.success}>{message}</Text> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>{t.homeSetup.createTitle}</Text>
        <TextInput placeholder={t.homeSetup.homeNamePlaceholder} style={styles.input} value={homeName} onChangeText={setHomeName} />
        <TouchableOpacity style={styles.primaryButton} onPress={handleCreate} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.primaryLabel}>{t.homeSetup.createButton}</Text>}
        </TouchableOpacity>
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>{t.homeSetup.joinTitle}</Text>
        <Text style={styles.helper}>{t.homeSetup.joinDescription}</Text>
        <TextInput placeholder={t.homeSetup.codePlaceholder} style={styles.input} value={code} onChangeText={(text) => setCode(text.toUpperCase())} />
        <TouchableOpacity style={styles.secondaryButton} onPress={handleJoin} disabled={loading}>
          {loading ? <ActivityIndicator /> : <Text style={styles.secondaryLabel}>{t.homeSetup.joinButton}</Text>}
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    padding: spacing.lg,
    gap: spacing.md,
    backgroundColor: colors.background,
  },
  heading: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.text,
  },
  card: {
    backgroundColor: '#fff',
    padding: spacing.lg,
    borderRadius: radii.lg,
    gap: spacing.sm,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowOffset: { width: 0, height: 10 },
    shadowRadius: 20,
    elevation: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.md,
    padding: spacing.md,
  },
  helper: {
    color: colors.mutedText,
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
  secondaryButton: {
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    alignItems: 'center',
  },
  secondaryLabel: {
    fontWeight: '600',
    color: colors.text,
  },
  success: {
    color: '#15803d',
  },
  error: {
    color: colors.danger,
  },
});

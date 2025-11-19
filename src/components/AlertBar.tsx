import { StyleSheet, Text, View } from 'react-native';

import { colors, radii, spacing } from '../theme/tokens';

export const AlertBar = ({ message }: { message: string }) => (
  <View style={styles.container}>
    <Text style={styles.label}>{message}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fee2e2',
    borderRadius: radii.md,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  label: {
    color: colors.danger,
    fontWeight: '600',
  },
});

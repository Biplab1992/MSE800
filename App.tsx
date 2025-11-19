import { StatusBar } from 'expo-status-bar';
import { ActivityIndicator, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AuthProvider, useAuth } from './src/context/AuthContext';
import { LanguageProvider } from './src/context/LanguageContext';
import { AuthScreen } from './src/screens/AuthScreen';
import { HomeSetupScreen } from './src/screens/HomeSetupScreen';
import { HomeScreen } from './src/screens/HomeScreen';
import { colors } from './src/theme/tokens';

const RootContent = () => {
  const { user, token, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background }}>
        <ActivityIndicator size="large" color={colors.accent} />
      </View>
    );
  }

  if (!token || !user) {
    return <AuthScreen />;
  }

  if (!user.home) {
    return <HomeSetupScreen />;
  }

  return <HomeScreen />;
};

export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <LanguageProvider>
          <StatusBar style="dark" />
          <RootContent />
        </LanguageProvider>
      </AuthProvider>
    </SafeAreaProvider>
  );
}

import AsyncStorage from '@react-native-async-storage/async-storage';
import { ReactNode, createContext, useContext, useEffect, useState } from 'react';

import { createHome, fetchCurrentUser, joinHome, loginUser, registerUser, setAuthToken } from '../services/api';
import { AuthUser, HomeInfo } from '../types/auth';

const TOKEN_KEY = 'wct-token';

const persistToken = async (token: string | null) => {
  if (token) {
    await AsyncStorage.setItem(TOKEN_KEY, token);
  } else {
    await AsyncStorage.removeItem(TOKEN_KEY);
  }
};

type AuthContextValue = {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  register: (payload: { name: string; email: string; password: string }) => Promise<void>;
  login: (payload: { email: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  createHome: (payload: { name: string }) => Promise<HomeInfo>;
  joinHome: (payload: { code: string }) => Promise<HomeInfo>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem(TOKEN_KEY)
      .then((stored) => {
        if (stored) {
          setToken(stored);
          setAuthToken(stored);
          return fetchCurrentUser().then((res) => setUser(res.user));
        }
        return undefined;
      })
      .catch(() => undefined)
      .finally(() => setLoading(false));
  }, []);

  const handleAuthSuccess = async (tokenValue: string, nextUser: AuthUser) => {
    await persistToken(tokenValue);
    setAuthToken(tokenValue);
    setToken(tokenValue);
    setUser(nextUser);
  };

  const registerAction = async (payload: { name: string; email: string; password: string }) => {
    const response = await registerUser(payload);
    await handleAuthSuccess(response.token, response.user);
  };

  const loginAction = async (payload: { email: string; password: string }) => {
    const response = await loginUser(payload);
    await handleAuthSuccess(response.token, response.user);
  };

  const logoutAction = async () => {
    await persistToken(null);
    setAuthToken(null);
    setToken(null);
    setUser(null);
  };

  const createHomeAction = async (payload: { name: string }) => {
    const { home } = await createHome(payload);
    setUser((prev) => (prev ? { ...prev, home } : prev));
    return home;
  };

  const joinHomeAction = async (payload: { code: string }) => {
    const { home } = await joinHome(payload);
    setUser((prev) => (prev ? { ...prev, home } : prev));
    return home;
  };

  return (
    <AuthContext.Provider
      value={{ user, token, loading, register: registerAction, login: loginAction, logout: logoutAction, createHome: createHomeAction, joinHome: joinHomeAction }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
};

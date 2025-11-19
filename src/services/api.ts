import Constants from 'expo-constants';

import { AuthResponse, AuthUser, HomeInfo } from '../types/auth';
import { Meal, MealFormData, WeekMealsResponse } from '../types/meals';

const defaultHost = Constants.expoGoConfig?.debuggerHost?.split(':')?.[0];
const defaultApiUrl = defaultHost ? `http://${defaultHost}:4000` : 'http://localhost:4000';

const API_URL =
  (Constants.expoConfig?.extra as { apiUrl?: string } | undefined)?.apiUrl ||
  process.env.EXPO_PUBLIC_API_URL ||
  defaultApiUrl;

let authToken: string | null = null;

export const setAuthToken = (token: string | null) => {
  authToken = token;
};

const request = async <T>(path: string, options?: RequestInit): Promise<T> => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string> | undefined),
  };
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = 'Request failed';
    try {
      const body = await response.json();
      message = body.error || body.errors?.join(', ') || message;
    } catch (err) {
      // ignore parse errors
    }
    throw new Error(message);
  }

  return response.json();
};

export const fetchTodayMeals = () => request<Meal[]>('/meals/today');
export const fetchWeekMeals = () => request<WeekMealsResponse>('/meals/week');
export const createMeal = (payload: MealFormData) =>
  request<Meal>('/meals', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
export const updateMeal = (id: string, payload: MealFormData) =>
  request<Meal>(`/meals/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
export const deleteMeal = (id: string) =>
  request<{ message: string }>(`/meals/${id}`, {
    method: 'DELETE',
  });

export const registerUser = (payload: { name: string; email: string; password: string }) =>
  request<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

export const loginUser = (payload: { email: string; password: string }) =>
  request<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

export const fetchCurrentUser = () => request<{ user: AuthUser }>('/auth/me');

export const createHome = (payload: { name: string }) =>
  request<{ home: HomeInfo }>('/homes', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

export const joinHome = (payload: { code: string }) =>
  request<{ home: HomeInfo }>('/homes/join', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

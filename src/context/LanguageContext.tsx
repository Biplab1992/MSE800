import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

import { Language, translations, TranslationStrings } from '../i18n/translations';

export type LanguageContextValue = {
  language: Language;
  strings: TranslationStrings;
  setLanguage: (lang: Language) => void;
  toggleLanguage: () => void;
};

const defaultLanguage: Language = 'en';

const LanguageContext = createContext<LanguageContextValue>({
  language: defaultLanguage,
  strings: translations[defaultLanguage],
  setLanguage: () => undefined,
  toggleLanguage: () => undefined,
});

const STORAGE_KEY = 'wct-lang';

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguageState] = useState<Language>(defaultLanguage);
  const [bootstrapped, setBootstrapped] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY)
      .then((stored) => {
        if (stored === 'en' || stored === 'np') {
          setLanguageState(stored);
        }
      })
      .finally(() => setBootstrapped(true));
  }, []);

  useEffect(() => {
    AsyncStorage.setItem(STORAGE_KEY, language).catch(() => undefined);
  }, [language]);

  const setLanguage = (lang: Language) => setLanguageState(lang);
  const toggleLanguage = () => setLanguageState((prev) => (prev === 'en' ? 'np' : 'en'));

  const value = useMemo(
    () => ({ language, strings: translations[language], setLanguage, toggleLanguage }),
    [language]
  );

  if (!bootstrapped) {
    return null;
  }

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};

export const useLanguage = () => useContext(LanguageContext);

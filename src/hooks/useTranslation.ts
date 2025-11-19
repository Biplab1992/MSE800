import { useLanguage } from '../context/LanguageContext';

export const useTranslation = () => {
  const ctx = useLanguage();
  return { language: ctx.language, t: ctx.strings, setLanguage: ctx.setLanguage, toggleLanguage: ctx.toggleLanguage };
};

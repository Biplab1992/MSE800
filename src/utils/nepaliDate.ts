import { Language } from '../i18n/translations';

const NEPALI_MONTHS = [
  'बैशाख',
  'जेठ',
  'असार',
  'साउन',
  'भदौ',
  'असोज',
  'कार्तिक',
  'मंसिर',
  'पौष',
  'माघ',
  'फागुन',
  'चैत',
];

const NEPALI_WEEKDAYS = ['आइतबार', 'सोमबार', 'मङ्गलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार'];

const DIGITS: Record<string, string> = {
  '0': '०',
  '1': '१',
  '2': '२',
  '3': '३',
  '4': '४',
  '5': '५',
  '6': '६',
  '7': '७',
  '8': '८',
  '9': '९',
};

const MONTH_RULES = [
  { month: 3, day: 13, bsMonth: 0, yearOffset: 0 },
  { month: 4, day: 14, bsMonth: 1, yearOffset: 0 },
  { month: 5, day: 14, bsMonth: 2, yearOffset: 0 },
  { month: 6, day: 16, bsMonth: 3, yearOffset: 0 },
  { month: 7, day: 17, bsMonth: 4, yearOffset: 0 },
  { month: 8, day: 17, bsMonth: 5, yearOffset: 0 },
  { month: 9, day: 18, bsMonth: 6, yearOffset: 0 },
  { month: 10, day: 17, bsMonth: 7, yearOffset: 0 },
  { month: 11, day: 16, bsMonth: 8, yearOffset: 0 },
  { month: 0, day: 14, bsMonth: 9, yearOffset: 1 },
  { month: 1, day: 12, bsMonth: 10, yearOffset: 1 },
  { month: 2, day: 14, bsMonth: 11, yearOffset: 1 },
];

const DAY_MS = 24 * 60 * 60 * 1000;

const toNepaliDigits = (value: number) =>
  value
    .toString()
    .split('')
    .map((digit) => DIGITS[digit] ?? digit)
    .join('');

const getBsYear = (date: Date) => {
  const baseYear = date.getFullYear();
  const nepaliNewYear = new Date(baseYear, 3, 13);
  return date >= nepaliNewYear ? baseYear + 57 : baseYear + 56;
};

const getBsMonthInfo = (date: Date) => {
  const baseYear = date.getFullYear();
  const nepaliNewYear = new Date(baseYear, 3, 13);
  const cycleYear = date >= nepaliNewYear ? baseYear : baseYear - 1;

  let selectedRule = MONTH_RULES[0];
  let selectedStart = new Date(cycleYear + selectedRule.yearOffset, selectedRule.month, selectedRule.day);

  MONTH_RULES.forEach((rule) => {
    const start = new Date(cycleYear + rule.yearOffset, rule.month, rule.day);
    if (date >= start) {
      selectedRule = rule;
      selectedStart = start;
    }
  });

  const day = Math.floor((date.getTime() - selectedStart.getTime()) / DAY_MS) + 1;
  return { bsMonth: selectedRule.bsMonth, day };
};

const formatNepaliDate = (date: Date) => {
  const weekday = NEPALI_WEEKDAYS[date.getDay()];
  const { bsMonth, day } = getBsMonthInfo(date);
  const bsYear = getBsYear(date);
  return `${weekday}, ${NEPALI_MONTHS[bsMonth]} ${toNepaliDigits(day)}, ${toNepaliDigits(bsYear)}`;
};

const formatEnglishDate = (date: Date) =>
  new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  }).format(date);

export const formatDisplayDate = (date: Date, language: Language) =>
  language === 'np' ? formatNepaliDate(date) : formatEnglishDate(date);

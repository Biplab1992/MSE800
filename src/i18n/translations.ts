import { MealType } from '../types/meals';

export type Language = 'en' | 'np';

export type TranslationStrings = {
  headingToday: string;
  today: string;
  thisWeek: string;
  weeklyPlan: string;
  addMeal: string;
  editMeal: string;
  deleteMeal: string;
  save: string;
  cancel: string;
  noMeal: string;
  addedByPrefix: string;
  tabsLabel: string;
  fieldLabels: {
    mealType: string;
    date: string;
    title: string;
    description: string;
    imageUrl: string;
    createdBy: string;
  };
  formErrors: {
    title: string;
    mealType: string;
    date: string;
  };
  mealTypeLabel: Record<MealType, string>;
  todayDatePrefix: string;
  focusLabel: string;
  weeklyLeadCopy: string;
  deleteConfirm: string;
  logout: string;
  auth: {
    welcome: string;
    name: string;
    email: string;
    password: string;
    login: string;
    register: string;
    switchToLogin: string;
    switchToRegister: string;
  };
  homeSetup: {
    heading: string;
    createTitle: string;
    homeNamePlaceholder: string;
    createButton: string;
    joinTitle: string;
    joinDescription: string;
    codePlaceholder: string;
    joinButton: string;
    codeLabel: string;
  };
};

export const translations: Record<Language, TranslationStrings> = {
  en: {
    headingToday: "What's cooking today?",
    today: 'Today',
    thisWeek: 'This Week',
    weeklyPlan: 'Weekly Plan',
    addMeal: 'Add meal',
    editMeal: 'Edit meal',
    deleteMeal: 'Delete',
    save: 'Save',
    cancel: 'Cancel',
    noMeal: 'No meal planned yet',
    addedByPrefix: 'Added by',
    tabsLabel: 'View',
    fieldLabels: {
      mealType: 'Meal type',
      date: 'Date',
      title: 'Title',
      description: 'Description',
      imageUrl: 'Image URL',
      createdBy: 'Added by',
    },
    formErrors: {
      title: 'Please add a title',
      mealType: 'Select breakfast, lunch, or dinner',
      date: 'Pick a date for the meal',
    },
    mealTypeLabel: {
      breakfast: 'Breakfast',
      lunch: 'Lunch',
      dinner: 'Dinner',
    },
    todayDatePrefix: 'Today is',
    focusLabel: 'Highlighted meal',
    weeklyLeadCopy: 'Tap any slot to add or edit meals for the week.',
    deleteConfirm: 'Delete meal',
    logout: 'Logout',
    auth: {
      welcome: 'Sign in to your family planner',
      name: 'Name',
      email: 'Email',
      password: 'Password',
      login: 'Log in',
      register: 'Create account',
      switchToLogin: 'Already have an account? Log in',
      switchToRegister: 'New here? Create an account',
    },
    homeSetup: {
      heading: 'Create or join your home',
      createTitle: 'Start a new home',
      homeNamePlaceholder: 'e.g. Sharma Family',
      createButton: 'Create home & code',
      joinTitle: 'Join with a code',
      joinDescription: 'Ask a family member for the invite code.',
      codePlaceholder: 'ABC123',
      joinButton: 'Join home',
      codeLabel: 'Your home code',
    },
  },
  np: {
    headingToday: 'आज के पक्दैछ?',
    today: 'आज',
    thisWeek: 'यो हप्ता',
    weeklyPlan: 'साप्ताहिक योजना',
    addMeal: 'खाना थप्नुहोस्',
    editMeal: 'खाना सम्पादन गर्नुहोस्',
    deleteMeal: 'हटाउनुहोस्',
    save: 'सेभ',
    cancel: 'रद्द गर्नुहोस्',
    noMeal: 'अझै योजना बनेको छैन',
    addedByPrefix: 'कोद्वारा जोडिएको',
    tabsLabel: 'दृश्य',
    fieldLabels: {
      mealType: 'खाना प्रकार',
      date: 'मिति',
      title: 'शीर्षक',
      description: 'विवरण',
      imageUrl: 'तस्बिरको लिङ्क',
      createdBy: 'कसले थपे',
    },
    formErrors: {
      title: 'शीर्षक आवश्यक छ',
      mealType: 'कृपया खाना प्रकार छान्नुहोस्',
      date: 'कृपया मिति छान्नुहोस्',
    },
    mealTypeLabel: {
      breakfast: 'बिहानको खाजा',
      lunch: 'दिउँसोको खाना',
      dinner: 'बेलुकीको खाना',
    },
    todayDatePrefix: 'आजको मिति',
    focusLabel: 'मौजुदा भोजन',
    weeklyLeadCopy: 'हप्ताको कुनै पनि स्लटमा ट्याप गरेर खाना थप्न वा सम्पादन गर्नुस्।',
    deleteConfirm: 'खाना हटाउनुहोस्',
    logout: 'लगआउट',
    auth: {
      welcome: 'आफ्नो परिवार योजनामा प्रवेश गर्नुहोस्',
      name: 'नाम',
      email: 'इमेल',
      password: 'पासवर्ड',
      login: 'लगइन',
      register: 'खाता खोल्नुहोस्',
      switchToLogin: 'पहिलेबाट खाता छ? लगइन गर्नुहोस्',
      switchToRegister: 'नयाँ हुनुहुन्छ? खाता बनाउनुहोस्',
    },
    homeSetup: {
      heading: 'घरको योजना बनाउनुहोस्',
      createTitle: 'नयाँ घर सुरु गर्नुहोस्',
      homeNamePlaceholder: 'जस्तै शर्मा परिवार',
      createButton: 'घर र कोड बनाउनुहोस्',
      joinTitle: 'कोड प्रयोग गरेर जोडिनुहोस्',
      joinDescription: 'आमन्त्रक परिवार सदस्यसँग कोड माग्नुहोस्।',
      codePlaceholder: 'ABC123',
      joinButton: 'घरमा जोडिनुहोस्',
      codeLabel: 'तपाईंको घर कोड',
    },
  },
};

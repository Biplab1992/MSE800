export type MealType = 'breakfast' | 'lunch' | 'dinner';

export type Meal = {
  _id: string;
  date: string;
  mealType: MealType;
  title: string;
  description?: string;
  imageUrl?: string;
  createdBy?: string;
};

export type MealFormData = {
  date: string;
  mealType: MealType;
  title: string;
  description?: string;
  imageUrl?: string;
  createdBy?: string;
};

export type WeekMealsResponse = {
  weekDates: string[];
  meals: Meal[];
};

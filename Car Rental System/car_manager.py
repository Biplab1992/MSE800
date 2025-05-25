import database

class CarManager:
    def add_car(self):
        """
        Admin adds a car to the database.
        """
        car_id = input("Enter car ID: ").strip()
        make = input("Enter make: ").strip()
        model = input("Enter model: ").strip()
        year = input("Enter year: ").strip()
        mileage = input("Enter mileage: ").strip()
        available = input("Is the car available (yes/no)? ").strip().lower() == "yes"
        min_rent_period = int(input("Enter min rental period in days: "))
        max_rent_period = int(input("Enter max rental period in days: "))
        bonus_points = int(input("Enter bonus loyalty points for this car (0 for standard vehicles): "))

        database.add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
        database.cars[car_id]["bonus_points"] = bonus_points  # Store bonus loyalty points
        print(f"Car added successfully. Bonus loyalty points: {bonus_points}")

    def view_available_cars(self):
        """
        Displays available cars with bonus loyalty points (if applicable).
        """
        cars = database.view_available_cars()
        if cars:
            print("\n--- Available Cars ---")
            for car_id, details in cars.items():
                bonus_points = details.get("bonus_points", 0)
                print(f"{car_id}: {details} | Bonus Points: {bonus_points}")
        else:
            print("No cars available.")

    def update_car_loyalty_points(self):
        """
        Admin updates bonus loyalty points for a car.
        """
        car_id = input("Enter car ID to update loyalty points: ").strip()
        if car_id in database.cars:
            new_bonus_points = int(input("Enter new bonus points: "))
            database.cars[car_id]["bonus_points"] = new_bonus_points
            print(f"Updated bonus loyalty points for {car_id} to {new_bonus_points}.")
        else:
            print("Car ID not found.")

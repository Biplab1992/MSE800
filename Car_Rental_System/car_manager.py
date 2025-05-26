import sqlite3
import database

DB_PATH = "database/rental_system.db"

class CarManager:
    def add_car(self):
        """
        Admin adds a car to the database. Bonus points must be 10, 20, or 30.
        """
        car_id = input("Enter car ID: ").strip()
        make = input("Enter make: ").strip()
        model = input("Enter model: ").strip()
        year = int(input("Enter year: "))
        mileage = int(input("Enter mileage: "))
        available = 1 if input("Is the car available (yes/no)? ").strip().lower() == "yes" else 0
        min_rent_period = int(input("Enter min rental period in days: "))
        max_rent_period = int(input("Enter max rental period in days: "))

        # Ensure valid bonus points input
        while True:
            try:
                bonus_points = int(input("Enter bonus loyalty points for this car (10 for standard / 20 for premium / 30 for luxury vehicles): "))
                if bonus_points in [10, 20, 30]:
                    break
                else:
                    print("Invalid bonus points! Please enter either 10, 20, or 30.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        database.add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points)
        print(f"Car added successfully. Bonus loyalty points: {bonus_points}")

    def list_cars(self):
        """
        Admin views all available cars.
        """
        cars = database.list_cars()
        if cars:
            print("\n--- Car List ---")
            for car in cars:
                print(f"Car ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Available: {'Yes' if car[5] else 'No'}, Min Days: {car[6]}, Bonus Points: {car[8]}")
        else:
            print("No cars available in the system.")

    def update_car(self):
        car_id = input("Enter car ID to update: ").strip()
        updated_info = {}
        for key in ["make", "model", "year", "mileage", "available", "min_rent_period", "max_rent_period", "bonus_points"]:
            new_value = input(f"Enter new {key} (leave blank to keep current): ").strip()
            if new_value:
                updated_info[key] = int(new_value) if key in ["min_rent_period", "max_rent_period", "bonus_points"] else new_value

        database.update_car(car_id, updated_info)


    def delete_car(self):
        """
        Admin deletes a car from the system.
        """
        car_id = input("Enter car ID to delete: ").strip()
        database.delete_car(car_id)
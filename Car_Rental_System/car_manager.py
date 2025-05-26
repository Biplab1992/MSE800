import sqlite3
import database
import os

DB_PATH = os.path.join("Car_Rental_System", "database", "rental_system.db")

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
        """
        Admin updates car details after viewing available cars.
        """
        print("\n--- Available Cars ---")
        self.list_cars()
        
        car_id = input("\nEnter the Car ID to update: ").strip()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()
        conn.close()

        if not car:
            print(f"Error: Car ID {car_id} not found. Please enter a valid ID.")
            return

        updated_info = {}

        # Prompt for new values
        for key in ["make", "model", "year", "mileage", "min_rent_period", "max_rent_period"]:
            new_value = input(f"Enter new {key} (leave blank to keep current): ").strip()
            if new_value:
                updated_info[key] = int(new_value) if key in ["year", "mileage", "min_rent_period", "max_rent_period"] else new_value

        # Ensure valid input for availability
        new_value = input("Is the car available (yes/no)? ").strip().lower()
        updated_info["available"] = 1 if new_value == "yes" else 0

        # Ensure valid bonus points input
        while True:
            try:
                bonus_points = int(input("Enter bonus loyalty points for this car (10 for standard / 20 for premium / 30 for luxury vehicles): "))
                if bonus_points in [10, 20, 30]:
                    updated_info["bonus_points"] = bonus_points
                    break
                else:
                    print("Invalid bonus points! Please enter either 10, 20, or 30.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        database.update_car(car_id, updated_info)
        print(f"Car {car_id} has been successfully updated with new information.")

    def delete_car(self):
        """
        Admin deletes a car from the system.
        """
        car_id = input("Enter car ID to delete: ").strip()
        
        # Call the delete function from database.py
        database.delete_car(car_id)

        # Print confirmation message
        print(f"Car {car_id} has been successfully deleted.")
import database

class CarManager:
    def add_car(self):
        car_id = input("Enter car ID: ").strip()
        make = input("Enter make: ").strip()
        model = input("Enter model: ").strip()
        year = int(input("Enter year: "))
        mileage = int(input("Enter mileage: "))
        available = input("Is the car available (yes/no)? ").strip().lower() == "yes"
        min_rent_period = int(input("Enter min rental period in days: "))
        max_rent_period = int(input("Enter max rental period in days: "))
       
        while True:
            try:
                bonus_points = int(input("Enter bonus loyalty points for this car (10 for standard / 20 for premium / 30 for luxury vehicles): "))
                if bonus_points in [10, 20, 30]:  # Only accept 10, 20, or 30
                    break
                else:
                    print("Invalid bonus points! Please enter either 10, 20, or 30.")
            except ValueError:
                print("Invalid input! Please enter a number.")


        database.add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points)
        print(f"Car added successfully. Bonus loyalty points: {bonus_points}")

    def list_cars(self):
        cars = database.list_cars()
        if cars:
            print("\n--- Car List ---")
            for car in cars:
                print(f"Car ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Available: {'Yes' if car[5] else 'No'}, Min Days: {car[6]}, Bonus Points: {car[8]}")
        else:
            print("No cars available in the system.")

    def update_car(self):
        """
        Admin updates car details. Ensures valid car ID before proceeding.
        """
        import sqlite3
        car_id = input("Enter car ID to update: ").strip()

        # Check if the car exists in the database before updating
        conn = sqlite3.connect("database/rental_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()
        conn.close()

        if not car:
            print(f"Error: Car ID {car_id} not found. Please enter a valid ID.")
            return

        updated_info = {}

        for key in ["make", "model", "year", "mileage", "available", "min_rent_period", "max_rent_period"]:
            new_value = input(f"Enter new {key} (leave blank to keep current): ").strip()
            if new_value:
                updated_info[key] = int(new_value) if key in ["min_rent_period", "max_rent_period"] else new_value

        # Ensures valid bonus points input
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

        # Apply the update in the database
        conn = sqlite3.connect("database/rental_system.db")
        cursor = conn.cursor()
        for key, value in updated_info.items():
            cursor.execute(f"UPDATE cars SET {key} = ? WHERE car_id = ?", (value, car_id))
        conn.commit()
        conn.close()

        print(f"Car {car_id} updated successfully.")

    def delete_car(self):
        car_id = input("Enter car ID to delete: ").strip()
        database.delete_car(car_id)
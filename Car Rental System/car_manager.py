import database

class CarManager:
    def add_car(self):
        car_id = input("Enter car ID: ").strip()
        make = input("Enter make: ").strip()
        model = input("Enter model: ").strip()
        year = input("Enter year: ").strip()
        mileage = input("Enter mileage: ").strip()
        available = input("Is the car available (yes/no)? ").strip().lower() == "yes"
        min_rent_period = int(input("Enter min rental period in days: "))
        max_rent_period = int(input("Enter max rental period in days: "))
        bonus_points = int(input("Enter bonus loyalty points for this car (10 for standard / 20 for premium / 30 for luxury vehicles): "))

        database.add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
        database.cars[car_id]["bonus_points"] = bonus_points  # Store bonus loyalty points
        print(f"Car added successfully. Bonus loyalty points: {bonus_points}")

    def list_cars(self):
        """
        Displays all cars in the system.
        """
        if database.cars:
            print("\n--- Car List ---")
            for car_id, details in database.cars.items():
                print(f"{car_id}: {details}")
        else:
            print("No cars available in the system.")

    def update_car(self):
        """
        Admin updates car details.
        """
        car_id = input("Enter car ID to update: ").strip()
        if car_id in database.cars:
            print(f"Current details: {database.cars[car_id]}")
            updated_info = {}
            for key in ["make", "model", "year", "mileage", "available", "min_rent_period", "max_rent_period", "bonus_points"]:
                new_value = input(f"Enter new {key} (leave blank to keep current): ").strip()
                if new_value:
                    updated_info[key] = int(new_value) if key in ["min_rent_period", "max_rent_period", "bonus_points"] else new_value
            
            database.update_car(car_id, updated_info)
            print(f"Car {car_id} updated successfully.")
        else:
            print("Car ID not found.")

    def delete_car(self):
        """
        Admin deletes a car from the system.
        """
        car_id = input("Enter car ID to delete: ").strip()
        if database.delete_car(car_id):
            print(f"Car {car_id} deleted successfully.")
        else:
            print("Car ID not found.")
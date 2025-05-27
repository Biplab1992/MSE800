import database  # This is your Firebase-based database module

class CarManager:
    def add_car(self):
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
        cars = database.list_cars()
        if cars:
            print("\n--- Car List ---")
            for car in cars:
                # car is now a dictionary with keys: car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points
                available_str = "Yes" if car.get("available") else "No"
                print(f"Car ID: {car.get('car_id')}, Make: {car.get('make')}, Model: {car.get('model')}, "
                      f"Year: {car.get('year')}, Mileage: {car.get('mileage')}, Available: {available_str}, "
                      f"Min Days: {car.get('min_rent_period')}, Max Days: {car.get('max_rent_period')}, Bonus Points: {car.get('bonus_points')}")
        else:
            print("No cars available in the system.")

    def update_car(self):
        print("\n--- Available Cars ---")
        self.list_cars()
        
        car_id = input("\nEnter the Car ID to update: ").strip()
        
        # Retrieve all cars from Firebase and check if provided car_id exists.
        cars = database.list_cars()
        selected_car = None
        for car in cars:
            if car.get("car_id") == car_id:
                selected_car = car
                break

        if not selected_car:
            print(f"Error: Car ID {car_id} not found. Please enter a valid ID.")
            return

        updated_info = {}

        # Prompt for new values for certain fields.
        for key in ["make", "model", "year", "mileage", "min_rent_period", "max_rent_period"]:
            new_value = input(f"Enter new {key} (leave blank to keep current): ").strip()
            if new_value:
                if key in ["year", "mileage", "min_rent_period", "max_rent_period"]:
                    updated_info[key] = int(new_value)
                else:
                    updated_info[key] = new_value

        new_value = input("Is the car available (yes/no)? ").strip().lower()
        updated_info["available"] = 1 if new_value == "yes" else 0

        # Ensure valid bonus points input.
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
        car_id = input("Enter car ID to delete: ").strip()
        database.delete_car(car_id)
        print(f"Car {car_id} has been successfully deleted.")
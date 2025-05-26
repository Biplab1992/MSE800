import sqlite3
import database
import os
import uuid
import datetime

# Set the correct path for rental_system.db inside Car_Rental_System/database
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "Car_Rental_System"))  # Ensure correct base path
DB_DIR = os.path.join(BASE_DIR, "database")  # Database folder path
DB_PATH = os.path.join(DB_DIR, "rental_system.db")  # SQLite database file path

class BookingManager:
    def request_rental(self, customer_email):
        """
        Allows the customer to view available cars, select one, and request a rental.
        """
        print("\n--- Available Cars for Rental ---")
        cars = database.list_cars()
        
        if not cars:
            print("No cars are available for rental.")
            return
        
        for car in cars:
            print(f"Car ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Available: {'Yes' if car[5] else 'No'}, Min Days: {car[6]}, Bonus Points: {car[8]}")

        # Customer selects a car
        car_id = input("\nEnter the Car ID you want to rent: ").strip()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE car_id = ?", (car_id,))
        selected_car = cursor.fetchone()
        conn.close()

        if not selected_car:
            print(f"Error: Car ID {car_id} not found. Please enter a valid ID.")
            return
        
        # Check car availability before booking
        if selected_car[5] == 0:  # Availability field in database (0 = Not Available)
            print(f"Sorry, the car {selected_car[1]} {selected_car[2]} (ID: {car_id}) is not available for rental right now.")
            return

        
        # Enter rental dates
        try:
            today = datetime.date.today()

            start_date = input("Enter rental **start date** (YYYY-MM-DD): ").strip()
            end_date = input("Enter rental **end date** (YYYY-MM-DD): ").strip()

            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

            # Ensure the start date is **not in the past**
            if start_date_obj < today:
                print("Error: Start date cannot be in the past.")
                return

            # Ensure the end date is **after** the start date
            if end_date_obj <= start_date_obj:
                print("Error: End date must be after the start date.")
                return

            # Calculate rental duration (days)
            rental_days = (end_date_obj - start_date_obj).days
            
            if rental_days < selected_car[6]:  # Check if rental period meets min requirement
                print(f"Error: Minimum rental period for this car is {selected_car[6]} days.")
                return
            
        except ValueError:
            print("Invalid date format! Please enter dates in YYYY-MM-DD.")
            return
        
        # Calculate rental cost based on bonus points
        base_rate = self.get_car_rate(selected_car[8])  # Ensure correct attribute is passed
        rental_cost = base_rate * rental_days
        
        print("\n--- Rental Cost Calculation ---")
        print(f"Base rate: ${base_rate} per day (Based on Bonus Points: {selected_car[8]})")
        print(f"Rental duration: {rental_days} days")
        print(f"Total cost: ${rental_cost}")

        # Generate booking ID
        booking_id = f"BOOK-{str(uuid.uuid4())[:8]}"    

        # Store rental request in database
        database.add_rental(booking_id, customer_email, car_id, rental_days, rental_cost)
        print(f"\nRental request submitted successfully! Booking ID: {booking_id}")

    def get_car_rate(self, bonus_points):
        """
        Determines the rental base rate based on bonus points.
        """
        rate_mapping = {10: 50, 20: 100, 30: 150}
        return rate_mapping.get(bonus_points, 50)  # Defaults to 50 if bonus points are invalid

    def approve_rental(self):
        """
        Admin reviews and approves or disapproves rental requests.
        If no rentals exist, display a message.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rentals WHERE status = 'Pending'")
        pending_rentals = cursor.fetchall()
        conn.close()

        if not pending_rentals:
            print("\nThere are no approval rental requests pending.")
            return
        
        print("\n--- Pending Rental Requests ---")
        for rental in pending_rentals:
            print(f"Booking ID: {rental[0]}, Customer: {rental[1]}, Car ID: {rental[2]}, Rental Days: {rental[3]}, Total Cost: ${rental[4]}")
        
        # Approve or disapprove rental request
        booking_id = input("\nEnter Booking ID to review: ").strip()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rentals WHERE booking_id = ?", (booking_id,))
        rental = cursor.fetchone()
        conn.close()

        if not rental:
            print(f"Error: Booking ID {booking_id} not found. Please enter a valid ID.")
            return
        
        # Admin decision
        decision = input("Approve this rental request? (yes/no): ").strip().lower()

        if decision == "yes":
            status = "Approved"
            print(f"Rental request {booking_id} has been approved.")
        elif decision == "no":
            status = "Rejected"
            print(f"Rental request {booking_id} has been disapproved.")
        else:
            print("Invalid input. Please enter 'yes' to approve or 'no' to disapprove.")
            return

        # Update rental status in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE rentals SET status = ? WHERE booking_id = ?", (status, booking_id))
        conn.commit()
        conn.close()

        # print(f"Rental request {booking_id} has been updated.")
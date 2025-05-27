import database
import uuid
import datetime
from firebase_admin import firestore  # For Increment operations
from database import get_users_collection  # To update the user's loyalty points
import payment_gateway  # Import the simulated payment gateway module

class BookingManager:
    def request_rental(self, customer_email):
        print("\n--- Available Cars for Rental ---")
        cars = database.list_cars()

        if not cars:
            print("No cars are available for rental.")
            return

        # Display available cars
        for car in cars:
            available_str = "Yes" if car.get("available") else "No"
            print(f"Car ID: {car.get('car_id')}, Make: {car.get('make')}, Model: {car.get('model')}, "
                  f"Year: {car.get('year')}, Mileage: {car.get('mileage')}, Available: {available_str}, "
                  f"Min Days: {car.get('min_rent_period')}, Bonus Points: {car.get('bonus_points')}")

        car_id = input("\nEnter the Car ID you want to rent: ").strip()
        selected_car = next((car for car in cars if car.get("car_id") == car_id), None)

        if not selected_car or not selected_car.get("available"):
            print(f"Error: Car ID {car_id} is either invalid or unavailable.")
            return

        # Enter rental dates
        try:
            today = datetime.date.today()
            start_date = input("Enter rental start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter rental end date (YYYY-MM-DD): ").strip()

            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date_obj < today or end_date_obj <= start_date_obj:
                print("Error: Invalid rental date range.")
                return

            rental_days = (end_date_obj - start_date_obj).days
            if rental_days < selected_car.get("min_rent_period"):
                print(f"Error: Minimum rental period is {selected_car.get('min_rent_period')} days.")
                return

        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            return

        # Fetch user's loyalty points from Firestore
        user = database.get_user(customer_email)
        available_points = user.get("loyalty_points", 0) if user else 0

        # Calculate rental cost
        base_rate = self.get_car_rate(selected_car.get("bonus_points"))
        total_rental_cost = base_rate * rental_days

        # Option to redeem loyalty points
        discount = min(available_points, total_rental_cost) if available_points >= 100 else 0
        if discount > 0:
            use_points = input(f"You have {available_points} loyalty points. Use them for a discount? (yes/no): ").strip().lower()
            if use_points != "yes":
                discount = 0

        final_cost = max(total_rental_cost - discount, 0)

        print("\n--- Rental Cost Calculation ---")
        print(f"Base rate: ${base_rate}/day (Bonus Points: {selected_car.get('bonus_points')})")
        print(f"Rental duration: {rental_days} days ({start_date} - {end_date})")
        print(f"Total cost before discount: ${total_rental_cost}")
        print(f"Discount applied: ${discount}")
        print(f"Final cost after discount: ${final_cost}")

        # **NEW: Simulated Payment Prompt via eSewa**
        payment_success = payment_gateway.process_payment(customer_email, final_cost)
        if not payment_success:
            print("Payment was not completed. Rental request canceled.")
            return

        # Generate unique booking ID
        booking_id = f"BOOK-{str(uuid.uuid4())[:8]}"

        # Deduct used loyalty points from user's account
        new_points = available_points - discount if discount > 0 else available_points
        get_users_collection().document(customer_email).update({"loyalty_points": new_points})

        # Store rental request in Firestore
        database.add_rental(booking_id, customer_email, car_id, rental_days, final_cost)
        print(f"\nRental request submitted successfully! Booking ID: {booking_id}")

    def get_car_rate(self, bonus_points):
        rate_mapping = {10: 50, 20: 100, 30: 150}
        return rate_mapping.get(bonus_points, 50)  # Default rate is 50 if bonus points are invalid

    def approve_rental(self):
        rentals = database.list_rentals()
        pending_rentals = [r for r in rentals if r.get("status") == "Pending"]

        if not pending_rentals:
            print("\nNo pending rental approvals.")
            return

        print("\n--- Pending Rental Requests ---")
        for rental in pending_rentals:
            print(f"Booking ID: {rental.get('booking_id')}, Customer: {rental.get('customer_email')}, "
                f"Car ID: {rental.get('car_id')}, Rental Days: {rental.get('rental_days')}, Total Cost: ${rental.get('total_cost')}")
        
        # Select a booking for review
        booking_id = input("\nEnter Booking ID to review: ").strip()
        selected_rental = next((r for r in pending_rentals if r.get("booking_id") == booking_id), None)
        
        if not selected_rental:
            print(f"Error: Booking ID {booking_id} not found.")
            return

        # Display customer records (rental & payment history)
        customer_email = selected_rental.get("customer_email")
        rental_history = database.get_customer_rentals(customer_email)
        payment_history = database.get_customer_payments(customer_email)

        print("\n--- Customer Records ---")
        if rental_history:
            print("\nRental History:")
            for rental in rental_history:
                print(f"Booking ID: {rental.get('booking_id')}, Car ID: {rental.get('car_id')}, Days: {rental.get('rental_days')}, "
                    f"Total Cost: ${rental.get('total_cost')}, Status: {rental.get('status')}")
        else:
            print("\nNo rental history found.")

        if payment_history:
            print("\nPayment History:")
            print(f"Amount Paid: ${payment_history.get('amount')}")
            print(f"Payment Status: {payment_history.get('status')}")
        else:
            print("\nNo payment records found.")

        # Admin decision for approval
        decision = input("Approve rental request? (yes/no): ").strip().lower()
        if decision == "yes":
            status = "Approved"
            print(f"\nRental request {booking_id} has been approved.")
        else:
            status = "Rejected"
            print(f"\nRental request {booking_id} has been rejected.")

        # If approved, update loyalty points for the customer
        if status == "Approved":
            cars = database.list_cars()
            car = next((c for c in cars if c.get("car_id") == selected_rental.get("car_id")), None)
            if car:
                bonus_points = car.get("bonus_points")
                total_loyalty_points = bonus_points * selected_rental.get("rental_days")
                get_users_collection().document(customer_email).update({
                    "loyalty_points": firestore.Increment(total_loyalty_points)
                })
                print(f"{total_loyalty_points} loyalty points added to {customer_email}.")
            else:
                print("Car not found. Cannot update loyalty points.")

        # Finally, update the rental status in Firestore
        database.update_rental_status(booking_id, status)
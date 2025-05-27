import database
import uuid
import datetime
from firebase_admin import firestore  # For Increment operations
from database import get_users_collection  # To update the user's loyalty points
import payment_gateway  # Import the simulated payment gateway module


class BookingManager:
    def request_rental(self, customer_email):
        """
        Handles the rental request process:
         - Displays available cars.
         - Prompts the customer for car selection and rental dates.
         - Offers the option to redeem loyalty points for a discount.
         - Calculates the final cost and simulates payment via eSewa.
         - Records the payment as a separate record.
         - Deducts redeemed loyalty points (if applicable) and saves the rental record.
        """
        print("\n--- Available Cars for Rental ---")
        cars = database.list_cars()
        if not cars:
            print("No cars are available for rental.")
            return

        # Display available cars
        for car in cars:
            available_str = "Yes" if car.get("available") else "No"
            print(
                f"Car ID: {car.get('car_id')}, Make: {car.get('make')}, Model: {car.get('model')}, "
                f"Year: {car.get('year')}, Mileage: {car.get('mileage')}, Available: {available_str}, "
                f"Min Days: {car.get('min_rent_period')}, Bonus Points: {car.get('bonus_points')}"
            )

        # Prompt customer for car selection
        car_id = input("\nEnter the Car ID you want to rent: ").strip()
        selected_car = next((car for car in cars if car.get("car_id") == car_id), None)
        if not selected_car or not selected_car.get("available"):
            print(f"Error: Car ID {car_id} is either invalid or unavailable.")
            return

        # Prompt for rental dates and validate them
        try:
            today = datetime.date.today()
            start_date = input("Enter rental start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter rental end date (YYYY-MM-DD): ").strip()
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

            # Ensure rental period is valid
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

        # Retrieve the user's loyalty points from Firestore
        user = database.get_user(customer_email)
        available_points = user.get("loyalty_points", 0) if user else 0

        # Calculate rental cost
        base_rate = self.get_car_rate(selected_car.get("bonus_points"))
        total_rental_cost = base_rate * rental_days
        discount = 0  # Initialize discount

        # Offer to redeem loyalty points if available (threshold >= 100 points)
        if available_points >= 100:
            use_points = input(
                f"You have {available_points} loyalty points. Would you like to redeem them for a discount? (yes/no): "
            ).strip().lower()
            if use_points == "yes":
                # Redeem points up to the total cost amount
                discount = min(available_points, total_rental_cost)
                print(f"Discount of ${discount} has been applied using your loyalty points.")
            else:
                print("No loyalty points redeemed.")

        # Calculate the final cost after discount
        final_cost = max(total_rental_cost - discount, 0)

        # Display the cost breakdown for confirmation
        print("\n--- Rental Cost Calculation ---")
        print(f"Base rate: ${base_rate}/day (Bonus Points: {selected_car.get('bonus_points')})")
        print(f"Rental duration: {rental_days} days ({start_date} - {end_date})")
        print(f"Total cost before discount: ${total_rental_cost}")
        print(f"Discount applied: ${discount}")
        print(f"Final cost after discount: ${final_cost}")

        # Process payment simulation via eSewa
        payment_success = payment_gateway.process_payment(customer_email, final_cost)
        if not payment_success:
            print("Payment was not completed. Rental request canceled.")
            return

        # Record the payment as a separate record in the database
        database.record_payment(customer_email, final_cost)

        # Generate a unique booking ID for this rental
        booking_id = f"BOOK-{str(uuid.uuid4())[:8]}"

        # Deduct redeemed loyalty points from the user's account (if any were redeemed)
        if discount > 0:
            new_points = available_points - discount
            get_users_collection().document(customer_email).update({"loyalty_points": new_points})

        # Store the rental request in Firestore
        database.add_rental(booking_id, customer_email, car_id, rental_days, final_cost)
        print(f"\nRental request submitted successfully! Booking ID: {booking_id}")

    def get_car_rate(self, bonus_points):
        """
        Determines the base rental rate based on the car's bonus points.
        Uses a predefined mapping; returns a default rate if bonus points are not specified.
        """
        rate_mapping = {10: 50, 20: 100, 30: 150}
        return rate_mapping.get(bonus_points, 50)

    def approve_rental(self):
        """
        Allows an admin to review and approve/reject pending rental requests.
        Displays customer rental and payment history to assist with the decision.
        """
        rentals = database.list_rentals()
        pending_rentals = [r for r in rentals if r.get("status") == "Pending"]

        if not pending_rentals:
            print("\nNo pending rental approvals.")
            return

        print("\n--- Pending Rental Requests ---")
        for rental in pending_rentals:
            print(
                f"Booking ID: {rental.get('booking_id')}, Customer: {rental.get('customer_email')}, "
                f"Car ID: {rental.get('car_id')}, Rental Days: {rental.get('rental_days')}, "
                f"Total Cost: ${rental.get('total_cost')}"
            )

        # Admin selects a booking ID for review
        booking_id = input("\nEnter Booking ID to review: ").strip()
        selected_rental = next((r for r in pending_rentals if r.get("booking_id") == booking_id), None)
        if not selected_rental:
            print(f"Error: Booking ID {booking_id} not found.")
            return

        # Retrieve customer's rental and payment history
        customer_email = selected_rental.get("customer_email")
        rental_history = database.get_customer_rentals(customer_email)
        payment_history = database.get_customer_payments(customer_email)

        print("\n--- Customer Records ---")
        if rental_history:
            print("\nRental History:")
            for rental in rental_history:
                print(
                    f"Booking ID: {rental.get('booking_id')}, Car ID: {rental.get('car_id')}, "
                    f"Days: {rental.get('rental_days')}, Total Cost: ${rental.get('total_cost')}, "
                    f"Status: {rental.get('status')}"
                )
        else:
            print("\nNo rental history found.")

        if payment_history:
            print("\nPayment History:")
            for payment in payment_history:
                print(
                    f"Amount Paid: ${payment.get('amount')}, "
                    f"Status: {payment.get('status')}, "
                    f"Timestamp: {payment.get('timestamp')}"
                )
        else:
            print("\nNo payment records found.")

        # Admin decision: approve or reject the rental request
        decision = input("Approve rental request? (yes/no): ").strip().lower()
        if decision == "yes":
            status = "Approved"
            print(f"\nRental request {booking_id} has been approved.")
        else:
            status = "Rejected"
            print(f"\nRental request {booking_id} has been rejected.")

        # If approved, update the customer's loyalty points based on the car's bonus points and rental duration
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

        # Update the rental status in Firestore
        database.update_rental_status(booking_id, status)
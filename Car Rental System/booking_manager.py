import database

class BookingManager:
    def request_rental(self, customer_email):
        """
        Customer requests a rental.
        """
        cars = database.view_available_cars()
        if not cars:
            print("No cars available for rent.")
            return

        for car_id, details in cars.items():
            print(f"{car_id}: {details}")

        car_id = input("Enter the car ID to rent: ").strip()
        rental_days = int(input("Enter rental days: "))

        if car_id in cars:
            total_cost = rental_days * 50  # Example pricing model
            booking_id = f"BK-{len(database.rental_requests) + 1}"
            database.add_rental_request(booking_id, customer_email, car_id, rental_days, total_cost)

            # Reward loyalty points (5 points per rental day)
            database.add_loyalty_points(customer_email, rental_days * 5)
            print(f"Rental request submitted. Booking ID: {booking_id}")
            print(f"Loyalty points earned: {rental_days * 5}")
        else:
            print("Invalid car selection.")
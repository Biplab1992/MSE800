import database

class UserManager:
    def register_user(self):
        name = input("Enter your full name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        role = input("Enter user role (customer/admin): ").strip().lower()

        if database.get_user(email):
            print(f"Registration failed: A user with email '{email}' already exists.")
        else:
            database.add_user(name, email, password, role)
            print(f"User {name} registered successfully with role: {role}")

    def login_user(self):
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        user = database.get_user(email)

        if user:
            if user.get("password") == password:  # Validate password
                print(f"User {user.get('name')} logged in successfully as {user.get('role')}.")
                return user.get("role"), email
            else:
                print("Login failed: Incorrect password.")
        else:
            print("Login failed: User not found.")

        return None, None

    def view_loyalty_points(self, email):
        user = database.get_user(email)

        if user:
            print(f"\nYour loyalty points: {user.get('loyalty_points')}")
        else:
            print("\nError: User not found.")

    def view_payment_history(self, email):
        """
        Retrieves a user's payment history from Firestore.
        """
        payment_data = database.get_payment_history(email)

        if payment_data:
            print("\n--- Payment History ---")
            print(f"Customer: {payment_data.get('customer_email')}")
            print(f"Amount Paid: ${payment_data.get('amount')}")
            print(f"Payment Status: {payment_data.get('status')}")
        else:
            print("\nNo payment records found.")

    def check_customer_records(self, email):
        """
        Retrieves and displays the customer's rental and payment history.
        """
        rental_history = database.get_customer_rentals(email)
        payment_history = database.get_customer_payments(email)

        print("\n--- Customer Records ---")
        print(f"User Email: {email}")

        if rental_history:
            print("\nRental History:")
            for rental in rental_history:
                print(f"Booking ID: {rental.get('booking_id')}, Car ID: {rental.get('car_id')}, "
                      f"Days: {rental.get('rental_days')}, Total Cost: ${rental.get('total_cost')}, "
                      f"Status: {rental.get('status')}")
        else:
            print("\nNo rental history found.")

        if payment_history:
            print("\nPayment History:")
            print(f"Amount Paid: ${payment_history.get('amount')}")
            print(f"Payment Status: {payment_history.get('status')}")
        else:
            print("\nNo payment records found.")
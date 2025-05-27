import database

class UserManager:
    def register_user(self):
        """
        Registers a new user by collecting their details,
        checking for existing accounts, and saving new accounts in the database.
        """
        name = input("Enter your full name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        role = input("Enter user role (customer/admin): ").strip().lower()

        # Check if a user with the given email already exists.
        if database.get_user(email):
            print(f"Registration failed: A user with email '{email}' already exists.")
        else:
            database.add_user(name, email, password, role)
            print(f"User {name} registered successfully with role: {role}")

    def login_user(self):
        """
        Authenticates a user by checking the email and password.
        Returns a tuple (role, email) upon successful login; otherwise (None, None).
        """
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        user = database.get_user(email)

        if user:
            if user.get("password") == password:
                print(f"User {user.get('name')} logged in successfully as {user.get('role')}.")
                return user.get("role"), email
            else:
                print("Login failed: Incorrect password.")
        else:
            print("Login failed: User not found.")

        return None, None

    def view_loyalty_points(self, email):
        """
        Displays the loyalty points associated with the given email.
        """
        user = database.get_user(email)
        if user:
            # Provide a default of 0 if 'loyalty_points' is not present in the user record.
            print(f"\nYour loyalty points: {user.get('loyalty_points', 0)}")
        else:
            print("\nError: User not found.")

    def view_payment_history(self, email):
        """
        Retrieves and displays the user's payment history from the database.
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
                print(
                    f"Booking ID: {rental.get('booking_id')}, Car ID: {rental.get('car_id')}, "
                    f"Days: {rental.get('rental_days')}, Total Cost: ${rental.get('total_cost')}, "
                    f"Status: {rental.get('status')}"
                )
        else:
            print("\nNo rental history found.")

        if payment_history:
            print("\nPayment History:")
            print(f"Amount Paid: ${payment_history.get('amount')}")
            print(f"Payment Status: {payment_history.get('status')}")
        else:
            print("\nNo payment records found.")
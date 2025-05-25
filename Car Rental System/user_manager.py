import database

class UserManager:
    def register_user(self):
        """
        Registers a new user in the system.
        """
        name = input("Enter your full name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        role = input("Enter user role (customer/admin): ").strip().lower() or "customer"

        if database.get_user(email):
            print(f"Registration failed: A user with email '{email}' already exists.")
        else:
            database.add_user(name, email, password, role)
            print(f"User {name} registered successfully with role: {role}")

    def login_user(self):
        """
        Authenticates user login.
        """
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        user = database.get_user(email)
        if user and user["password"] == password:
            print(f"User {user['name']} logged in successfully as {user['role']}.")
            return user["role"], email
        else:
            print("Invalid email or password.")
            return None, None

    def view_loyalty_points(self, email):
        """
        Allows customers to check their loyalty points.
        """
        points = database.get_loyalty_points(email)
        print(f"Your loyalty points: {points}")
        print(f"Your reward tier: {database.get_reward_tier(email)}")

    def redeem_loyalty_points(self, email):
        """
        Allows customers to redeem loyalty points for discounts.
        """
        points_to_redeem = int(input("Enter the number of points to redeem: "))

        if database.redeem_loyalty_points(email, points_to_redeem):
            print(f"Successfully redeemed {points_to_redeem} points.")
        else:
            print("Insufficient loyalty points.")
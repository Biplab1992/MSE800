import database 
import sqlite3
import os

# Define the database path directly
DB_PATH = os.path.join("Car_Rental_System", "database", "rental_system.db")

class UserManager:
    def register_user(self):
        """Registers a new user in the system."""
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
        """Authenticates a user based on email and password."""
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        user = database.get_user(email)

        if user:
            if user[2] == password:  # Validate password
                print(f"User {user[1]} logged in successfully as {user[3]}.")
                return user[3], email
            else:
                print("Login failed: Incorrect password.")
        else:
            print("Login failed: User not found.")
        
        return None, None

    def view_loyalty_points(self, email):
        """Displays the customer's loyalty points."""
        user = database.get_user(email)

        if user:
            print(f"\nYour loyalty points: {user[4]}")
        else:
            print("\nError: User not found.")
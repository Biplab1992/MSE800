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

        if user and user[2] == password:  # Validate password
            print(f"User {user[1]} logged in successfully as {user[3]}.")
            return user[3], email
        else:
            print("Invalid email or password.")
            return None, None
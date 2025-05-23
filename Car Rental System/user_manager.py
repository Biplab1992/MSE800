import database

class UserManager:
    """
    Provides user-related functionality such as registration,
    login, and checking customer records.
    """
    def __init__(self):
        pass  # No longer expecting a database instance

    def register_user(self, name, email, password):
        """
        Registers a new user by adding them to the database.
        """
        if database.get_user(email):
            print(f"Registration failed: A user with email '{email}' already exists.")
        else:
            database.add_user(name, email, password)
            print(f"User {name} registered successfully.")

    def login_user(self, email, password):
        """
        Logs in a user by verifying their credentials.
        """
        user = database.get_user(email)
        if user and user["password"] == password:
            print(f"User {user['name']} logged in successfully.")
        else:
            print("Invalid email or password.")

    def check_customer_records(self, email):
        """
        Retrieves and displays customer records associated with an email.
        """
        records = database.get_customer_records(email)
        if records:
            print(f"Customer records for {email}:\n" + "\n".join(records))
        else:
            print(f"No records found for {email}.")
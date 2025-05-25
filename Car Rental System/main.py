from user_manager import UserManager
from car_manager import CarManager
from booking_manager import BookingManager

user_manager = UserManager()
car_manager = CarManager()
booking_manager = BookingManager()

def main():
    while True:
        print("\n=== Car Rental System ===")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            user_manager.register_user()
        elif choice == "2":
            role, email = user_manager.login_user()
            if role == "customer":
                customer_menu(email)
            elif role == "admin":
                admin_menu()
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 3.")

def customer_menu(email):
    """
    Displays the customer menu after login.
    """
    while True:
        print("\n--- Customer Menu ---")
        print("1. Request Rental")
        print("2. View Loyalty Points")
        print("3. Redeem Loyalty Points")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            booking_manager.request_rental(email)
        elif choice == "2":
            user_manager.view_loyalty_points(email)
        elif choice == "3":
            user_manager.redeem_loyalty_points(email)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def admin_menu():
    """
    Displays the admin menu after login.
    """
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Car")
        print("2. Approve Rental Requests")
        print("3. Update Car Loyalty Points")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            car_manager.add_car()
        elif choice == "2":
            booking_manager.approve_rental()
        elif choice == "3":
            car_manager.update_car_loyalty_points()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
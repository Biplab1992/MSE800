from user_manager import UserManager

def main():
    user_manager = UserManager()

    while True:
        print("\n=== Car Rental System ===")
        print("1. Register User")
        print("2. Login User")
        print("3. Check Customer Records")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            name = input("Enter your full name: ").strip()
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            user_manager.register_user(name, email, password)
        elif choice == "2":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            user_manager.login_user(email, password)
        elif choice == "3":
            email = input("Enter your email to check records: ").strip()
            user_manager.check_customer_records(email)
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main()

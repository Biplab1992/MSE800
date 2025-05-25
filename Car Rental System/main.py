from user_manager import UserManager
from booking_manager import BookingManager

user_manager = UserManager()
booking_manager = BookingManager()

def main():
    role, email = user_manager.login_user()

    if role == "customer":
        user_manager.view_loyalty_points(email)
        booking_manager.request_rental(email)
        user_manager.redeem_loyalty_points(email)

    elif role == "admin":
        booking_manager.approve_rental()

if __name__ == "__main__":
    main()
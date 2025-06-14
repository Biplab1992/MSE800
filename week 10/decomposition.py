import datetime

def log_event(message):
    """
    Logs an event with the current timestamp.
    
    This helper function formats the event message with a timestamp
    and appends it to the rental log file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    with open("rental_log.txt", "a") as log_file:
        log_file.write(log_message + "\n")

def view_available_cars(cars):
    """
    Displays a list of available cars.
    
    Iterates over the cars dictionary and prints only those cars
    that are currently available. It then logs the event.
    """
    print("\nAvailable Cars:")
    for car_id, details in cars.items():
        if details["available"]:
            print(f"{car_id} - {details['type']}")
    log_event("Viewed available cars")

def process_rental(cars, rentals, users):
    """
    Processes car rental requests.
    
    Checks if the input user is valid. If so, shows available cars,
    takes a car selection, and if the car is available, marks it as rented.
    Logs the rental event accordingly.
    """
    user_id = input("Enter your user ID: ")
    if user_id not in users:
        print("Invalid user.")
        return
    
    # Display the available cars for rental
    view_available_cars(cars)
    car_id = input("Enter Car ID to rent: ")

    if car_id in cars and cars[car_id]["available"]:
        cars[car_id]["available"] = False
        rentals[user_id] = car_id
        print(f"{user_id} rented {car_id}")
        log_event(f"{user_id} rented {car_id}")
    else:
        print("Car not available or invalid ID.")
        log_event(f"{user_id} failed to rent {car_id}")

def process_return(cars, rentals):
    """
    Processes the return of a rented car.
    
    Checks if the user has an active rental. If yes, returns the car,
    updates the rental record, and logs the event.
    """
    user_id = input("Enter your user ID: ")
    if user_id in rentals:
        car_id = rentals[user_id]
        cars[car_id]["available"] = True
        del rentals[user_id]
        print(f"{user_id} returned {car_id}")
        log_event(f"{user_id} returned {car_id}")
    else:
        print("No rental record found.")
        log_event(f"{user_id} attempted return with no rental")

def display_menu():
    """
    Displays the menu options and reads the user's choice.
    
    Returns:
        str: The menu choice entered by the user.
    """
    print("\n--- Car Rental System ---")
    print("1. View Available Cars")
    print("2. Rent a Car")
    print("3. Return a Car")
    print("4. Exit")
    return input("Enter your choice: ")

def car_rental_system():
    """
    Main function for the car rental system.
    
    Initializes the necessary data structures and runs the main loop,
    delegating tasks to the helper functions based on user input.
    """
    cars = {
        "CAR001": {"type": "SUV", "available": True},
        "CAR002": {"type": "Sedan", "available": True},
        "CAR003": {"type": "Hatchback", "available": True}
    }
    users = ["user1", "user2"]
    rentals = {}

    while True:
        choice = display_menu()

        if choice == "1":
            view_available_cars(cars)
        elif choice == "2":
            process_rental(cars, rentals, users)
        elif choice == "3":
            process_return(cars, rentals)
        elif choice == "4":
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")
            log_event("Invalid menu choice")

if __name__ == "__main__":
    car_rental_system()
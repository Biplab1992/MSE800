import firebase_admin
from firebase_admin import credentials, firestore

# --------------------------
# Firebase Initialization
# --------------------------
cred = credentials.Certificate(r"C:\Users\BEEPLOVE\Documents\GitHub\MSE800\Car_Rental_System\serviceAccount.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# --------------------------
# Helper Functions for Firestore Collections
# --------------------------
def get_users_collection():
    """
    Returns a reference to the 'users' subcollection located under:
    Car_Rental_System/UsersDirectory/users
    """
    return db.collection("Car_Rental_System").document("UsersDirectory").collection("users")

def get_cars_collection():
    """
    Returns a reference to the 'cars' subcollection located under:
    Car_Rental_System/CarsDirectory/cars
    """
    return db.collection("Car_Rental_System").document("CarsDirectory").collection("cars")

def get_rentals_collection():
    """
    Returns a reference to the 'Rentals' subcollection located under:
    Car_Rental_System/RentalDirectory/Rentals
    """
    return db.collection("Car_Rental_System").document("RentalDirectory").collection("Rentals")

def get_payments_collection():
    """
    Returns a reference to the 'payments' subcollection located under:
    Car_Rental_System/PaymentsDirectory/payments
    """
    return db.collection("Car_Rental_System").document("PaymentsDirectory").collection("payments")

# --------------------------
# User Management Functions
# --------------------------
def add_user(name, email, password, role="customer"):
    """
    Adds a new user document to the 'users' collection with default loyalty points set to 0.
    """
    user_data = {
        "name": name,
        "password": password,
        "role": role,
        "loyalty_points": 0
    }
    get_users_collection().document(email).set(user_data)
    print(f"User '{name}' added successfully.")

def get_user(email):
    """
    Retrieves a user document by email from the 'users' collection.
    Returns the document data as a dictionary if found; otherwise None.
    """
    doc = get_users_collection().document(email).get()
    return doc.to_dict() if doc.exists else None

# --------------------------
# Car Management Functions
# --------------------------
def add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points):
    """
    Adds a new car document to the 'cars' collection with the specified details.
    """
    car_data = {
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "available": bool(available),
        "min_rent_period": min_rent_period,
        "max_rent_period": max_rent_period,
        "bonus_points": bonus_points
    }
    get_cars_collection().document(car_id).set(car_data)
    print(f"Car {make} {model} (ID: {car_id}) added successfully.")

def list_cars():
    """
    Retrieves all car documents from the 'cars' collection and returns a list of dictionaries
    with car details, including the document ID as 'car_id'.
    """
    cars_ref = get_cars_collection()
    return [{**doc.to_dict(), "car_id": doc.id} for doc in cars_ref.stream()]

def update_car(car_id, updated_info):
    """
    Updates the car document with the given car_id using the provided updated_info dictionary.
    """
    get_cars_collection().document(car_id).update(updated_info)
    print(f"Car {car_id} updated successfully.")

def delete_car(car_id):
    """
    Deletes the car document with the specified car_id from the 'cars' collection.
    """
    get_cars_collection().document(car_id).delete()
    print(f"Car {car_id} deleted successfully.")

# --------------------------
# Rental Management Functions
# --------------------------
def add_rental(booking_id, customer_email, car_id, rental_days, total_cost):
    """
    Adds a new rental document to the 'Rentals' collection with a default status of 'Pending'.
    Each rental request is saved as a separate record.
    """
    rental_data = {
        "customer_email": customer_email,
        "car_id": car_id,
        "rental_days": rental_days,
        "total_cost": total_cost,
        "status": "Pending"
    }
    get_rentals_collection().document(booking_id).set(rental_data)
    print(f"Rental booking '{booking_id}' added successfully.")

def list_rentals():
    """
    Retrieves all rental documents from the 'Rentals' collection and returns a list of dictionaries
    with rental details, including the document ID as 'booking_id'.
    """
    rentals_ref = get_rentals_collection()
    return [{**doc.to_dict(), "booking_id": doc.id} for doc in rentals_ref.stream()]

def update_rental_status(booking_id, status):
    """
    Updates the status of a rental document with the given booking_id.
    """
    get_rentals_collection().document(booking_id).update({"status": status})
    print(f"Rental booking '{booking_id}' status updated to '{status}'.")

# --------------------------
# Payment Processing Functions
# --------------------------
def record_payment(customer_email, amount):
    """
    Stores payment transaction details in the 'payments' collection as a separate record.
    The payment is recorded with a status of 'Completed' and a server timestamp.
    """
    payment_data = {
        "customer_email": customer_email,
        "amount": amount,
        "status": "Completed",
        "timestamp": firestore.SERVER_TIMESTAMP  # Automatically assign a server timestamp.
    }
    # Using add() to let Firestore generate an auto ID for each payment record.
    doc_ref = get_payments_collection().add(payment_data)[1]
    print(f"Payment record saved for {customer_email} with document ID: {doc_ref.id}")

def get_payment_history(customer_email):
    """
    Retrieves all payment records for the specified customer from the 'payments' collection.
    Returns a list of payment records as dictionaries, or an empty list if no records exist.
    """
    payments_ref = get_payments_collection()
    docs = payments_ref.where("customer_email", "==", customer_email).stream()
    return [doc.to_dict() for doc in docs]

def get_customer_rentals(customer_email):
    """
    Retrieves all rental documents where the customer_email matches the provided value.
    Returns a list of rental dictionaries, or an empty list if no rentals are found.
    """
    rentals_ref = get_rentals_collection()
    docs = rentals_ref.where("customer_email", "==", customer_email).stream()
    return [doc.to_dict() for doc in docs]

def get_customer_payments(customer_email):
    """
    Retrieves all payment records for the specified customer from the 'payments' collection.
    Returns a list of payment records as dictionaries, or an empty list if no records exist.
    """
    payments_ref = get_payments_collection()
    docs = payments_ref.where("customer_email", "==", customer_email).stream()
    return [doc.to_dict() for doc in docs]
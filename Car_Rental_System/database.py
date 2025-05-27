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
# Helper functions for directories
# --------------------------
def get_users_collection():
    return db.collection("Car_Rental_System").document("UsersDirectory").collection("users")

def get_cars_collection():
    return db.collection("Car_Rental_System").document("CarsDirectory").collection("cars")

def get_rentals_collection():
    return db.collection("Car_Rental_System").document("RentalDirectory").collection("Rentals")

def get_payments_collection():
    """
    Returns a reference to the 'payments' subcollection under 'PaymentsDirectory'
    in the 'Car_Rental_System' collection.
    """
    return db.collection("Car_Rental_System").document("PaymentsDirectory").collection("payments")

# --------------------------
# User Management Functions
# --------------------------
def add_user(name, email, password, role="customer"):
    user_data = {
        "name": name,
        "password": password,
        "role": role,
        "loyalty_points": 0
    }
    get_users_collection().document(email).set(user_data)
    print(f"User '{name}' added successfully.")

def get_user(email):
    doc = get_users_collection().document(email).get()
    return doc.to_dict() if doc.exists else None

# --------------------------
# Car Management Functions
# --------------------------
def add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points):
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
    cars_ref = get_cars_collection()
    return [{**doc.to_dict(), "car_id": doc.id} for doc in cars_ref.stream()]

def update_car(car_id, updated_info):
    get_cars_collection().document(car_id).update(updated_info)
    print(f"Car {car_id} updated successfully.")

def delete_car(car_id):
    get_cars_collection().document(car_id).delete()
    print(f"Car {car_id} deleted successfully.")

# --------------------------
# Rental Management Functions
# --------------------------
def add_rental(booking_id, customer_email, car_id, rental_days, total_cost):
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
    rentals_ref = get_rentals_collection()
    return [{**doc.to_dict(), "booking_id": doc.id} for doc in rentals_ref.stream()]

def update_rental_status(booking_id, status):
    get_rentals_collection().document(booking_id).update({"status": status})

# --------------------------
# Payment Processing Functions (NEW)
# --------------------------
def record_payment(customer_email, amount):
    """
    Stores payment transaction details in Firestore under:
    Car_Rental_System/PaymentsDirectory/payments/{customer_email}
    """
    payment_data = {
        "customer_email": customer_email,
        "amount": amount,
        "status": "Completed"
    }
    get_payments_collection().document(customer_email).set(payment_data)
    print(f"Payment record saved for {customer_email}.")

def get_payment_history(customer_email):
    """
    Retrieves payment records for a specific customer.
    Returns None if no record exists.
    """
    doc = get_payments_collection().document(customer_email).get()
    return doc.to_dict() if doc.exists else None

def get_customer_rentals(customer_email):
    """
    Retrieves all rental records for a specific customer from Firestore.
    """
    rentals_ref = get_rentals_collection()
    docs = rentals_ref.where("customer_email", "==", customer_email).stream()
    
    rental_history = [doc.to_dict() for doc in docs]
    return rental_history if rental_history else None

def get_customer_payments(customer_email):
    """
    Retrieves payment history for a specific customer from Firestore.
    """
    doc = get_payments_collection().document(customer_email).get()
    return doc.to_dict() if doc.exists else None
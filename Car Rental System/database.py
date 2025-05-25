# database.py

# Dictionary for storing user details (key: email, value: dictionary with user info)
users = {}

# Dictionary for storing car details (key: car ID, value: car attributes)
cars = {}

# Dictionary for storing rental bookings (key: booking ID, value: booking details)
rental_requests = {}

# Dictionary for loyalty program (key: email, value: points earned)
loyalty_points = {}

# Dictionary for reward tiers (Bronze, Silver, Gold)
reward_tiers = {"Bronze": 0, "Silver": 100, "Gold": 250}

def add_user(name, email, password, role="customer"):
    """
    Adds a new user to the database with a specified role and initializes loyalty points.
    """
    users[email] = {
        "name": name,
        "password": password,
        "role": role  # Either 'customer' or 'admin'
    }
    loyalty_points[email] = 0  # Initialize points at zero

def get_user(email):
    """
    Retrieves user data by email.
    """
    return users.get(email)

def add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period):
    """
    Adds a car to the database.
    """
    cars[car_id] = {
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "available": available,
        "min_rent_period": min_rent_period,
        "max_rent_period": max_rent_period
    }

def update_car(car_id, updated_info):
    """
    Updates car details.
    """
    if car_id in cars:
        cars[car_id].update(updated_info)
        return True
    return False

def delete_car(car_id):
    """
    Deletes a car from the database.
    """
    return cars.pop(car_id, None)

def view_available_cars():
    """
    Returns cars that are currently available.
    """
    return {car_id: details for car_id, details in cars.items() if details["available"]}

def add_rental_request(booking_id, customer_email, car_id, rental_days, total_cost):
    """
    Adds a rental request.
    """
    rental_requests[booking_id] = {
        "customer": customer_email,
        "car_id": car_id,
        "rental_days": rental_days,
        "total_cost": total_cost,
        "status": "Pending"
    }

def manage_rental_request(booking_id, approval):
    """
    Admin approves or rejects a rental request.
    """
    if booking_id in rental_requests:
        rental_requests[booking_id]["status"] = "Approved" if approval else "Rejected"
        return True
    return False

def add_loyalty_points(email, points):
    """
    Adds loyalty points to a customer's account.
    """
    if email in loyalty_points:
        loyalty_points[email] += points
        return True
    return False

def get_loyalty_points(email):
    """
    Retrieves the loyalty points of a customer.
    """
    return loyalty_points.get(email, 0)

def get_reward_tier(email):
    """
    Determines the reward tier based on points.
    """
    points = loyalty_points.get(email, 0)
    if points >= reward_tiers["Gold"]:
        return "Gold"
    elif points >= reward_tiers["Silver"]:
        return "Silver"
    return "Bronze"

def redeem_loyalty_points(email, points_to_redeem):
    """
    Allows customers to redeem points for discounts.
    """
    if loyalty_points.get(email, 0) >= points_to_redeem:
        loyalty_points[email] -= points_to_redeem
        return True
    return False
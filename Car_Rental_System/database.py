import sqlite3
import os

# Ensure database directory exists
os.makedirs("database", exist_ok=True)

DB_PATH = "Car_Rental_System/database/rental_system.db"

def create_tables():
    """
    Creates all necessary tables in the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            loyalty_points INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id TEXT PRIMARY KEY,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER NOT NULL,
            available INTEGER NOT NULL CHECK (available IN (0,1)),
            min_rent_period INTEGER NOT NULL,
            max_rent_period INTEGER NOT NULL,
            bonus_points INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            booking_id TEXT PRIMARY KEY,
            customer_email TEXT NOT NULL,
            car_id TEXT NOT NULL,
            rental_days INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(customer_email) REFERENCES users(email),
            FOREIGN KEY(car_id) REFERENCES cars(car_id)
        )
    """)

    conn.commit()
    conn.close()

# Call to create tables when the system starts
create_tables()

# User Management Functions
def add_user(name, email, password, role="customer"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, name, password, role) VALUES (?, ?, ?, ?)", (email, name, password, role))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cars (car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (car_id, make, model, year, mileage, available, min_rent_period, max_rent_period, bonus_points))
    conn.commit()
    conn.close()

def list_cars():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return cars

def update_car(car_id, updated_info):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for key, value in updated_info.items():
        cursor.execute(f"UPDATE cars SET {key} = ? WHERE car_id = ?", (value, car_id))
    conn.commit()
    conn.close()

def delete_car(car_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE car_id=?", (car_id,))
    conn.commit()
    conn.close()
import sqlite3
from database import create_connection

def add_user(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("✅ User added successfully.")
    except sqlite3.IntegrityError:
        print("⚠️ Email must be unique.")
    conn.close()

def view_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows if rows else print("⚠️ No users found.")

def search_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows if rows else print("⚠️ No matching user found.")

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    print("🗑️ User deleted successfully.")

def advanced_search(user_id, name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ? AND name LIKE ?", (user_id, '%' + name + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows if rows else print("⚠️ No matching user found for the given ID and name.")

def create_course_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            units INTEGER NOT NULL,
            UNIQUE(id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_course(course_id, course_name, units):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO courses (id, name, units) VALUES (?, ?, ?)", (course_id, course_name, units))
        conn.commit()
        print("📚 Course added successfully.")
    except sqlite3.IntegrityError:
        print("⚠️ Course ID must be unique.")
    conn.close()

def search_course(course_id, user_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.* FROM courses 
        JOIN users ON users.name LIKE ? 
        WHERE courses.id = ?
    """, ('%' + user_name + '%', course_id))
    rows = cursor.fetchall()
    conn.close()
    return rows if rows else print("⚠️ No matching course found.")
from database import create_table, create_connection
from user_manager import add_user, view_users, search_user, delete_user, advanced_search, insert_course, search_course

def menu():
    print("\n==== User & Course Manager ====")
    print("1. Add User")
    print("2. View All Users")
    print("3. Search User by Name")
    print("4. Delete User by ID")
    print("5. Advanced Search by ID and Name")
    print("6. Add Course")
    print("7. Search Course by Course ID and User Name")
    print("8. Exit")

def main():
    create_table()  # Ensures users and courses tables exist before running
    
    while True:
        menu()
        choice = input("Select an option (1-8): ")
        
        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            add_user(name, email)
        
        elif choice == '2':
            users = view_users()
            if users:
                for user in users:
                    print(user)
            else:
                print("⚠️ No users found.")
        
        elif choice == '3':
            name = input("Enter name to search: ")
            users = search_user(name)
            if users:
                for user in users:
                    print(user)
            else:
                print("⚠️ No matching user found.")
        
        elif choice == '4':
            user_id = input("Enter user ID to delete: ")
            try:
                user_id = int(user_id)
                delete_user(user_id)
            except ValueError:
                print("❌ Invalid ID format. Please enter a number.")
        
        elif choice == '5':
            user_id = input("Enter user ID: ")
            name = input("Enter name: ")
            try:
                user_id = int(user_id)
                users = advanced_search(user_id, name)
                if users:
                    for user in users:
                        print(user)
                else:
                    print("⚠️ No matching user found. Check the ID and name.")
            except ValueError:
                print("❌ Invalid ID format. Please enter a number.")
        
        elif choice == '6':
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            units = input("Enter course units: ")
            try:
                course_id = int(course_id)
                units = int(units)
                insert_course(course_id, course_name, units)
            except ValueError:
                print("❌ Invalid course ID or units format. Please enter numbers.")
        
        elif choice == '7':
            course_id = input("Enter course ID: ")
            user_name = input("Enter user name: ")
            try:
                course_id = int(course_id)
                courses = search_course(course_id, user_name)
                if courses:
                    for course in courses:
                        print(course)
                else:
                    print("⚠️ No matching course found.")
            except ValueError:
                print("❌ Invalid course ID format. Please enter a number.")
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
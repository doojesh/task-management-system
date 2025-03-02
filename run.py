from user import User
from connector import save_user, load_user, save_tasks, load_tasks
from authentication_manager import AuthMgr

def register():
    print("Enter Agent Details")
    agent_id = input("🔹 Agent ID: ")
    username = input("👤 Username: ")
    password = input("🔑 Password: ")
    full_name = input("📝 Full Name: ")
    email = input("📧 Email Address: ")
    phone = input("📞 Phone Number: ")
    clearance_level = input("🔒 Clearance Level (Top Secret / Secret / Confidential): ")
    role = input("🎭 Role (Field Agent, Analyst, Director, etc.): ")

    user = User(agent_id, username, password, full_name, email, phone, clearance_level, role)
    save_user(user)
    print("******************************")
    print("Account Created successfully!")
    print("******************************")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = load_user(username)
    if user and user.verify_password(password):
        user.update_last_login()
        print("Login successful!")
        return user
    else:
        print("Invalid credentials.")
        return None

def run():
    print("*** Task Management System ***")
    print("1. Create an Account")
    print("2. Access your Account")
    print("******************************")
    choice = input("Choose an option: ")
    print("******************************")
    if choice == "1":
        register()
    elif choice == "2":
        user = login()
        if user:
            auth = AuthMgr()
            otp = auth.generate_otp()
            print(f"Your OTP: {otp}")

            user_otp = input("Enter OTP: ")
            if auth.verify_otp(user_otp):
                print("Access granted.")
                
                # Load all tasks on login
                user.tasks = load_tasks(user.username)

                while True:
                    print("\n1. Create a New Task")
                    print("2. Show My Tasks")
                    print("3. Unlock Task Details")
                    print("4. Exit")
                    option = input("\nSelect an option: ")
                    print("******************************")
                    if option == "1":
                        desc = input("Enter task description: ")
                        due_date = input("Enter due date: ")
                        classification = input("Enter classification (Top Secret, Secret, Confidential): ")
                        user.add_task(desc, due_date, classification)

                        # Save tasks after adding
                        save_tasks(user.username, user.tasks)
                        print("Task added successfully.")
                        print("******************************")
                    elif option == "2":
                        # Ensure all tasks are displayed
                        tasks = user.view_tasks()
                        print("Tasks:", tasks)
                    
                    elif option == "3":
                        password = input("Re-enter password: ")
                        print(user.decrypt_tasks(password))
                    
                    elif option == "4":
                        print("Exiting...")
                        save_tasks(user.username, user.tasks)  # Save tasks before logout
                        break
                    else:
                        print("Invalid option. Try again.")
            else:
                print("Invalid OTP. Access Denied.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    run()

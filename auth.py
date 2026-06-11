import json
from models.user import User

USERS_FILE = "data/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def register_user(username, password, role="member"):
    users = load_users()

    for user in users:
        if user["username"] == username:
            print("User already exists!")
            return

    new_user = User(username, password, role)
    users.append(new_user.to_dict())
    save_users(users)
    print("User registered successfully!")

def login(username, password):
    users = load_users()

    for user in users:
        temp_user = User(username, password)
        temp_user.password = user["password"]

        if user["username"] == username and temp_user.verify_password(password):
            print(f"Welcome {username}!")
            return True

    print("Invalid username or password.")
    return False 

def logout():
    print("User logged out successfully.")
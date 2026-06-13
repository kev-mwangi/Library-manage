import json
import hashlib
from models.user import User

current_user = None

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
    global current_user

    users = load_users()

    for user in users:
        if user["username"] == username:
            hashed_password = hashlib.sha256(
                password.encode()
            ).hexdigest()

            if user["password"] == hashed_password:
                current_user = user
                print(f"Welcome {username}!")
                return True

    print("Invalid username or password.")
    return False


def logout():
    global current_user

    if current_user:
        print(f"{current_user['username']} logged out.")
        current_user = None
    else:
        print("No user is logged in.")
import json
from models.user import User

USERS_FILE = "data/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
import os
import json


USERS_FILE = "users.json"

def load_users():
    """Load user data from the JSON file."""
    if not os.path.exists(USERS_FILE):
        # Create an empty JSON file if it doesn't exist
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)  # Initialize with an empty dictionary
        return {}

    try:
        # Load existing user data
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, ValueError):
        # If the file is corrupted, reset it to an empty dictionary
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)
        return {}

def save_users(users):
    """Save user data to the JSON file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def add_user(chat_id):
    """Add a new user to the JSON file."""
    users = load_users()
    if str(chat_id) not in users:
        users[str(chat_id)] = {"ticker": None}
        save_users(users)

def update_user_ticker(chat_id, ticker):
    """Update the stock ticker for an existing user."""
    users = load_users()
    if str(chat_id) in users:
        users[str(chat_id)]["ticker"] = ticker
        save_users(users)

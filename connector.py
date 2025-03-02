import json
import os
from user import User

USER_DB = "users.json"
TASK_DB = "tasks.json"

def save_user(user):
    """Save user data to the users database (JSON file)."""
    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    users[user.username] = user.to_dict()

    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def load_user(username):
    """Load user data from the users database."""
    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    if username in users:
        return User.from_dict(users[username])
    
    return None

def save_tasks(username, tasks):
    """Save tasks to a separate tasks file per user."""
    try:
        with open(TASK_DB, "r") as f:
            all_tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_tasks = {}

    all_tasks[username] = tasks

    with open(TASK_DB, "w") as f:
        json.dump(all_tasks, f, indent=4)

def load_tasks(username):
    """Load tasks for a specific user."""
    try:
        with open(TASK_DB, "r") as f:
            all_tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return all_tasks.get(username, [])


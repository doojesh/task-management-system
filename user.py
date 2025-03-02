import bcrypt
import json
from crypto_utils import AESCipher
from datetime import datetime

class User:
    def __init__(self, agent_id, username, password, full_name, email, phone, clearance_level, role):
        self.agent_id = agent_id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.clearance_level = clearance_level  # e.g., "Top Secret", "Secret", "Confidential"
        self.role = role  
        self.status = "Active"  # Default status is active
        self.last_login = None  # Updated on successful login

        # Secure Password Storage
        self.hashed_password = self.hash_password(password)

        # Use a separate key for encryption
        self.encryption_key = password  # Using the raw password here ensures AES encryption consistency
        self.aes_cipher = AESCipher(self.encryption_key)

        # Store Encrypted Tasks
        self.tasks = []  

    def hash_password(self, password):
        """Hash the user's password for secure storage"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password):
        """Verify user password against stored hash"""
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    def add_task(self, task_description, due_date, classification):
        """Encrypt and add a task"""
        task = {
            "description": self.aes_cipher.encrypt(task_description),
            "due_date": due_date,
            "classification": self.aes_cipher.encrypt(classification),
        }
        self.tasks.append(task)

    def view_tasks(self):
        """View all tasks with redacted sensitive details."""
        if not self.tasks:
            self.tasks = load_tasks(self.username)
        
        return [{"due_date": task["due_date"], "classification": "[REDACTED]"} for task in self.tasks]

    def decrypt_tasks(self, password):
        """Decrypt tasks only if correct password is provided"""
        if not self.verify_password(password):
            return "Authentication failed."

        decrypted_tasks = [
            {
                "description": self.aes_cipher.decrypt(task["description"]),
                "due_date": task["due_date"],
                "classification": self.aes_cipher.decrypt(task["classification"]),
            }
            for task in self.tasks
        ]
        return decrypted_tasks

    def update_last_login(self):
        """Update last login timestamp when user logs in."""
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def deactivate_user(self):
        """Deactivate the agent's account."""
        self.status = "Inactive"

    def activate_user(self):
        """Reactivate the agent's account."""
        self.status = "Active"

    def to_dict(self):
        """Convert user object to a dictionary for storage"""
        return {
            "agent_id": self.agent_id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "clearance_level": self.clearance_level,
            "role": self.role,
            "status": self.status,
            "last_login": self.last_login,
            "hashed_password": self.hashed_password,
            "tasks": self.tasks,
        }

    @classmethod
    def from_dict(cls, data):
        """Recreate a user object from stored dictionary data"""
        user = cls(
            data["agent_id"], data["username"], "temp_password", 
            data["full_name"], data["email"], data["phone"], 
            data["clearance_level"], data["role"]
        )
        user.hashed_password = data["hashed_password"]
        user.tasks = data["tasks"]
        user.status = data["status"]
        user.last_login = data["last_login"]
        return user
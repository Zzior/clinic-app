import json
import hashlib
from pathlib import Path
from src.services.data_classes import SessionInfo, AccessLevel


class AuthenticationService:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        # Load existing users if the file exists, otherwise initialize an empty dictionary
        if config_path.exists():
            with open(config_path, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}
            self.save_data()

    def save_data(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def register_user(self, access_level: AccessLevel, login: str, password: str) -> SessionInfo | None:
        if login in self.users:
            return None  # User already exists
        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[login] = {
            'access_level': access_level.value,
            'password': hashed_password
        }
        self.save_data()
        return SessionInfo(access_level=access_level, login=login)

    def authenticate(self, login: str, password: str) -> SessionInfo | None:
        user = self.users.get(login)
        if not user:
            return None  # User does not exist
        # Check the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user['password'] == hashed_password:
            return SessionInfo(access_level=AccessLevel(user['access_level']), login=login)
        return None  # Incorrect password

from dataclasses import dataclass
from .user import User

@dataclass
class NotificationChannel:
    def __init__(self, user_name: User, message: str, priority: str):
        self.user_name = user_name
        self.message = message
        self.priority = priority
from dataclasses import dataclass

@dataclass
class NotificationChannel:
    def __init__(self, user_name: str, message: str, priority: str):
        self.user_name = user_name
        self.message = message
        self.priority = priority
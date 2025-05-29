# notification_system/models.py
import uuid

class User:
    """
    Represents a user in the notification system.
    """
    def __init__(self, name: str, preferred_channel: str, available_channels: list[str]):
        if not name or not isinstance(name, str):
            raise ValueError("User name must be a non-empty string.")
        if not preferred_channel or not isinstance(preferred_channel, str):
            raise ValueError("Preferred channel must be a non-empty string.")
        if not isinstance(available_channels, list) or not all(isinstance(c, str) for c in available_channels):
            raise ValueError("Available channels must be a list of strings.")
        
        # Validate channel types
        allowed_channels = ["email", "sms"]
        if not all(c in allowed_channels for c in available_channels):
            raise ValueError(f"Invalid channel(s) in available_channels. Allowed: {', '.join(allowed_channels)}")
        if preferred_channel not in available_channels:
            raise ValueError("Preferred channel must be one of the available channels.")
        if preferred_channel not in allowed_channels:
            raise ValueError(f"Invalid preferred_channel. Allowed: {', '.join(allowed_channels)}")


        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
        self.user_id = str(uuid.uuid4()) # Unique ID for the user

    def to_dict(self) -> dict:
        """
        Converts the User object to a dictionary.
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

class Notification:
    """
    Represents a notification to be sent.
    """
    def __init__(self, user_name: str, message: str, priority: str):
        if not user_name or not isinstance(user_name, str):
            raise ValueError("User name must be a non-empty string.")
        if not message or not isinstance(message, str):
            raise ValueError("Message must be a non-empty string.")
        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be 'high', 'medium', or 'low'.")

        self.user_name = user_name
        self.message = message
        self.priority = priority

    def to_dict(self) -> dict:
        """
        Converts the Notification object to a dictionary.
        """
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }
# models.py
from typing import List, Dict, Any

# Usaremos diccionarios para almacenar usuarios en memoria
# Estructura: {"user_name": {"name": "Juan", "preferred_channel": "email", "available_channels": ["email", "sms"]}}
users_db: Dict[str, Dict[str, Any]] = {}

class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        return User(
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            available_channels=data['available_channels']
        )
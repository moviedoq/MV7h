class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: list[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

        # validación
        if preferred_channel not in available_channels:
            raise ValueError("Canal preferido debe estar en la lista de canales disponibles")
        
        def __repr__(self):
            return f"<User {self.name} - prefers {self.preferred_channel}>"

class Notification:
    def __init__(self, message: str, priority: str):
        self.message = message
        self.priority = priority

    def __repr__(self):
        return f"<Notification [{self.priority}] {self.message}>"


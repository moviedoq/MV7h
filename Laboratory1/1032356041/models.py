# Clase que representa a un usuario
class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: list):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
    
    # Convierte el usuario a un diccionario (útil para respuestas JSON)
    def to_dict(self):
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels
        }
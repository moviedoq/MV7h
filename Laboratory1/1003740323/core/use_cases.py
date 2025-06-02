from typing import List, Optional
from core.domain import User, Notification

# Interfaces
class UserRepositoryPort:
    """Puerto para el repositorio de usuarios."""
    def save(self, user: User) -> User:
        raise NotImplementedError
    
    def find_by_name(self, name: str) -> Optional[User]:
        raise NotImplementedError


class NotificationSenderPort:
    """Puerto para el envío de notificaciones."""
    def send(self, user: User, notification: Notification) -> bool:
        raise NotImplementedError


# Casos de uso
class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        if preferred_channel not in available_channels:
            raise ValueError("El canal preferido no está disponible")
        
        user = User(name, preferred_channel, available_channels)
        return self.user_repository.save(user)


class SendNotificationUseCase:
    def __init__(self, 
                 user_repository: UserRepositoryPort,
                 handlers: list):  # Lista de funciones (email.py, sms.py)
        self.user_repository = user_repository
        self.handlers = handlers

    def execute(self, user_name: str, message: str, priority: str) -> bool:
        user = self.user_repository.find_by_name(user_name)
        if not user:
            raise ValueError("Usuario no encontrado")

        # Chain of Responsibility
        for handler in self.handlers:
            if handler(user, message):  # Ejemplo: send_email(user, message)
                return True
        return False
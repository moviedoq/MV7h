import random
from abc import ABC, abstractmethod
from logger import logger

# Clase base abstracta para los handlers de notificación
class NotificationHandler(ABC):
    def __init__(self):
        self._next_handler = None
    
    # Configura el siguiente handler en la cadena
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, user, message: str, channel: str) -> bool:
        pass
    
    # Simula el éxito o fracaso del envío
    def _simulate_delivery(self) -> bool:
        return random.choice([True, False])

# Handler para notificaciones por email
class EmailHandler(NotificationHandler):
    def handle(self, user, message: str, channel: str) -> bool:
        if channel == "email":
            logger.log(f"Attempting to send email to {user.name}: {message}")
            success = self._simulate_delivery()
            if success:
                logger.log(f"SUCCESS: Email sent to {user.name}")
                return True
            else:
                logger.log(f"FAILED: Email delivery failed for {user.name}")
        
        # Si no es el canal o falla, pasa al siguiente handler
        if self._next_handler:
            return self._next_handler.handle(user, message, channel)
        return False

# Handler para notificaciones por SMS
class SMSHandler(NotificationHandler):
    def handle(self, user, message: str, channel: str) -> bool:
        if channel == "sms":
            logger.log(f"Attempting to send SMS to {user.name}: {message}")
            success = self._simulate_delivery()
            if success:
                logger.log(f"SUCCESS: SMS sent to {user.name}")
                return True
            else:
                logger.log(f"FAILED: SMS delivery failed for {user.name}")
        
        if self._next_handler:
            return self._next_handler.handle(user, message, channel)
        return False

# Handler para notificaciones por consola
class ConsoleHandler(NotificationHandler):
    def handle(self, user, message: str, channel: str) -> bool:
        if channel == "console":
            logger.log(f"Attempting to send console notification to {user.name}: {message}")
            print(f"CONSOLE NOTIFICATION for {user.name}: {message}")
            logger.log(f"SUCCESS: Console notification sent to {user.name}")
            return True
        
        if self._next_handler:
            return self._next_handler.handle(user, message, channel)
        return False

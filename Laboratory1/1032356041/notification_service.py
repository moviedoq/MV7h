from handlers import EmailHandler, SMSHandler, ConsoleHandler
from logger import logger

class NotificationService:
    def __init__(self):
        # Construir la cadena de responsabilidad
        self.email_handler = EmailHandler()
        self.sms_handler = SMSHandler()
        self.console_handler = ConsoleHandler()
        
        # Configurar el orden de los handlers
        self.email_handler.set_next(self.sms_handler).set_next(self.console_handler)
    
    def send_notification(self, user, message: str, priority: str) -> str:
        logger.log(f"Processing notification for {user.name} with priority {priority}")
        
        # Intentar primero el canal preferido
        preferred_success = self._try_channel(user, message, user.preferred_channel)
        if preferred_success:
            return f"Notification sent successfully via {user.preferred_channel}"
        
        # Intentar otros canales disponibles
        for channel in user.available_channels:
            if channel != user.preferred_channel:
                success = self._try_channel(user, message, channel)
                if success:
                    return f"Notification sent successfully via {channel} (fallback)"
        
        logger.log(f"All notification attempts failed for {user.name}")
        return "All notification attempts failed"
    
    def _try_channel(self, user, message: str, channel: str) -> bool:
        # Llama al handler correspondiente según el canal
        if channel == "email":
            return self.email_handler.handle(user, message, channel)
        elif channel == "sms":
            return self.sms_handler.handle(user, message, channel)
        elif channel == "console":
            return self.console_handler.handle(user, message, channel)
        return False

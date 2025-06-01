from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler
from handlers.console_handler import ConsoleHandler

class HandlerFactory:
    @staticmethod
    def create_handler_chain(order=None):
        """Crea la cadena de handlers con un orden personalizado"""
        order = order or ["email", "sms", "console"]
        
        # Crear handlers en orden inverso
        current = None
        for channel in reversed(order):
            if channel == "email":
                current = EmailHandler(current)
            elif channel == "sms":
                current = SMSHandler(current)
            elif channel == "console":
                current = ConsoleHandler(current)
        
        return current
    
    @staticmethod
    def create_preferred_handler(user):
        """Crea una cadena con el canal preferido primero"""
        preferred = user.preferred_channel
        other_channels = [c for c in user.available_channels if c != preferred]
        return HandlerFactory.create_handler_chain([preferred] + other_channels)
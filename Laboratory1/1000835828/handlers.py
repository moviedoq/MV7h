import random
from notification import logger

class NotificationHandler:
    def __init__(self, channel_name, next_handler=None):
        self.channel_name = channel_name
        self.next = next_handler
    
    def handle(self, user, message):
        if self.channel_name in user.available_channels:
            # Simular fallo aleatorio (50% de éxito)
            success = random.choice([True, False])
            logger.log(f"Intentando {self.channel_name} para {user.name}: {'Éxito' if success else 'Fallo'}")
            
            if success:
                return {
                    "status": "success",
                    "channel": self.channel_name,
                    "message": message
                }
        
        if self.next:
            return self.next.handle(user, message)
        
        return {
            "status": "error",
            "message": "Todos los canales fallaron"
        }

class EmailHandler(NotificationHandler):
    def __init__(self, next_handler=None):
        super().__init__("email", next_handler)

class SMSHandler(NotificationHandler):
    def __init__(self, next_handler=None):
        super().__init__("sms", next_handler)

class ConsoleHandler(NotificationHandler):
    def __init__(self, next_handler=None):
        super().__init__("console", next_handler)

def create_handler_chain():
    # Crear la cadena: Email -> SMS -> Console
    console_handler = ConsoleHandler()
    sms_handler = SMSHandler(console_handler)
    email_handler = EmailHandler(sms_handler)
    return email_handler
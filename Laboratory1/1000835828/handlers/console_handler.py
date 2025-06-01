from .base_handler import BaseHandler
from utils.logger import logger

class ConsoleHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__("console", next_handler)
    
    def handle(self, user, message):
        # Comportamiento especial: siempre tiene éxito si está disponible
        if self.channel_name in user.available_channels:
            logger.log(f"Intentando {self.channel_name} para {user.name}: Éxito")
            return {
                "status": "success",
                "channel": self.channel_name,
                "message": message
            }
        
        # Si no está disponible, pasa al siguiente handler
        if self.next:
            return self.next.handle(user, message)
        
        return None
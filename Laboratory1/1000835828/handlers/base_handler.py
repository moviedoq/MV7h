import random
from utils.logger import logger

class BaseHandler:
    def __init__(self, channel_name, next_handler=None):
        self.channel_name = channel_name
        self.next = next_handler
    
    def handle(self, user, message):
        if self.channel_name in user.available_channels:
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
        
        return None
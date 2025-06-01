import random
from domain.ports import NotificationChannel
from infrastructure.logger import Logger  # importa el logger

class SMSChannelHandler(NotificationChannel):
    def send(self, user, message):
        logger = Logger()
        logger.log(f"Trying to send SMS to {user.name}: {message}")
        
        success = random.choice([True, False])
        logger.log(f"SMS notification to {user.name} {'succeeded' if success else 'failed'}")
        
        return success

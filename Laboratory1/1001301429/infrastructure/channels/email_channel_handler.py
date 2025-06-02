import random
from domain.ports import NotificationChannel
from infrastructure.logger import Logger  # importa el logger

class EmailChannelHandler(NotificationChannel):
    def send(self, user, message):
        logger = Logger()
        logger.log(f"Trying to send EMAIL to {user.name}: {message}")
        
        success = random.choice([True, False])
        logger.log(f"EMAIL notification to {user.name} {'succeeded' if success else 'failed'}")
        
        return success

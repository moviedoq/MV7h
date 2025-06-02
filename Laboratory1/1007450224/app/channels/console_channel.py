from .base_channel import BaseChannel
import random

class ConsoleChannel(BaseChannel):
    def handle(self, message, logger):
        success = random.choice([True, False])
        logger.log("Trying Console channel...")
        if success:
            logger.log(f"Console displayed: {message}")
            return True
        elif self.next_channel:
            return self.next_channel.handle(message, logger)
        else:
            logger.log("All channels failed.")
            return False

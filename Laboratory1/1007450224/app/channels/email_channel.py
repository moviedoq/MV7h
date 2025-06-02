from .base_channel import BaseChannel
import random

class EmailChannel(BaseChannel):
    def handle(self, message, logger):
        success = random.choice([True, False])
        logger.log("Trying Email channel...")
        if success:
            logger.log(f"Email sent: {message}")
            return True
        elif self.next_channel:
            return self.next_channel.handle(message, logger)
        else:
            logger.log("All channels failed.")
            return False

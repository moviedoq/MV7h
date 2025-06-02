from channels.channel import Channel
import random
from utils.logger import Logger

class EmailChannel(Channel):
    def send_notification(self, message: str, user_name: str) -> bool:
        logger = Logger()
        success = random.choice([True, False])
        log_msg = f"EmailChannel: Attempt to send to {user_name} - {'Success' if success else 'Failure'}"
        logger.log(log_msg)
        if success:
            print(f"Email sent to {user_name}: {message}")
            return True
        else:
            print(f"Failed to send email to {user_name}.")
            return False

    def get_channel_name(self) -> str:
        return "email"
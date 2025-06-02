from channels.channel import Channel
import random
from utils.logger import Logger

class SmsChannel(Channel):
    def send_notification(self, message: str, user_name: str) -> bool:
        logger = Logger()
        success = random.choice([True, False])
        log_msg = f"SmsChannel: Attempt to send to {user_name} - {'Success' if success else 'Failure'}"
        logger.log(log_msg)
        if success:
            print(f"SMS sent to {user_name}: {message}")
            return True
        else:
            print(f"Failed to send SMS to {user_name}.")
            return False

    def get_channel_name(self) -> str:
        return "sms"
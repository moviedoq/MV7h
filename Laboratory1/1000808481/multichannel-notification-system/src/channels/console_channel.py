from channels.channel import Channel
from utils.logger import Logger

class ConsoleChannel(Channel):
    def send_notification(self, message: str, user_name: str) -> bool:
        logger = Logger()
        log_msg = f"ConsoleChannel: Attempt to send to {user_name} - Success"
        logger.log(log_msg)
        print(f"Sending message to console for {user_name}: {message}")
        return True

    def get_channel_name(self) -> str:
        return "console"
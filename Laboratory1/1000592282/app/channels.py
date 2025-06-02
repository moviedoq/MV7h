import random

class Channel:
    def __init__(self, next_channel=None):
        self.next_channel = next_channel

    def send(self, message, user_name):
        raise NotImplementedError

class EmailChannel(Channel):
    def send(self, message, user_name):
        if random.choice([True, False]):
            print(f"Email sent to {user_name}: {message}")
            return True
        print("Email failed")
        return self.next_channel.send(message, user_name) if self.next_channel else False

class SMSChannel(Channel):
    def send(self, message, user_name):
        if random.choice([True, False]):
            print(f"SMS sent to {user_name}: {message}")
            return True
        print("SMS failed")
        return self.next_channel.send(message, user_name) if self.next_channel else False

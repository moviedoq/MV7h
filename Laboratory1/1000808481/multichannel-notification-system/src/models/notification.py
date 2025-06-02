class Notification:
    def __init__(self, user_name, message, priority):
        self.user_name = user_name
        self.message = message
        self.priority = priority

    def __repr__(self):
        return f"Notification(user_name={self.user_name}, message={self.message}, priority={self.priority})"
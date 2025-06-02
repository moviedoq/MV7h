from models.user import User

VALID_CHANNELS = {"email", "sms", "console"}

class UserService:
    def __init__(self):
        self.users = []

    def add_user(self, name, preferred_channel, available_channels):
        # Check for missing fields
        if not name or not preferred_channel or not available_channels:
            return None, "Missing required fields"
        # Check for duplicate user
        if self.find_user(name):
            return None, "User already exists"
        # Validate channels
        if preferred_channel not in VALID_CHANNELS:
            return None, "Invalid preferred channel"
        if not set(available_channels).issubset(VALID_CHANNELS):
            return None, "Invalid available channels"
        if preferred_channel not in available_channels:
            return None, "Preferred channel must be in available channels"
        user = User(name, preferred_channel, available_channels)
        self.users.append(user)
        return user, None

    def get_users(self):
        return self.users
    
    def find_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None
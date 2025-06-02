class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def register_user(self, user_data):
        name = user_data.get('name')
        preferred_channel = user_data.get('preferred_channel')
        available_channels = user_data.get('available_channels')
        user, error = self.user_service.add_user(name, preferred_channel, available_channels)
        if error == "User already exists":
            return {"error": error}, 409
        elif error:
            return {"error": error}, 400
        return {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }, 201

    def list_users(self):
        users = self.user_service.get_users()
        return [
            {
                "name": user.name,
                "preferred_channel": user.preferred_channel,
                "available_channels": user.available_channels
            }
            for user in users
        ], 200
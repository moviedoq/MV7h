from models import notification

class users:
    def __init__(self, all_users=None):
        self.all_users = all_users

    def get_user(self, user_name):
        for i in self.all_users:
            if i['name'] == user_name:
                return i
        return None
    
    def add_user(self, user):
        if user['preferred_channel'] not in user['available_channels']:
            raise ValueError("Preferred channel must be in available channels")
        else:
            if self.get_user(user['name']) is None:
                temp = user['preferred_channel']
                user['available_channels'].remove(temp)
                user['available_channels'].insert(0,temp) 
                self.all_users.append(user)
                return f"User {user['name']} added successfully"
            else:
                raise ValueError("User already exists")
            
    def get_all_users(self):
        if not self.all_users:
            raise ValueError("No users found")
        else:
            return self.all_users


    def send_notification(self, user):
        userdb = self.get_user(user['name'])
        if userdb is None:
            raise ValueError("User not found")
        else:
            return notification.executeNotification(userdb['available_channels'],user['priority'])
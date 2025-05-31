class DataStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = {}
        return cls._instance
    
    def add_user(self, user):
        self.users[user.name] = user
    
    def get_user(self, name):
        return self.users.get(name)
    
    def get_all_users(self):
        return list(self.users.values())
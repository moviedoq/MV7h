from domain.ports import UserRepository

class InMemoryUserRepository(UserRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_data()
        return cls._instance

    def _init_data(self):
        self._users = []

    def add_user(self, user):
        self._users.append(user)

    def find_by_name(self, name):
        for user in self._users:
            if user.name == name:
                return user
        return None

    def list_users(self):
        return self._users
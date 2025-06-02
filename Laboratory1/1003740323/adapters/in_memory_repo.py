from core.use_cases import UserRepositoryPort
from core.domain import User

class InMemoryUserRepo(UserRepositoryPort):
    def __init__(self):
        self.users = []

    def save(self, user: User) -> User:
        self.users.append(user)
        return user

    def find_by_name(self, name: str) -> User | None:
        return next((u for u in self.users if u.name == name), None)

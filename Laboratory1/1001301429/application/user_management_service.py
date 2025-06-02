from domain.ports import UserRepository
from domain.entities.user import User
from application.exceptions import UserAlreadyExistsError

class UserManagementService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, name: str, preferred_channel: str, available_channels: list[str]):
        if self.user_repo.find_by_name(name):
            raise UserAlreadyExistsError("User already exists") #Usuario ya registrado.
        user = User(name, preferred_channel, available_channels)
        self.user_repo.add_user(user)

    def list_users(self):
        return self.user_repo.list_users()

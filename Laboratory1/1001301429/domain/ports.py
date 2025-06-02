from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, user, message: str) -> bool:
        pass

class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def find_by_name(self, name: str):
        pass

    @abstractmethod
    def list_users(self):
        pass

    

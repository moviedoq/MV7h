from abc import ABC, abstractmethod

class Channel(ABC):
    @abstractmethod
    def send_notification(self, message: str, user_name: str) -> bool:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass
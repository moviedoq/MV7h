from abc import ABC, abstractmethod
import random
from log_util import logger

class BaseHandler(ABC):
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, channel: str, user_name: str, message: str, priority: str):
        if channel == self.channel_name():
            success = random.choice([True, False])
            logger.log(f"Intentando {channel} para {user_name}: {'Éxito' if success else 'Fallo'}")
            if success:
                return True
        if self._successor:
            return self._successor.handle(channel, user_name, message, priority)
        return False

    @abstractmethod
    def channel_name(self) -> str:
        pass

import random
from core.domain import User
from adapters.logger import Logger

def send_email(user: User, message: str) -> bool:
    success = random.random() < 0.7  # 70% de éxito
    Logger().log(f"Email a {user.name}: {'✅' if success else '❌'}")
    return success
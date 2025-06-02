from pydantic import BaseModel
from typing import List

class UserSchema(BaseModel):
    name: str
    preferred_channel: str
    available_channels: List[str]

class NotificationSchema(BaseModel):
    user_name: str
    message: str
    priority: str  # "low", "medium", "high"
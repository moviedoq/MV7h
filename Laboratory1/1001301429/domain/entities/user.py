from typing import List
from dataclasses import dataclass

@dataclass
class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels


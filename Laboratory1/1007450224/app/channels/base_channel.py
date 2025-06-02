import random

class BaseChannel:
    def __init__(self):
        self.next_channel = None

    def set_next(self, channel):
        self.next_channel = channel
        return channel

    def handle(self, message, logger):
        raise NotImplementedError("Must implement in subclass")

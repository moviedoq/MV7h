class NotificationHandler:
    def __init__(self, channel):
        self.channel = channel
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, message, user_name):
        if not self.channel.send_notification(message, user_name):
            if self.next_handler:
                return self.next_handler.handle(message, user_name)
            return False
        return True

def create_notification_chain(preferred_channel, available_channels, channel_factory):
    # Build the chain: preferred channel first, then the rest
    ordered_channels = [preferred_channel] + [c for c in available_channels if c != preferred_channel]
    handlers = [NotificationHandler(channel_factory.create_channel(c)) for c in ordered_channels]
    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])
    return handlers[0] if handlers else None
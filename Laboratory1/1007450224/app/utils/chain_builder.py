from app.channels.email_channel import EmailChannel
from app.channels.sms_channel import SMSChannel
from app.channels.console_channel import ConsoleChannel

channel_classes = {
    "email": EmailChannel,
    "sms": SMSChannel,
    "console": ConsoleChannel
}

def build_chain(channel_names):
    if not channel_names:
        return None

    chain = channel_classes[channel_names[0]]()
    current = chain

    for name in channel_names[1:]:
        next_channel = channel_classes[name]()
        current.set_next(next_channel)
        current = next_channel

    return chain

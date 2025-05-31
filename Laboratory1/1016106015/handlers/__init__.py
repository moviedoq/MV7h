from .email_handler import EmailHandler
from .sms_handler import SmsHandler

def build_chain(channels: list):
    mapping = {
        "email": EmailHandler,
        "sms": SmsHandler
    }
    chain = None
    for ch in reversed(channels):
        HandlerClass = mapping.get(ch)
        if HandlerClass:
            chain = HandlerClass(successor=chain)
    return chain

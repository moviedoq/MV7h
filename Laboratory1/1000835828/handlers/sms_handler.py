from .base_handler import BaseHandler

class SMSHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__("sms", next_handler)
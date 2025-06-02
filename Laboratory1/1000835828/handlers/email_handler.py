from .base_handler import BaseHandler

class EmailHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__("email", next_handler)
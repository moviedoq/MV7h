from abc import ABC, abstractmethod
from db.users import users
class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
    
    @abstractmethod
    def handle_request(self, request):
        pass

users_db = users(all_users=[])

class LevelOneHandler(Handler):
    def handle_request(self, request):
        if request.level == 1: #create user
            message = users_db.add_user(request.data)
            return message
        else:
            return self.next_handler.handle_request(request)
    
class LevelTwoHandler(Handler):
    def handle_request(self, request):
        if request.level == 2: #get users
            message = users_db.get_all_users()
            return message
        else:
            return self.next_handler.handle_request(request)

class LevelThreeHandler(Handler):
    def handle_request(self, request):
        if request.level == 3: #send notification
            message = users_db.send_notification(request.data)
            return message
        else:
            return "Request level not handled"

from handler.handler import LevelOneHandler, LevelTwoHandler, LevelThreeHandler
from handler.request import Request


def execute_request(level, data=None):
    # Create the chain of handlers
    level_three_handler = LevelThreeHandler()
    level_two_handler = LevelTwoHandler(level_three_handler)
    level_one_handler = LevelOneHandler(level_two_handler)

    # Create a request object
    request = Request(level, data)

    # Process the request through the handler chain
    response = level_one_handler.handle_request(request)
    
    return response
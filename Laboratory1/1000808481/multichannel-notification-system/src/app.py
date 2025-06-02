from flask import Flask
from flasgger import Swagger
from controllers.user_controller import UserController
from controllers.notification_controller import NotificationController
from services.user_service import UserService
from services.notification_service import NotificationService
from patterns.channel_factory import ChannelFactory
from utils.logger import Logger
from flask import request

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger/swagger.yaml')

# Initialize services
user_service = UserService()
channelFactory = ChannelFactory()
notification_service = NotificationService(channelFactory)

# Initialize controllers with their dependencies
user_controller = UserController(user_service)
notification_controller = NotificationController(notification_service, user_service)

# Define routes
@app.route('/users', methods=['POST'])
def register_user():
    user_data = request.get_json()
    return user_controller.register_user(user_data)

@app.route('/users', methods=['GET'])
def list_users():
    return user_controller.list_users()

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')
    return notification_controller.send_notification(user_name, message, priority)

@app.route('/notifications', methods=['GET'])
def list_notifications():
    return notification_controller.get_notifications()

@app.route('/logs', methods=['GET'])
def get_logs():
    logger = Logger()
    return {"logs": logger.get_logs()}, 200

if __name__ == '__main__':
    app.run(debug=True)
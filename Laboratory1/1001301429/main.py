from flask import Flask
from flasgger import Swagger
from infrastructure.memory_repo import InMemoryUserRepository
from application.user_management_service import UserManagementService
from application.send_notifications_service import SendNotificationService
from infrastructure.http_handler import create_routes

app = Flask(__name__)
swagger = Swagger(app)

repo = InMemoryUserRepository()

user_service = UserManagementService(repo)
notification_service = SendNotificationService(repo)

app.register_blueprint(create_routes(user_service, notification_service))

if __name__ == "__main__":
    app.run(debug=True)

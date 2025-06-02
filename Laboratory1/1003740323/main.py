from flask import Flask, request, jsonify
from flasgger import Swagger
from core.use_cases import RegisterUserUseCase, SendNotificationUseCase
from adapters.in_memory_repo import InMemoryUserRepo
from adapters.notifications import send_email, send_sms
from web.schemas import UserSchema, NotificationSchema

app = Flask(__name__)
Swagger(app)

repo = InMemoryUserRepo()
notification_handlers = [send_email, send_sms]
register_use_case = RegisterUserUseCase(repo)
send_use_case = SendNotificationUseCase(repo, notification_handlers)

@app.route("/users", methods=["GET"])
def get_users():
    """
    Lista todos los usuarios registrados.
    ---
    tags:
      - Users
    responses:
      200:
        description: Lista de usuarios
    """
    users = [vars(user) for user in repo.users]
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def register_user():
    """
    Registra un nuevo usuario.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UserSchema'
    responses:
      201:
        description: Usuario registrado
    """
    data = UserSchema(**request.get_json())
    user = register_use_case.execute(data.name, data.preferred_channel, data.available_channels)
    return jsonify({"status": "success"}), 201

@app.route("/notifications/send", methods=["POST"])
def send_notification():
    """
    Envía una notificación.
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/NotificationSchema'
    responses:
      200:
        description: Notificación procesada
    """
    data = NotificationSchema(**request.get_json())
    success = send_use_case.execute(data.user_name, data.message, data.priority)
    return jsonify({"status": "success" if success else "failed"}), 200

if __name__ == "__main__":
    app.run(debug=True)
from flask import Blueprint, request, jsonify
from application.exceptions import UserAlreadyExistsError

def create_routes(user_service, notification_service):
    bp = Blueprint('routes', __name__)

    @bp.route("/users", methods=["POST"])
    def create_user():
        """
        Crear un nuevo usuario
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: user
            schema:
              type: object
              required:
                - name
                - preferred_channel
                - available_channels
              properties:
                name:
                  type: string
                  example: Juan
                preferred_channel:
                  type: string
                  example: email
                available_channels:
                  type: array
                  items:
                    type: string
                  example: ["email", "sms"]
        responses:
          201:
            description: Usuario creado
          409:
            description: Usuario ya existe
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    error:
                        type: string
        """
        data = request.json
        try:
            user_service.register_user(
                data["name"],
                data["preferred_channel"],
                data["available_channels"]
            )
            return jsonify({"status": "created"}), 201
        except UserAlreadyExistsError as e:
            return jsonify({"error": str(e)}), 409

    @bp.route("/users", methods=["GET"])
    def list_users():
        """
        Listar todos los usuarios
        ---
        tags:
          - Users
        responses:
          200:
            description: Lista de usuarios
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  preferred_channel:
                    type: string
                  available_channels:
                    type: array
                    items:
                      type: string
        """
        users = user_service.list_users()
        return jsonify([vars(user) for user in users]), 200

    @bp.route("/notifications/send", methods=["POST"])
    def send_notification():
        """
        Enviar notificación a usuario
        ---
        tags:
          - Notifications
        parameters:
          - in: body
            name: notification
            schema:
              type: object
              required:
                - user_name
                - message
                - priority
              properties:
                user_name:
                  type: string
                  example: Juan
                message:
                  type: string
                  example: Your appointment is tomorrow.
                priority:
                  type: string
                  enum: [high, medium, low]
                  example: high
        responses:
          200:
            description: Notificación enviada
            schema:
              type: object
              properties:
                delivered:
                  type: boolean
        """
        data = request.json
        success = notification_service.send_notification(
            data["user_name"],
            data["message"],
            data["priority"]
        )
        return jsonify({"delivered": success}), 200

    return bp

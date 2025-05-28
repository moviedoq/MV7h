from flask import Flask, request, jsonify
from services.user_service import create_user
from services.notification_service import send_notification
from utils.logger import LoggerSingleton
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/usuarios", methods=["POST"])
def registrar_usuario():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
            preferred_channel:
              type: string
              enum: ["email", "sms", "llamada"]
            available_channels:
              type: array
              items:
                type: string
    responses:
      201:
        description: Usuario registrado
      400:
        description: Error en la solicitud
    """
    data = request.json
    try:
        user = create_user(
            name=data["name"],
            preferred_channel=data["preferred_channel"],
            available_channels=data["available_channels"]
        )
        return jsonify({
            "message": "Usuario registrado con éxito.",
            "user": {
                "name": user.name,
                "preferred_channel": user.preferred_channel,
                "available_channels": user.available_channels
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/notificaciones/enviar", methods=["POST"])
def enviar_notificacion():
    """
    Enviar una notificación a un usuario registrado
    ---
    tags:
      - Notificaciones
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              description: Nombre del usuario registrado
            message:
              type: string
              description: Contenido de la notificación
    responses:
      200:
        description: Resultado del intento de notificación
        schema:
          type: object
          properties:
            success:
              type: boolean
            channel:
              type: string
              nullable: true
            error:
              type: string
              nullable: true
      404:
        description: Usuario no encontrado
    """
    data = request.json
    user_name = data.get("user_name")
    message = data.get("message")

    resultado = send_notification(user_name, message)
    return jsonify(resultado)

@app.route("/logs", methods=["GET"])
def ver_logs():
    logger = LoggerSingleton()
    return jsonify(logger.get_logs())

if __name__ == "__main__":
    app.run(debug=True)

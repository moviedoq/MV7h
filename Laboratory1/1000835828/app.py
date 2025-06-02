# from flask import Flask, request, jsonify
# from services.data_store import DataStore
# from models.user import User
# from services.notification_service import NotificationService
# from utils.logger import logger

# app = Flask(__name__)
# data_store = DataStore()

# @app.route('/users', methods=['POST'])
# def register_user():
#     data = request.get_json()
    
#     if not data or 'name' not in data or 'preferred_channel' not in data or 'available_channels' not in data:
#         return jsonify({"error": "Datos incompletos"}), 400
    
#     user = User(
#         name=data['name'],
#         preferred_channel=data['preferred_channel'],
#         available_channels=data['available_channels']
#     )
    
#     data_store.add_user(user)
#     return jsonify({
#         "message": "Usuario registrado",
#         "user": {
#             "name": user.name,
#             "preferred_channel": user.preferred_channel,
#             "available_channels": user.available_channels
#         }
#     }), 201

# @app.route('/users', methods=['GET'])
# def list_users():
#     users = data_store.get_all_users()
#     return jsonify([
#         {
#             "name": user.name,
#             "preferred_channel": user.preferred_channel,
#             "available_channels": user.available_channels
#         } for user in users
#     ])

# @app.route('/notifications/send', methods=['POST'])
# def send_notification_endpoint():
#     data = request.get_json()
    
#     if not data or 'user_name' not in data or 'message' not in data:
#         return jsonify({"error": "Datos incompletos"}), 400
    
#     user = data_store.get_user(data['user_name'])
#     if not user:
#         return jsonify({"error": "Usuario no encontrado"}), 404
    
#     result = NotificationService.send_notification(user, data['message'])
#     notification_logs = logger.get_logs(10)  # Últimas 10 entradas
    
#     return jsonify({
#         "result": result,
#         "logs": notification_logs
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from services.data_store import DataStore
from models.user import User
from services.notification_service import NotificationService
from utils.logger import logger

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa Flasgger/Swagger

data_store = DataStore()


@app.route('/users', methods=['POST'])
def register_user():
    """
    Registra un usuario en el DataStore.
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Juan Pérez"
            preferred_channel:
              type: string
              example: "email"
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms"]
    responses:
      201:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario registrado"
            user:
              type: object
              properties:
                name:
                  type: string
                  example: "Juan Pérez"
                preferred_channel:
                  type: string
                  example: "email"
                available_channels:
                  type: array
                  items:
                    type: string
                  example: ["email", "sms"]
      400:
        description: Datos incompletos o formato inválido
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Datos incompletos"
    """
    data = request.get_json()
    if not data or 'name' not in data or 'preferred_channel' not in data or 'available_channels' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    user = User(
        name=data['name'],
        preferred_channel=data['preferred_channel'],
        available_channels=data['available_channels']
    )

    data_store.add_user(user)
    return jsonify({
        "message": "Usuario registrado",
        "user": {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }
    }), 201


@app.route('/users', methods=['GET'])
def list_users():
    """
    Obtiene la lista de todos los usuarios registrados.
    ---
    tags:
      - Usuarios
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
                example: "Juan Pérez"
              preferred_channel:
                type: string
                example: "sms"
              available_channels:
                type: array
                items:
                  type: string
                example: ["email", "sms"]
    """
    users = data_store.get_all_users()
    return jsonify([
        {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        } for user in users
    ])


@app.route('/notifications/send', methods=['POST'])
def send_notification_endpoint():
    """
    Envía una notificación a un usuario existente.
    ---
    tags:
      - Notificaciones
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_name:
              type: string
              example: "Juan Pérez"
            message:
              type: string
              example: "Tienes un nuevo mensaje"
    responses:
      200:
        description: Resultado del envío y logs recientes
        schema:
          type: object
          properties:
            result:
              type: string
              example: "Notificación enviada por email"
            logs:
              type: array
              items:
                type: string
              example: ["[INFO] Enviando notificación a Juan Pérez...", "..."]
      400:
        description: Datos incompletos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Datos incompletos"
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario no encontrado"
    """
    data = request.get_json()
    if not data or 'user_name' not in data or 'message' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    user = data_store.get_user(data['user_name'])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    result = NotificationService.send_notification(user, data['message'])
    notification_logs = logger.get_logs(10)  # Últimas 10 entradas

    return jsonify({
        "result": result,
        "logs": notification_logs
    })


if __name__ == '__main__':
    app.run(debug=True)

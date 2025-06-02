from flask import Flask, request, jsonify
from flasgger import Swagger
from models import User
from notification_service import NotificationService
from logger import logger

app = Flask(__name__)
swagger = Swagger(app)

# Base de datos simulada de usuarios
users_db = {}
notification_service = NotificationService()

@app.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    tags:
      - Users
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
              description: User name
            preferred_channel:
              type: string
              description: Preferred communication channel
            available_channels:
              type: array
              items:
                type: string
              description: List of available communication channels
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    
    # Validar datos de entrada
    if not data or not all(k in data for k in ('name', 'preferred_channel', 'available_channels')):
        logger.log("User registration failed: Missing data")
        return jsonify({"error": "Missing data"}), 400
    
    if not isinstance(data['available_channels'], list):
        logger.log("User registration failed: available_channels must be a list")
        return jsonify({"error": "available_channels must be a list"}), 400
    
    if data['preferred_channel'] not in data['available_channels']:
        logger.log(f"User registration failed: Preferred channel not in available channels")
        return jsonify({"error": "Preferred channel must be one of the available channels"}), 400
    
    name = data['name']
    if name in users_db:
        logger.log(f"User registration failed: User {name} already exists")
        return jsonify({"error": f"User {name} already exists"}), 400
    
    # Crear y guardar usuario
    user = User(name=name, preferred_channel=data['preferred_channel'], available_channels=data['available_channels'])
    users_db[name] = user
    logger.log(f"User {name} registered successfully")
    
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    List all registered users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
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
    return jsonify([user.to_dict() for user in users_db.values()]), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
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
              description: Name of the user to notify
            message:
              type: string
              description: The notification message
            priority:
              type: string
              description: Priority of the message (high, medium, low)
    responses:
      200:
        description: Notification attempt processed
      400:
        description: Invalid input
      404:
        description: User not found
    """
    data = request.get_json()
    
    # Validar datos de entrada
    if not data or not all(k in data for k in ('user_name', 'message', 'priority')):
        logger.log("Notification sending failed: Missing data")
        return jsonify({"error": "Missing data for notification"}), 400
    
    user_name = data['user_name']
    user = users_db.get(user_name)
    
    if not user:
        logger.log(f"Notification sending failed: User '{user_name}' not found")
        return jsonify({"error": f"User '{user_name}' not found"}), 404
    
    message = data['message']
    priority = data['priority']
    
    # Enviar notificación usando el servicio
    result = notification_service.send_notification(user, message, priority)
    
    return jsonify({"status": "Notification processing completed", "detail": result}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Get system logs
    ---
    tags:
      - Logs
    responses:
      200:
        description: System logs
        schema:
          type: object
          properties:
            logs:
              type: array
              items:
                type: string
    """
    return jsonify({"logs": logger.get_logs()}), 200

if __name__ == '__main__':
    logger.log("Starting Notification API server...")
    # Iniciar el servidor Flask
    app.run(host='0.0.0.0', debug=True, port=5000)

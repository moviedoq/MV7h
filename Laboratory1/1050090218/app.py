# app.py
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import logging # <--- AÑADIR ESTA LÍNEA
from models import User, users_db
from notifications import NotificationService
from logger import logger 

app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

notification_service = NotificationService()

@app.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Register a new user.',
    # ... (resto de la definición de swag_from sin cambios) ...
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'UserRegistration',
                'required': ['name', 'preferred_channel', 'available_channels'],
                'properties': {
                    'name': {'type': 'string', 'description': 'User name.'},
                    'preferred_channel': {'type': 'string', 'description': 'Preferred communication channel (e.g., email, sms).'},
                    'available_channels': {'type': 'array', 'items': {'type': 'string'}, 'description': 'List of available communication channels.'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully.'},
        400: {'description': 'Invalid input.'}
    }
})
def register_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'preferred_channel', 'available_channels')):
        # CORREGIDO:
        logger.log("User registration failed: Missing data.", level=logging.WARNING)
        return jsonify({"error": "Missing data"}), 400
    if not isinstance(data['available_channels'], list):
        # CORREGIDO:
        logger.log("User registration failed: available_channels must be a list.", level=logging.WARNING)
        return jsonify({"error": "available_channels must be a list"}), 400
    if data['preferred_channel'] not in data['available_channels']:
        # CORREGIDO:
        logger.log(f"User registration failed for {data['name']}: Preferred channel not in available channels.", level=logging.WARNING)
        return jsonify({"error": "Preferred channel must be one of the available channels"}), 400
    
    name = data['name']
    if name in users_db:
        # CORREGIDO:
        logger.log(f"User registration failed: User {name} already exists.", level=logging.WARNING)
        return jsonify({"error": f"User {name} already exists"}), 400

    user = User(name=name, preferred_channel=data['preferred_channel'], available_channels=data['available_channels'])
    users_db[name] = user
    logger.log(f"User {name} registered successfully. Preferred: {user.preferred_channel}, Available: {user.available_channels}")
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'List all registered users.',
    # ... (resto de la definición de swag_from sin cambios) ...
    'responses': {
        200: {
            'description': 'A list of users.',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/UserRegistration'}
            }
        }
    }
})
def get_users():
    return jsonify([user.to_dict() for user in users_db.values()]), 200

@app.route('/notifications/send', methods=['POST'])
@swag_from({
    'tags': ['Notifications'],
    'summary': 'Send a notification to a user.',
    # ... (resto de la definición de swag_from sin cambios) ...
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'NotificationPayload',
                'required': ['user_name', 'message', 'priority'],
                'properties': {
                    'user_name': {'type': 'string', 'description': 'Name of the user to notify.'},
                    'message': {'type': 'string', 'description': 'The notification message.'},
                    'priority': {'type': 'string', 'description': 'Priority of the message (e.g., high, medium, low).'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Notification attempt processed.'},
        400: {'description': 'Invalid input.'},
        404: {'description': 'User not found.'}
    }
})
def send_notification_endpoint():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_name', 'message', 'priority')):
        # CORREGIDO:
        logger.log("Notification sending failed: Missing data.", level=logging.WARNING)
        return jsonify({"error": "Missing data for notification"}), 400

    user_name = data['user_name']
    user = users_db.get(user_name)

    if not user:
        # CORREGIDO:
        logger.log(f"Notification sending failed: User '{user_name}' not found.", level=logging.WARNING)
        return jsonify({"error": f"User '{user_name}' not found"}), 404

    message_text = data['message']
    priority = data['priority']
    
    result = notification_service.send_notification(user, message_text, priority)
    
    if "failed" in result.lower():
         return jsonify({"status": "Notification processing completed.", "detail": result}), 200
    return jsonify({"status": "Notification processing completed.", "detail": result}), 200


if __name__ == '__main__':
    logger.log("Starting Notification API server...")
    app.run(debug=True, port=5000)
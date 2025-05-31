from flask import Flask, request, jsonify
from data_store import DataStore
from user import User
from notification import send_notification, logger

app = Flask(__name__)
data_store = DataStore()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Validación básica
    if not data or 'name' not in data or 'preferred_channel' not in data or 'available_channels' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Crear y almacenar usuario
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
    data = request.get_json()
    
    # Validación
    if not data or 'user_name' not in data or 'message' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Obtener usuario
    user = data_store.get_user(data['user_name'])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Enviar notificación
    result = send_notification(user, data['message'])
    
    # Obtener últimos logs para la respuesta
    notification_logs = logger.get_logs()[-5:]  # Últimas 5 entradas
    
    return jsonify({
        "result": result,
        "logs": notification_logs
    })

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from models.user import UserStore
from notifications.chain import NotificationChain

app = Flask(__name__)

# Instancias globales en memoria
store = UserStore()
chain = NotificationChain()

# Ruta raíz opcional para comprobar que el servidor está levantado
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Bienvenido al Multichannel Notification System. Usa /users o /notifications/send"
    }), 200

# Crear usuario
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = store.add_user(
        name=data["name"],
        preferred=data["preferred_channel"],
        channels=data["available_channels"]
    )
    return jsonify(user.to_dict()), 201

# Listar usuarios
@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([u.to_dict() for u in store.get_all()]), 200

# Enviar notificación
@app.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.get_json()
    user = store.find_by_name(data["user_name"])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    result = chain.send(
        user=user,
        message=data["message"],
        priority=data["priority"]
    )
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

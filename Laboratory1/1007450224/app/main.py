from flask import Flask, request, jsonify
from app.models.user import User
from app.services.logger_singleton import LoggerSingleton
from app.utils.chain_builder import build_chain

app = Flask(__name__)
users = []
logger = LoggerSingleton()

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(
        name=data["name"],
        preferred_channel=data["preferred_channel"],
        available_channels=data["available_channels"]
    )
    users.append(user)
    return jsonify({"message": "User created successfully"}), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([
        {
            "name": u.name,
            "preferred_channel": u.preferred_channel,
            "available_channels": u.available_channels
        } for u in users
    ])

@app.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.json
    user_name = data["user_name"]
    message = data["message"]
    user = next((u for u in users if u.name == user_name), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    ordered_channels = [user.preferred_channel] + [ch for ch in user.available_channels if ch != user.preferred_channel]
    chain = build_chain(ordered_channels)
    success = chain.handle(message, logger)

    return jsonify({"delivered": success})

if __name__ == "__main__":
    app.run(debug=True)

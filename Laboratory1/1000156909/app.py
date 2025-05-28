from models.user import User
from flask import Flask, request, jsonify
from data.store import user_store
from notifications.chain_builder import build_notification_chain
from utils.logger import Logger

app = Flask(__name__)
logger = Logger.get_instance()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    user = User(
        name=data['name'],
        preferred_channel=data['preferred_channel'],
        available_channels=data['available_channels']
    )
    user_store[user.name] = user
    return jsonify({'message': 'User registered'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify({name: user.to_dict() for name, user in user_store.items()}), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    name = data['user_name']
    message = data['message']

    user = user_store.get(name)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    chain = build_notification_chain(user.preferred_channel, user.available_channels)
    result = chain.handle(message, name)
    return jsonify({'status': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
from flask import request, jsonify
from flasgger import swag_from
from app.handler import build_chain


users = {}

def register_routes(app):
    @app.route('/users', methods=['POST'])
    @swag_from({
        'parameters': [{
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'example': {
                    'name': 'Juan',
                    'preferred_channel': 'email',
                    'available_channels': ['email', 'sms']
                }
            }
        }]
    })
    def add_user():
        data = request.get_json()
        users[data['name']] = data
        return jsonify({'message': 'User registered'}), 201

    @app.route('/users', methods=['GET'])
    def list_users():
        return jsonify(list(users.values()))


    @swag_from({
        'summary': 'Enviar una notificacion a un usuario',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'user_name': {'type': 'string'},
                        'message': {'type': 'string'},
                        'priority': {'type': 'string'}
                    },
                    'example': {
                        'user_name': 'Juan',
                        'message': 'Your appointment is tomorrow.',
                        'priority': 'high'
                    }
            }
            }
        ],
        'responses': {
            200: {
                'description': 'Notificacion procesada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'}
                    }
                }
            },
            404: {
            'description': 'Usuario no encontrado'
            }
        }
    })

    @app.route('/notifications/send', methods=['POST'])
    def send_notification():
        data = request.get_json()
        user = users.get(data['user_name'])

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Construye la cadena de canales (preferido primero, luego el resto)
        ordered_channels = [user['preferred_channel']] + [
            ch for ch in user['available_channels'] if ch != user['preferred_channel']
        ]
        channel_chain = build_chain(ordered_channels)

        # Envía el mensaje
        success = channel_chain.send(data['message'], user['name'])

        return jsonify({'status': 'sent' if success else 'failed'})

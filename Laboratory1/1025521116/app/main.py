from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from typing import List

from app.models.user import User
from app.models.notification import Notification

from app.channels.email_channel import EmailChannel
from app.channels.sms_channel import SMSChannel
from app.channels.console_channel import ConsoleChannel  # Si lo usas en pruebas

from app.channels.base_channel import BaseChannel
from app.logger.singleton_logger import SingletonLogger

app = Flask(__name__)
api = Api(app, version='1.0', title='Notification System API',
          description='API para gestionar usuarios y enviar notificaciones')

# Namespace para separar rutas
ns_users = Namespace('users', description='Operaciones relacionadas con usuarios')
ns_notifications = Namespace('notifications', description='Operaciones relacionadas con notificaciones')

api.add_namespace(ns_users)
api.add_namespace(ns_notifications)

users = []

# Modelos para Swagger
user_model = api.model('User', {
    'name': fields.String(required=True, description='Nombre del usuario'),
    'preferred_channel': fields.String(required=True, description='Canal preferido (email, sms, console)'),
    'available_channels': fields.List(fields.String, required=True, description='Lista de canales disponibles')
})

notification_model = api.model('Notification', {
    'user_name': fields.String(required=True, description='Nombre del usuario destinatario'),
    'message': fields.String(required=True, description='Mensaje de la notificación'),
    'priority': fields.String(required=False, description='Prioridad de la notificación', default='normal', enum=['low', 'normal', 'high'])
})


def create_channel_chain(channels: List[str]) -> BaseChannel:
    mapping = {
        "email": EmailChannel,
        "sms": SMSChannel,
        "console": ConsoleChannel  # opcional para pruebas
    }

    chain = None
    for ch in reversed(channels):
        cls = mapping.get(ch)
        if cls:
            chain = cls(next_channel=chain)
    return chain


@ns_users.route('')
class UserList(Resource):
    @ns_users.expect(user_model)
    def post(self):
        """Registrar un nuevo usuario"""
        data = request.get_json()
        user = User(**data)
        users.append(user)
        return {"message": "User registered."}, 201

    def get(self):
        """Listar todos los usuarios"""
        return [user.__dict__ for user in users]


@ns_notifications.route('/send')
class NotificationSend(Resource):
    @ns_notifications.expect(notification_model)
    def post(self):
        """Enviar una notificación"""
        data = request.get_json()
        notification = Notification(**data)
        user = next((u for u in users if u.name == notification.user_name), None)
        if not user:
            return {"error": "User not found"}, 404

        ordered_channels = [user.preferred_channel] + [ch for ch in user.available_channels if ch != user.preferred_channel]
        chain = create_channel_chain(ordered_channels)

        if not chain:
            return {"error": "No valid notification channels found"}, 400

        success = chain.send(user, notification.message)

        if success:
            return {"message": "Notification sent successfully"}, 200
        else:
            return {"message": "All notification channels failed"}, 500


@app.route("/")
def home():
    return "API Notification System Running"


@app.route('/logs', methods=['GET'])
def view_logs():
    logger = SingletonLogger()
    return jsonify(logger.get_logs())


if __name__ == "__main__":
    app.run(debug=True)

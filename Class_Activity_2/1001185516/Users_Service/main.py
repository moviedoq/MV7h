from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Agregado
import os

service_a = Flask(__name__)
CORS(service_a)  # 👈 Habilita CORS

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'users.db')

os.makedirs(os.path.dirname(db_path), exist_ok=True)

service_a.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
service_a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(service_a)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@service_a.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'El nombre es requerido'}), 400

    user = User(name=data['name'].strip())
    db.session.add(user)
    db.session.commit()
    print({'id': user.id, 'name': user.name})
    return jsonify({'id': user.id, 'name': user.name}), 201

@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    return jsonify({'error': 'User not found'}), 404

@service_a.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@service_a.route('/reset', methods=['POST'])
def reset_users():
    try:
        num_rows_deleted = db.session.query(User).delete()
        db.session.commit()
        return jsonify({'mensaje': f'Se eliminaron {num_rows_deleted} usuarios'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)

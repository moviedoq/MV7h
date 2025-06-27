from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import os

service_b = Flask(__name__)
CORS(service_b)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'tasks.db')

os.makedirs(os.path.dirname(db_path), exist_ok=True)

service_b.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
service_b.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_b)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@service_b.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Datos inválidos'}), 400
    try:
        user_check = requests.get(f'http://localhost:5001/users/{data["user_id"]}')
    except Exception as e:
        return jsonify({'error': f'Error de conexión al verificar usuario: {str(e)}'}), 500

    if user_check.status_code != 200:
        return jsonify({'error': 'ID de usuario inválido'}), 400

    task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 201

@service_b.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])

@service_b.route('/reset', methods=['POST'])
def reset_tasks():
    try:
        num_rows_deleted = db.session.query(Task).delete()
        db.session.commit()
        return jsonify({'mensaje': f'Se eliminaron {num_rows_deleted} tareas'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)

from flask import Flask, request, jsonify
from flasgger import Swagger
from handler import main as handler_main

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/users', methods=['POST'])
def registrar_usuario():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
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
            preferred_channel:
              type: string
              enum: ["email", "sms", "call"]
            available_channels:
              type: array
              items:
                type: string
          example: |
            {
              "name": "Juan Perez",
              "preferred_channel": "email",
              "available_channels": ["email", "sms", "call"]
            }
    responses:
      201:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Error en la solicitud
        schema:
          type: object
          properties:
            error:
              type: string

    """
    data = request.get_json()
    try:
        executed_request = handler_main.execute_request(1, data)
        return jsonify({"message": str(executed_request)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users', methods=['GET'])
def get_users():
    """
    Obtener la lista de usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
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
      401:
        description: Error en la solicitud
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        executed_request = handler_main.execute_request(2)
        return executed_request, 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - message
            - priority
          properties:
            name:
              type: string
            message:
              type: string
            priority:
              type: string
          example: |
            {
              "name": "Juan Perez",
              "message": "Your appointment is tomorrow.",
              "priority": "high"
            }
    responses:
      201:
        description: Mensaje enviado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Error en la solicitud
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    try:
        executed_request = handler_main.execute_request(3, data)
        return executed_request, 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
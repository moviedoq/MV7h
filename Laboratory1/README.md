# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

**Autor:** Jacel Thomás Enciso Pinzón

---

## 🧠 Descripción del Sistema

Este sistema REST permite registrar usuarios con múltiples canales de comunicación (`email`, `SMS`, `llamada`, `consola`). Cuando se envía una notificación, el sistema intenta primero con el canal **preferido** del usuario. Si ese canal falla (simulado aleatoriamente), recurre a los canales alternativos usando una **cadena de responsabilidad**. Todos los intentos de envío se registran usando un **logger Singleton**.

---

## 🧩 Patrones de Diseño Usados

### 🔗 Chain of Responsibility

Cada canal de comunicación (Email, SMS, Llamada, Consola) actúa como un **handler** en una cadena. Si un canal falla, el mensaje se pasa al siguiente.

### 🧱 Singleton

El logger implementa el patrón Singleton para asegurar que todas las notificaciones sean registradas por una sola instancia global.

---

## 📦 Estructura del Proyecto

```text
├── app.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── notification_controller.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── notification_service.py
├── notifications/
│   ├── __init__.py
│   ├── channels.py
│   ├── chain.py
│   └── logger.py
├── models/
│   ├── __init__.py
│   └── user.py
│
└── README.md
```

---

## 🛠️ Instalación y Ejecución

1. Clona el repositorio:

    ```bash
    git clone https://github.com/SwEng2-2025i/MV7h.git
    cd Laboratory1
    cd 1000809070
    ```

2. Instala las dependencias y ejecuta el servidor:

    ```bash
    pip install -r requirements.txt
    python app.py
    ```

3. Abre tu navegador en:

    [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

   Para probar la API con Swagger UI.

---

## 📡 Endpoints de la API

| Método | Endpoint              | Descripción                            | Ejemplo JSON / Curl                                                                                                                                                                                                                                |
|--------|-----------------------|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POST   | `/users`              | Registra un usuario nuevo.             | **JSON:**<br>```json<br>{<br>  "name": "Thomas",<br>  "preferred_channel": "email",<br>  "available_channels": ["email", "sms", "call"]<br>}```<br>**Curl:**<br>```bash<br>curl -X POST http://127.0.0.1:5000/users \ <br>  -H "Content-Type: application/json" \ <br>  -d "{\"name\":\"Thomas\",\"preferred_channel\":\"email\",\"available_channels\":[\"email\",\"sms\",\"call\"]}"<br>``` |
| GET    | `/users`              | Lista todos los usuarios registrados.  | **Curl:**<br>```bash<br>curl http://127.0.0.1:5000/users<br>```                                                                                                                                                                                   |
| POST   | `/notifications/send` | Envía una notificación a un usuario.   | **JSON:**<br>```json<br>{<br>  "user_name": "Juan",<br>  "message": "Tu cita es mañana.",<br>  "priority": "high"<br>}```<br>**Curl:**<br>```bash<br>curl -X POST http://127.0.0.1:5000/notifications/send \ <br>  -H "Content-Type: application/json" \ <br>  -d "{\"user_name\":\"Juan\",\"message\":\"Tu cita es mañana.\",\"priority\":\"high\"}"<br>``` |

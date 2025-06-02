# Advanced Individual Lab: Multichannel Notification System (REST API)

## Autor
**Nombre completo:** Gbriel Felipe Gonzalez Bohorquez

---

## Descripción del sistema

Este proyecto implementa una API REST para gestionar usuarios y enviar notificaciones usando múltiples canales de comunicación (email, SMS, etc.). Se simulan fallos en los canales de envío para aplicar un sistema de fallback, priorizando el canal preferido de cada usuario. El sistema está construido en Python con Flask y utiliza patrones de diseño avanzados para mantener una arquitectura limpia y extensible.

---

## Patrones de diseño aplicados

### 1. Chain of Responsibility
Permite procesar el envío de una notificación pasando por una cadena de canales (email → sms → consola) hasta que uno tenga éxito.

- **Ubicación:** `channels.py`, `handler.py`
- **Ejemplo:** Si el canal "email" falla, se intenta automáticamente con "sms" y luego "console".

### 2. Singleton (Logger)
Evita múltiples instancias del logger; asegura un registro centralizado y único de intentos de notificación.

- **Ubicación:** `logger.py`
- **Uso:** Se instancia solo una vez, imprime y guarda cada intento de envío.

---

## Endpoints de la API

### POST `/users`
**Descripción:** Registra un nuevo usuario.

**Payload:**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```
**Respuesta:**
```json
{ "message": "User registered" }
```

### GET `/users`
**Descripción:** Lista todos los usuarios registrados.

**Respuesta:**
```json
[
  {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
]
```

### POST `/notifications/send`
**Descripción:** Envía una notificación a un usuario. Si el canal preferido falla, intenta con los siguientes.

**Payload:**
```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```
**Respuesta:**
```json
{ "status": "sent" }
```

---

## Pruebas rápidas con curl

```bash
curl -X POST http://127.0.0.1:5000/users \
 -H "Content-Type: application/json" \
 -d "{\"name\": \"Juan\", \"preferred_channel\": \"email\", \"available_channels\": [\"email\", \"sms\"]}"

curl -X POST http://127.0.0.1:5000/notifications/send \
 -H "Content-Type: application/json" \
 -d "{\"user_name\": \"Juan\", \"message\": \"Hello\", \"priority\": \"high\"}"
```

---

## Configuración y ejecución

### Requisitos globales:
- Python 3.9+
- Flask
- Flasgger

### Instalación:
```bash
pip install flask flasgger
python main.py
```
Accede a Swagger en: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## Diagrama de clases

```
User
├── name
├── preferred_channel
└── available_channels

Channel (abstract)
├── next_channel
└── send()

EmailChannel → Channel
SMSChannel   → Channel

Logger (Singleton)
└── log()

handler.py
└── build_chain()
```
 

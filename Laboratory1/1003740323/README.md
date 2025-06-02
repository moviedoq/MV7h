# Sistema de Notificaciones

**Autor:** Javier Andrés Carrillo Carrasco

---

## 📘 Descripción

Este proyecto implementa un sistema de notificaciones multicanal mediante una API REST construida con **Flask**. 
Los usuarios se registran con un canal preferido y una lista de canales disponibles. Al enviar una notificación, el sistema intentará primero el canal preferido; si falla, aplicará una cadena de responsabilidad para intentar con los demás canales disponibles.
Además, se implementa un patrón **Singleton** para el logger del sistema, el cual registra cada intento de envío de notificación, permitiendo trazabilidad centralizada de los eventos.

---

## 🎯 Objetivos

- Uso de Flask para construir la API REST.
- Aplicación de **al menos dos patrones de diseño**:
  - Chain of Responsability
  - Singleton
- Simulación de fallos en canales de notificación.
- Registro de cada intento de entrega.
- Documentación interactiva con Swagger.
- Código limpio, modular y comentado.

---

## 🧱 Estructura del Proyecto

```
Laboratory1/1003740323
├── 📂core/
│   ├── 🐍domain.py                # User, Notification
│   └── 🐍use_cases.py             # RegisterUser, SendNotification
├── 📂adapters/
│   ├── 📂notifications/           
│   │   ├── 🐍email.py             # send_email(user, message) -> bool
│   │   ├── 🐍sms.py               # send_sms(user, message) -> bool
│   │   └── 🐍__init__.py          # Exporta funciones
│   ├── 🐍in_memory_repo.py        # UserRepositoryPort 
│   └── 🐍logger.py                # Singleton Logger
├── 📂web/
│   ├── 🐍app.py                   # Flask + Swagger (config integrada)
│   └── 🐍schemas.py               # Pydantic: UserSchema, NotificationSchema
└── 🐍main.py                      
```

---

## 🔁 Patrones de diseño utilizados

### 🔗 1. Chain of Responsability

- En la clase SendNotificationUseCase, se define una cadena de funciones (handlers) que simulan los canales de notificación (como send_email, send_sms). Estas se recorren en orden, y la ejecución se detiene en la primera que tenga éxito.

### 🧩 2. Singleton

- El Logger se implementa como un singleton para asegurar que todas las partes del sistema usen la misma instancia al registrar logs. Esto centraliza la trazabilidad de los eventos y garantiza que los registros no se pierdan entre instancias separadas.

---

## 🚀 Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/SwEng2-2025i/MV7h.git
cd Laboratory1
cd 1003740323
```

2. instalar las dependencias y ejecutar el servidor:

```bash
python main.py o con el compilador que se tenga
```

3. Ejecutar los endpoints:

📫 **Registro de usuario**

Puedes probar los endpoints usando Postman o directamente desde la terminal con curl.

Primero, asegúrate de que el servidor esté corriendo:

```
(http://127.0.0.1:5000)
```

Luego, en Postman, selecciona método POST y usa la siguiente URL:

```bash
http://127.0.0.1:5000/users
```
En la pestaña Body, selecciona raw y el formato JSON, y pega este ejemplo:

```json
{
  "name": "Javier",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}

```

✅ Esto registrará al usuario con sus canales de comunicación.

También puedes hacer lo mismo desde terminal con curl:

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anderson",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }'
```
📨 **Enviar notificación**

Luego, puedes probar el envío de una notificación con este endpoint:

```
http://127.0.0.1:5000/notifications/send
```

De nuevo en Postman o con curl, usa el método POST y este cuerpo JSON:


```json
{
  "user_name": "Javier",
  "message": "Tu cita es mañana a las 9:00 AM.",
  "priority": "high"
}
```

Desde terminal:
```
curl -X POST http://127.0.0.1:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Anderson",
    "message": "Tu cita es mañana a las 9:00 AM.",
    "priority": "high"
  }'
```
📌 El sistema intentará enviar la notificación por el canal preferido (email), y si falla, probará los demás en orden usando una cadena de responsabilidad.

📄 Documentación Swagger
Puedes explorar y probar la API de forma visual accediendo a la documentación generada automáticamente por Swagger:
```
http://127.0.0.1:5000/apidocs
```


## 📘 Endpoints de la API

| Método | Endpoint               | Descripción                                 |
|--------|------------------------|---------------------------------------------|
| POST   | `/users`               | Registra un usuario nuevo con canales preferidos y disponibles.                  |
| GET    | `/users`               | Lista todos los usuarios registrados.       |
| POST   | `/notifications/send`  | Envía una notificación con mensaje y prioridad.        |


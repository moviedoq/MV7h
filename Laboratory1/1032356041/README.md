# API REST de Notificaciones a Usuarios

**Autor**: Cristian Liu Chois Amaya

## Descripción

Esta API REST permite registrar usuarios y enviarles notificaciones mediante distintos canales de comunicación (correo electrónico, SMS, consola). La entrega se realiza utilizando una **cadena de responsabilidad** que simula fallos y busca un canal alternativo disponible.
El sistema está desarrollado en Flask, es modular y utiliza patrones de diseño avanzados para mantener el código limpio, extensible y fácil de probar.




### Ejemplos de Carga Útil (Payload)

#### `POST /users`
```json
{
  "name": "David",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}
```
#### `POST /notifications/send`
```json
{
  "user_name": "David",
  "message": "Tu cita es mañana.",
  "priority": "alta"
}
```

##  Endpoints Disponibles

| Método | Endpoint                    | Descripción                           |
|--------|-----------------------------|---------------------------------------|
| POST   | `/users`                    | Registra un nuevo usuario             |
| GET    | `/users`                    | Lista todos los usuarios registrados  |
| POST   | `/notifications/send`       | Envía una notificación a un usuario   |
| GET    | `/logs`                     | Lista los logs del sistema            |

##  Patrones de Diseño Utilizados

1. **Chain of Responsibility (Cadena de Responsabilidad)**  
   Permite intentar enviar la notificación a través del canal preferido. Si falla (simulado aleatoriamente), se intenta con los siguientes canales disponibles.
2. **Singleton**  
   Utilizado para implementar un logger que registra cada intento de envío de notificación. Solo existe una instancia de este logger durante toda la ejecución del sistema.

## 📂 Estructura 

```
1032356041/
├── app.py                      # Punto de entrada de la aplicación
├── models.py                   # Clase User
├── handlers.py                 # Handlers para cada canal (email, sms, consola)
├── notification_service.py     # Lógica de notificación y cadena de responsabilidad
├── logger.py                   # Logger Singleton
└── README.md
```

## 🖼️ Diagrama 

![image](https://github.com/user-attachments/assets/50e757b1-df3f-40bc-bebb-06b1e2ee1bf1)



##⚙️ Instalación y ejecución

1. Clona el repositorio:
```
git clone https://github.com/SwEng2-2025i/MV7h.git
cd 1032356041
```

2. Instala las dependencias:
```
pip install flask flasgger
```

3. Ejecuta la aplicación:
```
python app.py
```

##  Ejemplos de Prueba con curl

### Registrar un usuario

```
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"David\", \"preferred_channel\": \"email\", \"available_channels\": [\"email\", \"sms\", \"console\"]}"
```

### Listar usuarios

```
curl http://localhost:5000/users
```

### Enviar una notificación

```
curl -X POST http://localhost:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d "{\"user_name\": \"David\", \"message\": \"Tu cita es mañana.\", \"priority\": \"alta\"}"
```

### Consultar logs

```
curl http://localhost:5000/logs
```

## 📘 Documentación Swagger

Una vez iniciada la app, Se puede acceder a Sawgger mediante:

```
http://localhost:5000/apidocs
```



# Sistema de Notificación Multicanal (API REST)

**Nombre completo:** Diego Felipe Benitez Cely

---

## 🧠 Descripción del sistema

Este proyecto implementa una API REST que permite registrar usuarios y enviar notificaciones a través de múltiples canales como correo electrónico, SMS o consola. Se emplea el patrón de diseño **Cadena de Responsabilidad** para intentar múltiples canales hasta que uno tenga éxito.

---

## 🧱 Patrones de Diseño Aplicados

### ✅ Chain of Responsibility
Se utiliza para gestionar el reintento entre canales disponibles de un usuario si falla el preferido.

### ✅ Singleton
Se utiliza para el logger del sistema, asegurando que todas las clases compartan la misma instancia para registrar los intentos de envío.

---

## 📦 Endpoints disponibles

| Método | Ruta                  | Descripción                                    |
|--------|-----------------------|------------------------------------------------|
| POST   | `/users`              | Crea un usuario nuevo                         |
| GET    | `/users`              | Devuelve todos los usuarios registrados       |
| POST   | `/notifications/send` | Envía una notificación a un usuario registrado|

---

## 🧪 Cómo probar la API

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor
```bash
python -m app.main
```

### 3. Probar con `curl` o Postman

#### Crear usuario
```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}'
```

#### Ver usuarios
```bash
curl http://127.0.0.1:5000/users
```

#### Enviar notificación
```bash
curl -X POST http://127.0.0.1:5000/notifications/send -H "Content-Type: application/json" -d '{
  "user_name": "Juan",
  "message": "Tu cita es mañana a las 10am.",
  "priority": "alta"
}'
```

---

## 🧭 Diagrama de clases (descripción textual)

- `User`: contiene nombre, canal preferido y lista de canales disponibles.
- `BaseChannel`: clase abstracta para todos los canales.
- `EmailChannel`, `SMSChannel`, `ConsoleChannel`: implementan `handle()` y heredan de `BaseChannel`.
- `LoggerSingleton`: clase logger compartida por toda la aplicación.
- `build_chain`: función que arma dinámicamente la cadena de canales según prioridad.



---

## 📚 Documentación Swagger
Abre `swagger.yml` en [https://editor.swagger.io](https://editor.swagger.io) para visualizar la documentación de la API y probarla.

---

¡Gracias por revisar este proyecto! 🚀

# ✅ Task Manager - Arquitectura Hexagonal

Este es un sistema básico de gestión de tareas implementado en Python usando Flask y organizado siguiendo los principios de la **arquitectura hexagonal** (puertos y adaptadores).

Permite:
- Crear tareas
- Listar todas las tareas
- Marcar tareas como completadas

---

## 🧱 Arquitectura Hexagonal

Este proyecto sigue la **arquitectura hexagonal**. Su objetivo es aislar la lógica de negocio del resto del sistema (como frameworks, bases de datos o interfaces de usuario), facilitando el mantenimiento, la prueba y la extensión del código.

La organización del proyecto se divide en tres capas principales:

### 🧠 Dominio (`domain/`)
Contiene los conceptos centrales del negocio:

- `entities.py`: Define la entidad `Task`, que representa una tarea con su estado (`done`).
- `ports.py`: Declara interfaces (puertos) para:
  - **Entrada**: lo que el sistema permite hacer (crear, listar y completar tareas).
  - **Salida**: lo que el sistema necesita de otros componentes (guardar y buscar tareas).

### ⚙️ Aplicación (`application/`)
Implementa la lógica de negocio usando las interfaces del dominio:

- `use_cases.py`: Implementa `TaskUseCase`, que define cómo se crean, listan y completan tareas, interactuando solo con puertos, no con detalles técnicos como HTTP o almacenamiento.

### 🔌 Adaptadores (`adapters/`)
Implementan los puertos del dominio y permiten que el sistema interactúe con el "mundo exterior":

- `http_handler.py`: Adaptador HTTP usando Flask, expone los endpoints como interfaz externa.
- `memory_repo.py`: Implementa un repositorio en memoria que simula la persistencia de datos.

### 🚀 Punto de entrada (`main.py`)
Ensamblaje del sistema: instancia los adaptadores y los conecta con los casos de uso para ejecutar la aplicación.

---

## 🚀 Endpoints disponibles

El servidor corre en: `http://localhost:5000`

### 📌 1. Crear una tarea

**POST /tasks**

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar leche"}'
```

### 📤 Respuesta esperada:

```bash
{
  "id": "uuid-generado",
  "title": "Comprar leche",
  "done": false
}
```

### 📌 2. Listar todas las tareas

**GET /tasks**

```bash
curl http://localhost:5000/tasks
```

### 📤 Respuesta esperada:

```bash
[
  {
    "id": "uuid-generado",
    "title": "Comprar leche",
    "done": false
  }
]
```

### 📌 3. Marcar una tarea como completada

**PUT /tasks/<task_id>/done**

```bash
curl -X PUT http://localhost:5000/tasks/<task_id>/done
```

### 📤 Respuesta esperada:

```bash
{
  "id": "uuid-generado",
  "title": "Comprar leche",
  "done": true
}
```

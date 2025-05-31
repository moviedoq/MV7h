# Task Manager – Hexagonal Architecture

This service allows you to create and list tasks using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

## 📋 Endpoints disponibles

### ➕ Create a task

Create a new task with a title.

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender arquitectura hexagonal"}'
```

### 📄 List all tasks

Returns a list of all created tasks.

```bash
curl http://localhost:5000/tasks
```

### ✅ Mark task as done

Marks a task as completed by setting its done attribute to true.

```bash
curl -X PUT http://localhost:5000/tasks/<id>/done
```

Path Parameter:

{id}: the unique identifier of the task to be marked as done.

Successful response (HTTP 200): JSON

```json
{
  "done": true,
  "id": "daa344e4-d3ff-4dfd-bc73-63022b139ec3",
  "title": "Finish challenge"
}
```

Error responses:

404 Not Found: Task not found.

## 🔁 Flowchart – Mark Task as Done

```mermaid
flowchart TD
    A["Client sends PUT /tasks/{id}/done"] --> B["Flask route: mark_task_done(task_id)"]
    B --> C["Use case: TaskUseCase.marked_as_complete(task_id)"]
    C --> D["Repository: get_by_id(task_id)"]
    D --> E{Task found?}
    E -->|Yes| F["Entity: Task.mark_done()"]
    E -->|No| J["Return 404 error to client"]
    F --> G["Repository: save(updated Task)"]
    G --> H["Return updated Task to use case"]
    H --> I["Return JSON response (200 OK) or (400 Error) to client"]
    J --> I
```

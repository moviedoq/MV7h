# Task Manager – Hexagonal Architecture

This service allows you to create, list tasks and mark as completed using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

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

### Marks a task as completed by setting its done attribute to true.

```bash
curl -X PUT http://localhost:5000/tasks/<id>/done
```

### Flowchart 
``` mermaid
flowchart TD
    A[Cliente HTTP] -->|Peticiones| B[HTTP Handler]
    B -->|Operaciones| C[Caso de Uso]
    C -->|Datos| D[Repositorio]
    D -->|Entidades| E[Task Entity]
    
    subgraph Adaptadores
        B[Flask HTTP Handler]
        D[InMemory Repository]
    end
    
    subgraph Aplicación
        C[TaskUseCase]
    end
    
    subgraph Dominio
        E[Task Entity]
        F[TaskInputPort]
        G[TaskOutputPort]
    end
    
    B -. Implementa .-> F
    D -. Implementa .-> G
    C -. Implementa .-> F
    C -. Depende .-> G
    C -->|Crea/Modifica| E
    D -->|Almacena| E
```

### Sequence diagram

``` mermaid
sequenceDiagram
    participant Cliente
    participant HTTP_Handler
    participant TaskUseCase
    participant InMemoryRepo
    participant TaskEntity
    
    Cliente->>HTTP_Handler: POST /tasks {title: "Comprar leche"}
    activate HTTP_Handler
    HTTP_Handler->>TaskUseCase: create_task("Comprar leche")
    activate TaskUseCase
    TaskUseCase->>TaskEntity: new Task(id, title)
    activate TaskEntity
    TaskEntity-->>TaskUseCase: Task instance
    deactivate TaskEntity
    TaskUseCase->>InMemoryRepo: save(task)
    activate InMemoryRepo
    InMemoryRepo-->>TaskUseCase: OK
    deactivate InMemoryRepo
    TaskUseCase-->>HTTP_Handler: Task
    deactivate TaskUseCase
    HTTP_Handler-->>Cliente: 201 Created {task_data}
    deactivate HTTP_Handler
```
### Demostración nueva funcionalidad

### Request /POST 
![alt text](/Class_Activity_1/Aguilas/Aguilas%20-%20Hexagonal%20Architecture/Images/image2.png)
### Request /PATCH
![alt text](/Class_Activity_1/Aguilas/Aguilas%20-%20Hexagonal%20Architecture/Images/image3.png)
### Request /GET
![alt text](/Class_Activity_1/Aguilas/Aguilas%20-%20Hexagonal%20Architecture/Images/image4.png)

## Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/SwEng2-2025i/MV7h.git
cd Class_Activity_1
cd Aguilas
```

2. Instala Flask:
   
```bash
pip install flask
```

3. Ejecuta la app:
   
```bash
python main.py
```
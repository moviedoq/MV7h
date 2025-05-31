from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    def __init__(self):
        self.tasks = []

    # Se modificó el método para que no se guarde la misma tarea varias veces
    def save(self, task: Task) -> None:
        for i, existing in enumerate(self.tasks):
            if existing.id == task.id:
                self.tasks[i] = task
                return
        self.tasks.append(task)


    def list_all(self) -> list[Task]:
        return self.tasks
    
    def get_by_id(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id {task_id} not found")

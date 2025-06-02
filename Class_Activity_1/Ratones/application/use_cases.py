import uuid
from domain.entities import Task
from domain.ports import TaskInputPort, TaskOutputPort

class TaskUseCase(TaskInputPort):
    def __init__(self, repo: TaskOutputPort):
        self.repo = repo

    def create_task(self, title: str) -> Task:
        task = Task(id=str(uuid.uuid4()), title=title)
        self.repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self.repo.list_all()
    
    def marked_as_complete(self, task_id: str) -> Task:
        task = self.repo.get_by_id(task_id)
        task.mark_done() # Se usa la lógica del dominio
        self.repo.save(task)
        return task

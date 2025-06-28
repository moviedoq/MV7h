import requests
from reportlab.pdfgen import canvas
import os

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code != 200:
        print("No se pudo eliminar el usuario")
    else:
        print("Usuario eliminado correctamente.")

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code != 200:
        print("No se pudo eliminar la tarea")
    else:
        print("Tarea eliminada correctamente.")


def save_test_report(content):
    os.makedirs("reports", exist_ok=True)
    files = os.listdir("reports")
    num = len([f for f in files if f.endswith(".pdf")]) + 1
    filename = f"reports/report_{num:03}.pdf"

    c = canvas.Canvas(filename)
    c.drawString(100, 800, "Resultado del test de integración:")
    for i, line in enumerate(content.splitlines()):
        c.drawString(100, 780 - i*20, line)
    c.save()
    print(f"Reporte guardado: {filename}")

def limpiar_backend():
    try:
        r1 = requests.post("http://localhost:5001/reset")
        print("Usuarios limpiados:", r1.status_code)
        r2 = requests.post("http://localhost:5002/reset")
        print("Tareas limpiadas:", r2.status_code)
    except Exception as e:
        print("Error al limpiar backend:", e)

def integration_test():
    limpiar_backend()
    logs = []

    user_id = create_user("Camilo")
    logs.append(f"Usuario creado con ID {user_id}")

    task_id = create_task(user_id, "Prepare presentation")
    logs.append(f"Tarea creada con ID {task_id}")

    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    assert any(t["id"] == task_id for t in user_tasks), "❌ Task not registered"
    logs.append("✅ Tarea correctamente registrada.")

    delete_task(task_id)
    delete_user(user_id)
    logs.append("🧹 Datos eliminados.")

    tasks = get_tasks()
    assert not any(t["id"] == task_id for t in tasks), "❌ La tarea no fue eliminada"
    logs.append("✅ Limpieza verificada.")

    # Generar PDF con los logs
    save_test_report("\n".join(logs))
    limpiar_backend()



if __name__ == "__main__":
    integration_test()
import requests

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

def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    cleanup(user_id, task_id)
    print("✅ Datos de prueba eliminados correctamente")

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    print("✅ Test completed: task was successfully registered and linked to the user.")

def cleanup(user_id, task_id):
    # 1) Borrar la tarea
    requests.delete(f"{TASKS_URL}/{task_id}").raise_for_status()
    # 2) Confirmar que ya no está
    assert requests.get(f"{TASKS_URL}/{task_id}").status_code == 404

    # 3) Borrar el usuario
    requests.delete(f"{USERS_URL}/{user_id}").raise_for_status()
    # 4) Confirmar
    assert requests.get(f"{USERS_URL}/{user_id}").status_code == 404


if __name__ == "__main__":
    integration_test()
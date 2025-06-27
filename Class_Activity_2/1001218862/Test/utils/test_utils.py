import requests

# Endpoints base
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

def cleanup(user_id):
    delete_url = f"{USERS_URL}/{user_id}"
    response = requests.delete(delete_url)

    try:
        response.raise_for_status()
        print(f"🧹 User {user_id} and their tasks have been cleaned up.")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Cleanup failed for user {user_id}: {e}")

def verify_user_deleted(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    assert response.status_code == 404, f"❌ User {user_id} still exists."

def verify_tasks_deleted(user_id):
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    assert len(user_tasks) == 0, f"❌ Tasks for user {user_id} were not deleted."
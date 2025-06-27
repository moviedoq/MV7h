import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
RESET_USERS_URL = "http://localhost:5001/reset"
RESET_TASKS_URL = "http://localhost:5002/reset"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("Usuario creado:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("Tarea creada:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def limpiar_datos():
    try:
        r1 = requests.post(RESET_USERS_URL)
        r2 = requests.post(RESET_TASKS_URL)
        print("Limpieza completada:",
                r1.status_code, r1.json(),
                r2.status_code, r2.json())
    except Exception as e:
        print("Error al limpiar las bases:", e)

def generar_pdf_evidencia(nombre, tarea, user_id, task_id, test_exitoso):
    basedir = os.path.abspath(os.path.dirname(__file__))
    pdf_dir = os.path.join(basedir, 'reportes')
    os.makedirs(pdf_dir, exist_ok=True)

    nombre_archivo = f"evidencia_integracion_{nombre}.pdf"
    ruta_archivo = os.path.join(pdf_dir, nombre_archivo)

    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    c.drawString(100, 750, f"Nombre: {nombre}")
    c.drawString(100, 730, f"Tarea: {tarea}")
    c.drawString(100, 710, f"ID Usuario: {user_id}")
    c.drawString(100, 690, f"ID Tarea: {task_id}")
    c.drawString(100, 670, f"Estado del Test: {'ÉXITO' if test_exitoso else 'FALLÓ'}")
    c.save()

def integration_test():
    casos = [
        {"nombre": "Camilo", "tarea": "Preparar presentación"},
        {"nombre": "Lucía", "tarea": "Revisar informe"},
        {"nombre": "Andrés", "tarea": "Enviar correo"}
    ]

    for i, caso in enumerate(casos, start=1):
        test_exitoso = False
        user_id = "N/A"
        task_id = "N/A"

        try:
            user_id = create_user(caso["nombre"])
            task_id = create_task(user_id, caso["tarea"])
            tasks = get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]

            assert any(t["id"] == task_id for t in user_tasks), "La tarea no se registró correctamente"
            print(f"Test #{i} exitoso para {caso['nombre']}")
            test_exitoso = True

        except Exception as e:
            print(f"Test #{i} falló para {caso['nombre']}: {e}")

        finally:
            generar_pdf_evidencia(caso["nombre"], caso["tarea"], user_id, task_id, test_exitoso)

    limpiar_datos()

if __name__ == "__main__":
    integration_test()
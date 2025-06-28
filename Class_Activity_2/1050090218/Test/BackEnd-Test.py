import requests
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

# --- Endpoints ---
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# --- Funciones de API (sin cambios) ---
def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print(f"✅ User created: {user_data}")
    return user_data

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    task_data = response.json()
    print(f"✅ Task created: {task_data}")
    return task_data

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted.")
    return response

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted.")
    return response

# --- NUEVA FUNCIÓN DE REPORTE DETALLADO ---
def generate_detailed_pdf_report(test_name, status, start_time, duration, log_lines):
    report_num = 1
    while os.path.exists(f"{test_name}_report_{report_num}.pdf"):
        report_num += 1
    file_name = f"{test_name}_report_{report_num}.pdf"

    pdf = FPDF()
    pdf.add_page()
    
    # Título del reporte
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, text=f"Test Report: {test_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5) # Espacio

    # Resumen de la ejecución
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, text=f"Execution Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, text=f"Duration: {duration.total_seconds():.2f} seconds", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Estado final con color
    if status == "SUCCESS":
        pdf.set_text_color(34, 139, 34) # Verde oscuro
    else:
        pdf.set_text_color(220, 20, 60) # Rojo carmesí
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, text=f"Overall Status: {status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0) # Resetear a color negro
    pdf.ln(5)

    # Log detallado de la ejecución
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, text="Execution Log:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 10)
    
    # Usar multi_cell para el texto del log
    log_text = "\n".join(log_lines)
    pdf.multi_cell(0, 5, text=log_text)

    pdf.output(file_name)
    print(f"📄 Detailed report generated: {file_name}")

# --- FUNCIÓN DE PRUEBA MODIFICADA ---
def integration_test():
    user_data = None
    task_data = None
    test_status = "FAILED"
    log_lines = []
    start_time = datetime.now()

    try:
        # Paso 1: Crear usuario
        user_data = create_user("Camilo")
        log_lines.append(f"[SUCCESS] User '{user_data['name']}' created with ID: {user_data['id']}")

        # Paso 2: Crear tarea para ese usuario
        task_data = create_task(user_data['id'], "Prepare presentation")
        log_lines.append(f"[SUCCESS] Task '{task_data['title']}' created with ID: {task_data['id']}")

        # Paso 3: Verificar que la tarea está registrada
        tasks = get_tasks()
        log_lines.append(f"[INFO] Fetched all tasks to verify creation.")
        user_tasks = [t for t in tasks if t["user_id"] == user_data['id']]

        assert any(t["id"] == task_data['id'] for t in user_tasks), "The task was not correctly registered"
        log_lines.append("[SUCCESS] Verification passed: Task is linked to the correct user.")
        
        test_status = "SUCCESS"

    except Exception as e:
        log_lines.append(f"[ERROR] Test failed with exception: {e}")
        test_status = "FAILED" # Asegurarse de que el estado es FAILED

    finally:
        # Paso 4: Limpieza de datos
        log_lines.append("\n--- Starting Data Cleanup ---")
        if task_data:
            delete_task(task_data['id'])
            log_lines.append(f"[CLEANUP] Attempted to delete task ID: {task_data['id']}")
        if user_data:
            delete_user(user_data['id'])
            log_lines.append(f"[CLEANUP] Attempted to delete user ID: {user_data['id']}")

            # Paso 5: Verificar que los datos fueron eliminados
            response = requests.get(f"{USERS_URL}/{user_data['id']}")
            assert response.status_code == 404, "User data was not deleted."
            log_lines.append(f"[CLEANUP] Verified that user ID: {user_data['id']} is deleted.")
        
        end_time = datetime.now()
        duration = end_time - start_time

        # Generar el reporte PDF detallado
        generate_detailed_pdf_report(
            test_name="Backend_Integration",
            status=test_status,
            start_time=start_time,
            duration=duration,
            log_lines=log_lines
        )

if __name__ == "__main__":
    integration_test()
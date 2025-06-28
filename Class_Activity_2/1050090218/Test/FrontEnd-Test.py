import time
import os
import requests
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Endpoints de API para la limpieza ---
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# --- Funciones de limpieza de API (para usar en el finally) ---
def delete_user_api(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted via API.")
    return response

def delete_task_api(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted via API.")
    return response

# --- Función de reporte (idéntica a la del backend test) ---
def generate_detailed_pdf_report(test_name, status, start_time, duration, log_lines):
    report_num = 1
    while os.path.exists(f"{test_name}_report_{report_num}.pdf"):
        report_num += 1
    file_name = f"{test_name}_report_{report_num}.pdf"

    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, text=f"Test Report: {test_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5)

    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, text=f"Execution Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, text=f"Duration: {duration.total_seconds():.2f} seconds", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    if status == "SUCCESS":
        pdf.set_text_color(34, 139, 34)
    else:
        pdf.set_text_color(220, 20, 60)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, text=f"Overall Status: {status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, text="Execution Log:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 10)
    
    log_text = "\n".join(log_lines)
    pdf.multi_cell(0, 5, text=log_text)

    pdf.output(file_name)
    print(f"📄 Detailed report generated: {file_name}")

# --- Funciones de Selenium (sin cambios en su lógica interna) ---
def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Pablo")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result_element = wait.until(EC.presence_of_element_located((By.ID, "user-result")))
    user_result = user_result_element.text
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio E2E")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    time.sleep(1)

    crear_tarea_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']")))
    crear_tarea_btn.click()
    
    wait.until(EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID"))
    task_result = driver.find_element(By.ID, "task-result").text
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks_list = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio E2E" in tasks_list

# --- FUNCIÓN PRINCIPAL MODIFICADA ---
def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    log_lines = []
    test_status = "FAILED"
    start_time = datetime.now()
    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        
        log_lines.append("[BEGIN] Starting Frontend E2E Test.")
        abrir_frontend(driver)
        log_lines.append(f"[INFO] Opened frontend URL: http://localhost:5000")
        
        user_id = crear_usuario(driver, wait)
        log_lines.append(f"[SUCCESS] User created via UI with name 'Ana Frontend' and ID: {user_id}")
        
        task_id = crear_tarea(driver, wait, user_id)
        log_lines.append(f"[SUCCESS] Task created via UI for user {user_id} with ID: {task_id}")
        
        ver_tareas(driver)
        log_lines.append("[SUCCESS] Verification passed: New task is visible in the task list.")
        
        test_status = "SUCCESS"
        log_lines.append("\n[END] All UI tests passed successfully.")

    except Exception as e:
        log_lines.append(f"\n[ERROR] Test failed with exception: {e}")
        # test_status ya es 'FAILED' por defecto

    finally:
        log_lines.append("\n--- Starting Data Cleanup ---")
        if task_id:
            delete_task_api(task_id)
            log_lines.append(f"[CLEANUP] API call to delete task ID: {task_id}")
        if user_id:
            delete_user_api(user_id)
            log_lines.append(f"[CLEANUP] API call to delete user ID: {user_id}")
            
            # Verificación de limpieza
            response = requests.get(f"{USERS_URL}/{user_id}")
            if response.status_code == 404:
                log_lines.append(f"[CLEANUP] Verified that user ID: {user_id} is deleted.")
            else:
                log_lines.append(f"[ERROR] Cleanup failed. User ID: {user_id} was not deleted.")

        end_time = datetime.now()
        duration = end_time - start_time
        
        generate_detailed_pdf_report(
            test_name="Frontend_E2E",
            status=test_status,
            start_time=start_time,
            duration=duration,
            log_lines=log_lines
        )
        
        driver.quit()

if __name__ == "__main__":
    main()
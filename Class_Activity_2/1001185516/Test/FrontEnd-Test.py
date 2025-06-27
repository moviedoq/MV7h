import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
import os

def limpiar_datos_usuarios():
    try:
        resp = requests.post("http://localhost:5001/reset")
        print("Respuesta limpieza usuarios:", resp.status_code, resp.json())
    except Exception as e:
        print("Error al limpiar usuarios:", e)

def limpiar_datos_tasks():
    try:
        resp = requests.post("http://localhost:5002/reset")
        print("Respuesta limpieza tareas:", resp.status_code, resp.json())
    except Exception as e:
        print("Error al limpiar tareas:", e)

def generar_pdf_evidencia(nombre, tarea, user_id, task_result, test_exitoso, index):
    basedir = os.path.abspath(os.path.dirname(__file__))
    pdf_dir = os.path.join(basedir, 'reportes')

    os.makedirs(pdf_dir, exist_ok=True)
    
    nombre_archivo = f"evidencia_test_{index}_{nombre}.pdf"
    ruta_archivo = os.path.join(pdf_dir, nombre_archivo)

    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    c.drawString(100, 750, f"Nombre: {nombre}")
    c.drawString(100, 730, f"Tarea: {tarea}")
    c.drawString(100, 710, f"ID Usuario: {user_id}")
    c.drawString(100, 690, f"Resultado tarea: {task_result}")
    c.drawString(100, 670, f"Estado del Test: {'ÉXITO' if test_exitoso else 'FALLÓ'}")
    c.save()

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    casos_de_prueba = [
        {"username": "Ana", "task": "Terminar laboratorio"},
        {"username": "Luis", "task": "Revisar informe"},
        {"username": "Marta", "task": "Enviar correo"},
    ]

    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)

        for i, caso in enumerate(casos_de_prueba, start=1):
            try:
                # Crear usuario
                username_input = driver.find_element(By.ID, "username")
                username_input.clear()
                username_input.send_keys(caso["username"])
                time.sleep(1)
                driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
                time.sleep(2)

                user_result = driver.find_element(By.ID, "user-result").text
                assert "Usuario creado con ID" in user_result
                user_id = ''.join(filter(str.isdigit, user_result))

                # Crear tarea
                task_input = driver.find_element(By.ID, "task")
                task_input.clear()
                task_input.send_keys(caso["task"])

                userid_input = driver.find_element(By.ID, "userid")
                userid_input.clear()
                userid_input.send_keys(user_id)
                userid_input.send_keys('\t')
                time.sleep(1)

                crear_tarea_btn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
                )
                crear_tarea_btn.click()
                time.sleep(2)

                wait.until(
                    EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
                )
                task_result = driver.find_element(By.ID, "task-result").text
                assert "Tarea creada con ID" in task_result

                # Verificar tarea en lista
                driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
                time.sleep(2)
                tasks = driver.find_element(By.ID, "tasks").text
                assert caso["task"] in tasks

                generar_pdf_evidencia(caso["username"], caso["task"], user_id, task_result, True, i)

            except Exception as e:
                generar_pdf_evidencia(caso["username"], caso["task"], "Error", str(e), False, i)

    finally:
        limpiar_datos_usuarios()
        limpiar_datos_tasks()
        driver.quit()

if __name__ == "__main__":
    main()
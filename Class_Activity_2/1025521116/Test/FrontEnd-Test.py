import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

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

def eliminar_tarea(driver):
    # Hace clic en el botón de eliminar (🗑) de la última tarea creada
    eliminar_botones = driver.find_elements(By.XPATH, "//button[contains(text(), '🗑')]")
    if eliminar_botones:
        eliminar_botones[-1].click()
        time.sleep(2)
    else:
        print("❌ No se encontró ningún botón 🗑 para eliminar la tarea.")

    # Verifica que la tarea eliminada ya no aparece
    tasks = driver.find_element(By.ID, "tasks").text
    print("Contenido actual de tareas:", tasks)
    assert "Terminar laboratorio" not in tasks

def limpiar_datos():
    try:
        resp1 = requests.post("http://localhost:5001/reset")
        print("Limpieza usuarios:", resp1.status_code, resp1.text)

        resp2 = requests.post("http://localhost:5002/reset")
        print("Limpieza tareas:", resp2.status_code, resp2.text)
    except Exception as e:
        print("Error al limpiar:", e)

def main():
    limpiar_datos()
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        eliminar_tarea(driver)
    finally:
        driver.quit()
        limpiar_datos()

if __name__ == "__main__":
    main()

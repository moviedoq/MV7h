# Actividad Testing

Esta actividad tiene como finalidad implementar pruebas de integración automáticas sobre dos microservicios desarrollados en Flask: uno para usuarios y otro para tareas. Además, se agregaron mejoras clave para soporte de testing, generación de reportes y mejor manejo en las bases.

---

## Cambios implementados respecto al código original

### 1. Endpoints `/reset` agregados a cada microservicio

- **Objetivo:** Permitir la limpieza total de las bases de datos de forma segura después de cada prueba.
- **Servicios afectados:**
  - `Users_Service.py` (usuarios): se agregó `@app.route('/reset', methods=['POST'])`
  - `Task_Service.py` (tareas): se agregó `@app.route('/reset', methods=['POST'])`
- **Resultado:** Se elimina todo el contenido de las bases `User` y `Task` respectivamente.

En el apartado del Backend, por la construccion el código, debimos poner directamente las rutas que se van a eliminar:

```python
RESET_USERS_URL = "http://localhost:5001/reset"
RESET_TASKS_URL = "http://localhost:5002/reset"
```

Al finalizar el main en el caso del Frontend, llamamos a la funcion creada para borrar las tareas:

```python
def limpiar_datos_usuarios():
    try:
        resp = requests.post("http://localhost:5001/reset")
        print("Respuesta limpieza usuarios:", resp.status_code, resp.json())
    except Exception as e:
        print("Error al limpiar usuarios:", e)
```

Y la llamada al final:

```python
limpiar_datos_usuarios()
limpiar_datos_tasks()
```

---

### 2. Manejo seguro de rutas y archivos

En ambos servicios (`Users_Service.py`, `Task_Service.py`) se reemplazaron rutas fijas por rutas dinámicas y seguras usando:

```python
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'users.db')  # o 'tasks.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
```

- **Ventaja:** Permite ejecutar el código desde cualquier ubicación sin errores de rutas relativas.
- **Impacto:** Asegura que la base de datos se guarde junto al script y crea automáticamente el directorio si no existe.

---

### 3. Script de integración con múltiples casos de prueba

### I. Archivo: `BackEnd-Test.py`

Se implementó un test automático que:

1. Crea usuarios y tareas.
2. Verifica que las tareas se registren correctamente.
3. Genera un **PDF por cada caso de prueba** con los resultados.
4. Limpia ambas bases de datos al finalizar.

Los casos de prueba están definidos como una lista de diccionarios:

```python
casos = [
    {"nombre": "Camilo", "tarea": "Preparar presentación"},
    {"nombre": "Lucía", "tarea": "Revisar informe"},
    {"nombre": "Andrés", "tarea": "Enviar correo"}
]
```

### II. Archivo: `FrontEnd-Test.py`

Se implementa el mismo test automatico, hace lo mismo, pero esta vez desde la vista del FrontEnd y con un diferente numero de casos:

```python
casos_de_prueba = [
        {"username": "Ana", "task": "Terminar laboratorio"},
        {"username": "Luis", "task": "Revisar informe"},
        {"username": "Marta", "task": "Enviar correo"},
    ]
```

---

### 4. Generación de reportes en PDF

- **Biblioteca utilizada:** `reportlab`
- Se genera un archivo PDF por cada combinación usuario-tarea.
- Los archivos se guardan en la carpeta `reportes/` con nombres como:

```plaintext
evidencia_integracion_1_Camilo.pdf
evidencia_integracion_2_Lucía.pdf
evidencia_integracion_3_Andrés.pdf
```

- Cada PDF incluye:
  - Nombre del usuario
  - Tarea asignada
  - ID del usuario
  - ID de la tarea
  - Estado del test: `ÉXITO` o `FALLÓ`

Esto lo hacemos con una nueva funcion en ambos test:

```python
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
```

---

## Requisitos del proyecto

Se actualizan los requerimientos del proyecto on nuevas librerías externas:

```txt
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Cors==4.0.0
requests==2.32.3
selenium==4.20.0
reportlab==4.1.0
```

Puedes instalarlas ejecutando:

```bash
pip install -r requirements.txt
```

> Por desarrollo de entorno, se debe verificar que se este usando Python `3.12.6` o superior para garantizar compatibilidad con estas versiones.

---

## Ejecución del test

1. Asegúrate de tener corriendo los servicios:

- `http://localhost:5001` (servicio de usuarios)
- `http://localhost:5002` (servicio de tareas)
- `http://localhost:5000` (FrontEnd)

2. Luego ejecuta el script de pruebas:

```bash
python BackEnd-Test.py
```
o

```bash
python FrontEnd-Test.py
```

3. Al finalizar:

- Se imprimirán los resultados por consola.
- Se generarán los archivos PDF en la carpeta `reportes/`.
- Las bases de datos `users.db` y `tasks.db` serán limpiadas automáticamente.

---

## Limpieza automática

El sistema realiza una limpieza segura de datos al final de cada prueba mediante los endpoints `/reset` creados específicamente para este propósito.

---

## Recomendaciones finales

El nuevo programa se entrega sin pruebas, la intencion es que el docente lo pruebe y compruebe por el mismo que el sistema funciona correctamente

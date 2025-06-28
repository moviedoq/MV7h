# Reporte de la Actividad de Clase 2

**Nombre del Estudiante:** Andres Caro
**ID del Estudiante:** 1050090218

## Resumen del Proyecto

Este proyecto extiende un ejemplo de pruebas de integración entre microservicios. Se implementaron dos características principales solicitadas en las instrucciones de la actividad:

1.  **Limpieza de datos automática** después de la ejecución de las pruebas.
2.  **Generación automática de reportes** de resultados en formato PDF.

## Descripción de las Modificaciones

Para cumplir con los requisitos de la actividad, se realizaron las siguientes modificaciones al código base.

### 1. Limpieza de Datos (Data Cleanup)

Se implementó un sistema para asegurar que todos los datos generados durante las pruebas (usuarios y tareas) fueran eliminados al finalizar, incluso si las pruebas fallan.

* **Modificaciones en el Backend (`main-user.py` y `main-task.py`):**
    * Se añadieron nuevos *endpoints* `DELETE /users/<id>` y `DELETE /tasks/<id>` a los microservicios para permitir la eliminación de registros específicos.

* **Modificaciones en los Scripts de Prueba (`BackEnd-Test.py` y `FrontEnd-Test.py`):**
    * Se utilizó una estructura `try...finally` para garantizar que el código de limpieza siempre se ejecute.
    * Al finalizar cada prueba, se realizan llamadas `requests.delete` a los nuevos *endpoints* para eliminar los datos creados.
    * Se añadió un paso de verificación que confirma que los datos han sido eliminados correctamente (esperando una respuesta `HTTP 404 Not Found`).

### 2. Generación Automática de Reportes en PDF

Se implementó un sistema para guardar los resultados de las pruebas en archivos PDF de forma automática.

* **Librería Utilizada:** Se utilizó la librería `fpdf2` de Python para la creación de los documentos PDF.
* **Nomenclatura de Archivos:** Los reportes se guardan con un número secuencial (ej. `Backend_Integration_report_1.pdf`, `Backend_Integration_report_2.pdf`). Esto evita que los reportes se sobrescriban y preserva el historial de ejecuciones.
* **Contenido Detallado del Reporte:** Los reportes fueron enriquecidos para incluir información valiosa sobre la ejecución de la prueba:
    * Nombre de la prueba y fecha/hora de ejecución.
    * Duración total de la prueba en segundos.
    * Un estado final (`SUCCESS` o `FAILED`) resaltado con color para fácil identificación.
    * Un log de ejecución detallado con cada paso realizado, incluyendo la creación de datos, verificaciones y el proceso de limpieza.

## Archivos Modificados

* `main-user.py`:
    * Se añadió el endpoint `@service_a.route('/users/<int:user_id>', methods=['DELETE'])` para permitir la eliminación de usuarios.

* `main-task.py`:
    * Se añadió el endpoint `@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])` para permitir la eliminación de tareas.

* `BackEnd-Test.py`:
    * Se reestructuró la función `integration_test` para usar un bloque `try...except...finally`.
    * Se añadió la recopilación de logs de ejecución en una lista.
    * Se implementaron llamadas a las funciones de limpieza en el bloque `finally`.
    * Se añadió la función `generate_detailed_pdf_report` que crea un PDF con los resultados detallados de la prueba.

* `FrontEnd-Test.py`:
    * Se reestructuró la función `main` para usar un bloque `try...except...finally`.
    * Se añadieron funciones auxiliares (`delete_user_api`, `delete_task_api`) para realizar la limpieza de datos mediante llamadas directas a la API en el bloque `finally`.
    * Se integró la misma función `generate_detailed_pdf_report` para generar un reporte detallado de la prueba End-to-End.

## Cómo Ejecutar las Pruebas

1.  Asegúrese de tener todas las dependencias instaladas: `pip install Flask Flask-SQLAlchemy Flask-Cors requests selenium fpdf2`.
2.  Inicie los servicios de backend en terminales separadas:
    ```bash
    python main-user.py
    python main-task.py
    ```
3.  Inicie el servicio de frontend en otra terminal:
    ```bash
    python main-front.py
    ```
4.  Ejecute los scripts de prueba en otra terminal:
    ```bash
    # Para la prueba de backend
    python BackEnd-Test.py

    # Para la prueba de frontend
    python FrontEnd-Test.py
    ```

## Resultados

Al ejecutar los scripts de prueba, cada uno realiza sus respectivas verificaciones, limpia los datos creados en la base de datos y genera un archivo PDF único y detallado en la carpeta raíz del proyecto, documentando el resultado de la ejecución.
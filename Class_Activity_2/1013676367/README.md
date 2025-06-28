# Sistema de Gestión de Usuarios y Tareas

Jesus David Giraldo Gomez - 1013676367

Este proyecto tiene como objetivo implementar un sistema completo de gestión de usuarios y tareas mediante una arquitectura de microservicios en Flask, con énfasis en pruebas de integración automatizadas y generación de reportes. La actividad se centra en:

* Pruebas de integración automatizadas para validar la comunicación entre componentes

* Limpieza automática de datos después de cada ejecución de pruebas

* Generación de reportes en PDF con resultados

* Verificación de consistencia del sistema post-ejecución


## Tecnologías utilizadas

|Componente	|Tecnologías|
|--------------|--------------|
|Backend	|Python, Flask, REST APIs|
|Frontend	|HTML, JavaScript|
|Pruebas |Backend	requests, pytest|
|Pruebas |Frontend	Selenium WebDriver|
|Reportes	|FPDF (generación PDF)|


## Instalación
```bash
clone https://github.com/SwEng2-2025i/MV7h.git
cd Class_Activity_2
cd 1013676367
pip install -r requirements.txt
```
### Iniciar servicios de Usuarios
```bash
cd Users_Service
flask run

```
### Iniciar servicios de Task
```bash
cd Task_Service
flask run

```

### Iniciar servicios de FrontEnd
```bash
cd Front-End
flask run

```

---
## Estructura del proyecto

```bash
📦 Proyecto
├── 📂 Front-End/
│   └── main.py
├── 📂 instance/
│   ├── tasks.db
│   └── users.db
├── 📂 Task_Service/
│   └── main.py
├── 📂 Test/
│   ├── BackEnd-Test.py
│   └── FrontEnd-Test.py
├── 📂 Users_Service/
│   └── main.py
├── README.md                
└── requirements.txt 
```

## Funcionalidades Implementadas

### Limpieza automática post-pruebas

Se implementaron endpoints específicos en los microservicios para garantizar la limpieza de datos de prueba:

#### Users_Service:
```bash
GET /users/delete/<user_id>
```
* Elimina un usuario específico por ID
* Retorna código 200 si la operación fue exitosa

#### Task_Service:
```bash
GET /tasks/delete/<task_id>
```
* Elimina una tarea específica por ID
* Retorna código 204 (No Content) al completarse

### Flujo de limpieza:

* Las pruebas registran IDs de recursos creados

* Al finalizar la ejecución, invocan los endpoints de limpieza
---
### Generación Automática de Reportes PDF

* Librería FPDF para generación programática de documentos
* Numeración secuencial automática (Report_1.pdf, Report_2.pdf, ...)
* en Test/BackEnd_reports and Test/ ordenados secuencialmente

#### Estructura de reportes:

```bash
📦 Test
├── 📂 BackEnd_reports
│   ├── Report_1.pdf
│   ├── Report_2.pdf
│   └── ...
└── 📂 FrontEnd_reports
    ├── Report_1.pdf
    ├── Report_2.pdf
    └── ...

```
___
## Cómo Ejecutar las Pruebas
### Preparación:
```bash
pip install fpdf selenium requests pytest fpdf
```
### Ejecutar pruebas Backend:
```bash
python Backend.py
```
### Ejecutar pruebas Frontend:
```bash
python Frontend.py
```
### Ver reportes generados:
* Backend: Test/BackEnd_reports/Report_*.pdf
* Frontend: Test/FrontEnd_reports/Report_*.pdf

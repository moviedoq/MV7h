from utils.test_utils import create_user, create_task, get_tasks, cleanup, verify_user_deleted, verify_tasks_deleted
from reports.report_utils import get_next_report_number, generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def integration_test():
    user_id = None  # Declarar la variable aquí para que sea accesible en finally
    report_content = []

    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        report_content.append(f"✅ User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        report_content.append(f"✅ Task created with ID: {task_id} for user {user_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        report_content.append("✅ Task was successfully registered and linked to the user.")

    except Exception as e:
        report_content.append(f"❌ Test failed: {str(e)}")
        raise e

    finally:
        # Limpieza garantizada
        if user_id is not None:
            cleanup(user_id)
            report_content.append(f"🧹 Cleanup completed for user ID: {user_id}")

            # Verificación de que se eliminó correctamente
            verify_user_deleted(user_id)
            report_content.append(f"✅ Verified user ID {user_id} was deleted.")
            verify_tasks_deleted(user_id)
            report_content.append(f"✅ Verified tasks for user ID {user_id} were deleted.")
            print("✅ Cleanup verification completed successfully.")

        # Generar reporte
        report_number = get_next_report_number()
        generate_pdf_report(report_content, report_number)


if __name__ == "__main__":
    integration_test()
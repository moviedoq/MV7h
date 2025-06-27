# 🔧 Project: User and Task Management System with Frontend Integration
##### Julian Andrés Vargas - 1001218862

---

This project consists of two backend microservices and a frontend interface:

- **User Service:** Manages user creation and deletion.

- **Task Service:** Manages task creation and assignment to users.

- **Frontend:** Provides a simple web interface for interacting with both services.

The system also includes automated testing for both the backend and frontend, with automatic cleanup and PDF reporting of test results.

### ✅ New Features and Changes Implemented

1. HTTP Method for User Deletion

    - A new DELETE endpoint was added to the User Service:

    ```http
    DELETE /users/<user_id>
    ```

    - When a user is deleted, their associated tasks are also deleted via a call to the Task Service.

2. Task Service: Deleting Tasks by User
    - A new DELETE endpoint was added to the Task Service:

    ```http
    DELETE /tasks/user/<user_id>
    ```
    - This endpoint deletes all tasks associated with a given user.

3. Test Data Cleanup and Verification

    - The backend and frontend tests now include:

        - Cleanup of test data by calling the DELETE endpoint after each test.

        - Verification that the user and their tasks were successfully deleted.

    - Cleanup and verification functions were moved to a shared utility module:

        ```bash
        tests/utils/test_utils.py
        ```

4. Reusable Test Utilities
    - A new module was created by moving methods that were used in the back-end test:
        ```bash
        tests/utils/test_utils.py
        ```

    - These functions are now shared between backend and frontend tests.

5. Automated PDF Report Generation
    - A reporting module was created:
tests/reports/report_utils.py

    - Each test automatically generates a sequential PDF report summarizing the test results.

    - Report files are stored in the test_reports/ folder.

    - Reports include:

        - Test steps and their results.

        - Cleanup verification.

        - Error messages if the test fails.

    - Reports are named as report1.pdf, report2.pdf, ..., and never overwrite previous reports.

### ✅ Summary of Changes in the Codebase
| Section                         | Description                                             |
| ------------------------------- | ------------------------------------------------------- |
| `User Service`                  | New `DELETE /users/<user_id>` method implemented        |
| `Task Service`                  | New `DELETE /tasks/user/<user_id>` method implemented   |
| `tests/utils/test_utils.py`     | New shared functions: cleanup, verification, get\_tasks |
| `tests/reports/report_utils.py` | New PDF reporting system with sequential numbering      |
| `BackEnd-Test.py`               | Integrated cleanup, verification, and PDF reporting     |
| `FrontEnd-Test.py`              | Integrated cleanup, verification, and PDF reporting     |

### ⚠️ Both the database and the reports folder are automatically generated in the root of the full repository.

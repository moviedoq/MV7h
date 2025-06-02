from datetime import datetime

class Logger:
    _instance = None
    _log_file = "app.log"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.logs.append(full_message)

        # Escribe en el archivo de log
        with open(self._log_file, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")

# Un Logger muy sencillo como Singleton

import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, message: str):
        # Aquí podrías escribir a archivo; por simplicidad, va a stdout
        print(f"[LOG] {message}")

logger = Logger()

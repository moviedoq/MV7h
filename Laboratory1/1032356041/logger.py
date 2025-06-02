import logging
from datetime import datetime

# Implementación del patrón Singleton para el logger
class Logger:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logs = []
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
            Logger._initialized = True
    
    # Agrega un mensaje al log
    def log(self, message: str, level=logging.INFO):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        self.logger.log(level, message)
        print(log_entry)
    
    # Devuelve todos los logs
    def get_logs(self):
        return self.logs

# Instancia global del logger
logger = Logger()

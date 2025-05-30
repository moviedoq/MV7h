# logger.py
import logging
import sys

class LoggerSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if LoggerSingleton._instance is None:
            LoggerSingleton()
        return LoggerSingleton._instance

    def __init__(self):
        if LoggerSingleton._instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        else:
            self._logger = logging.getLogger("NotificationSystemLogger")
            self._logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            # StreamHandler para la consola
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)
            
            # Opcional: FileHandler para guardar logs en un archivo
            # file_handler = logging.FileHandler('notifications.log')
            # file_handler.setFormatter(formatter)
            # self._logger.addHandler(file_handler)
            
            LoggerSingleton._instance = self
            self._logger.info("Logger initialized.")

    def log(self, message, level=logging.INFO):
        if level == logging.ERROR:
            self._logger.error(message)
        elif level == logging.WARNING:
            self._logger.warning(message)
        else:
            self._logger.info(message)

# Uso global (opcional, pero común para fácil acceso)
logger = LoggerSingleton.get_instance()
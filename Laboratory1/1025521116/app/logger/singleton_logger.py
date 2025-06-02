import logging

class SingletonLogger:
    _instance = None
    _log_history = []  # Aquí guardamos los logs

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("NotificationLogger")
            cls._instance.logger.setLevel(logging.INFO)

            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
        return cls._instance

    def log(self, message):
        self._log_history.append(message)
        self.logger.info(message)

    def get_logs(self):
        return self._log_history
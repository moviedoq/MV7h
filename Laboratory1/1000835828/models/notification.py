class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance
    
    def log(self, message):
        self.logs.append(message)
        print(message)  # También imprimimos en consola
    
    def get_logs(self):
        return self.logs

# Singleton global
logger = Logger()

def send_notification(user, message):
    from handlers import create_handler_chain
    
    # Construir cadena basada en preferencias del usuario
    handler_chain = create_handler_chain()
    
    # Iniciar el proceso con el canal preferido
    logger.log(f"\nIniciando notificación para {user.name}")
    logger.log(f"Canal preferido: {user.preferred_channel}")
    logger.log(f"Canales disponibles: {user.available_channels}")
    
    # Ejecutar la cadena de responsabilidad
    result = handler_chain.handle(user, message)
    
    logger.log(f"Resultado final: {result['status']}")
    return result
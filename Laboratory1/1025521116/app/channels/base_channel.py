import random
from app.logger.singleton_logger import SingletonLogger

# Clase base para los canales de notificación (email, sms, consola, etc.)
class BaseChannel:
    def __init__(self, next_channel=None):
        # Referencia al siguiente canal en la cadena de responsabilidad

        self.next_channel = next_channel

    # Método para asignar el siguiente canal que se usará en caso de fallo
    def set_next(self, channel):
        self.next_channel = channel

    # Método para intentar enviar el mensaje al usuario por este canal
    def send(self, message, user_name):
        # Instancia del logger singleton para registrar intentos
        logger = SingletonLogger()
        
        # Simula aleatoriamente si el envío fue exitoso o fallido
        if random.choice([True, False]):
            # Éxito: registrar log de envío exitoso con detalles
            logger.log(f"[SUCCESS] Sent to {user_name} via {self.name}: {message}")
            return True
        else:
            # Fallo: registrar log de intento fallido
            logger.log(f"[FAILURE] Failed to send to {user_name} via {self.name}")

            # Si hay un siguiente canal en la cadena, intentar enviar con ese canal
            if self.next_channel:
                return self.next_channel.send(message, user_name)
            else:
                # No hay canales de respaldo, registrar error definitivo y devolver False
                logger.log(f"[ERROR] No backup channels left for {user_name}.")
                return False

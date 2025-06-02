# app/channels/sms.py
import random
from app.channels.base_channel import BaseChannel
from app.logger.singleton_logger import SingletonLogger

# Canal de notificación que simula el envío de mensajes SMS
class SMSChannel(BaseChannel):
    def __init__(self, next_channel=None):
        super().__init__(next_channel)
    # Sobrescribe el método send para simular el envío por SMS
    def send(self, user, message):
        # Obtener la instancia singleton del logger para registrar los intentos
        logger = SingletonLogger()  # Correct usage (no ._instance() call)


        # Simular aleatoriamente si el envío es exitoso o falla
        success = random.choice([True, False])

        # Registrar el intento con el resultado (éxito o fallo)
        logger.log(f"Attempting SMS to {user.name}... {'Success' if success else 'Failed'}")

        if success:
            # Si fue exitoso, devolver mensaje confirmando el envío
            return f"SMS sent to {user.name}: {message}"
        elif self.next_channel:
            # Si falló y existe un canal siguiente, pasar la responsabilidad al siguiente canal
            return self.next_channel.send(user, message)
        else:
            # Si no hay más canales y falló, devolver mensaje indicando que todos fallaron
            return f"All channels failed for {user.name}."

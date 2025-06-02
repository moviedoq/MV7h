# app/channels/email.py
import random
from .base_channel import BaseChannel
from ..logger.singleton_logger import SingletonLogger

# Canal de notificación que simula el envío de emails
class EmailChannel(BaseChannel):
    def __init__(self, next_channel=None):
        super().__init__(next_channel)
    # Sobrescribe el método send para simular envío por email
    def send(self, user, message):
        # Obtener la instancia singleton del logger para registrar intentos
        logger = SingletonLogger()
        
        # Simular aleatoriamente éxito o fallo en el envío
        success = random.choice([True, False])
        
        # Registrar intento con resultado (éxito o fallo)
        logger.log(f"Attempting email to {user.name}... {'Success' if success else 'Failed'}")
        
        if success:
            # Si el envío es exitoso, devolver mensaje confirmando envío
            return f"Email sent to {user.name}: {message}"
        elif self.next_channel:
            # Si falló y hay un canal siguiente, pasar la responsabilidad a ese canal
            return self.next_channel.send(user, message)
        else:
            # Si no hay más canales y falló, devolver mensaje de error definitivo
            return f"All channels failed for {user.name}."

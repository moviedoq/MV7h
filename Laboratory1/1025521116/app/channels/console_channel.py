# app/channels/console.py
import random
from app.channels.base_channel import BaseChannel
from app.logger.singleton_logger import SingletonLogger

# Canal de notificación que "envía" mensajes a la consola (simulado)
class ConsoleChannel(BaseChannel):

    def __init__(self, next_channel=None):
        super().__init__(next_channel)
        
    # Sobrescribe el método send para implementar la lógica específica de consola
    def send(self, user, message):
        # Obtener instancia del logger singleton para registrar el intento
        logger = SingletonLogger()

        # Simular aleatoriamente si el envío es exitoso o no
        success = random.choice([True, False])

        # Registrar el intento de notificación en consola con resultado
        logger.log(f"Attempting console notification to {user.name}... {'Success' if success else 'Failed'}")

        if success:
            # Si fue exitoso, imprimir el mensaje en consola y devolver mensaje de éxito
            print(f"[Console Notification] To {user.name}: {message}")
            return f"Console message sent to {user.name}."
        elif self.next_channel:
            # Si falló y existe un canal siguiente en la cadena, intentar enviar por ese canal
            return self.next_channel.send(user, message)
        else:
            # Si falló y no hay más canales, devolver mensaje de error definitivo
            return f"All channels failed for {user.name}."

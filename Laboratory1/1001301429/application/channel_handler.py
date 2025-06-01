from domain.entities.notification import NotificationChannel

class ChannelHandler:
    def __init__(self, channel: NotificationChannel):
        self.channel = channel
        self.next_handler = None

    def set_next(self, handler: 'ChannelHandler') -> 'ChannelHandler':
        self.next_handler = handler
        
    def handle(self, user, message):
        success = self.channel.send(user, message)
        if success:
            # Se envió bien, no se envía más
            return True
        elif self.next_handler:
            # No se envió, se intenta con el siguiente canal
            return self.next_handler.handle(user, message)
        else:
            # No hay más canales para intentar y no se envió
            return False

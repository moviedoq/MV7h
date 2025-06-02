from utils.logger import logger
from factories.handler_factory import HandlerFactory

class NotificationService:
    @staticmethod
    def send_notification(user, message):
        logger.log(f"\nIniciando notificacion para {user.name}")
        logger.log(f"Canal preferido: {user.preferred_channel}")
        logger.log(f"Canales disponibles: {user.available_channels}")
        
        # Crear cadena basada en preferencia del usuario
        handler_chain = HandlerFactory.create_preferred_handler(user)
        
        # Ejecutar la cadena
        result = handler_chain.handle(user, message)
        
        if result:
            logger.log(f"Resultado final: exito por {result['channel']}")
            return result
        else:
            logger.log("Resultado final: todos los canales fallaron")
            return {
                "status": "error",
                "message": "Todos los canales fallaron"
            }
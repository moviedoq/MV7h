from infrastructure.channels.email_channel_handler import EmailChannelHandler
from infrastructure.channels.sms_channel_handler import SMSChannelHandler
from infrastructure.channels.console_channel_handler import ConsoleChannelHandler
from application.channel_handler import ChannelHandler

class SendNotificationService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def send_notification(self, user_name, message: str, priority: str):
        user = self.user_repo.find_by_name(user_name)
        if not user:
            raise ValueError("User not found")

        strategies = {
            "email": EmailChannelHandler(),
            "sms": SMSChannelHandler(),
            "console": ConsoleChannelHandler()
        }

        # Política de canales según prioridad
        priority_channels = {
            "high": ["email", "sms", "console"],
            "medium": ["email", "console"],
            "low": ["console"]
        }

        if priority not in priority_channels:
            raise ValueError(f"Invalid priority '{priority}'")

        allowed_channels = priority_channels[priority]

        # Validar que el canal preferido está disponible y permitido
        preferred = user.preferred_channel
        if preferred not in user.available_channels or preferred not in allowed_channels:
            preferred = None  # no se usa el preferido si no está permitido o no está disponible

        # Armar lista de canales a usar: primero el preferido si aplica
        selected_channels = []
        if preferred:
            selected_channels.append(preferred)

        # Luego agregar el resto de canales permitidos y disponibles, sin repetir el preferido
        for ch in allowed_channels:
            if ch != preferred and ch in user.available_channels:
                selected_channels.append(ch)

        if not selected_channels:
            raise ValueError("No available channels match the priority policy")

        # Construir la cadena de responsabilidad
        first_handler = None
        prev_handler = None

        for channel_name in selected_channels:
            handler = ChannelHandler(strategies[channel_name])
            if not first_handler:
                first_handler = handler
            if prev_handler:
                prev_handler.set_next(handler)
            prev_handler = handler

        return first_handler.handle(user, message)

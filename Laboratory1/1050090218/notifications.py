# notifications.py
from abc import ABC, abstractmethod
from typing import List, Optional
import logging # <--- AÑADIR ESTA LÍNEA
from models import User
from utils import simulate_failure
from logger import logger

# --- Patrón Estrategia: Define cómo se envía una notificación por un canal específico ---
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, user: User, message: str, priority: str) -> bool:
        pass

class EmailStrategy(NotificationStrategy):
    def send(self, user: User, message: str, priority: str) -> bool:
        channel_name = "email"
        logger.log(f"Attempting to send via {channel_name} to {user.name} (Priority: {priority}). Message: '{message}'")
        success = simulate_failure(channel_name)
        if success:
            logger.log(f"SUCCESS: {channel_name} notification sent to {user.name}.")
        else:
            # CORREGIDO:
            logger.log(f"FAILURE: {channel_name} notification failed for {user.name}.", level=logging.WARNING)
        return success

class SMSStrategy(NotificationStrategy):
    def send(self, user: User, message: str, priority: str) -> bool:
        channel_name = "sms"
        logger.log(f"Attempting to send via {channel_name} to {user.name} (Priority: {priority}). Message: '{message}'")
        success = simulate_failure(channel_name)
        if success:
            logger.log(f"SUCCESS: {channel_name} notification sent to {user.name}.")
        else:
            # CORREGIDO:
            logger.log(f"FAILURE: {channel_name} notification failed for {user.name}.", level=logging.WARNING)
        return success

class ConsoleStrategy(NotificationStrategy):
    def send(self, user: User, message: str, priority: str) -> bool:
        channel_name = "console"
        logger.log(f"Attempting to send via {channel_name} to {user.name} (Priority: {priority}). Message: '{message}'")
        print(f"\nCONSOLE NOTIFICATION for {user.name} (Priority: {priority}):\n{message}\n")
        logger.log(f"SUCCESS: {channel_name} notification sent to {user.name}.")
        return True

# --- Patrón Cadena de Responsabilidad: Gestiona el flujo de intentos de notificación ---
class NotificationHandler(ABC):
    def __init__(self, channel_name: str, strategy: NotificationStrategy):
        self.channel_name = channel_name
        self.strategy = strategy
        self._next_handler: Optional[NotificationHandler] = None

    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle_request(self, user: User, message: str, priority: str, attempted_channels: List[str]) -> bool:
        pass

class ChannelNotificationHandler(NotificationHandler):
    def handle_request(self, user: User, message: str, priority: str, attempted_channels: List[str]) -> bool:
        if self.channel_name in user.available_channels and self.channel_name not in attempted_channels:
            attempted_channels.append(self.channel_name)
            if self.strategy.send(user, message, priority):
                return True
        
        if self._next_handler:
            return self._next_handler.handle_request(user, message, priority, attempted_channels)
        
        return False


# --- Servicio de Notificación ---
class NotificationService:
    def __init__(self):
        self.strategies = {
            "email": EmailStrategy(),
            "sms": SMSStrategy(),
            "console": ConsoleStrategy()
        }
        self.base_handlers = {
            name: ChannelNotificationHandler(name, strategy)
            for name, strategy in self.strategies.items()
        }

    def send_notification(self, user: User, message: str, priority: str) -> str:
        logger.log(f"Received notification request for user {user.name}. Preferred: {user.preferred_channel}, Available: {user.available_channels}")
        
        ordered_channels_to_try: List[str] = []

        if user.preferred_channel in user.available_channels:
            ordered_channels_to_try.append(user.preferred_channel)

        for channel in user.available_channels:
            if channel not in ordered_channels_to_try:
                ordered_channels_to_try.append(channel)
        
        if not ordered_channels_to_try:
            # CORREGIDO:
            logger.log(f"No channels configured or available for user {user.name}. Notification failed.", level=logging.ERROR)
            return f"Notification failed for {user.name}: No channels available or configured."

        current_chain_head: Optional[NotificationHandler] = None
        previous_handler_in_chain: Optional[NotificationHandler] = None

        for channel_name in ordered_channels_to_try:
            handler_instance = self.base_handlers.get(channel_name)
            if not handler_instance:
                # CORREGIDO:
                logger.log(f"Warning: Handler for channel '{channel_name}' not found in base_handlers.", level=logging.WARNING)
                continue
            
            handler_instance._next_handler = None 

            if current_chain_head is None:
                current_chain_head = handler_instance
            
            if previous_handler_in_chain:
                previous_handler_in_chain.set_next(handler_instance)
            
            previous_handler_in_chain = handler_instance
        
        attempted_channels: List[str] = []
        if current_chain_head:
            success = current_chain_head.handle_request(user, message, priority, attempted_channels)
            if success:
                final_channel = attempted_channels[-1] 
                result_message = f"Notification for {user.name} sent successfully via {final_channel}."
                logger.log(result_message)
                return result_message
            else:
                result_message = f"Notification for {user.name} failed on all attempted channels: {', '.join(attempted_channels)}."
                # CORREGIDO:
                logger.log(result_message, level=logging.ERROR)
                return result_message
        else:
            result_message = f"Notification failed for {user.name}: No valid channels to form a chain."
            # CORREGIDO:
            logger.log(result_message, level=logging.ERROR)
            return result_message
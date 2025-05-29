# notification_system/handlers.py
import abc
import random
from logger import Logger
from models import User # Import User for type hinting

class NotificationHandler(abc.ABC):
    """
    Abstract base class for notification channel handlers.
    Implements the Chain of Responsibility pattern.
    """
    def __init__(self):
        self._next_handler: NotificationHandler = None

    def set_next(self, handler: "NotificationHandler") -> "NotificationHandler":
        """
        Sets the next handler in the chain.
        """
        self._next_handler = handler
        return handler

    @abc.abstractmethod
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Abstract method to handle a notification attempt for a specific channel.
        Returns True if delivery was successful, False otherwise.
        """
        pass

    def _simulate_delivery(self, channel_name: str, user_name: str) -> bool:
        """
        Simulates the delivery attempt for a channel.
        Randomly returns True for success or False for failure.
        Logs the attempt and result.
        """
        success = random.choice([True, False]) # Simulate random failure
        if success:
            Logger.log(f"Attempting to send notification to {user_name} via {channel_name} - SUCCESS")
        else:
            Logger.log(f"Attempting to send notification to {user_name} via {channel_name} - FAILED")
        return success

class EmailHandler(NotificationHandler):
    """
    Concrete handler for email notifications.
    """
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Handles email notification. If successful, stops the chain.
        If failed, passes to the next handler if available.
        """
        if self._simulate_delivery("email", user.name):
            Logger.log(f"Notification sent successfully to {user.name} via Email: '{message}'")
            return True
        elif self._next_handler:
            Logger.log(f"Email delivery failed for {user.name}. Trying next channel...")
            return self._next_handler.handle_notification(user, message)
        else:
            Logger.log(f"Email delivery failed for {user.name} and no more handlers in chain.")
            return False

class SMSHandler(NotificationHandler):
    """
    Concrete handler for SMS notifications.
    """
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Handles SMS notification. If successful, stops the chain.
        If failed, passes to the next handler if available.
        """
        if self._simulate_delivery("sms", user.name):
            Logger.log(f"Notification sent successfully to {user.name} via SMS: '{message}'")
            return True
        elif self._next_handler:
            Logger.log(f"SMS delivery failed for {user.name}. Trying next channel...")
            return self._next_handler.handle_notification(user, message)
        else:
            Logger.log(f"SMS delivery failed for {user.name} and no more handlers in chain.")
            return False
from patterns.chain_of_responsibility import create_notification_chain
from models.notification import Notification

class NotificationService:
    def __init__(self, channel_factory):
        self.channel_factory = channel_factory
        self.notifications = []  # Store sent notifications

    def send_notification(self, user, message, priority):
        preferred_channel = user.preferred_channel
        available_channels = user.available_channels

        chain = create_notification_chain(preferred_channel, available_channels, self.channel_factory)
        if chain:
            result = chain.handle(message, user.name)
            if result:
                # Store the notification
                self.notifications.append(Notification(user.name, message, priority))
                return {"message": "Notification sent successfully"}, 200
            else:
                return {"error": "Failed to send notification"}, 500
        return {"error": "No channels available"}, 500

    def get_all_notifications(self):
        # Return a list of dicts for JSON serialization
        return [
            {
                "user_name": n.user_name,
                "message": n.message,
                "priority": n.priority
            }
            for n in self.notifications
        ], 200
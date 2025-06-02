class NotificationController:
    def __init__(self, notification_service, user_service):
        self.notification_service = notification_service
        self.user_service = user_service

    def send_notification(self, user_name, message, priority):
        user = self.user_service.find_user(user_name)
        if not user:
            return {"error": "User not found"}, 404
        return self.notification_service.send_notification(user, message, priority)

    def get_notifications(self):
        return self.notification_service.get_all_notifications()
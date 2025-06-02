import random

class SendNotification:
    def sendNoification(self, priority):
        pass

class EmailNotification(SendNotification):
    def sendNotification(self, priority):
        random_bool = random.choice([True, False])
        if random_bool:
            return f"email sent successfully with {priority} priority."
        else:
            return "Failed to send email."

class SMSNotification(SendNotification):
    def sendNotification(self, priority):
        random_bool = random.choice([True, False])
        if random_bool:
            return f"sms sent successfully with {priority} priority"
        else:
            return "Failed to send SMS."

class CallNotification(SendNotification):
    def sendNotification(self, priority):
        random_bool = random.choice([True, False])
        if random_bool:
            return f"call made successfully with {priority} priority"
        else:
            return "Failed to make call."
        
def executeNotification(channel, priority):
    temp = False
    for i in channel:
        if i == "email":
            message = EmailNotification().sendNotification(priority)
        elif i == "sms":
            message = SMSNotification().sendNotification(priority)
        elif i == "call":
            message = CallNotification().sendNotification(priority)
        if  not temp:
            notification = f"Using the preferred channel {channel[0]}, " + message + "\n"
            temp = True
        else:
            notification = notification + f"Using the channel {i}, " + message + "\n"

        if "Failed" not in message:
            break
        
    return notification
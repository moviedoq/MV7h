class ChannelFactory:
    @staticmethod
    def create_channel(channel_type):
        if channel_type == "email":
            from channels.email_channel import EmailChannel
            return EmailChannel()
        elif channel_type == "sms":
            from channels.sms_channel import SmsChannel
            return SmsChannel()
        elif channel_type == "console":
            from channels.console_channel import ConsoleChannel
            return ConsoleChannel()
        else:
            raise ValueError(f"Unknown channel type: {channel_type}")
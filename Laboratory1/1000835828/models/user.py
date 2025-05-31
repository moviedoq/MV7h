class User:
    def __init__(self, name, preferred_channel, available_channels):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
    
    def __repr__(self):
        return f"User(name={self.name}, preferred={self.preferred_channel}, available={self.available_channels})"
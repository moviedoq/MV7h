class Logger:
    logs = []  # Class variable shared by all instances

    def log(self, message):
        Logger.logs.append(message)
        print(message)

    def get_logs(self):
        return Logger.logs

    def clear_logs(self):
        Logger.logs = []
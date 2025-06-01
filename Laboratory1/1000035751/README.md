# REST API for managing users and notifications

**By:** Santiago Villota Alava

## 📕 Description

This proyect implements a REST API in flask, for managing users and sending notifications. Users can register depending on their prefered method of communications (SMS, email, phonecall, etc).

In case of communication failure, the system tries again with a fallback communication method, if availible.

All user notifications are logged.

## 🎯 Objectives

**Use:**

- Flask for REST API.
- Chain of responsability pattern.
- Singleton pattern.

**Implement:**

- System response for channel failure and retry fallback.
- User creation, specifing name, preffered_channel, available_channels.
- Send notifications, specifing username of receiver, message, and priority of message.
- Logger for notifications.
- No database.
- Modular, clean and documented code.

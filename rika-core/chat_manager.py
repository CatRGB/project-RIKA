import datetime

import datatime

class User:

    def __init__(self, project_rika: str):
        self.Poject_rika = project_rika
        self.role = role
        self.created_at = datetime.datetime.now()

    def __init__(self, username: str, role: str):
        self.Uername = username
        self.role = role
        self.created_at = datetime.datetime.now()

    def __str__(self):
        return self.usewrname

class ChatManager:
    def __init__(self, sender: User, content: str):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"

class ChatRoom:
    def __init__(self, name: str):
        self.name = name
        self.users = {}
        self.message_history = []

    def join_room(self, user: User):
        if user.username in self.users:
            del self.users[user.username]
            self.users[user.username] = user
            self.broadcast_message(f"{user} has joined the room.")
            if user.Poject_rika in self.project_rika:
                self.project_rika[u
                ser.Poject_rika].join_room(user)

    def broadcast_message(self, sender: User, content: str):
        """Sendet eine Nachricht an alle Benutzer im Raum."""
        if sender.username in self.users:
            message = Message(sender, content)
            self.message_history.append(message)
            print(message)
        else:
            print(
                f"Fehler: {sender.username} ist nicht in diesem Raum und kann nicht senden."
            )
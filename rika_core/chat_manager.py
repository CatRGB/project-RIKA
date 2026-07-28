import datetime

from rika_core.datenbank import (
    create_chat as create_chat_in_database,
    create_local_user,
    get_local_user,
    load_messages,
    save_message,
)


class User:
    def __init__(
        self,
        username: str,
        role: str,
        user_id: int | None = None,
        created_at: datetime.datetime | None = None,
    ):
        self.id = user_id
        self.username = username
        self.role = role
        self.created_at = created_at or datetime.datetime.now()

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Message:
    def __init__(
        self,
        sender: User,
        content: str,
        timestamp: datetime.datetime | None = None,
    ):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.datetime.now()

    def __str__(self):
        formatted_time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return (
            f"[{formatted_time}] "
            f"{self.sender.username}: "
            f"{self.content}"
        )

    def to_dict(self):
        return {
            "sender_id": self.sender.id,
            "sender": self.sender.username,
            "role": self.sender.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


class ChatRoom:
    def __init__(
        self,
        name: str,
        chat_id: int | None = None,
    ):
        self.id = chat_id
        self.name = name
        self.users: dict[str, User] = {}
        self.message_history: list[Message] = []
        self.local_user: User | None = None

        # Nur vorhandene Chats besitzen bereits Nachrichten.
        if self.id is not None:
            self.load_chat_history()

    def create_connection():
        password = os.getenv("DB_PASSWORD")

        if not password:
            raise RuntimeError(
                "Die Umgebungsvariable DB_PASSWORD wurde nicht gesetzt."
            )

        return pymysql.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "rika"),
            user=os.getenv("DB_USER", "rika_user"),
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def get_or_create_local_user(self):
        """Lädt den lokalen Benutzer oder erstellt ihn."""

        user_data = get_local_user()

        if user_data is None:
            username = input(
                "Wie möchtest du von RIKA genannt werden? "
            ).strip()

            while not username:
                username = input(
                    "Bitte gib einen gültigen Benutzernamen ein: "
                ).strip()

            user_data = create_local_user(username)

        user = User(
            user_id=user_data["id"],
            username=user_data["username"],
            role=user_data["role"],
            created_at=user_data.get("created_at"),
        )

        self.local_user = user
        return user

    def create(self):
        """Erstellt den Chat in MariaDB."""

        if self.id is not None:
            print(f"Der Chatraum '{self.name}' existiert bereits.")
            return

        user = self.get_or_create_local_user()

        chat_data = create_chat_in_database(
            chat_name=self.name,
            user_id=user.id,
        )
        self.id = chat_data["id"]

        self.join_room(user)

        print(
            f"Neuer Chatraum '{self.name}' wurde erstellt. "
            f"{user.username} ist beigetreten."
        )

    def join_room(self, user: User):
        """Fügt einen Benutzer zum Chatraum hinzu."""

        if user.username in self.users:
            print(f"{user.username} ist bereits im Raum.")
            return

        self.users[user.username] = user
        print(f"{user.username} hat den Raum '{self.name}' betreten.")

    def leave_room(self, user: User):
        """Entfernt einen Benutzer aus dem Chatraum."""

        if user.username not in self.users:
            print(f"{user.username} befindet sich nicht im Raum.")
            return

        del self.users[user.username]
        print(f"{user.username} hat den Raum '{self.name}' verlassen.")

    def broadcast_message(self, sender: User, content: str):
        """Speichert eine neue Nachricht in MariaDB."""

        if self.id is None:
            print("Der Chat wurde noch nicht erstellt.")
            return

        if sender.id is None:
            print(f"{sender.username} besitzt keine Datenbank-ID.")
            return

        if sender.username not in self.users:
            print(
                f"{sender.username} befindet sich nicht im Raum "
                "und kann keine Nachricht senden."
            )
            return

        content = content.strip()

        if not content:
            print("Eine leere Nachricht wird nicht gespeichert.")
            return

        message = Message(
            sender=sender,
            content=content,
        )

        save_message(
            chat_id=self.id,
            sender_id=sender.id,
            content=message.content,
        )

        self.message_history.append(message)
        print(message)

    def load_chat_history(self):
        """Lädt den Chatverlauf aus MariaDB."""

        if self.id is None:
            return

        self.message_history.clear()
        message_data_list = load_messages(self.id)

        for message_data in message_data_list:
            sender = User(
                user_id=message_data["sender_id"],
                username=message_data["sender_username"],
                role=message_data["sender_role"],
            )

            message = Message(
                sender=sender,
                content=message_data["content"],
                timestamp=message_data["timestamp"],
            )

            self.message_history.append(message)

    def show_chat_history(self):
        """Zeigt alle geladenen Nachrichten an."""

        print(f"\nChatverlauf für Raum '{self.name}':")

        if not self.message_history:
            print("Es wurden noch keine Nachrichten geschrieben.")
            return

        for message in self.message_history:
            print(message)


if __name__ == "__main__":
    lobby = ChatRoom(name="Lobby")
    lobby.create()

    user = lobby.local_user

    if user is not None:
        lobby.broadcast_message(
            sender=user,
            content="Hallo, RIKA!",
        )

    lobby.show_chat_history()
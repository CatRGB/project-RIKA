import os
import pymysql


def create_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "mariadb"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "rika"),
        user=os.getenv("DB_USER", "rika_user"),
        password=os.getenv("Josi"),
        cursorclass=pymysql.cursors.DictCursor
    )


def get_local_user():
    connection = create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, role
                FROM users
                WHERE is_local_user = TRUE
                LIMIT 1
                """
            )

            return cursor.fetchone()
    finally:
        connection.close()


def create_local_user(username: str):
    connection = create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, role, is_local_user)
                VALUES (%s, 'user', TRUE)
                """,
                (username,)
            )

            user_id = cursor.lastrowid
            connection.commit()

            return {
                "id": user_id,
                "username": username,
                "role": "user"
            }
    finally:
        connection.close()

def create_chat(chat_name: str):
    connection = create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chats (name)
                VALUES (%s)
                """,
                (chat_name,)
            )

            chat_id = cursor.lastrowid
            connection.commit()

            return {
                "id": chat_id,
                "name": chat_name
            }
    finally:
        connection.close()

def load_messages(chat_id: int):
    connection = create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT m.id, m.content, m.timestamp, u.id AS sender_id, u.username AS sender_username, u.role AS sender_role
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.chat_id = %s
                ORDER BY m.timestamp ASC
                """,
                (chat_id,)
            )

            return cursor.fetchall()
    finally:
        connection.close()

def save_message(chat_id: int, sender_id: int, content: str):
    connection = create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (chat_id, sender_id, content)
                VALUES (%s, %s, %s)
                """,
                (chat_id, sender_id, content)
            )

            message_id = cursor.lastrowid
            connection.commit()

            return {
                "id": message_id,
                "chat_id": chat_id,
                "sender_id": sender_id,
                "content": content
            }
    finally:
        connection.close()
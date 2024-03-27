import sqlite3

from fastapi import HTTPException
from database.models import User
from database.connect import create_connection


def create_table() -> None:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(512) NOT NULL
        )
    """
    )

    connection.commit()
    connection.close()


def insert_user(user: User) -> None:
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (email, password)
            VALUES (?, ?)
        """,
            (user.email, user.password),
        )

        connection.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")

    connection.close()


def get_all_users() -> list[User]:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    connection.close()
    return [User(email=row[1], password=row[2]) for row in rows]

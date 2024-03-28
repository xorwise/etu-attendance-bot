import sqlite3


def create_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("etu.db")
    return conn

import os
import psycopg

"""Module for connecting to the database"""


async def connect() -> psycopg.AsyncConnection:
    """Function for connecting to the database

    Returns:
        psycopg.AsyncConnection: async connection to the database
    """
    conn = await psycopg.AsyncConnection.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    return conn

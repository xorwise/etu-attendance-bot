from database.models import User
from database import connect
from utils.exceptions import EtuNotFoundException

"""Users queries module"""


async def get_user(id: int) -> User:
    """Function for getting a user from the database

    Args:
        id (int): user id
    Returns:
        User: user
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT id, email, group_id FROM users WHERE id = %s
            """,
            (id,),
        )
        row = await cursor.fetchone()
    await conn.close()
    if not row:
        raise EtuNotFoundException
    return User(id=row[0], email=row[1], group_id=row[2])


async def insert_or_update_user(user: User) -> None:
    """Function for inserting a new user if it doesn't exist, otherwise updating it

    Args:
        user (User): provided user
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            INSERT INTO users (id, email, group_id) VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (user.id, user.email, user.group_id),
        )
    await conn.commit()
    await conn.close()


async def get_all_users() -> list[User]:
    """Function for getting all users from the database

    Returns:
        list[User]: list of users
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT id, email, group_id FROM users
            """
        )
        rows = await cursor.fetchall()
    await conn.close()
    return [User(id=row[0], email=row[1], group_id=row[2]) for row in rows]


async def delete_user(id: int) -> None:
    """Function for deleting a user

    Args:
        id (int): user id
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            DELETE FROM users WHERE id = %s
            """,
            (id,),
        )
        if cursor.rowcount == 0:
            raise EtuNotFoundException(
                "Пользователь не был авторизован! Авторизуйтесь с помощью команды /login."
            )
    await conn.commit()
    await conn.close()


async def is_user_present(user_id: int) -> bool:
    """Function for checking if a user is present in the database

    Args:
        user_id (int): user id
    Returns:
        bool: True if user is present, False otherwise
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT id FROM users WHERE id = %s
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
    await conn.close()
    return bool(row)


async def get_user_deadlines(user_id: int, weekday: str) -> list[str]:
    conn = await connect()
    deadlines = []
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT deadline_id FROM users_deadlines WHERE user_id = %s 
            """,
            (user_id,),
        )
        rows = await cursor.fetchall()
        for row in rows:
            await cursor.execute(
                """
                SELECT weekday, time FROM deadlines WHERE id = %s
                """,
                (row[0],),
            )
            row = await cursor.fetchone()
            if row[0] == weekday:
                deadlines.append(row[1])
    await conn.close()
    return deadlines


async def insert_or_update_user_deadlines(
    user_id: int, subjects: dict[str, list[dict]]
) -> None:
    """Function for inserting or updating user deadlines

    Args:
        user_id (int): user id
        subjects (dict[str, list[dict]]): subjects
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        for weekday in subjects:
            for subject in subjects[weekday]:
                await cursor.execute(
                    """
                SELECT id FROM deadlines WHERE weekday = %s AND time = %s;
                """,
                    (weekday, subject["time"]),
                )
                row = await cursor.fetchone()
                await cursor.execute(
                    """
                    INSERT INTO users_deadlines (user_id, deadline_id) VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (user_id, row[0]),
                )
    await conn.commit()
    await conn.close()


async def insert_or_delete_user_deadline(user_id: int, weekday: str, time: str) -> None:
    """Function for inserting or deleting user deadline

    Args:
        user_id (int): user id
        weekday (str): weekday ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
        time (str): time HH:MM
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT id FROM deadlines WHERE weekday = %s AND time = %s
            """,
            (weekday, time),
        )
        row = await cursor.fetchone()
        await cursor.execute(
            """
        SELECT user_id, deadline_id FROM users_deadlines WHERE user_id = %s AND deadline_id = %s;
        """,
            (user_id, row[0]),
        )
        row1 = await cursor.fetchone()
        if not row1:
            await cursor.execute(
                """
                INSERT INTO users_deadlines (user_id, deadline_id) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (user_id, row[0]),
            )
        else:
            await cursor.execute(
                """
                DELETE FROM users_deadlines WHERE user_id = %s AND deadline_id = %s
                """,
                (user_id, row[0]),
            )
    await conn.commit()
    await conn.close()


async def get_users_by_deadline(weekday: str, time: str) -> list[User]:
    """Function for getting users by deadline

    Args:
        weekday (str): weekday ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
        time (str): time HH:MM

    Returns:
        list[User]: list of users
    """
    conn = await connect()
    users = []
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT user_id FROM users_deadlines 
            WHERE deadline_id = (SELECT id FROM deadlines WHERE weekday = %s AND time = %s)
            """,
            (weekday, time),
        )
        rows = await cursor.fetchall()
        for row in rows:
            users.append(await get_user(row[0]))
    await conn.close()
    return users

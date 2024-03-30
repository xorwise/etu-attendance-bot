from database.models import User
from database import connect
from utils.exceptions import EtuNotFoundException


async def create_tables():
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE
            );
            """
        )
        await conn.commit()
        await cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cookies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                domain TEXT,
                path TEXT,
                expiry INTEGER,
                httpOnly BOOLEAN,
                secure BOOLEAN,
                user_email TEXT,
                FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
            );
            """
        )
        await conn.commit()
        await conn.close()


async def insert_or_update_user(user: User) -> None:
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            INSERT INTO users (id, email) VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            (user.id, user.email),
        )
    await conn.commit()
    await conn.close()


async def get_all_users() -> list[User]:
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT id, email FROM users
            """
        )
        rows = await cursor.fetchall()
    await conn.close()
    return [User(id=row[0], email=row[1]) for row in rows]


async def insert_or_update_cookies(cookies: list[dict], email: str):
    conn = await connect()
    async with conn.cursor() as cursor:
        for cookie in cookies:
            await cursor.execute(
                """
                SELECT id FROM cookies WHERE name = %s AND user_email = %s
                """,
                (cookie["name"], email),
            )
            row = await cursor.fetchone()
            if row:
                await cursor.execute(
                    """
                    UPDATE cookies SET name = %s, value = %s, domain = %s, path = %s, expiry = %s, httpOnly = %s, secure = %s WHERE id = %s
                    """,
                    (
                        cookie["name"],
                        cookie["value"],
                        cookie["domain"],
                        cookie["path"],
                        cookie["expiry"],
                        cookie["httpOnly"],
                        cookie["secure"],
                        row[0],
                    ),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO cookies (name, value, domain, path, expiry, httpOnly, secure, user_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        cookie["name"],
                        cookie["value"],
                        cookie["domain"],
                        cookie["path"],
                        cookie["expiry"],
                        cookie["httpOnly"],
                        cookie["secure"],
                        email,
                    ),
                )
    await conn.commit()
    await conn.close()


async def get_cookies_by_user(email: str) -> list[dict]:
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT name, value, domain, path, expiry, httpOnly, secure FROM cookies WHERE user_email = %s
            """,
            (email,),
        )
        rows = await cursor.fetchall()
    await conn.close()
    return [
        {
            "name": row[0],
            "value": row[1],
            "domain": row[2],
            "path": row[3],
            "expiry": row[4],
            "httpOnly": row[5],
            "secure": row[6],
        }
        for row in rows
    ]


async def delete_user(id: int) -> None:
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

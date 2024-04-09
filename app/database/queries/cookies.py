from database import connect


async def insert_or_update_cookies(cookies: list[dict], email: str) -> None:
    """Function for inserting cookies if they doesn't exist for a specific user, otherwise updating them

    Args:
        cookies (list[dict]): cookies
        email (str): user email
    """
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
    """Function for getting cookies for a specific user

    Args:
        email (str): user email
    Returns:
        list[dict]: list of cookies
    """
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

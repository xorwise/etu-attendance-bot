from database import connect

"""Groups queries module"""


async def insert_all_groups(groups: list[dict]) -> None:
    """Insert all groups into the database

    Args:
        groups (list[dict]): list of groups
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        for group in groups:
            await cursor.execute(
                """
                INSERT INTO groups (id, api_id) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (group["id"], group["api_id"]),
            )
    await conn.commit()


async def get_group_api_id(group_id: int) -> int:
    """Function for getting group api id

    Args:
        group_id (int): group id
    Returns:
        int: group api id
    """
    conn = await connect()
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT api_id FROM groups WHERE id = %s
            """,
            (group_id,),
        )
        row = await cursor.fetchone()
    await conn.close()
    return row[0]

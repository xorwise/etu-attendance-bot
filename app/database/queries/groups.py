from database import connect


async def insert_all_groups(groups: list[dict]) -> None:
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

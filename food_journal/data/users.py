from psycopg import AsyncConnection


async def add_user(conninfo: str, username: str, password: str):
    async with await AsyncConnection.connect(conninfo) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO migrations (name) VALUES (%s)", (migration_name,)
            )
            await conn.commit()

from psycopg import AsyncConnection
from psycopg.rows import class_row
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str


async def get_user(conn: AsyncConnection, username: str) -> User | None:
    async with conn.cursor(row_factory=class_row(User)) as cur:
        await cur.execute(
            "SELECT id, username, password FROM users WHERE username = %s", (username,)
        )
        return await cur.fetchone()


async def user_exists(conn: AsyncConnection, username: str) -> bool:
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT COUNT(id) FROM users WHERE username = %s", (username,)
        )
        result = await cur.fetchone()
        if result is None:
            return False
        return result[0] > 0


async def add_user(conn: AsyncConnection, username: str, password: str):
    if await user_exists(conn, username):
        return
    async with conn.cursor() as cur:
        await cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        await conn.commit()

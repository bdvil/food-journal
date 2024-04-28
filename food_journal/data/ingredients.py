from datetime import datetime

from psycopg import AsyncConnection
from psycopg.rows import class_row
from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    ingredient: str
    user_id: int
    count: int
    last_used: datetime
    is_group: bool


async def get_latest_ingredients(
    conn: AsyncConnection, user_id: int, query: str
) -> list[Ingredient]:
    async with conn.cursor(row_factory=class_row(Ingredient)) as cur:
        await cur.execute(
            "SELECT * FROM ingredients WHERE user_id = %s AND ingredient LIKE %s LIMIT 10",
            (user_id, f"%{query}%"),
        )
        return await cur.fetchall()

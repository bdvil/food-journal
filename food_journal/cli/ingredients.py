from datetime import date, datetime

import click
from psycopg import Connection
from psycopg.rows import class_row

from food_journal.config import load_config
from food_journal.constants import LOGGER
from food_journal.data.ingredients import Ingredient
from food_journal.security import hash_password


@click.group("ingredients")
def ingredients_group():
    pass


def get_ingredient(conn: Connection, user_id: int) -> Ingredient | None:
    with conn.cursor(row_factory=class_row(Ingredient)) as cur:
        cur.execute(
            "SELECT * FROM ingredients WHERE user_id = %s",
            (user_id,),
        )
        return cur.fetchone()


def ingredient_exists(conn: Connection, user_id: int, ingredient: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(id) FROM ingredients WHERE user_id = %s AND ingredient = %s",
            (user_id, ingredient),
        )
        result = cur.fetchone()
        if result is None:
            return False
        return result[0] > 0


@ingredients_group.command("add")
@click.argument("user_id", type=int)
@click.argument("ingredient", type=str)
@click.option("--group", is_flag=True)
def ingredient_add_command(user_id: int, ingredient: str, group: bool):
    config = load_config()
    with Connection.connect(config.database_url) as conn:
        if ingredient_exists(conn, user_id, ingredient):
            LOGGER.info("ingredient already exists.")
            return

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO ingredients (ingredient, user_id, count, last_userd, is_group) VALUES (%s, %s, %s, %s, %s)",
                (ingredient, user_id, 1, datetime.now(), group),
            )
            conn.commit()
        LOGGER.info("ingredient added.")

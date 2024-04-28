from datetime import datetime

import click
from psycopg import Connection
from psycopg.rows import class_row

from food_journal.cli.users import get_user
from food_journal.config import load_config
from food_journal.data.ingredients import Ingredient


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
@click.argument("username", type=str)
@click.argument("ingredient", type=str)
@click.option("--group", is_flag=True)
def ingredient_add_command(username: str, ingredient: str, group: bool):
    config = load_config()
    with Connection.connect(config.database_url) as conn:
        user = get_user(conn, username)
        if user is None:
            click.echo(click.style(f"User {username} does not exist.", fg="red"))
            return

        if ingredient_exists(conn, user.id, ingredient):
            click.echo(click.style("Ingredient already exists.", fg="red"))
            return

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO ingredients (ingredient, user_id, count, last_used, is_group) VALUES (%s, %s, %s, %s, %s)",
                (ingredient, user.id, 1, datetime.now(), group),
            )
            conn.commit()
        click.echo(click.style("Ingredient added.", fg="green"))

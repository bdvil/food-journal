import click
from psycopg import Connection
from psycopg.rows import class_row

from food_journal.config import load_config
from food_journal.constants import LOGGER
from food_journal.data.users import User
from food_journal.security import hash_password


@click.group("users")
def users_group():
    pass


def get_user(conn: Connection, username: str) -> User | None:
    with conn.cursor(row_factory=class_row(User)) as cur:
        cur.execute(
            "SELECT id, username, password FROM users WHERE username = %s", (username,)
        )
        return cur.fetchone()


def user_exists(conn: Connection, username: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(id) FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result is None:
            return False
        return result[0] > 0


@users_group.command("add")
@click.argument("username", type=str)
@click.password_option()
def user_add_command(username: str, password: str):
    config = load_config()
    with Connection.connect(config.database_url) as conn:
        if user_exists(conn, username):
            LOGGER.info("User already exists.")
            return

        encoded_pass = hash_password(password)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, encoded_pass),
            )
            conn.commit()
        LOGGER.info("User added.")


@users_group.command("search")
@click.argument("username", type=str)
def user_search_command(username: str):
    config = load_config()
    with Connection.connect(config.database_url) as conn:
        user = get_user(conn, username)
        if user is None:
            LOGGER.info("Does not exist")
            return
        LOGGER.info(f"* {user.username}")

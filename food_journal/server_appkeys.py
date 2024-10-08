from aiohttp.web import AppKey
from psycopg import AsyncConnection

from food_journal.config import Config

config_key = AppKey("config", Config)
pg_key = AppKey("pg", AsyncConnection)


__all__ = ["config_key", "pg_key"]

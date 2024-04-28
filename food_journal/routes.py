from aiohttp import web

from food_journal.handlers.index import handle_index
from food_journal.handlers.ingredients import search_ingredients

ROUTES: list[web.RouteDef] = [
    web.get("/", handle_index),
    web.get("/search/ingredients", search_ingredients),
]


__all__ = ["ROUTES"]

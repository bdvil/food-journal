from aiohttp import web

from food_journal.handlers.index import handle_index

ROUTES: list[web.RouteDef] = [web.get("/", handle_index)]


__all__ = ["ROUTES"]

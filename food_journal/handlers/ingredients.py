from aiohttp import web

from food_journal.data.ingredients import get_latest_ingredients
from food_journal.server_appkeys import pg_key


async def search_ingredients(request: web.Request) -> web.Response:
    ingredient = request.query.get("ingredient", "")
    similar_ingredients = await get_latest_ingredients(
        request.app[pg_key], 0, ingredient
    )
    response = [f"<li>{e.ingredient}</li>" for e in similar_ingredients]
    response_text = "No match"
    if len(response):
        response_text = "<ul>" + "".join(response) + "</ul>"
    return web.Response(text=response_text)

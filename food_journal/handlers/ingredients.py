from aiohttp import web

from food_journal.data.ingredients import get_latest_ingredients
from food_journal.data.users import get_user
from food_journal.server_appkeys import pg_key


async def search_ingredients(request: web.Request) -> web.Response:
    ingredient = request.query.get("ingredient", "")
    conn = request.app[pg_key]
    user = await get_user(conn, "bdvllrs")
    if user is None:
        return web.Response(text="")
    similar_ingredients = await get_latest_ingredients(conn, user.id, ingredient)
    response = [
        f'<li '
        f'id="search-result-{e.id}" '
        f'data-ingredient-id="{e.id}" '
        f'data-selected="{'true' if k == 0 else 'false'}">{e.ingredient}</li>'
        for k, e in enumerate(similar_ingredients)
    ]
    if not len(response):
        return web.Response(text="")
    return web.Response(text="<ul>" + "".join(response) + "</ul>")

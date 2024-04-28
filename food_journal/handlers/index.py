from aiohttp import web
from aiohttp_jinja2 import render_template_async


async def handle_index(request: web.Request) -> web.Response:
    return await render_template_async("index.html", request, {})

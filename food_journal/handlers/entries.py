from aiohttp import web
from aiohttp_jinja2 import render_template_async


async def add_journal_entry(request: web.Request) -> web.Response:
    form_data = await request.post()
    additional_notes: str = ""
    ingredients: list[str] = []
    for key, val in form_data.items():
        if key == "additional-notes" and isinstance(val, str):
            additional_notes = val
        elif isinstance(val, str):
            ingredients.append(val)

    print(additional_notes)
    print(ingredients)
    return await render_template_async("index.html", request, {})

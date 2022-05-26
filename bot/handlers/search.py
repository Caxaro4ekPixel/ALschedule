import asyncio
from aiogram import types, html, Router
from misc.api.anilibria import AnilibriaApi

loop = asyncio.get_event_loop()
al_api = AnilibriaApi(loop)

inline_router = Router()

@inline_router.inline_query(commands="search")
async def cmd_search(message: types.Message):
    query = message.get_args()
    titles = await al_api.get_titles(query)
    
    if titles:
        titles_names = [f"\n[{title.id}] - {title.names.ru}" for title in titles]
        await message.answer(html.bold("Найдено:") + html.code(*titles_names))
    else:
        await message.answer('🧐Ничего не найдено🧐')
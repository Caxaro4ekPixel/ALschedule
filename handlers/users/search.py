from aiogram import types

from aiogram.utils.markdown import hcode, hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, al_api


@dp.message_handler(commands="search")
async def cmd_search(message: types.Message):
    query = message.get_args()
    titles = await al_api.search_title(query)

    if titles:
        titles_names = [title.get("names").get("ru") for title in titles]
        await message.answer(hbold("Найдено:\n") + hcode("\n".join(titles_names)))
    else:
        await message.answer('🧐Ничего не найдено🧐')


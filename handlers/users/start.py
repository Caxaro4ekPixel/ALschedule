import logging
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils.markdown import hitalic, hcode
import aiohttp

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    relese_id = message.text.replace("/start ", "")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://api.anilibria.tv/v2/getTitle?id={relese_id}') as response:
                json = await response.json()
        except Exception as ex:
            logging.info(ex)

    if "error" in json:
        await message.answer('🧐Такого релиза не существует!🧐')
        await message.answer('Этот бот используеться в каналах! Для использования нужно прописать /start [id релиза]')
    else:
        bottons = [[types.InlineKeyboardButton(text="Да", callback_data='1')], [types.InlineKeyboardButton(text="Нет", callback_data='0')]]
        await message.answer(f'Релиз: {json.get("names").get("ru")}?\nID: {relese_id}', reply_markup=types.InlineKeyboardMarkup(bottons))


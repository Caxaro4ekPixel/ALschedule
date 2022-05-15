import logging
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils.markdown import hitalic, hcode
import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, al_api


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    title_id = message.get_args()
    title = await al_api.get_title(title_id)

    start_keyboard = InlineKeyboardMarkup()
    start_keyboard.row(
        InlineKeyboardButton(text="Да", callback_data='1'), 
        InlineKeyboardButton(text="Нет", callback_data='0')
    )

    if "error" in title:
        await message.answer('🧐Такого релиза не существует!🧐')
        await message.answer('Этот бот используеться в каналах! Для использования нужно прописать /start [id релиза]')
    else:
        await message.answer(f'Релиз: {title.get("names").get("ru")}?\nID: {title_id}', reply_markup=start_keyboard)


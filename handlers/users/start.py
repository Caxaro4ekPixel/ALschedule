from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hcode, hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, al_api


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    title_id = message.get_args()
    title = await al_api.get_title_by_id(title_id)

    start_keyboard = InlineKeyboardMarkup()
    start_keyboard.row(
        InlineKeyboardButton(text="✅Да", callback_data=f'add-{title_id}'), 
        InlineKeyboardButton(text="❌Нет", callback_data='cancel')
    )

    if title:
        await message.answer(
            f'{hbold("Релиз: ") + hcode(title.get("names").get("ru"))} ?',   
            reply_markup=start_keyboard
        )
    else:
        await message.answer('🧐Такого релиза не существует!🧐')
        await message.answer('Этот бот используеться в каналах! Для использования нужно прописать /start [id релиза]')


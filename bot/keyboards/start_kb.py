from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_kb(title_id) -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅Да", callback_data=f'add-{title_id}')
    kb.button(text="❌Нет", callback_data='cancel')
    return kb.as_markup(resize_keyboard=True)   
from typing import Optional
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData


class Registration(CallbackData, prefix="reg"):
    type: str
    chat_id: int


# Эта клавиатура отправиться юзеру
def register_user(user_id) -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Зарегистрироваться", 
        callback_data=Registration(type="user", chat_id=user_id)
    )
    return kb.as_markup(resize_keyboard=True)   


# Эта клавиатура отправиться в админский чат
def register_admin(user_id) -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅Да", callback_data=Registration(type="accept", chat_id=user_id))
    kb.button(text="❌Нет", callback_data=Registration(type="decline", chat_id=user_id))
    return kb.as_markup(resize_keyboard=True)  
